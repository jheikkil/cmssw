
#ifndef L1Trigger_DemonstratorTools_codecs_vertices_h
#define L1Trigger_DemonstratorTools_codecs_vertices_h

#include <vector>

#include "DataFormats/L1Trigger/interface/Vertex.h"

#include "L1Trigger/DemonstratorTools/interface/Frame.h"

namespace l1t::demo::codecs {

  std::vector<l1t::Vertex> decodeVertices(const std::vector<l1t::demo::Frame>&);

}

#endif