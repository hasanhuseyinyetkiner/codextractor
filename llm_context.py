#!/usr/bin/env python3
import os
import argparse
import fnmatch
from pathlib import Path
from datetime import datetime

# Default ignored directories
DEFAULT_IGNORE_DIRS = {
    'node_modules', '.git', '.venv', 'venv', 'env', '__pycache__',
    'dist', 'build', '.idea', '.vscode', 'coverage', '.claude', '.serena'
}

# Default ignored extensions
DEFAULT_IGNORE_EXTS = {
    '.pdf', '.exe', '.dll', '.so', '.dylib', '.png', '.jpg', '.jpeg',
    '.gif', '.zip', '.tar', '.gz', '.lock', '.pyc', '.ico', '.svg'
}

def load_gitignore_patterns(target_dir: Path):
    """Loads patterns from .gitignore if it exists."""
    patterns = []
    gitignore_path = target_dir / '.gitignore'
    if gitignore_path.exists():
        with open(gitignore_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    patterns.append(line)
    return patterns

def should_ignore(path: Path, target_path: Path, gitignore_patterns: list, verbose: bool) -> bool:
    """Checks if a path should be ignored based on defaults and .gitignore."""
    rel_path = path.relative_to(target_path)

    # Check default ignored dirs
    if any(part in DEFAULT_IGNORE_DIRS for part in rel_path.parts):
        return True

    # Check extension
    if path.suffix.lower() in DEFAULT_IGNORE_EXTS:
        return True

    # Check .gitignore patterns
    for pattern in gitignore_patterns:
        # Simple glob matching
        if fnmatch.fnmatch(str(rel_path), pattern) or fnmatch.fnmatch(path.name, pattern):
            if verbose:
                print(f"  [Ignored by .gitignore]: {rel_path}")
            return True

    return False

def is_text_file(filepath: Path) -> bool:
    """Checks if a file is readable as UTF-8 text."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            f.read(1024)
        return True
    except (UnicodeDecodeError, PermissionError):
        return False

def generate_context(target_dir: str, output_file: str, allowed_exts: list = None, verbose: bool = False):
    """Aggregates codebase into a single Markdown file for LLM context."""
    target_path = Path(target_dir).resolve()
    out_path = Path(output_file).resolve()

    if not target_path.is_dir():
        print(f"❌ Error: '{target_path}' is not a valid directory.")
        return

    print(f"🔍 Scanning: {target_path}")
    gitignore_patterns = load_gitignore_patterns(target_path)
    if gitignore_patterns:
        print(f"📝 Loaded {len(gitignore_patterns)} patterns from .gitignore")

    processed_count = 0

    with open(out_path, 'w', encoding='utf-8') as out:
        out.write(f"# Codebase Context: {target_path.name}\n")
        out.write(f"> Generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        out.write("---\n\n")

        for root, dirs, files in os.walk(target_path):
            # In-place modification of dirs to skip ignored ones
            dirs[:] = [d for d in dirs if d not in DEFAULT_IGNORE_DIRS and not d.startswith('.')]

            for file in files:
                filepath = Path(root) / file

                if should_ignore(filepath, target_path, gitignore_patterns, verbose):
                    continue

                if allowed_exts and filepath.suffix.lower() not in allowed_exts:
                    continue

                if is_text_file(filepath):
                    relative_path = filepath.relative_to(target_path)

                    if str(relative_path) == str(out_path.relative_to(target_path)):
                        continue # Don't include the output file itself

                    ext = filepath.suffix.lstrip('.') or 'text'
                    out.write(f"## File: `{relative_path}`\n\n")
                    out.write(f"```{ext}\n")

                    try:
                        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                            out.write(f.read().strip() + "\n")
                        out.write("```\n\n---\n\n")
                        processed_count += 1
                        if verbose:
                            print(f"✅ Processed: {relative_path}")
                    except Exception as e:
                        print(f"⚠️  Error reading {relative_path}: {e}")

    print(f"\n🚀 Success! {processed_count} files aggregated.")
    print(f"📄 Saved to: {out_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Pack your project into a single Markdown for ChatGPT/Claude.")
    parser.add_argument("dir", nargs="?", default=".", help="Target directory (default: current)")
    parser.add_argument("-o", "--output", default="llm_context.md", help="Output filename (default: llm_context.md)")
    parser.add_argument("-e", "--ext", nargs="+", help="Filter by extensions (e.g. -e .py .js)")
    parser.add_argument("-v", "--verbose", action="store_true", help="Show detailed processing logs")

    args = parser.parse_args()
    generate_context(args.dir, args.output, args.ext, args.verbose)
