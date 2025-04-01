@subgraph
@namespace("custom")
def filterRotation(vector:Vector3):
    x = apex.getComponent(vector,0)
    y = apex.getComponent(vector,1)
    z = apex.getComponent(vector,2)
    if x<-180.0:
        x+=360.0
    if x>180.0:
        x-=360.0
    if y<-180.0:
        y+=360.0
    if y>180.0:
        y-=360.0
    if z<-180.0:
        z+=360.0
    if z>180.0:
        z-=360.0
    
    out:Vector3 = (x,y,z)
    return out