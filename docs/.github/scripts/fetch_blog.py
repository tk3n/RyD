import json
import os
from datetime import datetime

def create_test_json():
    data = {
        "last_updated": datetime.now().isoformat(),
        "message": "Hello, World from GitHub Actions!"
    }
    
    os.makedirs('data', exist_ok=True)
    
    with open('data/hello_world.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    create_test_json()
