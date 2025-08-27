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

def save_dict(df, filepath="my_dict.json"):
    data = {
        row["Plugin"]: {
            "module": row["Module"],
            "class": row["Class"]
        }
        for _, row in df.iterrows()
    }
    
    with open(DICT_FILE, "w") as f:
        json.dump(data, f, indent=4)
