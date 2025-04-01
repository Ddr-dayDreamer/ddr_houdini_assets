@subgraph
@namespace("custom")
def P_createParentSpaceBlend(graph:ApexGraphHandle,basename:String,parentspacenamelist:StringArray,nodename:String,absconarray:StringArray,updatenode:Bool = False):
    # this function will create several parent to get for one node.
    # it is intend to use in ik controls/reverse foot.
    # it will not directly wire to this node,but will output name of the array:get node and port name of xform output.
    # so you will need to wire this port to this node as parent mannually.
    abscontrolname:String = absconarray[0]
    abscontrolref:String = absconarray[1]
    parentarrayname = basename+"_parentarray"
    parentarray = graph.findOrAddNode(parentarrayname,"array::Build<Matrix4>")
    getxformname = basename+"_getparent"
    getxform = graph.findOrAddNode(getxformname,"array::Get<Matrix4>")
    graph = P_wire(graph,parentarrayname+":result",getxformname+":array")

    for index,parentspacename in enumerate(parentspacenamelist):
        idstr = apex.string.FromInteger(index)
        graph,parentname= custom.P_createRest(graph,nodename,basename+"_parent"+idstr+parentspacename,mode = "specify",specifyParentName = parentspacename)
        graph = P_wire(graph,parentname+":xform[out]",parentarrayname+":values")

    # create  parent space blend control and promote it
    graph,parentspacecontolname,parentspacecontol = custom.P_createAbstractControl(graph,abscontrolname,abscontrolref,promote = True)

    graph.updateNodeTags(parentspacecontol,["ik_parentspace"])

    convertnodename = basename+"_convert"
    convertnode = graph.addNode(convertnodename,"custom::floatToInt")

    graph = P_wire(graph,parentspacecontolname+":x[out]",convertnodename+":a")
    graph = P_wire(graph,convertnodename+":b",getxformname+":index")

    getxformportname = getxformname+":value"


    if updatenode:
        zero:Matrix4 = ((1,0,0,0),(0,1,0,0),(0,0,1,0),(0,0,0,1))
        node = graph.findNode(nodename)
        graph.updateNodeParms(node,parms = {"restlocal":zero})

        graph = P_wire(graph,getxformportname,nodename+":parent[in]")

    return graph,getxformname,getxformportname