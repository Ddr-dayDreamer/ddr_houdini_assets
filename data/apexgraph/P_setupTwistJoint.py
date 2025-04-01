@subgraph
@namespace("custom")
def P_setupTwistJoint(graph:ApexGraphHandle,twistjointdict:Dict,jointname:String,axis:Vector3 = (1.0,0.0,0.0),rangefactor:Float = 1.0):
    # format of twistjointdict:{"twist_joint_name1":weight1,"twist_joint_name2":weight2}
    # twistjointdict的格式：{"名字":权重数值}
    
    
    # create extract node
    extractnodename = jointname+"_twistJointExtract"
    extractnode = graph.addNode(extractnodename,"custom::twistJointExtract",parms = {"axis":axis,"rangefactor":rangefactor})
    graph = P_wire(graph,jointname+":r[out]",extractnodename+":jointrotation[in]")
    blue:Vector3 = (0.2,0.2,1)
    graph.updateNode(extractnode,color = blue)


    # setup multiple twistjoints
    for twistjointname in twistjointdict.keys():
        weight:Float = twistjointdict[twistjointname]
        twistjointmultiplyname = twistjointname+"_twistJointWeight"
        weightVector:Vector3 = (weight,weight,weight)
        graph.addNode(twistjointmultiplyname,"Multiply<Vector3>",parms={"a":weightVector})
        graph = P_wire(graph,extractnodename+":rot[out]",twistjointmultiplyname+":b[in]")
        graph = P_wire(graph,twistjointmultiplyname+":result[out]",twistjointname+":r[in]")



    return graph