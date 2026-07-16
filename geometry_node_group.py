import bpy

# Create a new Geometry Node group
crowd_group = bpy.data.node_groups.new("CubeCrowdGenerator", "GeometryNodeTree")

# Create input/output nodes
group_in = crowd_group.nodes.new("NodeGroupInput")
group_out = crowd_group.nodes.new("NodeGroupOutput")

group_in.location = (-600, 0)
group_out.location = (600, 0)

# Define group interface sockets
interface = crowd_group.interface
interface.new_socket(name="Surface", in_out="INPUT", socket_type="NodeSocketGeometry")
interface.new_socket(name="Cubes", in_out="OUTPUT", socket_type="NodeSocketGeometry")

# Create internal nodes
distribute = crowd_group.nodes.new("GeometryNodeDistributePointsOnFaces")
instance = crowd_group.nodes.new("GeometryNodeInstanceOnPoints")
cube = crowd_group.nodes.new("GeometryNodeMeshCube")
realize = crowd_group.nodes.new("GeometryNodeRealizeInstances")
set_pos = crowd_group.nodes.new("GeometryNodeSetPosition")
rand_vec = crowd_group.nodes.new("FunctionNodeRandomValue")

# Configure random vector node
rand_vec.data_type = "FLOAT_VECTOR"
rand_vec.inputs["Min"].default_value = (-0.5, -0.5, 0.0)  # minimum offset
rand_vec.inputs["Max"].default_value = (0.5, 0.5, 0.5)  # maximum offset

# Layout nodes
distribute.location = (-400, 0)
rand_vec.location = (-200, -200)
set_pos.location = (-100, 0)
instance.location = (100, 0)
cube.location = (-400, -200)
realize.location = (300, 0)

# Create links
links = crowd_group.links
links.new(group_in.outputs["Surface"], distribute.inputs["Mesh"])
links.new(distribute.outputs["Points"], set_pos.inputs["Geometry"])
links.new(rand_vec.outputs["Value"], set_pos.inputs["Offset"])
links.new(set_pos.outputs["Geometry"], instance.inputs["Points"])
links.new(cube.outputs["Mesh"], instance.inputs["Instance"])
links.new(instance.outputs["Instances"], realize.inputs["Geometry"])
links.new(realize.outputs["Geometry"], group_out.inputs["Cubes"])
