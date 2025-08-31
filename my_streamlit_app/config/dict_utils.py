import json
import pandas as pd
import os
import sys
from pathlib import Path
parent_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(parent_dir))

DICT_FILE = "plugins/plugins.json"
SCRIPT_FILE = "scripts/scripts.json"

def load_dict(DICT_FILE="plugins/plugins.json"):
    if os.path.exists(DICT_FILE):
        with open(DICT_FILE, "r") as f:
            data = json.load(f)
        df = pd.DataFrame.from_dict(data, orient="index")
        df.reset_index(inplace=True)
        df.columns = ["Plugin", "Module", "Class"]
        return df
        # return pd.DataFrame(list(data.items()), columns=["Key", "Value"])
    else:
        return pd.DataFrame(columns=["Plugin", "Module", "Class"])

def save_dict(df, filepath=DICT_FILE):
    data = {
        row["Plugin"]: {
            "module": row["Module"],
            "class": row["Class"]
        }
        for _, row in df.iterrows()
    }
    
    with open(filepath, "w") as f:
        json.dump(data, f, indent=4)

def append_dict(df, filepath=DICT_FILE):
    with open(filepath, "r") as f:
        file = json.load(f)

    data = {
        row["Plugin"]: {
            "module": row["Module"],
            "class": row["Class"]
        }
        for _, row in df.iterrows()
    }
    file.update(data)

    with open(filepath, "w") as f:
        json.dump(file, f, indent=4)

def load_script_json(SCRIPT_FILE="scripts/scripts.json"):
    if os.path.exists(SCRIPT_FILE):
        with open(SCRIPT_FILE, "r") as f:
            data = json.load(f)
        df = pd.DataFrame.from_dict(data, orient="index")
        df.reset_index(inplace=True)
        df.columns = ["Scripts", "Module", "Arguments"]
        return df
        # return pd.DataFrame(list(data.items()), columns=["Key", "Value"])
    else:
        return pd.DataFrame(columns=["Scripts", "Module", "Arguments"])

def save_script_json(df, filepath=SCRIPT_FILE):
    data = {
        row["Scripts"]: {
            "module": row["Module"],
            "arguments": row["Arguments"]
        }
        for _, row in df.iterrows()
    }
    
    with open(filepath, "w") as f:
        json.dump(data, f, indent=4)

def append_script_json(df, filepath=SCRIPT_FILE):
    with open(filepath, "r") as f:
        file = json.load(f)

    data = {
        row["Scripts"]: {
            "module": row["Module"],
            "arguments": "Empty"
        }
        for _, row in df.iterrows()
    }
    file.update(data)

    with open(filepath, "w") as f:
        json.dump(file, f, indent=4)