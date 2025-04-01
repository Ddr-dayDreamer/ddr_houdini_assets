@subgraph
@namespace("custom")
def P_setupReverseFoot(graph:ApexGraphHandle,
                        jointlist:StringArray,
                        basename:String,
                        reflist:StringArray,
                        ikgoalname:String,
                        walkcontrolarray:StringArray,
                        walkconvaluearray:Vector3Array,
                        parentspacenamelist:StringArray,
                        parentblendarray:StringArray,
                        ):
    # jointlist stands for [jnt_l_ball_001,jnt_l_toe_001]
    # basename for clear node name
    # ref list has 7 element:
    #     handleref,    heelref,    tipref,    inpivot,    outpivot,    toeref,    ballref
    # mind here toeref is before ballref
    # ikgoalname stans for the ik goal nodename,for leg always ctl_l_leg_IKGoal_001
    # walkcontrolarray is [walkcon name,walk con ref]
    # walkconvaluearray is [vector when walkcon is 1 set to ball control,vector when walkcon is -1 set to heel control]
    # parentspacenamelist and parentblend array should be the same as ik leg.


    toejointname:String = jointlist[1]
    balljointname:String = jointlist[0]

    # handleref:String,heelref:String,tipref:String,inpivotref:String,outpivotref:String,toeref:String,ballref:String,
    handleref = reflist[0]
    heelref= reflist[1]
    tipref= reflist[2]
    inpivotref= reflist[3]
    outpivotref= reflist[4]
    toeref= reflist[5]
    ballref= reflist[6]

    # create handle first.
    handlename = basename+"_handle_001"
    handle = graph.addNode(handlename,"TransformObject")
    graph.updateNodeTags(handle,["ik_handle"])
    # create parent blend for handle
    graph,parentxformname = custom.P_createParentSpaceBlend(graph,basename,parentspacenamelist,handleref,parentblendarray)
    # wire parent blend to handle
    graph = P_wire(graph,parentxformname+":value",handlename+":parent[in]")

    # create otrher controls
    heelname = basename+"_heel_001"
    graph = custom.P_createRest(graph,heelref,heelname,mode = "specify",specifyParentName = handlename)

    tipname = basename+"_tip_001"
    graph = custom.P_createRest(graph,tipref,tipname,mode = "specify",specifyParentName = heelname)

    inpivotname = basename+"_inPivot_001"
    graph = custom.P_createRest(graph,inpivotref,inpivotname,mode = "specify",specifyParentName = tipname)

    outpivotname = basename+"_outPivot_001"
    graph = custom.P_createRest(graph,outpivotref,outpivotname,mode = "specify",specifyParentName = inpivotname)


    toename = basename+"_toe_001"
    graph = custom.P_createRest(graph,toeref,toename,mode = "specify",specifyParentName = outpivotname)
    toenode = graph.findNode(toename)
    graph.updateNodeTags(toenode,["reverse_foot","reverse_foot_toe"])


    ballname = basename+"_ball_001"
    graph = custom.P_createRest(graph,ballref,ballname,mode = "specify",specifyParentName = outpivotname)
    ballnode = graph.findNode(ballname)
    graph.updateNodeTags(ballnode,["reverse_foot","reverse_foot_ball"])

    # reparent old ik goal to ball conrol.
    graph = custom.P_updateRest(graph,ikgoalname,ikgoalname,ballname)
    graph = custom.P_parentByName(graph,ikgoalname,ballname)

    # control ball joint by ball control
    graph = P_wire(graph,ballname+":xform[out]",balljointname+":xform[in]")

    # control toe joint by toe control
    toejoint = graph.findNode(toejointname)
    n,callback,p,color,parms = graph.NodeData(toejoint)
    toerest:Matrix4 = parms["restlocal"]
    multiplyname = basename+"_toeJointRest_001"
    multiplynode = graph.addNode(multiplyname,"Multiply<Matrix4>",parms = {"a":toerest})
    graph = P_wire(graph,toename+":xform[out]",multiplyname+":b")
    graph = P_wire(graph,multiplyname+":result",toejointname+":xform[in]")

    # promote controls:
    for name in [handlename,heelname,tipname,toename,inpivotname,outpivotname,ballname]:
        node = graph.findNode(name)
        graph.updateNodeTags(node,["reverse_foot"])
        graph = custom.P_promotePortByName(graph,name+":r[in]",name+"_r")
    
    graph = custom.P_promotePortByName(graph,handlename+":t[in]",handlename+"_t")

    # unpromote ball and toe joint

    graph = P_unWireInputByName(graph,balljointname+":r[in]")
    graph = P_unWireInputByName(graph,toejointname+":r[in]")

    graph = P_unWireInputByName(graph,ikgoalname+":r[in]")
    graph = P_unWireInputByName(graph,ikgoalname+":t[in]")
    graph = P_unWireInputByName(graph,ikgoalname+"_goal"+":r[in]")
    # create walkcon blend
    walkconparentname = basename+"_walkConParent_001"
    graph = custom.P_createRest(graph,walkcontrolarray[1],walkconparentname,mode = "specify",specifyParentName = handlename)
    # graph,walkconname,walkcon = custom.P_createAbstractControl(graph,walkcontrolarray[0],walkconparentname,True,tags = ["reverse_foot_walkcon","fkik_blend"])
    graph = custom.P_createBlendRotate(graph,ballname,walkcontrolarray[0],walkconparentname,controltags = ["reverse_foot_walkcon"],maxvector = walkconvaluearray[0])
    graph = custom.P_createBlendRotate(graph,heelname,walkcontrolarray[0],walkconparentname,maxvalue = -1.0,maxvector = walkconvaluearray[1])

    # create a output list for fkik blend
    outportlist:StringArray=[ballname+":xform[out]",multiplyname+":result"]


    return graph,outportlist