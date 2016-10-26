import bpy
import math
from mathutils import Vector

# offset between the beginning end the end of the bevel
t_offset = 20

# read 10 stream lines
for c in range(1664):

    #obtain the correct streamlines from the files
    c_extended = "%d" % c

    file_name = "/tmp/testcase2/slines/sline" + str(c)
    f = open(file_name)
    points = f.readlines()

    # read the points and the associated velocity
    pointlist=[]
    v_accumulate = 0.
    for i in range(len(points)):
        buffer = points[i].split()
        pointlist.append((float(buffer[0]), float(buffer[1]), float(buffer[2]), float(buffer[3])))
        v_accumulate = v_accumulate + float(buffer[3])
    v_mean = v_accumulate/(float(len(points)))

    # create the curve from the pointlist
    
    curvedata = bpy.data.curves.new(name = "Curve." + c_extended, type = 'CURVE')
    curvedata.dimensions = '3D'

    objectdata = bpy.data.objects.new("ObjCurve", curvedata)
    objectdata.location = (0,0,0)
    bpy.context.scene.objects.link(objectdata)

    polyline = curvedata.splines.new('POLY')
    polyline.points.add(len(pointlist)-1)

    for num in range(len(pointlist)):
        x, y, z, w = pointlist[num]
        polyline.points[num].co = (x, y, z, 1.0)

    # set bevel to full so that we have an entire tube
        
    curvedata.fill_mode = 'FULL'
    # set the tube radius
    curvedata.bevel_depth = 0.01

    # generate the keyframes at the right position

    t_start = 0.
    t_end = t_offset
    for i in range(len(pointlist)):
        x, y, z, v = pointlist[i]
        if ( v > 0.):
            t_start = (1/3.)*(1./v)+t_start
            t_end = (1/3.)*(1./v)+t_end
        # save a keframe only each 20th steps to save some space.. 
        if ( i%20 == 0 ):
            curvedata.bevel_factor_start = i/float(len(pointlist))
            curvedata.bevel_factor_end = i/float(len(pointlist))
            curvedata.keyframe_insert("bevel_factor_start", frame = t_start)
            curvedata.keyframe_insert("bevel_factor_end", frame = t_end)
