import bpy
import bmesh

bpy.ops.object.select_pattern(pattern="Cylinder")
bpy.ops.object.mode_set(mode='EDIT')

obj = bpy.context.active_object


bm = bmesh.from_edit_mesh(obj.data)
bpy.ops.mesh.select_all()

bm.edges.ensure_lookup_table()
bm.edges[2].seam = True

bpy.context.tool_settings.mesh_select_mode = (False, False, True)

bpy.ops.mesh.select_all()
bm.faces.ensure_lookup_table()

# Disable Top and Buttum Faces
bm.faces[30].select = False
bm.faces[33].select = False

bpy.ops.uv.unwrap()

uv_layer = bm.loops.layers.uv.verify()

u_scale = 1.
v_scale = 1.

du = u_scale/32.

for i in range(0,30):
    bm.faces[i].loops[0][uv_layer].uv[0] = u_scale-(i)*du
    bm.faces[i].loops[0][uv_layer].uv[1] = 0
    bm.faces[i].loops[1][uv_layer].uv[0] = u_scale-(i)*du
    bm.faces[i].loops[1][uv_layer].uv[1] = v_scale
    bm.faces[i].loops[2][uv_layer].uv[0] = u_scale-(i+1)*du
    bm.faces[i].loops[2][uv_layer].uv[1] = v_scale
    bm.faces[i].loops[3][uv_layer].uv[0] = u_scale-(i+1)*du
    bm.faces[i].loops[3][uv_layer].uv[1] = 0

bm.faces[31].loops[0][uv_layer].uv[0] = u_scale-(32-1)*du
bm.faces[31].loops[0][uv_layer].uv[1] = 0
bm.faces[31].loops[1][uv_layer].uv[0] = u_scale-(32-1)*du
bm.faces[31].loops[1][uv_layer].uv[1] = v_scale
bm.faces[31].loops[2][uv_layer].uv[0] = u_scale-(32)*du
bm.faces[31].loops[2][uv_layer].uv[1] = v_scale
bm.faces[31].loops[3][uv_layer].uv[0] = u_scale-(32)*du
bm.faces[31].loops[3][uv_layer].uv[1] = 0

bm.faces[32].loops[0][uv_layer].uv[0] = u_scale-(31-1)*du
bm.faces[32].loops[0][uv_layer].uv[1] = 0
bm.faces[32].loops[1][uv_layer].uv[0] = u_scale-(31-1)*du
bm.faces[32].loops[1][uv_layer].uv[1] = v_scale
bm.faces[32].loops[2][uv_layer].uv[0] = u_scale-(31)*du
bm.faces[32].loops[2][uv_layer].uv[1] = v_scale
bm.faces[32].loops[3][uv_layer].uv[0] = u_scale-(31)*du
bm.faces[32].loops[3][uv_layer].uv[1] = 0
