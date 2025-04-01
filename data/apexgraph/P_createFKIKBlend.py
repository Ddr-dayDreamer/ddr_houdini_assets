@subgraph
@namespace("custom")
def P_createFKIKBlend(graph:ApexGraphHandle,jointnamelist:StringArray,ikoutportlist:StringArray,absconarray:StringArray,controlTags:StringArray = []):
    # create abscon to drive blend
    graph,ctlname,ctl = custom.P_createAbstractControl(graph,absconarray[0],absconarray[1])
    graph.UpdateNodeTags(ctl,["fkik_blend"])
    graph = custom.P_promotePortByName(graph,ctlname+":x[in]",ctlname+"_x")
    

    # create fk chains and promote them
    graph,fkjointnamelist= custom.P_createRestChain(graph,jointnamelist,suffix = "_fk",promote = True)

    for index,fkjointname in enumerate(fkjointnamelist):
        jointname = jointnamelist[index]
        # promote fk rotation
        fkjointnode = graph.findNode(fkjointname)
        graph.UpdateNodeTags(fkjointnode,["fk_r"])
        graph.UpdateNodeTags(fkjointnode,controlTags)
        graph = custom.P_promotePortByName(graph,fkjointname+":r[in]",fkjointname+"_r")
        
        # setup blend node and blend parm
        blendnodename = jointname+"_fkik_blend"
        blendnode = graph.addNode(blendnodename,"transform::Blend")
        graph = P_wire(graph,fkjointname+":xform[out]",blendnodename+":a[in]")
        graph = P_wire(graph,ikoutportlist[index],blendnodename+":b[in]")

        graph = P_wire(graph,ctlname+":x[out]",blendnodename+":blend[in]")

        # setup blend result
        graph = P_wire(graph,blendnodename+":result",jointname+":xform[in]")

    return graph,ctlname