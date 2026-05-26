import sys
import json


def solve(root_name, json_text):
    """Parse JSON and generate TypeScript interface definitions."""

    data = json.loads(json_text)

    # Normalize input to always be a list of objects
    if isinstance(data, dict):
        data = [data]

    nodes = {}        # path to InterfaceNode
    node_order = []   # insertion ordered list of paths




    class InterfaceNode:
        def __init__(self, path):
            self.path = path
            self.fields = {}
            self.record_count = 0  # number of objects merged into this node


        def merge(self, obj):
            """Merge a JSON object into this node, updating field info."""
            self.record_count += 1
            for key, value in obj.items():
                if key not in self.fields:
                    self.fields[key] = FieldInfo(key)
                self.fields[key].observe(value)

        def mark_absent(self, keys):
            """Handle fields absent in some records (reserved for future use)."""
            pass


    class FieldInfo:
        def __init__(self, key):
            self.key = key
            self.count = 0          # number of times this field was seen
            self.types = set()      # primitive types observed

            self.has_array = False
            self.has_object = False

            self.array_elements = []  # flattened array elements
            self.object_values = []   # collected nested objects

        def observe(self, value):
            """Record the type of an observed field value."""
            self.count += 1

            if value is None:
                self.types.add("null")
            elif isinstance(value, str):
                self.types.add("string")
            elif isinstance(value, bool):
                self.types.add("boolean")
            elif isinstance(value, (int, float)):
                self.types.add("number")
            elif isinstance(value, list):
                self.has_array = True
                self.array_elements.extend(value)
            elif isinstance(value, dict):
                self.has_object = True
                self.object_values.append(value)


    def get_or_create_node(path):
        """Return existing node for path, or register a new one."""
        if path not in nodes:
            node = InterfaceNode(path)
            nodes[path] = node
            node_order.append(path)
        return nodes[path]


    # Bootstrap root node and feed top level objects into it
    root_path = ()
    root_node = get_or_create_node(root_path)
    for obj in data:
        root_node.merge(obj)


    visited = set()

    def traverse(path):
        """DFS: discover nested object/array nodes and register them."""
        if path in visited:
            return
        visited.add(path)

        node = nodes[path]

        for key in sorted(node.fields.keys()):
            field = node.fields[key]
            child_path = path + (key,)

            # Merge nested objects into a child node for this field
            if field.has_object:
                child_node = get_or_create_node(child_path)
                for obj in field.object_values:
                    child_node.merge(obj)

            # Collect dict elements from arrays into the same child node
            dict_elements = []
            if field.has_array:
                dict_elements = [e for e in field.array_elements if isinstance(e, dict)]
                if dict_elements:
                    child_node = get_or_create_node(child_path)
                    for obj in dict_elements:
                        child_node.merge(obj)

            # Recurse into child if it holds structured data
            if field.has_object or dict_elements:
                if child_path in nodes:
                    traverse(child_path)

    traverse(root_path)


    # Assign unique TypeScript interface names to each path
    used_names = set()
    path_to_name = {}

    used_names.add(root_name)
    path_to_name[root_path] = root_name

    for path in node_order:
        if path == root_path:
            continue

        key = path[-1]
        base = key[0].upper() + key[1:]

        if base not in used_names:
            used_names.add(base)
            path_to_name[path] = base
        else:
            # Append numeric suffix to resolve name collisions
            suffix = 2
            while f"{base}{suffix}" in used_names:
                suffix += 1
            name = f"{base}{suffix}"
            used_names.add(name)
            path_to_name[path] = name


    def build_type_string(path, field):
        """Construct the TypeScript type annotation for a field."""
        type_parts = set()

        # Add primitive types directly
        for primitive in field.types:
            type_parts.add(primitive)

        # Nested object to reference the child interface by name
        if field.has_object:
            child_path = path + (field.key,)
            type_parts.add(path_to_name[child_path])

        # Array to infer element types and produce T[] or (A | B)[]
        if field.has_array:
            element_types = set()
            for element in field.array_elements:
                if element is None:
                    element_types.add("null")
                elif isinstance(element, str):
                    element_types.add("string")
                elif isinstance(element, bool):
                    element_types.add("boolean")
                elif isinstance(element, (int, float)):
                    element_types.add("number")
                elif isinstance(element, dict):
                    child_path = path + (field.key,)
                    element_types.add(path_to_name[child_path])

            if not element_types:
                array_str = "unknown[]"
            elif len(element_types) == 1:
                array_str = f"{next(iter(element_types))}[]"
            else:
                array_str = f'({" | ".join(sorted(element_types))})[]'

            type_parts.add(array_str)

        return " | ".join(sorted(type_parts))


    def render_interface(path):


        """Serialize an InterfaceNode to a TypeScript interface block."""
        node = nodes[path]
        name = path_to_name[path]

        if not node.fields:
            return f"export interface {name} {{}}"

        lines = [f"export interface {name} {{"]
        for key in sorted(node.fields.keys()):
            field = node.fields[key]
            type_str = build_type_string(path, field)
            # Mark field optional if it was absent in some records
            optional = "?" if field.count < node.record_count else ""
            lines.append(f"  {key}{optional}: {type_str};")
        lines.append("}")
        return "\n".join(lines)


    # Emit interfaces sorted alphabetically by name
    sorted_paths = sorted(node_order, key=lambda p: path_to_name[p])
    return "\n\n".join(render_interface(p) for p in sorted_paths)


def main():
    """Read test cases from stdin and write TypeScript interfaces to stdout."""
    lines = sys.stdin.read().split("\n")
    t = int(lines[0])

    results = []
    for i in range(t):
        root_name = lines[1 + 2 * i]
        json_text = lines[2 + 2 * i]
        results.append(solve(root_name, json_text))

    sys.stdout.write("\n---\n".join(results) + "\n")


if __name__ == "__main__":
    main()