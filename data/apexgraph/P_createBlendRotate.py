@subgraph
@namespace("custom")
def P_createBlendRotate(graph:ApexGraphHandle,
                        drivenname:String,
                        controlname:String,
                        controlrefname:String,
                        contorlportname:String = "x[out]",
                        controltags:StringArray = ["blend_rot"],
                        minvalue:Float = 0.0,
                        maxvalue:Float = 1.0,
                        minvector:Vector3 = (0.0,0.0,0.0),
                        maxvector:Vector3 = (90.0,90.0,90.0),
                        ):
    
    

    # create remapVector
    remapname = drivenname+"_blendRotateRemap_001"
    nodelist = graph.FindNodes(drivenname+"_blendRotateRemap_00*")
    length = apex.array.Length(nodelist)
    if length == 0:
        pass
    else:
        number:Int = length +1
        remapname = drivenname+"_blendRotateRemap_00"+apex.string.FromInteger(number)


    remapnode = graph.addNode(remapname,"custom::remapVector")
    graph.updateNodeParms(remapnode,{"minvalue":minvalue,"maxvalue":maxvalue,"minvector":minvector,"maxvector":maxvector})

    # create or find control
    graph,controlname,controlnode = custom.P_createAbstractControl(graph,controlname,controlrefname,promote = True,tags = controltags)

    # connect control to remap node
    graph = P_wire(graph,controlname+":"+contorlportname,remapname+":value[in]")


    
    # find or create new parent node
    drivennode = graph.findNode(drivenname)

    parentname = drivenname+"_blendRotateParent"
    parentnode = graph.findNode(parentname)
    hasparent:Bool = Convert(parentnode)
    if hasparent:
        pass
    else:
        # check if parent node is a transform object
        drivenparentport = graph.findPort(drivennode,"parent")
        connectedportid = graph.getConnectedPort(drivenparentport)
        isconnected:Bool = Convert(connectedportid)

        if isconnected:
            connectednodeid = graph.portNode(connectedportid)
            name,callback = graph.nodeData(connectednodeid)
            if callback != "TransformObject":
                graph.UpdateNodeTags(drivennode,["this node has special parent."])
                parentnode=graph.DuplicateNode(drivenname,parentname,False)
                parentnodeparentport = graph.findPort(parentnode,"parent")
                graph.connectInput(connectedportid,parentnodeparentport)
                parentxformoutport = graph.findPort(parentnode,"xform[out]")
                graph.connectInput(parentxformoutport,drivenparentport)

            else:
                graph = custom.P_createRest(graph,drivenname,parentname)
                parentnode = graph.findNode(parentname)
                graph = custom.P_parentByName(graph,drivenname,parentname)

        else:
            graph = custom.P_createRest(graph,drivenname,parentname)
            parentnode = graph.findNode(parentname)
            graph = custom.P_parentByName(graph,drivenname,parentname)


        # graph = custom.P_createRest(graph,drivenname,parentname)
        # parentnode = graph.findNode(parentname)
        # graph = custom.P_parentByName(graph,drivenname,parentname)
        rest:Matrix4 = ((1,0,0,0),(0,1,0,0),(0,0,1,0),(0,0,0,1))
        graph.updateNodeParms(drivennode,{"restlocal":rest})

    # check if parent's r[in] port is already connected.
    parentportname = parentname+":r[in]"
    parentportid = graph.findFirstPort(parentportname)
    
    connectedportid = graph.getConnectedPort(parentportid)
    isconnected:Bool = Convert(connectedportid)
    if isconnected:

        # make sure addname is unique
        addname = drivenname+"_blendRotateAdd_001"
        nodelist = graph.FindNodes(drivenname+"_blendRotateAdd_00*")
        length = apex.array.Length(nodelist)
        if length == 0:
            pass
        else:
            number:Int = length +1
            addname = drivenname+"_blendRotateAdd_00"+apex.string.FromInteger(number)
        

        addnode = graph.addNode(addname,"Add<Vector3>")
        addportaid = graph.findPort(addnode,"a")
        graph.connectInput(connectedportid,addportaid)
        graph = P_wire(graph,remapname+":vectorout",addname+":b")
        graph = P_wire(graph,addname+":result",parentportname)

    else:
        graph = P_wire(graph,remapname+":vectorout",parentportname)



    return graph