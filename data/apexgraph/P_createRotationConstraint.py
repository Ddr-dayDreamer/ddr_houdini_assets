@subgraph
@namespace("custom")
def P_createRotationConstraint(graph:ApexGraphHandle,nodename:String,targetname:String,weight:Float,connect:Bool=False):


    node = graph.findNode(nodename)
    target = graph.findNode(targetname)
    
    graph,noderestname = custom.P_createRest(graph,nodename,nodename+"_rest4rotcons")
    graph,targetrestname = custom.P_createRest(graph,targetname,targetname+"_rest4rotconstarget")

    rotconsname = nodename+"_rotcons_"+targetname
    rotcons = graph.addNode(rotconsname,"custom::rotationConstraint")
    
    graph = P_wire(graph,noderestname+":xform[out]",rotconsname+":xform_rest")
    graph = P_wire(graph,targetname+":xform[out]",rotconsname+":targetxform")
    graph = P_wire(graph,targetrestname+":xform[out]",rotconsname+":targetxform_rest")
    graph.updateNodeParms(rotcons,{"weight":weight})

    if connect:
        graph = P_wire(graph,rotconsname+":world_matrix",nodename+":xform[in]")

    return graph,rotconsname