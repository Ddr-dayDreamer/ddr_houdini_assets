@subgraph
@namespace("custom")
def P_setupExtraNormal(graph:ApexGraphHandle,angle:Float,bonedeformname:String = "Bonedeformation"):
    normalname = bonedeformname+"_normal"
    normalnode = graph.addNode(bonedeformname+"_normal","sop::normal",parms = {"cuspangle":angle})
    bonedeformnode = graph.findNode(bonedeformname)
    bonedeformoutport = graph.findPort(bonedeformnode,"geo")
    outputport = graph.GetConnectedPort(bonedeformoutport)
    normaloutport = graph.findPort(normalnode,"geo")

    graph = P_wire(graph,bonedeformname+":geo",normalname+":geoinput0")
    graph.connectInput(normaloutport,outputport)
    return graph
