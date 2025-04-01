@subgraph
@namespace("custom")
def P_createAbstractControl(graph:ApexGraphHandle,absconname:String,refname:String,promote:Bool = False,defaultvalue:Float = 0.0,tags:StringArray = ["None"]):
    abscon = graph.FindOrAddNode(absconname,"AbstractControl")
    
    # if this abs control has already there and has xform input,then pass
    xformport = graph.GetConnectedPort(graph.findPort(abscon,"xform[in]"))
    if not convert(graph.GetConnectedPort(xformport)):
        graph = P_wire(graph,refname+":xform[out]",absconname+":xform[in]")
    else:
        pass
        
    # setup parms/tags
    graph.updateNodeParms(abscon,parms = {"x":defaultvalue})
    if tags[0] != "None":
        graph.updateNodeTags(abscon,tags)

    if promote == True:
        graph = custom.P_promotePortByName(graph,absconname+":x[in]",absconname+"_x")
        
    return graph,abscon.name(),abscon