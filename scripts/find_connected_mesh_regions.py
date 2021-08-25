""" Find the connected regions of a volumetric mesh.

This script contains methods that find the connected regions of a volumetric mesh
This is done by assembling an adjacency matrix of the nodal-connectivity, 
constructing a graph from this matrix, and then finding the 'connected components'
of the graph.

Parameters
----------
1. No arguments are passed into the script
2. Script operates on a Cubit session that has at least one volumetric element

Results
----------
1. No values are returned by the script
2. Script constructs Cubit groups that contain the volumetric elements of a 
-- unique connected component of the graph.  These are the unique connected
-- regions of the volumetric mesh

Example
----------
import find_connected_mesh_regions
find_connected_mesh_regions.main()

Requirements
----------
This script requires NumPy and SciPy modules
1. Almost any version of NumPy should be fine, only basic capabilities needed
---- Tested with version 1.19.2
2. SciPy minimum version: 0.11.0
---- Tested with version: 1.5.3

Future work
----------
1. Improve performance of `create_connected_component_groups()`
2. Improve performance of `get_all_edge_list()`
3. Support non-volumetric elements and hybrid meshes.
"""

import time
import enum
import numpy
import scipy
import cubit
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import connected_components

## Main Functions ##
def get_connected_components():
  elem_conn, elem_type = get_element_connectivity()
  edge_list = get_all_edge_list(elem_conn, elem_type)
  row = edge_list[:,0]-1
  col = edge_list[:,1]-1
  data = numpy.ones(len(row), dtype="bool")
  num_verts = cubit.get_node_count()
  ADJ = csr_matrix((data, (row, col)), shape=(num_verts, num_verts))
  n_components, labels = connected_components(csgraph=ADJ, directed=False, return_labels=True)
  return n_components, labels

def create_connected_component_groups():  
  n_components, labels = get_connected_components()
  n_components = len(set(labels))
  for i in range(0,n_components):
    cubit.cmd(f"delete connected_region_{i+1}")
    cubit.cmd(f"create group 'connected_region_{i+1}'")
  
  hex_label_list = [[] for i in range(0,n_components)]
  pyr_label_list = [[] for i in range(0,n_components)]
  wed_label_list = [[] for i in range(0,n_components)]
  tet_label_list = [[] for i in range(0,n_components)]
  
  node_id = cubit.get_entities("node")
  for node_idx in range(0,len(labels)):
    label_idx = labels[node_idx]
    hex_ids = cubit.parse_cubit_list("hex", f"in node {node_id[node_idx]}")
    pyr_ids = cubit.parse_cubit_list("pyramid", f"in node {node_id[node_idx]}")
    wed_ids = cubit.parse_cubit_list("wedge", f"in node {node_id[node_idx]}")
    tet_ids = cubit.parse_cubit_list("tet", f"in node {node_id[node_idx]}")
    hex_label_list[label_idx] += list(hex_ids)
    pyr_label_list[label_idx] += list(pyr_ids)
    wed_label_list[label_idx] += list(wed_ids)
    tet_label_list[label_idx] += list(tet_ids)
  
  for i in range(0,n_components):
    hex_label_list[i] = set(hex_label_list[i])
    pyr_label_list[i] = set(pyr_label_list[i])
    wed_label_list[i] = set(wed_label_list[i])
    tet_label_list[i] = set(tet_label_list[i])
  
  for i in range(0,n_components):
    if len(hex_label_list[i]) > 0:
      cubit.cmd(f"connected_region_{i+1} add hex {list_to_str(hex_label_list[i])}")
    if len(pyr_label_list[i]) > 0:
      cubit.cmd(f"connected_region_{i+1} add pyr {list_to_str(pyr_label_list[i])}")
    if len(wed_label_list[i]) > 0:
      cubit.cmd(f"connected_region_{i+1} add wed {list_to_str(wed_label_list[i])}")
    if len(tet_label_list[i]) > 0:
      cubit.cmd(f"connected_region_{i+1} add tet {list_to_str(tet_label_list[i])}")

## Supporting Functions ##
def get_element_connectivity():
  hex_id = cubit.get_entities("hex")
  pyr_id = cubit.get_entities("pyramid")
  wed_id = cubit.get_entities("wedge")
  tet_id = cubit.get_entities("tet")
  
  elem_conn = []
  elem_type = []
  for id in hex_id:
    elem_conn.append(cubit.get_connectivity("hex", id))
    elem_type.append(Element.HEX)
  for id in pyr_id:
    elem_conn.append(cubit.get_connectivity("pyramid", id))
    elem_type.append(Element.PYRAMID)
  for id in wed_id:
    elem_conn.append(cubit.get_connectivity("wedge", id))
    elem_type.append(Element.WEDGE)
  for id in tet_id:
    elem_conn.append(cubit.get_connectivity("tet", id))
    elem_type.append(Element.TET)
  return elem_conn, elem_type

def get_all_edge_list(elem_conn, elem_type):
  edge_list = []
  for i in range(0,len(elem_conn)):
    elem_edges = elem_type[i].edge_connectivity()
    for edge in elem_edges:
      node_pair = [elem_conn[i][edge[0]-1], elem_conn[i][edge[1]-1]] 
      node_pair.sort()
      edge_list.append(node_pair)
  edge_list = numpy.array(edge_list)
  return edge_list

## Utility Functions ##
def list_to_str(input_str):
  return " ".join([str(val) for val in input_str])

## Supporting Classes ##
class Element(enum.Enum):
  HEX = 1
  PYRAMID = 2
  WEDGE = 3
  TET = 4
  # Class Methods
  def edge_connectivity(self):
    if self == Element.HEX:
      edges = ((1,2),(1,4),(1,5),(2,3),(2,6),(3,4),(3,7),(4,8),(5,6),(5,8),(6,7),(7,8))
    elif self == Element.PYRAMID:
      edges = ((1,2),(1,4),(1,5),(2,3),(2,5),(3,4),(3,5),(4,5))
    elif self == Element.WEDGE:
      edges = ((1,2),(1,3),(1,4),(2,3),(2,5),(3,6),(4,5),(4,6),(5,6))
    elif self == Element.TET:
      edges = ((1,2),(1,3),(1,4),(2,3),(2,4),(3,4))
    return edges

if __name__ == "__main__":
  create_connected_component_groups()
