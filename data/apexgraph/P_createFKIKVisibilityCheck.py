# this module is not completed yet,dont use it.
def visibilityCompute(inputfloat:Float,invert:Bool=False,threshold:Float=0.01):
    if invert:
        inputfloat = 1.0-inputfloat

    outputScale:Vector3 = (1,1,1)

    if inputfloat>(1.0-threshold):
        outputScale:Vector3 = (1,1,1)
    else:
        outputScale:Vector3 = (0,0,0)
    
    return outputScale


@subgraph
@namespace("custom")
def P_createFKIKVisibilityCheck(graph:ApexGraphHandle,
                        fkik_switch_portname:String,
                        fk_ctrl_list:StringArray,
                        ik_ctrl_list:StringArray
                        ):
    for fk_ctrl in fk_ctrl_list:
        compute_nodename = fk_ctrl+'_visibility'
        compute_node = graph.addSubnet(contents=visibilityCompute, subnetname=compute_nodename)
        graph.updateNodeParms(compute_node,{"invert":True,"threshold":0.01})
        graph = P_wire(graph,fkik_switch_portname,compute_nodename+":inputfloat[in]")
        graph = P_wire(graph,compute_nodename+":outputScale[out]",fk_ctrl+":s[in]")



    
    return graph

