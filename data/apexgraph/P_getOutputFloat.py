@subgraph
@namespace("custom")
def P_getOutputFloat(graph:ApexGraphHandle,nodename:String,portname:String):

    graph.compile(True)


    # dict = graph.Invoke(pattern = nodename+":"+portname)
    # matrixout:Matrix4 = dict[portname]


    nodeid = graph.findNode(nodename)
    name,callback,pos,color,parms,tags,pro,output = graph.NodeData(nodeid)
    out:Float = output[portname]
    

    return out
    
