@subgraph
@namespace("custom")
def P_createSimpleSplineIK(graph:ApexGraphHandle,
                     order:Int,
                     ctrlrefnamelist:StringArray,
                     ctrlnamebase:String,
                     ctrlparentname:String,
                     jointnodenamelist:StringArray,
                     respectctrlparents:Bool = False,
                     controltags:StringArray = ["ik_handle"],
                     tangent:Vector3 = (1.0,0.0,0.0)
                     ):
# create rest chain first to make sure dont lose xform    
    # graph,restjointnamelist = custom.P_createRestChain(graph,jointnodenamelist,"_ikrest")

# create controls
    ctrlnamelist:StringArray = []
    for index,ctrlref in enumerate(ctrlrefnamelist):
        indexstr:String = apex.string.FromInteger(index)
        ctrlname = ctrlnamebase+"00"+indexstr
        if respectctrlparents:
            graph = custom.P_createRest(graph,ctrlref,ctrlname)
        else:
            graph = custom.P_createRest(graph,ctrlref,ctrlname,"specify",ctrlparentname)
        ctrlnode = graph.findNode(ctrlname)
        graph.updateNodeTags(ctrlnode,controltags)
        graph = custom.P_promotePortByName(graph,ctrlname+":t[in]",ctrlname+"_t")
        graph = custom.P_promotePortByName(graph,ctrlname+":r[in]",ctrlname+"_r")
        ctrlnamelist.append(ctrlname)


# create all the node for splineIK
    consplinename = jointnodenamelist[0]+"_splineIKCreate"
    consplinenode = graph.addNode(consplinename,"rig::ControlSpline")
    graph.updateNodeParms(consplinenode,{"order":order})


    samplesplinename = jointnodenamelist[0]+"_splineIKSample"
    samplesplinenode = graph.addNode(samplesplinename,"rig::SampleSplineTransforms::2.0")
    graph.updateNodeParms(samplesplinenode,{"tangent":tangent})



# connect all control to controlSplineNode
    for ctrlname in ctrlnamelist:
        graph = P_wire(graph,ctrlname+":xform[out]",consplinename+":cvs")
    

    graph = P_wire(graph,consplinename+":geo",samplesplinename+":geo")


# setup sampleSpline
    OutPortList:StringArray = []
    for index,jointname in enumerate(jointnodenamelist):
        indexstr:String = apex.string.FromInteger(index)


        OutPortList.append(samplesplinename+":xforms"+indexstr)
        
        graph = P_wire(graph,samplesplinename+":xforms",jointname+":xform[in]")

        # unpromote original controls
        graph = P_unWireInputByName(graph,jointname+":r[in]")

    return graph,jointnodenamelist,OutPortList