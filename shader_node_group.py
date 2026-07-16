import bpy

# Create a new Geometry Node group
stripe_group = bpy.data.node_groups.new("Stripes", "ShaderNodeTree")

# Create input/output nodes
group_in = stripe_group.nodes.new("NodeGroupInput")
group_out = stripe_group.nodes.new("NodeGroupOutput")

group_in.location = (-600, 0)
group_out.location = (600, 0)

# Define group interface sockets
interface = stripe_group.interface
interface.new_socket(name="Coordinate", in_out="INPUT", socket_type="NodeSocketFloat")
interface.new_socket(name="Stripes", in_out="OUTPUT", socket_type="NodeSocketFloat")

# Create internal nodes
scale = stripe_group.nodes.new("ShaderNodeMath")
scale.operation = "MULTIPLY"
scale.inputs[1].default_value = 20

modulo = stripe_group.nodes.new("ShaderNodeMath")
modulo.operation = "FLOORED_MODULO"
modulo.inputs[1].default_value = 1.0

# Create links
links = stripe_group.links
links.new(group_in.outputs["Coordinate"], scale.inputs[0])
links.new(scale.outputs["Value"], modulo.inputs[0])
links.new(modulo.outputs["Value"], group_out.inputs["Stripes"])
