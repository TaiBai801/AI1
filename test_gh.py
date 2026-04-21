import os
import subprocess
import base64
import requests

# Get GitHub token
result = subprocess.run(
    ['gh', 'api', 'graphql', '-f', 'query={ viewer { login token } }'],
    capture_output=True, text=True
)
print(result.stdout)
print(result.stderr)