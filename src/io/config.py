from typing import Dict
import json

def load_config(path: str) -> Dict:
   
    file = open(path)
    configs_dict = json.load(file)
  
    return configs_dict