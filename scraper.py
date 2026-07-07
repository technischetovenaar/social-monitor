from datetime import datetime
import json
from pathlib import Path

output = {
    "status": "running",
    "updated": datetime.utcnow().isoformat() + "Z"
}

Path("data").mkdir(exist_ok=True)

with open("data/output.json", "w") as f:
    json.dump(output, f, indent=4)

print("Output generated.")