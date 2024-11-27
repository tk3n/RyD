import json
import os
from datetime import datetime

def create_test_json():
    file_path = os.environ['FILE_PATH']

    data = {
        "last_updated": datetime.now().isoformat(),
        "message": "Hello, World from GitHub Actions!"
    }
    
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    create_test_json()
