@subgraph
@namespace("custom")
def P_updateRest(graph:ApexGraphHandle, node_name:String,childref:String,parentref:String):
    
        
    graph.compile(True)
    node = graph.findNode(node_name)

    childnode = graph.findNode(childref)

    parentnode = graph.findNode(parentref)

    g,n,childTransform = apex.component.getRestTransform(graph,childnode,graph)
    g,n,parentTransform = apex.component.getRestTransform(graph,parentnode,graph)

    invertParentTransform:Matrix4 = invert(parentTransform)
        
    rest = childTransform * invertParentTransform
    

    graph.UpdateNodeTags(node,["this node is modified by P_updateRest."],False)
    red:Vector3 = (1.0,0.0,0.0)
    graph.UpdateNode(node,color = red)
    graph.updateNodeParms(node,parms = {"restlocal":rest})

    return graph,node_name
    
