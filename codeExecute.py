import technicalAnalysis  as ta
import binanceAPI as bAPIfunc
import json
from datetime import *

# Generate keys or load them
try:
    with open('keys.json', 'r') as f:
        keys = json.load(f)
except:
    keys = [
        input('API_KEY: '),
        input('SECRET_KEY: ')
    ]
    with open('keys.json', 'w', encoding='utf-8') as f:
        json.dump(keys, f, ensure_ascii=False, indent=4)
    print('Keys Generated')

# Set Keys
API_KEY = keys[0]
SECRET_KEY = keys[1]


