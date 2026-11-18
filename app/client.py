
import hashlib
import os
import time
import urllib.request

# Server address
SERVER_URL = os.getenv(
    "SERVER_URL",
    "http://server:8000/file"
)

# Client storage location
DATA_DIR = "/clientdata"
FILE_PATH = os.path.join(
    DATA_DIR, "received_payload.txt"
)

os.makedirs(DATA_DIR, exist_ok=True)

# Connect to server
for attempt in range(15):
    try:
        print(f"Connecting to: {SERVER_URL}")

        with urllib.request.urlopen(
            SERVER_URL, timeout=10
        ) as response:

            content = response.read()

            received_checksum = response.headers.get(
                "X-Checksum-SHA256"
            )

        break

    except Exception as error:
        print(f"Attempt {attempt + 1} failed: {error}")
        time.sleep(2)

else:
    raise RuntimeError("Could not connect to server")

# Save received file
with open(FILE_PATH, "wb") as file:
    file.write(content)

# Calculate checksum independently
calculated_checksum = hashlib.sha256(content).hexdigest()

print(f"File saved: {FILE_PATH}")
print(f"File size: {len(content)} bytes")

print(f"Server checksum: {received_checksum}")
print(f"Client checksum: {calculated_checksum}")

# Verify integrity
if (
    received_checksum == calculated_checksum
    and len(content) == 1024
):
    print("SUCCESS: File integrity verified!")
else:
    print("ERROR: File integrity verification failed!")
    raise SystemExit(1)
