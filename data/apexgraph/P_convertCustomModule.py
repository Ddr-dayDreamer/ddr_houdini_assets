@subgraph
@namespace("custom")
def P_convertCustomModule(graph:ApexGraphHandle,times:Int):
    for t in range(times):
    
        nodes = graph.findNodes("%callback(custom::*)")
        
        for node in nodes:
            graph.updateNode(node,callback = "__subnet__")


    return graph