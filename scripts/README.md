# Release Scripts

This directory contains scripts to help automate the release process for FCast terminal.

## bump-version.py

A Python script to automate version bumping and release preparation.

### Usage

```bash
# Bump patch version (0.1.0 -> 0.1.1)
python scripts/bump-version.py patch

# Bump minor version (0.1.0 -> 0.2.0)
python scripts/bump-version.py minor

# Bump major version (0.1.0 -> 1.0.0)
python scripts/bump-version.py major

# Dry run - see what would happen
python scripts/bump-version.py patch --dry-run

# Bump version and push tag to remote
python scripts/bump-version.py patch --push
```

### What it does

1. Reads the current version from `senders/terminal/Cargo.toml`
2. Calculates the new version based on the bump type
3. Updates the version in `Cargo.toml`
4. Creates a git commit with the version change
5. Creates a git tag (e.g., `v0.1.1`)
6. Optionally pushes the tag to remote

### Release Workflow

1. Make sure your working directory is clean
2. Run the version bump script:
   ```bash
   python scripts/bump-version.py patch --push
   ```
3. The GitHub Actions workflow will automatically:
   - Build binaries for all platforms and architectures
   - Create a GitHub release
   - Upload all compiled binaries to the release

### Manual Release

If you prefer to create releases manually:

1. Bump the version:
   ```bash
   python scripts/bump-version.py patch
   ```
2. Push the tag:
   ```bash
   git push origin v0.1.1
   ```
3. The workflow will trigger automatically and create the release.

## Supported Platforms

The release workflow builds for:

- **Windows**: x86_64, ARM64
- **Linux**: x86_64, ARM64, ARMv7
- **macOS**: x86_64, ARM64 (Apple Silicon)

Each binary is named with its platform and architecture for easy identification.
