@subgraph
@namespace("custom")
def P_createRestChain(graph:ApexGraphHandle,nodenamelist:StringArray,suffix:String = "_restchain",promote:Bool = False):
    restnodelist:StringArray = []
    for index,nodename in enumerate(nodenamelist):
        graph,restnodename= custom.P_createRest(graph,nodename,nodename+suffix)
        if index != 0:
            i = index-1
            graph = custom.P_parentByName(graph,restnodename,restnodelist[-1])

        if promote:
            graph = custom.P_promotePortByName(graph,restnodename+":r[in]",restnodename)
        restnodelist.append(restnodename)

    return graph,restnodelist