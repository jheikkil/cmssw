#!/bin/bash

CLUSTERID=$1
PROCID=$2

source params.sh


BATCH_DIR=${PWD}


echo "CLUSTER:" ${CLUSTERID}
echo "PROC-ID" ${PROCID}
echo 'TASKCONFDIR' ${ABSTASKCONFDIR}
echo 'OUT-DIR' ${OUTDIR}
echo 'OUTPUT-FILE' ${OUTFILE}

#dump job info
echo 'PROCID='${PROCID} >> job_info.sh
echo 'CLUSTERID='${CLUSTERID} >> job_info.sh

cd ${ABSTASKCONFDIR}
eval `scram runtime -sh`
python process_pickler.py job_config_${PROCID}.py ${BATCH_DIR}/job_config.py
cd ${BATCH_DIR}
ls -lrt
echo 'now about to run it: '
cmsRun job_config.py
