#include <array> 
#include <unordered_set>
#include <unordered_map>
#include "L1Trigger/L1THGCal/interface/be_algorithms/HGCalClusteringImpl.h"
#include "DataFormats/Common/interface/PtrVector.h"
#include "DataFormats/Common/interface/OrphanHandle.h"

//class constructor
HGCalClusteringImpl::HGCalClusteringImpl(const edm::ParameterSet & conf):
    seedThreshold_(conf.getParameter<double>("seeding_threshold")),
    triggerCellThreshold_(conf.getParameter<double>("clustering_threshold")),
    dr_(conf.getParameter<double>("dR_cluster")),
    clusteringAlgorithmType_(conf.getParameter<string>("clusterType"))
{    
    edm::LogInfo("HGCalClusterParameters") << "C2d Clustering Algorithm selected : " << clusteringAlgorithmType_ ; 
    edm::LogInfo("HGCalClusterParameters") << "C2d seeding Thr: " << seedThreshold_ ; 
    edm::LogInfo("HGCalClusterParameters") << "C2d clustering Thr: " << triggerCellThreshold_ ; 
 
}


/* dR-algorithms */
bool HGCalClusteringImpl::isPertinent( const l1t::HGCalTriggerCell & tc, 
                                       const l1t::HGCalCluster & clu, 
                                       double distXY ) const 
{

    HGCalDetId tcDetId( tc.detId() );
    HGCalDetId cluDetId( clu.seedDetId() );
    if( (tcDetId.layer() != cluDetId.layer()) ||
        (tcDetId.subdetId() != cluDetId.subdetId()) ||
        (tcDetId.zside() != cluDetId.zside()) ){
        return false;
    }   
    if ( clu.distance((tc)) < distXY ){
        return true;
    }
    return false;

}


void HGCalClusteringImpl::clusterizeDR( const edm::PtrVector<l1t::HGCalTriggerCell> & triggerCellsPtrs, 
                                      l1t::HGCalClusterBxCollection & clusters
    ){

    bool isSeed[triggerCellsPtrs.size()];
    
    /* search for cluster seeds */
    int itc(0);
    for( edm::PtrVector<l1t::HGCalTriggerCell>::const_iterator tc = triggerCellsPtrs.begin(); tc != triggerCellsPtrs.end(); ++tc,++itc ){
        isSeed[itc] = ( (*tc)->mipPt() > seedThreshold_) ? true : false;
    }
    
    /* clustering the TCs */
    std::vector<l1t::HGCalCluster> clustersTmp;

    itc=0;
    for( edm::PtrVector<l1t::HGCalTriggerCell>::const_iterator tc = triggerCellsPtrs.begin(); tc != triggerCellsPtrs.end(); ++tc,++itc ){
            
        if( (*tc)->mipPt() < triggerCellThreshold_ ){
            continue;
        }
        
        /* searching for TC near the center of the cluster  */
        int iclu=0;
        vector<int> tcPertinentClusters; 
        for( std::vector<l1t::HGCalCluster>::iterator clu = clustersTmp.begin(); clu != clustersTmp.end(); ++clu,++iclu ){
            if( this->isPertinent(**tc, *clu, dr_) ){
                tcPertinentClusters.push_back(iclu);
            }
        }
        if( tcPertinentClusters.size() == 0 && isSeed[itc] ){
            clustersTmp.emplace_back( *tc );
        }
        else if ( tcPertinentClusters.size() > 0 ){
         
            unsigned minDist(300);
            unsigned targetClu(0);
                        
            for( std::vector<int>::const_iterator iclu = tcPertinentClusters.begin(); iclu != tcPertinentClusters.end(); ++iclu ){
                double d = clustersTmp.at(*iclu).distance(**tc);
                if( d < minDist ){
                    minDist = d;
                    targetClu = *iclu;
                }
            } 

            clustersTmp.at(targetClu).addTriggerCell( *tc );                    

        }
    }

    /* store clusters in the persistent collection */
    for( unsigned i(0); i<clustersTmp.size(); ++i ){
        clusters.push_back( 0, clustersTmp.at(i) );
    }
    
}



/* NN-algorithms */

/* storing trigger cells into vector per layer and per endcap */
void HGCalClusteringImpl::triggerCellReshuffling( const edm::PtrVector<l1t::HGCalTriggerCell> & triggerCellsPtrs, 
                                                  std::array< std::array<std::vector<edm::Ptr<l1t::HGCalTriggerCell>>,40>,2> & reshuffledTriggerCells 
    ){

    for( edm::PtrVector<l1t::HGCalTriggerCell>::const_iterator tc = triggerCellsPtrs.begin(); tc != triggerCellsPtrs.end(); ++tc){
        int endcap = (*tc)->zside() == -1 ? 0 : 1 ;
        HGCalDetId tcDetId( (*tc)->detId() );
        int subdet = tcDetId.subdetId();
        int layer = -1;

        if( subdet == HGCEE ){ 
            layer = (*tc)->layer();
        }
        else if( subdet == HGCHEF ){
            layer = (*tc)->layer() + 28;
        }
        else if( subdet == HGCHEB ){
            edm::LogWarning("DataNotFound") << "WARNING: the BH trgCells are not yet implemented";            
        }
        
        reshuffledTriggerCells[endcap][layer-1].emplace_back(*tc);
        
    }

}


