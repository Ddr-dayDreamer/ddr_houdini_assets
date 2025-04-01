@subgraph
@namespace("custom")
def P_setupBlendShape(graph:ApexGraphHandle,bsnodename:String,bsdict:Dict,
                      bsGeoGroupName:String = "",
                      bsAttribs:String = "P",
                      boneDeformNodeName:String = "Bonedeformation",
                      restGeoName = "pointtransform_rest",
                      pointTransformNodeName:String = "pointtransform",
                      shapename:String = "Base.shp",
                      skeletonname:String = "Base.skel"):
    # bsdict:{"blendshape name":"blendshape control parent name"}
    
    
    # setup or find blendshape node
    bsnode = graph.findNode(bsnodename,"sop::kinefx::characterblendshapescore")
    bsnodefound:Bool = convert(bsnode)
    if bsnodefound:
        pass
    else:
        bsnode = graph.addNode(bsnodename,"sop::kinefx::characterblendshapescore")
        if bsGeoGroupName!= "":
            graph.updateNodeParms(bsnode,parms = {"group":bsGeoGroupName})
        graph.updateNodeParms(bsnode,parms = {"attribs":bsAttribs})
        graph = custom.P_promotePortByName(graph,bsnodename+":geoinput0",shapename) 

        graph = P_wire(graph,bsnodename+":geo[out]",boneDeformNodeName+":geoinput0")
        

    # setup blendshape controls

    prev_portName = "None"
    keys = apex.dict.Keys(bsdict)
    for index,key in enumerate(keys):
        value:String = bsdict[key]
        bscontrolname = "ctl_"+key+"_bscontrol"
        graph,bscontrolname,bscontrol = custom.P_createAbstractControl(graph,bscontrolname,value,promote = True,tags = ["bs_con"])

        setDetailAttribNodeName = key+"_setdetail"
        setDetailAttribNode = graph.addNode(setDetailAttribNodeName,"geo::SetDetailAttribValue<Float>")
        graph.updateNodeParms(setDetailAttribNode,parms = {"attribname":key})
        # init prevportname and wire by loop
        if index == 0:
            restgeofound:Bool = convert(graph.findNode(restGeoName,"Value<Geometry>"))
            if restgeofound:
                
                graph = P_wire(graph,restGeoName+":value",setDetailAttribNodeName+":geo[in]")
            else:

                graph = custom.P_promotePortByName(graph,setDetailAttribNodeName+":geo[in]",skeletonname)
            
        else:
            graph = P_wire(graph,prev_portName,setDetailAttribNodeName+":geo[in]")

        prev_portName = setDetailAttribNodeName+":geo[out]"

        # wire abscon and setdetail
        graph = P_wire(graph,bscontrolname+":x[out]",setDetailAttribNodeName+":value[in]")

        # set last loop to wire bs node geoinput1

        if key == keys[-1]:
            graph = P_wire(graph,setDetailAttribNodeName+":geo[out]",bsnodename+":geoinput1")
            graph = P_wire(graph,setDetailAttribNodeName+":geo[out]",pointTransformNodeName+":geo[in]")


    return graph,bsnodename