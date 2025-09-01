import re
from pathlib import Path
import streamlit as st

st.write("Script Descriptions and the order of Arguments (until i make it named args)")
def parse_sh_metadata(file_path):
    metadata = {
        "module": None,
        "description": None,
        "arguments": []
    }

    with open(file_path, "r") as f:
        for line in f:
            line = line.strip()
            if line.startswith("# Module:"):
                metadata["module"] = line.split("Module:")[1].strip()
            elif line.startswith("# Desc:"):
                metadata["description"] = line.split("Desc:")[1].strip()
            elif line.startswith("# ARG:"):
                match = re.match(r"# ARG:\s*(\w+):(\w+):(.*)", line)
                if match:
                    arg_name, arg_type, arg_desc = match.groups()
                    metadata["arguments"].append({
                        "name": arg_name,
                        "type": arg_type,
                        "description": arg_desc.strip()
                    })
    return metadata

meta = parse_sh_metadata("scripts/truncate.sh")

def discover_plugins(directory):
    registry = {}
    for path in Path(directory).glob("*.sh"):
        meta = parse_sh_metadata(path)
        if meta["module"]:
            registry[meta["module"]] = {
                "path": str(path),
                "description": meta["description"],
                "arguments": meta["arguments"]
            }
    return registry

scripts = discover_plugins("scripts")

for script in scripts:
    with st.expander(f"{script}"):
        st.write(scripts[script])