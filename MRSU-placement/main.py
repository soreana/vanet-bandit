from random import randint
from anytree import AnyNode, RenderTree
import networkx as nx
import mrsu

max_benefit = 10
G = nx.Graph()
e = [('1', '2', 0.3), ('1', '3', 0.9), ('1', '4', 0.5), ('2', '3', 1.2),('2', '5', 0.3), ('3', '4', 0.9), ('3', '5', 0.5), ('4', '5', 1.2)]
G.add_weighted_edges_from(e)

# add benefits to G
for node in G :
    G.node[node]['benefit'] = randint(1, max_benefit)
    print (G.node[node]['benefit'])

root = AnyNode(id='1',cost=0,benefit=G.node['1']['benefit'])

mrsu.mobile_RSU_path('1',G,2,root,root,'1')

for pre, fill, node in RenderTree(root):
    print("%s%s:%s:%s" % (pre, node.id,node.benefit,node.cost))
    
best_node = root
for pre, fill, node in RenderTree(root):
    if best_node.benefit < node.benefit:
        best_node = node

while best_node.parent is not None:
    print best_node
    best_node = best_node.parent
