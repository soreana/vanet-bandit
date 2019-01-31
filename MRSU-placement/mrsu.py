
from anytree import AnyNode, RenderTree

def mobile_RSU_path(expanding_node,G,T,search_tree_root,search_tree_current,leaf_head):
    en = expanding_node
    
    print(G[en])
    search_tree_current.expanded = True
    for adj in G[en]:
        #print(G.node[adj])
        cost = search_tree_current.cost + G[en][adj]['weight']
        benefit = search_tree_current.benefit + G.node[adj]['benefit']

        if cost < T :
            tmp = AnyNode(id=adj,parent=search_tree_current,cost=cost,benefit=benefit,expanded=False)

        print ("benefit is %s" % (benefit))
        #G.node[adj]['cost'] = G.node[en]['cost'] + G[en][adj]['weight']
        #G.node[adj]['benefit'] = G.node[en]['benefit'] + G.node[adj]['benefit']
        #print(G.node[adj]['cost'])

    # choose next candidate
    benefit = 0
    best_node = None
    end = True
    for pre, fill, node in RenderTree(search_tree_root):
        if not node.expanded :
            if benefit < node.benefit:
                benefit = node.benefit
                best_node = node
                end = False

    if best_node is not None:
        print("best node %s:%s:%s" % (best_node.id,best_node.benefit,best_node.cost))

    if not end :
        mobile_RSU_path(best_node.id,G,T,search_tree_root,best_node,leaf_head)

