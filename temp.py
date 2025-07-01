import os
import logging
from pathlib import Path



list_of_files = [
    ".env" , 
    ".env.example" , 
    "requirements.txt" , 
    "LICENSE" , 
    "frontend.py" , 
    "System/helper.py" , 
    "README.md" , 
    "Notebooke/main.ipynb"
]


for filepath in list_of_files:
     filepath = Path(filepath)
     filedir, filename = os.path.split(filepath)
     if filedir != "":
          os.makedirs(name=filedir, exist_ok=True)
     if not os.path.exists(filepath):
          with open(file=filepath, mode="w") as f:
               pass
 