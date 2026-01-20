"""
project_overview.py
utility -> universal structure overview script
"""
import os
from collections import defaultdict
from pathlib import Path
import subprocess

# -----------------------------
# CONFIG
# -----------------------------
INCLUDE_EXCLUDED = False  # toggle for including ignored files (False = only tracked by Git)

# -----------------------------
# GET PROJECT FILES FROM GIT
# -----------------------------
def get_git_files():
    cmd = ["git", "ls-files"]
    result = subprocess.run(cmd, stdout=subprocess.PIPE, text=True)
    files = result.stdout.splitlines()
    return files

all_files = get_git_files()

# -----------------------------
# BUILD TREE STRUCTURE
# -----------------------------
tree = {}
file_types = defaultdict(int)
file_lines = defaultdict(int)

for file_path in all_files:
    parts = Path(file_path).parts
    current = tree
    for part in parts[:-1]:  # folders
        if part not in current:
            current[part] = {}
        current = current[part]
    # file
    current[parts[-1]] = None

    # file type + lines
    ext = Path(file_path).suffix or "no_ext"
    file_types[ext] += 1
    try:
        with open(file_path, encoding="utf-8") as f:
            file_lines[ext] += sum(1 for _ in f)
    except Exception:
        pass  # ignore unreadable files

# -----------------------------
# PRINT TREE FUNCTION
# -----------------------------
def print_tree(d, prefix=""):
    for key, value in sorted(d.items()):
        if isinstance(value, dict):
            # folder
            subfolders = sum(1 for v in value.values() if isinstance(v, dict))
            files = sum(1 for v in value.values() if v is None)
            total_files = sum_files(value)
            print(f"{prefix}{key}/ [subfolders: {subfolders}, files: {files}, total files: {total_files}]")
            print_tree(value, prefix + "    ")
        else:
            print(f"{prefix}{key}")

def sum_files(d):
    count = 0
    for v in d.values():
        if isinstance(v, dict):
            count += sum_files(v)
        else:
            count += 1
    return count

# -----------------------------
# CALCULATE STATS
# -----------------------------
total_files = len(all_files)
total_folders = sum(1 for f in tree if isinstance(tree[f], dict))

# -----------------------------
# PRINT RESULTS
# -----------------------------
print("\n================= PROJECT TREE =================\n")
print_tree(tree)

print("\n================= PROJECT STATS =================\n")
print(f"Total folders: {total_folders}")
print(f"Total files  : {total_files}\n")

print("File types:")
for ext, count in sorted(file_types.items()):
    lines = file_lines[ext]
    print(f"  {ext:6} -> {count:4} files, {lines:6} lines")
