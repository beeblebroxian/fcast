#!/usr/bin/env python3
"""
Version management script for FCast terminal releases.
This script helps automate version bumping and release preparation.
"""

import re
import sys
import subprocess
import argparse
from pathlib import Path
from typing import Tuple

def get_current_version() -> str:
    """Get current version from Cargo.toml"""
    cargo_toml = Path("senders/terminal/Cargo.toml")
    if not cargo_toml.exists():
        raise FileNotFoundError("Cargo.toml not found in senders/terminal/")
    
    content = cargo_toml.read_text()
    match = re.search(r'version\s*=\s*"([^"]+)"', content)
    if not match:
        raise ValueError("Could not find version in Cargo.toml")
    
    return match.group(1)

def parse_version(version: str) -> Tuple[int, int, int]:
    """Parse semantic version string"""
    parts = version.split('.')
    if len(parts) != 3:
        raise ValueError(f"Invalid version format: {version}")
    
    return tuple(int(part) for part in parts)

def bump_version(current: str, bump_type: str) -> str:
    """Bump version based on type"""
    major, minor, patch = parse_version(current)
    
    if bump_type == "major":
        major += 1
        minor = 0
        patch = 0
    elif bump_type == "minor":
        minor += 1
        patch = 0
    elif bump_type == "patch":
        patch += 1
    else:
        raise ValueError(f"Invalid bump type: {bump_type}")
    
    return f"{major}.{minor}.{patch}"

def update_cargo_toml(new_version: str) -> None:
    """Update version in Cargo.toml"""
    cargo_toml = Path("senders/terminal/Cargo.toml")
    content = cargo_toml.read_text()
    
    # Update version line
    content = re.sub(
        r'version\s*=\s*"[^"]+"',
        f'version = "{new_version}"',
        content
    )
    
    cargo_toml.write_text(content)
    print(f"Updated Cargo.toml to version {new_version}")

def create_git_tag(version: str) -> None:
    """Create and push git tag"""
    tag = f"v{version}"
    
    try:
        # Check if tag already exists
        result = subprocess.run(
            ["git", "tag", "-l", tag],
            capture_output=True,
            text=True
        )
        
        if tag in result.stdout.splitlines():
            print(f"Tag {tag} already exists")
            return
        
        # Create tag
        subprocess.run(["git", "add", "senders/terminal/Cargo.toml"], check=True)
        subprocess.run(["git", "commit", "-m", f"bump: version {version}"], check=True)
        subprocess.run(["git", "tag", tag], check=True)
        
        print(f"Created git tag: {tag}")
        
    except subprocess.CalledProcessError as e:
        print(f"Error creating git tag: {e}")
        sys.exit(1)

def push_tag(tag: str) -> None:
    """Push tag to remote"""
    try:
        subprocess.run(["git", "push", "origin", tag], check=True)
        print(f"Pushed tag {tag} to remote")
    except subprocess.CalledProcessError as e:
        print(f"Error pushing tag: {e}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Bump version for FCast terminal")
    parser.add_argument(
        "bump_type",
        choices=["major", "minor", "patch"],
        help="Type of version bump"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be done without making changes"
    )
    parser.add_argument(
        "--push",
        action="store_true",
        help="Push tag to remote after creating"
    )
    
    args = parser.parse_args()
    
    try:
        current_version = get_current_version()
        new_version = bump_version(current_version, args.bump_type)
        
        print(f"Current version: {current_version}")
        print(f"New version: {new_version}")
        
        if args.dry_run:
            print("Dry run - no changes made")
            return
        
        update_cargo_toml(new_version)
        create_git_tag(new_version)
        
        if args.push:
            push_tag(f"v{new_version}")
        else:
            print(f"Tag created locally. Use 'git push origin v{new_version}' to push.")
            
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
