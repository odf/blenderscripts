def load(path, name="Group"):
    import json
    import bpy

    # Read the JSON data
    with open(path) as fp:
        data = json.load(fp)

    # Grab the relevant bits of information
    nodes_in = data["nodes"]
    nodes_in_by_id = { node["id"]: node for node in nodes_in }

    outputs = data["outputs"]
    inputs = [v["id"] for v in nodes_in if v["type"] == "Input"]

    # Create a new Node group
    group = bpy.data.node_groups.new(name, "ShaderNodeTree")

    # Create input/output nodes
    group_in = group.nodes.new("NodeGroupInput")
    group_out = group.nodes.new("NodeGroupOutput")

    group_in.location = (-700, 0)
    group_out.location = (-400 + 20 * max(v["id"] for v in nodes_in), 0)

    # Define group interface sockets
    interface = group.interface

    for k, input in enumerate(inputs):
        node_in = nodes_in_by_id[input]
        name = node_in["name"]
        socket = interface.new_socket(
            name=name, in_out="INPUT", socket_type="NodeSocketFloat"
        )
        socket.default_value = node_in["value"]

    for output in outputs:
        name = nodes_in_by_id[output]["name"]
        interface.new_socket(
            name=name, in_out="OUTPUT", socket_type="NodeSocketFloat"
        )

    # Create internal nodes
    nodes_out_by_id = {}

    for v in nodes_in:
        if v["type"] == "Math":
            id = v["id"]
            op = v["op"]

            node = group.nodes.new("ShaderNodeMath")
            node.operation = op.upper()
            node.location = (-600 + 20 * id, -975 + 150 * (id % 12))

            nodes_out_by_id[id] = node

    # Create links
    links = group.links

    for id in nodes_out_by_id:
        node_in = nodes_in_by_id[id]
        node_out = nodes_out_by_id[id]

        for k, (key, val) in enumerate(node_in["inputs"]):
            if key == "node":
                source = nodes_out_by_id.get(val, None)
                if source is None:
                    input_name = nodes_in_by_id[val]["name"]
                    links.new(group_in.outputs[input_name], node_out.inputs[k])
                else:
                    links.new(source.outputs[0], node_out.inputs[k])
            elif key == "value":
                node_out.inputs[k].default_value = val

        if id in outputs:
            output_name = nodes_in_by_id[id]["name"]
            links.new(node_out.outputs[0], group_out.inputs[output_name])
