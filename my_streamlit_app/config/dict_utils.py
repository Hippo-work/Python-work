import json
import pandas as pd
import os
import sys
from pathlib import Path
parent_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(parent_dir))

DICT_FILE = "plugins/plugins.json"

def load_dict():
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

def save_dict(df):
    df["Plugin"] = df["Plugin"].astype(str)
    df["Module"] = df["Module"].astype(str)
    df["Class"] = df["Class"].astype(str)
    data = dict(zip(df["Plugin"], zip(df["Module"], df["Class"])))
    with open(DICT_FILE, "w") as f:
        json.dump(data, f, indent=4)
