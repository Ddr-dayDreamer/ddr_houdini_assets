# ddr的apex自定义模块帮助

## P_createRest

custom.P_createRest(
graph:ApexGraphHandle,
node_name:String,
restnodename:String = "default",
mode:String = 'parent',
specifyParentName:String = 'specifyParent')

return graph,restnodename

非常常用的一个函数，用于创建rest transformobject
nodename为参考节点（位置）的名字
restnodename代表将要创建的节点名字（不设置时为节点名后加"_rest"）
mode可选三个："parent","specify","world"
顾名思义，不做赘述
最后的参数specifyParentName仅在specify模式下启用，指定父级的名字


## P_updateRest
custom.P_updateRest(graph:ApexGraphHandle, node_name:String,childref:String,parentref:String)
更新指定节点的restlocal为子节点世界矩阵*父节点世界矩阵的逆
用于更新父子级关系。



## P_createRestChain
custom.P_createRestChain(
graph:ApexGraphHandle,
nodenamelist:StringArray,
suffix:String = "_restchain",
promote:Bool = False)

根据nodenamelist的顺序创建一条父子层级的transformobject链，
一般用于创建多关节ik时，准备关节的rest xform，或者用于创建fkikblend。
suffix指定关节链名字的后缀
promote将自动promote创建的r[in]属性



## P_createAbstractControl
P_createAbstractControl(
    graph,
    absconname,
    refname,
    promote:Bool = False,
    defaultvalue:Float = 0.0,
    tags:StringArray = ["None"]
    )

return graph,abscon.name(),abscon

根据refname的节点位置创建按钮
放心使用，带有内置检测，如果同名节点已存在，或者已经被连接了位置parm，将不会修改，只返还找到的节点名。
promote True 则会promote abscon的x属性

## P_createRotationConstraint
P_createRotationConstraint(
    graph:ApexGraphHandle,
    nodename:String,
    targetname:String,
    weight:Float,
    connect:Bool=False)

return graph,rotconsname

创建旋转约束，不过如果不设置connect为真，则不会显示效果，而是只创建节点，方便作为子模块使用


## P_parentByName
P_parentByName(graph,childname,parentname)

创建父子层级关系，但是其实就是连接了transformobject的对应端口，如果不是这种节点，大概率无效（比如AbstractControl）

## P_promotePortByName
P_promotePortByName(graph,pattern,name)

通过pattern promote端口,注意填写name，代表连向输入节点的频道名字，需要是独特的，哪怕是一个节点的t，r，s输入name也需要不同，否则会出问题（几个频道搅在一起了）


## P_wire
P_wire(graph,src_pattern,dst_pattern)
**不需要custom关键字调用**
非常常用的函数，连接两个端口
调用范例：graph = P_wire(graph,"src_pattern","dst_pattern")

## P_unWireInputByName
P_unWireInputByName(graph,pattern)
**不需要custom关键字调用**
取消一个input port的连接
主要用于解除promote的参数

## P_createFKIKBlend
P_createFKIKBlend(
    graph:ApexGraphHandle,
    jointnamelist:StringArray,
    ikoutportlist:StringArray,
    absconarray:StringArray,
    controlTags:StringArray = [])
    
目标为创建任意个关节和ik节点之间的fkik blend，用于创建了ik之后对已经可用的ik节点进行扩展。

jointnamelist 应该是一个按关节父子顺序排列的关节名 字符串序列（StringArray）  
ikoutportlist 应该是这个ik节点的端口名 字符串序列（StringArray）  
**jointnamelist和ikoutportlist必须是顺序上,数量上，意义上一一对应的**，

absconarray是将要创建的abstractcontrol节点的名字，参考位置（父级）


## P_createMultiBoneIK
P_createMultiBoneIK(
    graph:ApexGraphHandle,
    nodelist:StringArray,
    rootdriver:StringArray,
    twist:StringArray,
    goal:StringArray,
    parentspacenodelist:StringArray = ["None"],
    parentspaceconarray:StringArray = ["None","None"]
    )

    # rootdriver,twist and goal,these three array ,will define name of created node,whether to use specified node as xform ref,and specified node name
    # so it will be ["expected control name","True","control reference name"]
    # for root control,I think it will only be in the first joint position,so,for rootdriver[1],"True" means function will promote rootdriver to be animated.
    # and for rootdriver[2] it will mean nothing.
    # for twist,if twist[1]set to False,which means you dont use a twist ref,then i will set to use no twist in multiboneik node
    # which will result in your
    # as for parentspace blend ,parentspacearray means ["parent space blend abscon name","parent space blend abscon ref"].

nodelist：ik关节链（按父子顺序）
rootdriver，twist，goal三个序列有特殊格式[“控制器的名字”，“是/否”，“坐标参考节点名字”] rootdriver的【1】将代表是否promote root控制器的输入（一般不用）， 
twist【1】一般为是，以启用参考位置，而如果为否，则将禁用twist的作用，详见multiboneik节点。
goal【1】为是时，将创建一个额外的控制器在末端关节位置，主要为了合适的轴旋转。

