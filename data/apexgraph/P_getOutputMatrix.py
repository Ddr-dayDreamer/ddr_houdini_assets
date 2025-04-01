@subgraph
@namespace("custom")
def P_getOutputMatrix(graph:ApexGraphHandle,nodename:String,portname:String):

    graph.compile(True)


    # dict = graph.Invoke(pattern = nodename+":"+portname)
    # matrixout:Matrix4 = dict[portname]


    nodeid = graph.findNode(nodename)
    name,callback,pos,color,parms,tags,pro,output = graph.NodeData(nodeid)
    matrixout:Matrix4 = output[portname]
    

    return matrixout
    
