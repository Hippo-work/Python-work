import json
import pandas as pd
import os

DICT_FILE = "dictionary.json"

def load_dict():
    if os.path.exists(DICT_FILE):
        with open(DICT_FILE, "r") as f:
            data = json.load(f)
        return pd.DataFrame(list(data.items()), columns=["Key", "Value"])
    else:
        return pd.DataFrame(columns=["Key", "Value"])

def save_dict(df):
    df["Value"] = df["Value"].astype(str)
    data = dict(zip(df["Key"], df["Value"]))
    with open(DICT_FILE, "w") as f:
        json.dump(data, f, indent=4)