parentspacenodelist，指定父级节点名字列表，以设置多个父级空间的变换。
parentspaceconarray 不设置的话将不会创建多个父级空间。如果需要设置，格式为【想要的控制器名字，控制器参考位置】
另外，parentblend控制器将带有一个"ik_parentspace"标签用于控制器设置。




## P_createWingFollow
custom.P_createWingFollow(
    graph:ApexGraphHandle,
    nodename:String,
    targetname:String,
    targetname2:String,
    absconname:String,
    weight:Float = 0.5)

用于创建翅膀的跟随
其核心为两个旋转约束（自己写的）的混合，absconname用于连接已经创建的控制器，所以需要先创建好blend的控制器（P_createAbstractControl）


## P_setupTwistJoint
custom.P_setupTwistJoint(
    graph:ApexGraphHandle,
    twistjointname:String,
    parentname:String,
    childname:String,
    axis:Vector3 = (1.0,0.0,0.0),
    pos:Float = 0.5)

设置twistjoint。
需要事先创建好关节，这些关节应该是父级关节（parentname）的子级
axis代表各个旋转轴的weight。  
pos代表关节的在父子关节间的位置（从父到子的位置），在有多个twistjoint时使用。

## P_setupBlendShape

custom.P_setupBlendShape(graph:ApexGraphHandle,
    bsnodename:String,
    bsdict:Dict,
    bsGeoGroupName:String = "",
    bsAttribs:String = "P",
    boneDeformNodeName:String = "Bonedeformation",
    restGeoName = "pointtransform_rest",
    pointTransformNodeName:String = "pointtransform",
    shapename:String = "Base.shp",
    skeletonname:String = "Base.skel")

设置blendshape。一般只需要设置 前面三个参数，后面的参数仅是应对复杂情况。
bsdict这个字典的格式是{"blendshape的名字（pack后的name prim attr）":"希望创建bs控制器的父级的名字（用于设置控制器位置）"，...后面n个同上}
设计上希望这个函数可以支持在已经创建的bs节点上添加新的bs，但是似乎没这个必要了，我们是程序化绑定对吧，回来加上就行了。


## P_createBlendRotate
P_createBlendRotate(graph:ApexGraphHandle,
                    drivenname:String,
                    controlname:String,
                    controlrefname:String,
                    contorlportname:String = "x[out]",
                    controltags:StringArray = ["blend_rot"],
                    minvalue:Float = 0.0,
                    maxvalue:Float = 1.0,
                    minvector:Vector3 = (0.0,0.0,0.0),
                    maxvector:Vector3 = (90.0,90.0,90.0),
                    )

创建类似于手指弯曲等方便动画制作的pose blend效果
对于复杂的情况进行了优化，所以可以多次调用，创建一（控制器）对多（关节），多对一等效果。
value可以接受负值。


## P_createSplineIK
P_createSplineIK(graph:ApexGraphHandle,
                order:Int,
                ctrlrefnamelist:StringArray,
                ctrlnamebase:String,
                ctrlparentname:String,
                jointnodenamelist:StringArray,
                respectctrlparents:Bool = False,
                tangent:Vector3 = (1.0,0.0,0.0)
                )
创建一个固定长度的曲线ik
将根据namebase自动创建001-00n个控制器（在ref位置）
如果respectctrlparents为是，控制器将跟随参考节点的父级，如果为否将全部跟随指定父级。



## P_getOutputFloat/P_getOutputMatrix
P_getOutputFloat(graph:ApexGraphHandle,nodename:String,portname:String)
将会执行graph，并获取指定端口的输出
用于计算一个已有值，比如获取一个节点的xform矩阵。


## P_createParentSpaceBlend
P_createParentSpaceBlend(graph:ApexGraphHandle,
                        basename:String,
                        parentspacenamelist:StringArray,
                        nodename:String,
                        absconarray:StringArray,
                        updatenode:Bool = False)

    return graph,getxformname,getxformportname

为了在ik中创建parentspaceblend 而设计的函数，目前没有在createmultiboneik中使用（虽然是同款的内容和逻辑），而是在reverse foot中使用了。
nodename代表要给它创建parentblend的节点名字。
absconarray则是默认的【控制器名字，控制器参考】
默认不会连接创建的节点到parent in，updatenode 为true时会自动连接。


## P_setupReverseFoot
P_setupReverseFoot(graph:ApexGraphHandle,
                        jointlist:StringArray,
                        basename:String,
                        reflist:StringArray,
                        ikgoalname:String,
                        walkcontrolarray:StringArray,
                        walkconvaluearray:Vector3Array,
                        parentspacenamelist:StringArray,
                        parentblendarray:StringArray,
                        ):
    # jointlist stands for [jnt_l_ball_001,jnt_l_toe_001]
    # basename for clear node name
    # ref list has 7 element:
    #     handleref,    heelref,    tipref,    inpivot,    outpivot,    toeref,    ballref
    # mind here toeref is before ballref
    # ikgoalname stans for the ik goal nodename,for leg always ctl_l_leg_IKGoal_001
    # walkcontrolarray is [walkcon name,walk con ref]
    # walkconvaluearray is [vector when walkcon is 1 set to ball control,vector when walkcon is -1 set to heel control]
    # parentspacenamelist and parentblend array should be the same as ik leg.
