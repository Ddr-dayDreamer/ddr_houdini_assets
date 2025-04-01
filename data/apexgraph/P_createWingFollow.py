@subgraph
@namespace("custom")
def P_createWingFollow(graph:ApexGraphHandle,nodename:String,targetname:String,targetname2:String,absconname:String,weight:Float = 0.5):

    graph,rot1name = custom.P_createRotationConstraint(graph,nodename,targetname,1.0,False)
    graph,rot2name = custom.P_createRotationConstraint(graph,nodename,targetname2,-1.0,False)

    blendname = rot1name+"_rotblend"
    blend = graph.addNode(blendname,"custom::rotationBlendQuaternion",parms = {"weight":weight})
    graph = p_wire(graph,rot1name+":world_matrix",blendname+":m1")
    graph = p_wire(graph,rot2name+":world_matrix",blendname+":m2")

    

    # create additional control for constrainted wing control.
    controlname = "ctl_"+nodename
    control = graph.addNode(controlname,"TransformObject")
    # mark control as "wing extend" control
    graph.UpdateNodeTags(control,["wing_extend","fk_r"])

    

    # unpromote original joint control
    graph = P_unWireInputByName(graph,nodename+":r[in]")

    control.r_in.promote(controlname)
    
    # setup addition blend
    # another rest
    graph,restname = custom.P_createRest(graph,nodename,nodename+"_rest4wingfollow")
    blend2name = rot1name+"_blend"
    graph.addNode(blend2name,"transform::Blend")
    graph = P_wire(graph,restname+":xform[out]",blend2name+":a[in]")
    graph = P_wire(graph,blendname+":m",blend2name+":b[in]")
    graph = P_wire(graph,absconname+":x[out]",blend2name+":blend[in]")
    
    graph = p_wire(graph,blend2name+":result",controlname+":parent[in]")
    graph = p_wire(graph,controlname+":xform[out]",nodename+":xform[in]")

    return graph
