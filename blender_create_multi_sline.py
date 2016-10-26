import bpy
import math
from mathutils import Vector

for c in range(2240):

    c_extended = "%04d" % c

    file_name = "/home/haschka/stream/sline" + str(c)
    f = open(file_name)
    points = f.readlines()

    pointlist=[]
    v_accumulate = 0.
    for i in range(len(points)):
        buffer = points[i].split()
        pointlist.append((float(buffer[0]), float(buffer[1]), float(buffer[2]), float(buffer[3])))
        v_accumulate = v_accumulate + float(buffer[3])
    v_mean = v_accumulate/(float(len(points)))

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
    
    curvedata.use_path = True
    curvedata.use_path_follow = True
    curvedata.path_duration = len(pointlist)

    bpy.ops.mesh.primitive_cube_add(radius = 0.05, location = (0,0,0))
    cube = bpy.context.object
    #cyl.rotation_mode = 'XYZ'

    cube.name = 'flare' + c_extended

    cube.scale[0] = 0.02
    cube.scale[1] = 0.02
    cube.scale[2] = 0.08

    cube.constraints.new(type='FOLLOW_PATH')
    cube.constraints['Follow Path'].target = objectdata

    cube.constraints['Follow Path'].use_curve_follow = True
    cube.constraints['Follow Path'].use_curve_radius = True
    #cyl.constraints['Follow Path'].followpath_path_animate(constraint="Follow Path", owner='OBJECT')
    cube.rotation_euler = (math.pi/2.,0,0)

    t = 0.
    for i in range(len(pointlist)):
        x, y, z, v = pointlist[i]
        if ( v > 0.):
            t = (1/3.)*(1./v)+t
        if ( i%20 == 0 ):
            curvedata.eval_time = i
            curvedata.keyframe_insert("eval_time", frame = t)
