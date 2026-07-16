def load(path, name="Group"):
    import json
    import bpy

    # Read the JSON data
    with open(path) as fp:
        data = json.load(fp)

    # Grab the relevant bits of information
    nodes = data["nodes"]
    nodes_by_id = { node["id"]: node for node in nodes }
    nodes_by_name = { node["name"]: node for node in nodes }

    outputs = data["outputs"]
    inputs = [v["id"] for v in nodes if v["type"] == "Input"]

    # Create a new Node group
    group = bpy.data.node_groups.new(name, "ShaderNodeTree")

    # Create input/output nodes
    group_in = group.nodes.new("NodeGroupInput")
    group_out = group.nodes.new("NodeGroupOutput")

    group_in.location = (-600, 0)
    group_out.location = (600, 0)

    # Define group interface sockets
    interface = group.interface

    for input in inputs:
        name = nodes_by_id[input]["name"]
        interface.new_socket(name=name, in_out="INPUT", socket_type="NodeSocketFloat")

    for output in outputs:
        name = nodes_by_id[output]["name"]
        interface.new_socket(name=name, in_out="OUTPUT", socket_type="NodeSocketFloat")
