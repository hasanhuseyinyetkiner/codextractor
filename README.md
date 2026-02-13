# 🚀 LLM Context Generator

[![Python CI](https://github.com/hasanhuseyinyetkiner/codextractor/actions/workflows/ci.yml/badge.svg)](https://github.com/hasanhuseyinyetkiner/codextractor/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **"Stop copying and pasting file by file."**
> A zero-dependency, high-performance CLI tool that packs your entire codebase into a single, LLM-friendly Markdown file. Optimized for ChatGPT, Claude, and Gemini.

---

## ✨ Features

- 📦 **Zero Dependencies**: Uses only Python standard libraries. Scales anywhere.
- 🔍 **Intelligent Filtering**: Automatically skips binaries, lock files, and common noise (`node_modules`, `.git`, `venv`).
- 📝 **.gitignore Support**: Respects your existing `.gitignore` patterns.
- 🎯 **Extension Filtering**: Only include what you need (e.g., just `.py` and `.js`).
- 🤖 **LLM Optimized**: Outputs structured Markdown with relative path headers and code blocks.

---

## 🚀 Quick Start

### Basic Usage
Pack the current directory into `llm_context.md`:
```bash
python3 llm_context.py
```

### Advanced Usage
Pack a specific project, filtered by extensions, with verbose logging:
```bash
python3 llm_context.py /path/to/project -o codebase.md -e .py .js -v
```

---

## 🏗️ Architecture Decisions & Trade-offs

In a world full of "bloated" tools, this project takes a different path. Here are the core engineering decisions made:

### 1. Minimalistic Design vs. External Libraries
- **Decision**: Avoided using libraries like `pathspec` for `.gitignore` parsing.
- **Trade-off**: While `pathspec` is more compliant with Git's complex globbing, it requires a `pip install`. This tool chooses **portability**. We implemented a robust `fnmatch` based approach that covers 95% of use cases while remaining a single-file, zero-dependency script.

### 2. Functional Programming vs. OOP
- **Decision**: The logic is kept in focused functions rather than complex classes.
- **Rationale**: For a script of this size, OOP often adds unnecessary boilerplate. A functional approach makes the execution flow explicit and easier for other developers (and LLMs) to audit and extend.

### 3. UTF-8 Resilience
- **Decision**: Uses `errors='ignore'` during the final read phase after a `1024-byte` text-validation check.
- **Rationale**: Real-world projects often contain accidental non-UTF-8 characters in comments or documentation. We prioritize **completeness** over crashing on encoding errors.

---

## 🛠️ Installation

Simply download `llm_context.py` and you're ready to go. No `pip install` required.

```bash
curl -O https://raw.githubusercontent.com/hasanhuseyinyetkiner/codextractor/main/llm_context.py
```

---

## ⚖️ License

Distributed under the MIT License. See `LICENSE` for more information.

---
*Developed by [Hasan Yetkiner](https://github.com/hasanhuseyinyetkiner)*
