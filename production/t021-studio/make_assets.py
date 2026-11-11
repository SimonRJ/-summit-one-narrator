import bpy, math, os
from mathutils import Vector
from pathlib import Path
out=Path(__file__).parent/'assets';out.mkdir(exist_ok=True)
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
s=bpy.context.scene;s.render.engine='CYCLES';s.cycles.samples=96
s.cycles.use_denoising=False;s.render.resolution_x=320;s.render.resolution_y=320;s.render.resolution_percentage=100
s.render.film_transparent=True;s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGBA'
s.world.color=(.22,.22,.22);s.view_settings.view_transform='AgX'
bpy.ops.object.camera_add(location=(0,-5,9));cam=bpy.context.object
cam.rotation_euler=(Vector((0,0,0))-cam.location).to_track_quat('-Z','Y').to_euler()
cam.data.type='ORTHO';cam.data.ortho_scale=2.8;s.camera=cam
def light(loc,power,size):
 bpy.ops.object.light_add(type='AREA',location=loc);o=bpy.context.object;o.data.energy=power;o.data.shape='DISK';o.data.size=size;o.rotation_euler=(-o.location).to_track_quat('-Z','Y').to_euler()
light((-3,-4,7),650,5);light((4,1,5),450,4);light((0,4,3),350,3)
bpy.ops.mesh.primitive_cylinder_add(vertices=96,radius=1,depth=.30,location=(0,0,0))
o=bpy.context.object;b=o.modifiers.new('Soft machined edges','BEVEL');b.width=.105;b.segments=6
o.modifiers.new('Weighted normals','WEIGHTED_NORMAL')
for p in o.data.polygons:p.use_smooth=True
m=bpy.data.materials.new('Ceramic');m.use_nodes=True;o.data.materials.append(m)
bs=m.node_tree.nodes.get('Principled BSDF');bs.inputs['Roughness'].default_value=.27;bs.inputs['Metallic'].default_value=.25
for name,color in [('gold',(.72,.35,.075,1)),('blue',(.055,.28,.64,1)),('mint',(.10,.51,.34,1)),('white',(.67,.73,.8,1))]:
 bs.inputs['Base Color'].default_value=color;s.render.filepath=str(out/f'{name}.png');bpy.ops.render.render(write_still=True)
