#!/usr/bin/env python3
"""
Push code to GitHub using GitHub CLI with full path
"""
import os
import subprocess
import base64

REPO_OWNER = "TaiBai801"
REPO_NAME = "AI1"
PROJECT_DIR = r"C:\Users\ASUS1\.qclaw\workspace\match-making-app"
GH_PATH = r"C:\Users\ASUS1\AppData\Local\GitHubCLI\Program Files\GitHub CLI\gh.exe"

def run_cmd(args):
    """Run command and return output"""
    result = subprocess.run([GH_PATH] + args, capture_output=True, text=True, shell=False)
    return result.stdout.strip(), result.stderr.strip(), result.returncode

def get_files(directory):
    """Get all files in directory recursively"""
    files = []
    for root, dirs, filenames in os.walk(directory):
        # Skip .git and node_modules
        dirs[:] = [d for d in dirs if d not in ['.git', 'node_modules', '__pycache__']]
        for filename in filenames:
            filepath = os.path.join(root, filename)
            rel_path = os.path.relpath(filepath, directory)
            # Convert Windows path to Unix path
            rel_path = rel_path.replace('\\', '/')
            files.append((rel_path, filepath))
    return files

def push_to_github():
    print("=== GitHub Code Push ===\n")
    
    # Get token
    stdout, stderr, code = run_cmd(['auth', 'token'])
    token = stdout.strip()
    if not token:
        print("Error: Cannot get GitHub token")
        return
    print(f"Logged in: {REPO_OWNER}\n")
    
    # Get all files
    print(f"=== Scanning project files ===")
    files = get_files(PROJECT_DIR)
    print(f"Found {len(files)} files\n")
    
    # Upload files
    print(f"=== Uploading to GitHub ===")
    success = 0
    failed = 0
    
    for rel_path, full_path in files:
        try:
            # Read file content
            with open(full_path, 'rb') as f:
                content = f.read()
            
            encoded = base64.b64encode(content).decode()
            
            # Create or update file using gh api
            args = [
                'api', '--method', 'PUT',
                f'repos/{REPO_OWNER}/{REPO_NAME}/contents/{rel_path}',
                '-f', f'message=Add {rel_path}',
                '-f', f'content={encoded}'
            ]
            
            stdout, stderr, code = run_cmd(args)
            
            if code == 0:
                success += 1
                print(f"[OK] {rel_path}")
            else:
                failed += 1
                print(f"[FAIL] {rel_path}: {stderr[:80]}")
                
        except Exception as e:
            failed += 1
            print(f"[FAIL] {rel_path}: {str(e)[:80]}")
    
    print(f"\n=== Done ===")
    print(f"Success: {success}")
    print(f"Failed: {failed}")
    print(f"\nRepo: https://github.com/{REPO_OWNER}/{REPO_NAME}")

if __name__ == "__main__":
    push_to_github()