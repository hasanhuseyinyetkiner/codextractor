#!/usr/bin/env python3
import os
import argparse
from pathlib import Path
from datetime import datetime

# Asla taranmaması gereken klasörler (Hızlı filtreleme)
IGNORE_DIRS = {
    'node_modules', '.git', '.venv', 'venv', 'env', '__pycache__',
    'dist', 'build', '.idea', '.vscode', 'coverage'
}

# Asla okunmayacak dosya uzantıları (Binary, lock dosyaları vs.)
IGNORE_EXTS = {
    '.pdf', '.exe', '.dll', '.so', '.dylib', '.png', '.jpg', '.jpeg',
    '.gif', '.zip', '.tar', '.gz', '.lock', '.pyc'
}

def is_text_file(filepath: Path) -> bool:
    """Dosyanın okunabilir bir metin dosyası olup olmadığını kontrol eder."""
    if filepath.suffix.lower() in IGNORE_EXTS:
        return False
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            f.read(1024)
        return True
    except UnicodeDecodeError:
        return False # Muhtemelen binary dosya

def generate_context(target_dir: str, output_file: str, allowed_exts: list = None):
    """Belirtilen dizindeki kodları LLM'ler için tek bir Markdown dosyasında birleştirir."""
    target_path = Path(target_dir).resolve()
    out_path = Path(output_file).resolve()

    if not target_path.is_dir():
        print(f"❌ Hata: '{target_path}' geçerli bir klasör değil.")
        return

    print(f"🔍 Taranıyor: {target_path}")
    processed_count = 0

    with open(out_path, 'w', encoding='utf-8') as out:
        # LLM için Meta Data Başlığı
        out.write(f"# Codebase Context: {target_path.name}\n")
        out.write(f"> Generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        out.write("---\n\n")

        for root, dirs, files in os.walk(target_path):
            # İstenmeyen klasörleri atla (in-place modification)
            dirs[:] = [d for d in dirs if d not in IGNORE_DIRS and not d.startswith('.')]

            for file in files:
                filepath = Path(root) / file

                # Spesifik uzantı filtresi varsa uygula
                if allowed_exts and filepath.suffix.lower() not in allowed_exts:
                    continue

                if is_text_file(filepath):
                    relative_path = filepath.relative_to(target_path)

                    # LLM'in anlaması için Markdown kod bloğu
                    ext = filepath.suffix.lstrip('.') or 'text'
                    out.write(f"## File: `{relative_path}`\n\n")
                    out.write(f"```{ext}\n")

                    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                        out.write(f.read().strip() + "\n")

                    out.write("```\n\n---\n\n")
                    processed_count += 1
                    print(f"✅ Eklendi: {relative_path}")

    print(f"\n🚀 İşlem Tamam! {processed_count} dosya birleştirildi.")
    print(f"📄 Çıktı: {out_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Projeni tek bir Markdown dosyasına çevirerek ChatGPT/Claude'a besle.")
    parser.add_argument("dir", nargs="?", default=".", help="Taranacak klasör (Varsayılan: Mevcut klasör)")
    parser.add_argument("-o", "--output", default="llm_context.md", help="Çıktı dosya adı (Varsayılan: llm_context.md)")
    parser.add_argument("-e", "--ext", nargs="+", help="Sadece bu uzantıları al (örn: -e .py .js .html)")

    args = parser.parse_args()
    generate_context(args.dir, args.output, args.ext)