/* merge clusters that have common neighbors */
void HGCalClusteringImpl::mergeClusters( l1t::HGCalCluster & main_cluster, 
                                         l1t::HGCalCluster & secondary_cluster ) const
{

    const edm::PtrVector<l1t::HGCalTriggerCell>& pertinentTC = secondary_cluster.triggercells();
    
    for( edm::PtrVector<l1t::HGCalTriggerCell>::iterator tc = pertinentTC.begin(); tc != pertinentTC.end(); ++tc ){
        main_cluster.addTriggerCell(*tc);
    }

}


void HGCalClusteringImpl::NNKernel( const std::vector<edm::Ptr<l1t::HGCalTriggerCell>> & reshuffledTriggerCells,
                                    l1t::HGCalClusterBxCollection & clusters,
                                    const HGCalTriggerGeometryBase & triggerGeometry
    ){
   
    /* declaring the clusters vector */
    std::vector<l1t::HGCalCluster> clustersTmp;

    // map TC id -> cluster index in clustersTmp
    std::unordered_map<uint32_t, int> cluNNmap;

    /* loop over the trigger-cells */
    for( const auto& tc_ptr : reshuffledTriggerCells ){
                
        if( tc_ptr->mipPt() < triggerCellThreshold_ ){
            continue;
        }
        
        // Check if the neighbors of that TC are already included in a cluster
        // If this is the case, add the TC to the first (arbitrary) neighbor cluster
        // Otherwise create a new cluster
        bool createNewC2d(true);
        const auto neighbors = triggerGeometry.getNeighborsFromTriggerCell(tc_ptr->detId());
        for( const auto neighbor : neighbors ){
            auto tc_cluster_itr = cluNNmap.find(neighbor);
            if(tc_cluster_itr!=cluNNmap.end()){ 
                createNewC2d = false;
                try{
                    clustersTmp.at(tc_cluster_itr->second).addTriggerCell(tc_ptr);
                    // map TC id to the existing cluster
                    cluNNmap.emplace(tc_ptr->detId(), tc_cluster_itr->second);
                }
                catch(const std::out_of_range& e){
                    throw cms::Exception("HGCTriggerUnexpected")
                        << "Trying to access a non-existing cluster. But it should exist...\n";
                }
                break;
            }
        }
        if(createNewC2d){
            clustersTmp.emplace_back(tc_ptr);
            clustersTmp.back().setIsComplete(true);
            // map TC id to the cluster index (size - 1)
            cluNNmap.emplace(tc_ptr->detId(), clustersTmp.size()-1);
        }
    }
    
    /* declaring the vector with possible clusters merged */
    // Merge neighbor clusters together
    for(unsigned i_clu1 = 0; i_clu1 < clustersTmp.size(); ++i_clu1){
        l1t::HGCalCluster& cluster1 = clustersTmp.at(i_clu1);
        // If the cluster has been merged into another one, skip it
        if( !cluster1.isComplete() ) continue;
        // Fill a set containing all TC included in the clusters
        // as well as all neighbor TC
        std::unordered_set<uint32_t> cluTcSet;
        for(const auto& tc_clu1 : cluster1.triggercells()){ 
            cluTcSet.insert( tc_clu1->detId() );
            const auto neighbors = triggerGeometry.getNeighborsFromTriggerCell( tc_clu1->detId() );
            for(const auto neighbor : neighbors){
                cluTcSet.insert( neighbor );
            }
        }        
            
        for(unsigned i_clu2 = 0; i_clu2 < clustersTmp.size(); ++i_clu2){
            l1t::HGCalCluster& cluster2 = clustersTmp.at(i_clu2);
            // If the cluster has been merged into another one, skip it
            if( cluster1.seedDetId()==cluster2.seedDetId() ) continue;
            if( !cluster2.isComplete() ) continue;
            // Check if the TC in clu2 are in clu1 or its neighbors
            // If yes, merge the second cluster into the first one
            for(const auto& tc_clu2 : cluster2.triggercells()){ 
                if( cluTcSet.find(tc_clu2->detId())!=cluTcSet.end() ){
                    mergeClusters( cluster1, cluster2 );                    
                    cluTcSet.insert( tc_clu2->detId() );
                    const auto neighbors = triggerGeometry.getNeighborsFromTriggerCell( tc_clu2->detId() );
                    for(const auto neighbor : neighbors){
                        cluTcSet.insert( neighbor );
                    }                    
                    cluster2.setIsComplete(false);
                    break;
                }
            }
        }
    }

    /* store clusters in the persistent collection */
    // only if the cluster contain a TC above the seed threshold
    for( auto& cluster : clustersTmp ){
        if( !cluster.isComplete() ) continue;
        bool saveInCollection(false);
        for( const auto& tc_ptr : cluster.triggercells() ){
            /* threshold in transverse-mip */
            if( tc_ptr->mipPt() > seedThreshold_ ){
                saveInCollection = true;
                break;
            }
        }
        if(saveInCollection){
            clusters.push_back( 0, cluster );
        }
    }
}


void HGCalClusteringImpl::clusterizeNN( const edm::PtrVector<l1t::HGCalTriggerCell> & triggerCellsPtrs, 
                                      l1t::HGCalClusterBxCollection & clusters,
                                      const HGCalTriggerGeometryBase & triggerGeometry
    ){

    std::array< std::array< std::vector<edm::Ptr<l1t::HGCalTriggerCell> >,40>,2> reshuffledTriggerCells; 
    triggerCellReshuffling( triggerCellsPtrs, reshuffledTriggerCells );

    for(int iec=0; iec<2; ++iec){
        for(int il=0; il<40; ++il){
            NNKernel( reshuffledTriggerCells[iec][il], clusters, triggerGeometry );
        }
    }

}

