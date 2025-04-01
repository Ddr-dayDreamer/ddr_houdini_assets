@subgraph
@namespace("custom")
def P_createMultiBoneIK(graph:ApexGraphHandle,nodelist:StringArray,rootdriver:StringArray,twist:StringArray,goal:StringArray,parentspacenodelist:StringArray = ["None"],parentspaceconarray:StringArray = ["None","None"]):
    # rootdriver,twist and goal,these three array ,will define name of created node,whether to use specified node as xform ref,and specified node name
    # so it will be ["expected control name","True","control reference name"]
    # for root control,I think it will only be in the first joint position,so,for rootdriver[1],"True" means function will promote rootdriver to be animated.
    # and for rootdriver[2] it will mean nothing.
    # for twist,if twist[1]set to False,which means you dont use a twist ref,then i will set to use no twist in multiboneik node
    # which will result in your
    # as for parentspace blend ,parentspacearray means ["parent space blend abscon name","parent space blend abscon ref"].


    # create basic rest
    graph,restnodelist = custom.P_createRestChain(graph,nodelist,"_ikrest")
    
    
    
    # create controls
    rootref = nodelist[0]
    # if rootdriver[1] == "True":
    #     rootref = rootdriver[2]
    
    twistref = nodelist[1]
    if twist[1] == "True":
        twistref = twist[2]

    goalref = nodelist[-1]
    if goal[1] == "True":
        goalref = goal[2]


    

    # create parentspace to blend
    if parentspaceconarray[0] != "None":

        graph,twistgetxformname = custom.P_createParentSpaceBlend(graph,twist[0],parentspacenodelist,twistref,parentspaceconarray)
        graph,goalgetxformname = custom.P_createParentSpaceBlend(graph,goal[0],parentspacenodelist,goalref,parentspaceconarray)

    
        # setup root twist goal and parent space blend
        graph,rootname = custom.P_createRest(graph,rootref,rootdriver[0],mode = "parent")


        twistname = twist[0]
        twistnode = graph.findOrAddNode(twistname,"TransformObject")
        graph = P_wire(graph,twistgetxformname+":value",twistname+":parent[in]")


        if goal[1] == "True":
            goalconname = goal[0]
            goalconnode = graph.findOrAddNode(goalconname,"TransformObject")
            graph = P_wire(graph,goalgetxformname+":value",goalconname+":parent[in]")

            goalref = nodelist[-1]
            graph,goalname= custom.P_createRest(graph,goalref,goal[0]+"_goal",mode = "specify",specifyParentName = goalconname)
        else:
            goalname = goal[0]
            goalnode = graph.findOrAddNode(goalname,"TransformObject")
            graph = P_wire(graph,goalgetxformname+":value",goalname+":parent[in]")



    # define when not to use parent space blend
    else:
        # setup root twist goal
        singleparentname = parentspacenodelist[0]
        graph,rootname = custom.P_createRest(graph,rootref,rootdriver[0],mode = "parent")


        twistname = twist[0]
        graph = custom.P_createRest(graph,twistref,twistname,mode = "specify",specifyParentName =singleparentname)

        if goal[1] == "True":
            goalconname = goal[0]
            graph = custom.P_createRest(graph,goalref,goalconname,mode = "specify",specifyParentName =singleparentname)

            goalref = nodelist[-1]
            graph,goalname= custom.P_createRest(graph,goalref,goal[0]+"_goal",mode = "specify",specifyParentName = goalconname)
        else:
            goalname = goal[0]
            graph = custom.P_createRest(graph,goalref,goalname,mode = "specify",specifyParentName =singleparentname)





    # mark control as "ik" control
    rootnode = graph.findNode(rootname)
    graph.UpdateNodeTags(rootnode,["ik_handle"])
    twistnode = graph.findNode(twistname)
    graph.UpdateNodeTags(twistnode,["ik_twist"])
    if goal[1] == "True":
        goalconnode = graph.findNode(goalconname)
        graph.UpdateNodeTags(goalconnode,["ik_handle"])
        goalnode = graph.findNode(goalname)
        graph.UpdateNodeTags(goalnode,["ik_goal"])
    else:
        goalnode = graph.findNode(goalname)
        graph.UpdateNodeTags(goalnode,["ik_handle"])


    
    # create ik node
    iknodename = rootname+"_multiBoneIk_core"
    iknode = graph.findOrAddNode(iknodename,"rig::MultiBoneIK")
    graph.updateNodeParms(iknode,parms = {"blend":1.0,"usegoalrot":True,"trackingthreshold":0.001})



    # promote 
    if rootdriver[1] == "True":
        graph = custom.P_promotePortByName(graph,rootname+":r[in]",rootname+"_r")
        graph = custom.P_promotePortByName(graph,rootname+":t[in]",rootname+"_t")

    
    if twist[1] == "True":
        graph = custom.P_promotePortByName(graph,twistname+":t[in]",twistname+"_t")
    else:
    # set ik to no twist
        graph.updateNodeParms(iknode,parms = {"usetwist":False})

    if goal[1] == "True":
        graph = custom.P_promotePortByName(graph,goalconname+":t[in]",goalconname+"_t")
        graph = custom.P_promotePortByName(graph,goalconname+":r[in]",goalconname+"_r")
        graph = custom.P_promotePortByName(graph,goalname+":r[in]",goalname+"_r")
    else:
        graph = custom.P_promotePortByName(graph,goalname+":t[in]",goalname+"_t")
        graph = custom.P_promotePortByName(graph,goalname+":r[in]",goalname+"_r")



    # wire iknode
    graph = P_wire(graph,rootname+":xform[out]",iknodename+":rootdriver")
    graph = P_wire(graph,twistname+":xform[out]",iknodename+":twist")
    graph = P_wire(graph,goalname+":xform[out]",iknodename+":goal")

    # create an outportlist for fkik blend
    outportlist:StringArray = []

    # wire rest inputs and outputs
    for index,restnodename in enumerate(restnodelist):
        graph = P_wire(graph,restnodename+":xform[out]",iknodename+":in")

        graph = P_wire(graph,iknodename+":out",nodelist[index]+":xform[in]")

        # unpromote original joint control
        graph = P_unWireInputByName(graph,nodelist[index]+":r[in]")

        indexstr = apex.string.FromInteger(index)
        outportlist.append(iknodename+":out"+indexstr)


    
    # for node in nodelist:
    #     graph = P_unWireInputByName(graph,node+":r[in]")
    # graph = P_unWireInputByName(graph,rootname+":r[in]")
    # graph = P_unWireInputByName(graph,midname+":r[in]")
    # graph = P_unWireInputByName(graph,tipname+":r[in]")
    
    # graph = P_createExtraControl(graph,nodelist[-1]+":xform[in]","extracon")

    
    
    return graph,iknodename,outportlist