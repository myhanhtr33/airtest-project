import tests.popupSurprise
from tests import *
import os
from utils.device_setup import connect_to_unity
if __name__ == "__main__":
    # tests.popupSurprise.runTest()


    def print_poco_hierarchy(node=None, indent=0, lines=None):
        from airtest.core.api import sleep  # Optional, in case needed for timing

        if lines is None:
            lines = []
            node = poco()  # this is the entry point for UnityPoco

        try:
            name = node.get_name()
            node_type = node.attr('type')
            clickable = node.attr('clickable')
            visible = node.attr('visible')
            text = node.get_text()
            line = "  " * indent + f"{name} (type={node_type}, clickable={clickable}, visible={visible}, text={text})"
        except Exception as e:
            line = "  " * indent + f"[Error reading node]: {e}"

        print(line)
        lines.append(line)

        try:
            children = node.children()
            for child in children:
                print_poco_hierarchy(child, indent + 1, lines)
        except Exception as e:
            lines.append("  " * (indent + 1) + f"[Error getting children]: {e}")

        if indent == 0:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            file_path = os.path.join(script_dir, "hierarchyDump.txt")
            with open(file_path, "w", encoding="utf-8") as f:
                f.write("\n".join(lines))
            print(f"\nLive Unity UI hierarchy dumped to: {file_path}")


    def save_hierarchy_to_file(poco, filename="hierarchyDump.txt"):
        hierarchy = poco.agent.hierarchy.dump()

        def walk(node, indent=0):
            lines = []
            name = node.get("name", "Unknown")
            node_type = node.get("type", "Unknown")
            lines.append("  " * indent + f"{name} (type={node_type})")

            # Print all known attributes (clickable, visible, text, etc.)
            for key, value in node.items():
                # if key == "clickable" and value is False:
                #     continue
                if key not in ["name", "type", "children"]:
                        lines.append("  " * (indent + 1) + f"{key}: {value}")

            for child in node.get("children", []):
                lines.extend(walk(child, indent + 1))

            return lines

        lines = walk(hierarchy)
        with open(filename, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        print(f"Hierarchy saved to {filename}")

print("helolheloo")
poco = connect_to_unity()
# print_poco_hierarchy()
save_hierarchy_to_file(poco)