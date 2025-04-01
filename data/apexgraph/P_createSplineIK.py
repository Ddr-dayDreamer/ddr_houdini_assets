@subgraph
@namespace("custom")
def P_createSplineIK(graph:ApexGraphHandle,
                     order:Int,
                     ctrlrefnamelist:StringArray,
                     ctrlnamebase:String,
                     ctrlparentspacenamelist:StringArray,
                     ctrlparentspaceabsconarray:StringArray,
                     jointnodenamelist:StringArray,
                     respectctrlparents:Bool = False,
                     controltags:StringArray = ["ik_handle"],
                     tangent:Vector3 = (1.0,0.0,0.0),
                     keepoffset:Bool = True

                     ):
# create rest chain first to make sure dont lose xform    
    # graph,restjointnamelist = custom.P_createRestChain(graph,jointnodenamelist,"_ikrest")

# create controls
    ctrlnamelist:StringArray = []
    for index,ctrlref in enumerate(ctrlrefnamelist):
        indexstr:String = apex.string.FromInteger(index)
        ctrlname = ctrlnamebase+"00"+indexstr
        if respectctrlparents == True:
            graph = custom.P_createRest(graph,ctrlref,ctrlname)
        if respectctrlparents == False:
            if index == 0:
                graph = custom.P_createRest(graph,ctrlref,ctrlname)
            else:
                graph,getxformname,getxformportname = custom.P_createParentSpaceBlend(graph,ctrlname,ctrlparentspacenamelist,ctrlref,ctrlparentspaceabsconarray)
                graph.addNode(ctrlname,"TransformObject")
                graph = P_wire(graph,getxformportname,ctrlname+":parent[in]")
                # graph = custom.P_createRest(graph,ctrlref,ctrlname,"specify",ctrlparentname)
        ctrlnode = graph.findNode(ctrlname)
        graph.updateNodeTags(ctrlnode,controltags)
        graph = custom.P_promotePortByName(graph,ctrlname+":t[in]",ctrlname+"_t")
        graph = custom.P_promotePortByName(graph,ctrlname+":r[in]",ctrlname+"_r")
        ctrlnamelist.append(ctrlname)

    

# compute spline rest length
    restlengthname = jointnodenamelist[0]+"_splineIKGetRestLength"
    restlengthnode = graph.addNode(restlengthname,"rig::SplineInterpolateTransforms::2.0")
    graph.updateNodeParms(restlengthnode,{"order":order,"tangent":tangent})
    for ctrlref in ctrlrefnamelist:
        graph = P_wire(graph,ctrlref+":xform[out]",restlengthname+":cvs")

    restlength:Float = custom.P_getOutputFloat(graph,restlengthname,"arclength")

    # since we got rest length ,we can delete this node
    graph.deleteNode(restlengthnode)


    

# create all the node for splineIK
    consplinename = jointnodenamelist[0]+"_splineIKCreate"
    consplinenode = graph.addNode(consplinename,"rig::ControlSpline")
    graph.updateNodeParms(consplinenode,{"order":order})

    getpivotname = jointnodenamelist[0]+"_splineIKGetPivot"
    getpivotnode = graph.addNode(getpivotname,"transform::Explode")

    xformname = jointnodenamelist[0]+"_splineIKScale"
    xformnode = graph.addNode(xformname,"sop::xform")

    dividename = jointnodenamelist[0]+"_splineIKDivide"
    dividenode = graph.addNode(dividename,"Divide<Float>")

    getlengthname = jointnodenamelist[0]+"_splineIKGetLength"
    getlengthnode = graph.addNode(getlengthname,"rig::SampleSplineTransforms::2.0")
    graph.updateNodeParms(getlengthnode,{"tangent":tangent})

    samplesplinename = jointnodenamelist[0]+"_splineIKSample"
    samplesplinenode = graph.addNode(samplesplinename,"rig::SampleSplineTransforms::2.0")
    graph.updateNodeParms(samplesplinenode,{"tangent":tangent})

# connect all control to controlSplineNode
    for ctrlname in ctrlnamelist:
        graph = P_wire(graph,ctrlname+":xform[out]",consplinename+":cvs")
    
# setup xform for scale curve
    graph = P_wire(graph,ctrlrefnamelist[0]+":xform[out]",getpivotname+":m")
    graph = P_wire(graph,getpivotname+":t",xformname+":p")
    graph = P_wire(graph,getpivotname+":r",xformname+":pr")

    graph = P_wire(graph,consplinename+":geo",xformname+":geoinput0")

    # connect scale value to xform
    graph = P_wire(graph,dividename+":result",xformname+":scale")

    # connect xform to samplespline
    graph = P_wire(graph,xformname+":geo",samplesplinename+":geo")

    # compute rest_length/length
    graph.updateNodeParms(dividenode,{"a":restlength})
    graph = P_wire(graph,consplinename+":geo",getlengthname+":geo")
    graph = P_wire(graph,getlengthname+":arclength",dividename+":b")


# setup sampleSpline
    scaleMatrixNameList:StringArray = []
    restOffsetOutPortList:StringArray = []
    for index,jointname in enumerate(jointnodenamelist):

        # create scaleMatrix node to remove scale effect from xform node
        scaleMatrixName = jointname+"_splineIKInvertScale"
        scaleMatrixNode = graph.addNode(scaleMatrixName,"custom::scaleMatrix")
        graph.updateNodeParms(scaleMatrixNode,{"invertscale":True})

        graph = P_wire(graph,dividename+":result",scaleMatrixName+":scale")
        graph = P_wire(graph,samplesplinename+":xforms",scaleMatrixName+":matrixin")
        scaleMatrixNameList.append(scaleMatrixName)

    if keepoffset:
        for index,scaleMatrixName in enumerate(scaleMatrixNameList):
            
            parentm:Matrix4 = custom.P_getOutputMatrix(graph,scaleMatrixName,"matrixout")
            
            childm:Matrix4 = custom.P_getOutputMatrix(graph,jointnodenamelist[index],"xform")


            invertparentm:Matrix4 = invert(parentm)
            rest:Matrix4 = childm*invertparentm

            restOffsetName = jointnodenamelist[index]+"_restOffset"
            restOffsetNode = graph.addNode(restOffsetName,"Multiply<Matrix4>")
            graph.updateNodeParms(restOffsetNode,{"a":rest})
            restOffsetOutPortList.append(restOffsetName+":result")
            
            graph = P_wire(graph,scaleMatrixName+":matrixout",restOffsetName+":b")

            graph = P_wire(graph,restOffsetName+":result",jointnodenamelist[index]+":xform[in]")

            # unpromote original controls
            graph = P_unWireInputByName(graph,jointnodenamelist[index]+":r[in]")

    else:
        for index,scaleMatrixName in enumerate(scaleMatrixNameList):

            restOffsetOutPortList.append(scaleMatrixName+":matrixout")
            
            graph = P_wire(graph,scaleMatrixName+":matrixout",jointnodenamelist[index]+":xform[in]")

            # unpromote original controls
            graph = P_unWireInputByName(graph,jointnodenamelist[index]+":r[in]")

    return graph,jointnodenamelist,restOffsetOutPortList