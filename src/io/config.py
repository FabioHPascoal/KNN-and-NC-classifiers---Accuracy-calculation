from typing import Dict
import json

def load_config(path: str) -> Dict:
   
    with open(path) as file:
        configs_dict = json.load(file)
  
    return configs_dict