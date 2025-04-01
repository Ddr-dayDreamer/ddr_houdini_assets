@subgraph
@namespace("custom")
def P_createRest(graph:ApexGraphHandle, node_name:String,restnodename:String = "default", mode:String = 'parent', specifyParentName:String = 'specifyParent'):
    
    # exist:Bool = convert(node)
    # if not exist:
    #     return graph.compile()
        
    graph.compile(True)
    node = graph.findNode(node_name)

    g,n,nodeTransform = apex.component.getRestTransform(graph,node,graph)
    
    
    if mode == "parent":
        # get parent transform
        graph,parentNode = apex.component.GetTransformParent(graph,node)
        g,n,parentTransform = apex.component.getRestTransform(graph,parentNode,graph)
        
        invertParentTransform:Matrix4 = invert(parentTransform)
        
    #get specified parent transform
    if mode == "specify":
        parentNode = graph.findNode(specifyParentName)
        g,n,parentTransform = apex.component.getRestTransform(graph,parentNode,graph)
        
        invertParentTransform:Matrix4 = invert(parentTransform)
        
    if mode == "world":
        invertParentTransform = Matrix4(1)
        
    rest = nodeTransform * invertParentTransform
    
    if restnodename == "default":
        restnodename = node.name()+"_rest"

    restNode = graph.findNode(restnodename)
    if convert(restNode):
        graph.UpdateNodeTags(restNode,["this node is marked by P_createRest."],False)
        red:Vector3 = (1.0,0.0,0.0)
        graph.UpdateNode(restNode,color = red)
        return graph,restnodename
    
    else:
        restNode = graph.addNode(restnodename,"TransformObject")
        yellow:Vector3 = (1.0,0.5,0.0)
        graph.UpdateNode(restNode,color = yellow)
        graph.updateNodeParms(restNode,parms = {"restlocal":rest})
        graph.parentNodes(restNode,parentNode)

    return graph,restnodename