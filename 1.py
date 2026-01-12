#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import threading
import re
from datetime import datetime
try:
    from fpdf import FPDF
except ImportError:
    FPDF = None

class CodeExtractor:
    def __init__(self):
        import random, string
        self.root = tk.Tk()
        self.root.title("Kod Çıkarıcı")
        self.root.geometry("1000x1000")
        self.root.resizable(True, True)

        # Variables
        self.folders = []
        # Desktop yolunu bul
        self.desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
        self.output_file = self.generate_new_filename()
        self.scanning = False

        self.setup_ui()

        # GUI'de output_entry'ye dosya adını yaz
        if hasattr(self, 'output_entry'):
            self.output_entry.delete(0, tk.END)
            self.output_entry.insert(0, self.output_file)
    
    def generate_new_filename(self):
        """Her çıkarma işlemi için yeni dosya adı oluştur"""
        import random, string
        now = datetime.now()
        
        # Tarih ve saat damgası
        timestamp = now.strftime("%Y%m%d_%H%M%S")
        
        # Rastgele 3 karakter ekle
        random_chars = ''.join(random.choices(string.ascii_lowercase, k=3))
        
        # Formatı al
        ext = 'txt'
        if hasattr(self, 'output_format'):
            ext = self.output_format.get()
        
        # Dosya adı formatı: kodlar_YYYYMMDD_HHMMSS_abc.ext
        filename = f"kodlar_{timestamp}_{random_chars}.{ext}"
        
        return os.path.join(self.desktop_path, filename)
        
    def setup_ui(self):
        # Main container
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Title
        title = tk.Label(main_frame, text="Kod Çıkarıcı", font=("Arial", 16, "bold"))
        title.pack(pady=(0, 20))
        
        # Folder selection
        folder_frame = tk.LabelFrame(main_frame, text="Taranacak Klasörler")
        folder_frame.pack(fill='x', pady=(0, 10))
        
        # Folder listbox
        self.folder_listbox = tk.Listbox(folder_frame, height=3)
        self.folder_listbox.pack(fill='x', padx=5, pady=5)
        
        # Folder buttons
        btn_frame = tk.Frame(folder_frame)
        btn_frame.pack(fill='x', padx=5, pady=5)
        
        tk.Button(btn_frame, text="Klasör Ekle", command=self.add_folder).pack(side='left', padx=(0, 5))
        tk.Button(btn_frame, text="Klasör Kaldır", command=self.remove_folder).pack(side='left', padx=(0, 5))
        tk.Button(btn_frame, text="Tümünü Temizle", command=self.clear_folders).pack(side='left')
        
        # Quick folder selection
        quick_frame = tk.LabelFrame(main_frame, text="Hızlı Klasör Seçimi")
        quick_frame.pack(fill='x', pady=(0, 10))
        
        tk.Button(quick_frame, text="GitHub Klasörü Ekle", command=self.add_github_folder).pack(pady=5)
        
        # Output file selection
        output_frame = tk.LabelFrame(main_frame, text="Çıktı Dosyası")
        output_frame.pack(fill='x', pady=(0, 10))
        
        output_btn_frame = tk.Frame(output_frame)
        output_btn_frame.pack(fill='x', padx=5, pady=5)
        
        self.output_entry = tk.Entry(output_btn_frame)
        self.output_entry.pack(side='left', fill='x', expand=True, padx=(0, 5))
        
        tk.Button(output_btn_frame, text="Dosya Seç", command=self.select_output).pack(side='right')
        
        # Output format selection
        format_frame = tk.Frame(output_frame)
        format_frame.pack(fill='x', padx=5, pady=5)
        
        tk.Label(format_frame, text="Çıktı Formatı:").pack(side='left')
        self.output_format = tk.StringVar(value='md')
        tk.Radiobutton(format_frame, text="Markdown (.md)", variable=self.output_format, value='md').pack(side='left', padx=(10, 5))
        tk.Radiobutton(format_frame, text="Text (.txt)", variable=self.output_format, value='txt').pack(side='left', padx=5)
        tk.Radiobutton(format_frame, text="PDF (.pdf)", variable=self.output_format, value='pdf').pack(side='left', padx=5)
        
        # File type selection
        type_frame = tk.LabelFrame(main_frame, text="Sizin Yazdığınız Kod Dosyaları (Kütüphaneler Hariç)")
        type_frame.pack(fill='x', pady=(0, 10))
        
        # Web teknolojileri - varsayılan olarak açık
        self.html_var = tk.BooleanVar(value=True)
        self.css_var = tk.BooleanVar(value=True)
        self.js_var = tk.BooleanVar(value=True)
        self.jsx_var = tk.BooleanVar(value=False)
        self.ts_var = tk.BooleanVar(value=False)
        self.tsx_var = tk.BooleanVar(value=False)
        
        # Config dosyaları
        self.json_var = tk.BooleanVar(value=True)
        self.xml_var = tk.BooleanVar(value=False)
        self.yaml_var = tk.BooleanVar(value=False)
        self.ini_var = tk.BooleanVar(value=False)
        self.toml_var = tk.BooleanVar(value=False)
        
        # Script dosyaları
        self.sh_var = tk.BooleanVar(value=True)
        self.py_var = tk.BooleanVar(value=True)
        self.bat_var = tk.BooleanVar(value=False)
        self.ps1_var = tk.BooleanVar(value=False)
        
        # Programlama dilleri
        self.cpp_var = tk.BooleanVar(value=False)
        self.h_var = tk.BooleanVar(value=False)
        self.c_var = tk.BooleanVar(value=False)
        self.java_var = tk.BooleanVar(value=False)
        self.php_var = tk.BooleanVar(value=False)
        self.rb_var = tk.BooleanVar(value=False)
        self.go_var = tk.BooleanVar(value=False)
        
        # Diğer
        self.sql_var = tk.BooleanVar(value=False)
        self.md_var = tk.BooleanVar(value=False)
        self.txt_var = tk.BooleanVar(value=False)
        self.ui_var = tk.BooleanVar(value=False)

        # Web Teknolojileri bölümü
        web_frame = tk.LabelFrame(type_frame, text="Web Teknolojileri")
        web_frame.pack(fill='x', padx=5, pady=2)
        
        web_row1 = tk.Frame(web_frame)
        web_row1.pack(fill='x', padx=5)
        tk.Checkbutton(web_row1, text="HTML (.html, .htm)", variable=self.html_var).pack(side='left')
        tk.Checkbutton(web_row1, text="CSS (.css)", variable=self.css_var).pack(side='left', padx=(20,0))
        tk.Checkbutton(web_row1, text="JavaScript (.js)", variable=self.js_var).pack(side='left', padx=(20,0))
        
        web_row2 = tk.Frame(web_frame)
        web_row2.pack(fill='x', padx=5)
        tk.Checkbutton(web_row2, text="JSX (.jsx)", variable=self.jsx_var).pack(side='left')
        tk.Checkbutton(web_row2, text="TypeScript (.ts)", variable=self.ts_var).pack(side='left', padx=(20,0))
        tk.Checkbutton(web_row2, text="TSX (.tsx)", variable=self.tsx_var).pack(side='left', padx=(20,0))
        
        # Config Dosyaları bölümü
        config_frame = tk.LabelFrame(type_frame, text="Config Dosyaları")
        config_frame.pack(fill='x', padx=5, pady=2)
        
        config_row1 = tk.Frame(config_frame)
        config_row1.pack(fill='x', padx=5)
        tk.Checkbutton(config_row1, text="JSON (.json)", variable=self.json_var).pack(side='left')
        tk.Checkbutton(config_row1, text="XML (.xml)", variable=self.xml_var).pack(side='left', padx=(20,0))
        tk.Checkbutton(config_row1, text="YAML (.yaml, .yml)", variable=self.yaml_var).pack(side='left', padx=(20,0))
        
        config_row2 = tk.Frame(config_frame)
        config_row2.pack(fill='x', padx=5)
        tk.Checkbutton(config_row2, text="INI (.ini, .cfg)", variable=self.ini_var).pack(side='left')
        tk.Checkbutton(config_row2, text="TOML (.toml)", variable=self.toml_var).pack(side='left', padx=(20,0))
        
        # Script Dosyaları bölümü
        script_frame = tk.LabelFrame(type_frame, text="Script Dosyaları")
        script_frame.pack(fill='x', padx=5, pady=2)
        
        script_row = tk.Frame(script_frame)
        script_row.pack(fill='x', padx=5)
        tk.Checkbutton(script_row, text="Shell Script (.sh, .bash)", variable=self.sh_var).pack(side='left')
        tk.Checkbutton(script_row, text="Python (.py)", variable=self.py_var).pack(side='left', padx=(20,0))
        tk.Checkbutton(script_row, text="Batch (.bat, .cmd)", variable=self.bat_var).pack(side='left', padx=(20,0))
        tk.Checkbutton(script_row, text="PowerShell (.ps1)", variable=self.ps1_var).pack(side='left', padx=(20,0))
        
        # Programlama Dilleri bölümü
        prog_frame = tk.LabelFrame(type_frame, text="Programlama Dilleri")
        prog_frame.pack(fill='x', padx=5, pady=2)
        
        prog_row1 = tk.Frame(prog_frame)
        prog_row1.pack(fill='x', padx=5)
        tk.Checkbutton(prog_row1, text="C++ (.cpp, .cxx)", variable=self.cpp_var).pack(side='left')
        tk.Checkbutton(prog_row1, text="Header (.h, .hpp)", variable=self.h_var).pack(side='left', padx=(20,0))
        tk.Checkbutton(prog_row1, text="C (.c)", variable=self.c_var).pack(side='left', padx=(20,0))
        tk.Checkbutton(prog_row1, text="Java (.java)", variable=self.java_var).pack(side='left', padx=(20,0))
        
        prog_row2 = tk.Frame(prog_frame)
        prog_row2.pack(fill='x', padx=5)
        tk.Checkbutton(prog_row2, text="PHP (.php)", variable=self.php_var).pack(side='left')
        tk.Checkbutton(prog_row2, text="Ruby (.rb)", variable=self.rb_var).pack(side='left', padx=(20,0))
        tk.Checkbutton(prog_row2, text="Go (.go)", variable=self.go_var).pack(side='left', padx=(20,0))
        
        # Diğer bölümü
        other_frame = tk.LabelFrame(type_frame, text="Diğer")
        other_frame.pack(fill='x', padx=5, pady=2)
        
        other_row = tk.Frame(other_frame)
        other_row.pack(fill='x', padx=5)
        tk.Checkbutton(other_row, text="SQL (.sql)", variable=self.sql_var).pack(side='left')
        tk.Checkbutton(other_row, text="Markdown (.md)", variable=self.md_var).pack(side='left', padx=(20,0))
        tk.Checkbutton(other_row, text="Text (.txt)", variable=self.txt_var).pack(side='left', padx=(20,0))
        tk.Checkbutton(other_row, text="Qt Designer (.ui)", variable=self.ui_var).pack(side='left', padx=(20,0))
        
        # Options
        options_frame = tk.LabelFrame(main_frame, text="Seçenekler")
        options_frame.pack(fill='x', pady=(0, 10))
        
        self.add_filename_var = tk.BooleanVar(value=True)
        self.add_separator_var = tk.BooleanVar(value=True)
        self.skip_system_files_var = tk.BooleanVar(value=True)
        self.all_files_var = tk.BooleanVar(value=False)
        
        tk.Checkbutton(options_frame, text="Dosya adını ekle", variable=self.add_filename_var).pack(anchor='w', padx=5)
        tk.Checkbutton(options_frame, text="Dosyalar arası ayırıcı ekle", variable=self.add_separator_var).pack(anchor='w', padx=5)
        tk.Checkbutton(options_frame, text="Sistem dosyalarını atla (OpenSSL, kütüphaneler)", variable=self.skip_system_files_var).pack(anchor='w', padx=5)
        tk.Checkbutton(options_frame, text="Tüm dosya türlerini tara (Uzantı bağımsız)", variable=self.all_files_var).pack(anchor='w', padx=5)

        # Custom extensions
        custom_ext_frame = tk.Frame(options_frame)
        custom_ext_frame.pack(fill='x', padx=5, pady=2)
        tk.Label(custom_ext_frame, text="Özel Uzantılar (örn: .log, .inc):").pack(side='left')
        self.custom_extensions_entry = tk.Entry(custom_ext_frame)
        self.custom_extensions_entry.pack(side='left', fill='x', expand=True, padx=5)
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(main_frame, variable=self.progress_var, maximum=100)
        self.progress_bar.pack(fill='x', pady=(0, 5))
        
        # Status label
        self.status_label = tk.Label(main_frame, text="Hazır")
        self.status_label.pack()
        
        # Scan button
        self.scan_button = tk.Button(main_frame, text="Kodları Çıkar", command=self.start_extraction, 
                                   font=("Arial", 12, "bold"), bg='#4CAF50', fg='white')
        self.scan_button.pack(pady=10)
        
        # Results area
        results_frame = tk.LabelFrame(main_frame, text="Sonuçlar")
        results_frame.pack(fill='both', expand=True, pady=(10, 0))
        
        # Results text with scrollbar
        text_frame = tk.Frame(results_frame)
        text_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        self.results_text = tk.Text(text_frame, wrap='word')
        scrollbar = tk.Scrollbar(text_frame, orient='vertical', command=self.results_text.yview)
        self.results_text.configure(yscrollcommand=scrollbar.set)
        
        self.results_text.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
    def add_folder(self):
        folder = filedialog.askdirectory(title="Klasör Seç")
        if folder and folder not in self.folders:
            self.folders.append(folder)
            self.folder_listbox.insert(tk.END, folder)
            self.status_label.config(text=f"Klasör eklendi: {os.path.basename(folder)}")
    
    def remove_folder(self):
        selection = self.folder_listbox.curselection()
        if selection:
            index = selection[0]
            folder = self.folder_listbox.get(index)
            self.folders.remove(folder)
            self.folder_listbox.delete(index)
            self.status_label.config(text=f"Klasör kaldırıldı: {os.path.basename(folder)}")
    
    def add_github_folder(self):
        github_path = '/home/hasanyetkiner/Documents/GitHub'
        if github_path not in self.folders:
            self.folders.append(github_path)
            self.folder_listbox.insert(tk.END, github_path)
            self.status_label.config(text="GitHub klasörü eklendi")
        else:
            self.status_label.config(text="GitHub klasörü zaten ekli")
    
    def clear_folders(self):
        self.folders.clear()
        self.folder_listbox.delete(0, tk.END)
        self.status_label.config(text="Tüm klasörler temizlendi")
    
    def select_output(self):
        format_type = self.output_format.get()
        if format_type == 'md':
            filetypes = [("Markdown files", "*.md"), ("All files", "*.*")]
            defaultextension = ".md"
        elif format_type == 'pdf':
            filetypes = [("PDF files", "*.pdf"), ("All files", "*.*")]
            defaultextension = ".pdf"
        else:
            filetypes = [("Text files", "*.txt"), ("All files", "*.*")]
            defaultextension = ".txt"
            
        file_path = filedialog.asksaveasfilename(
            title="Çıktı Dosyası Seç",
            defaultextension=defaultextension,
            filetypes=filetypes
        )
        if file_path:
            self.output_file = file_path
            self.output_entry.delete(0, tk.END)
            self.output_entry.insert(0, file_path)
            self.status_label.config(text=f"Çıktı dosyası seçildi: {os.path.basename(file_path)}")
    
    def get_extensions(self):
        if self.all_files_var.get():
            return ['*']
            
        extensions = []
        
        # Web teknolojileri
        if self.html_var.get():
            extensions.extend(['.html', '.htm'])
        if self.css_var.get():
            extensions.append('.css')
        if self.js_var.get():
            extensions.append('.js')
        if self.jsx_var.get():
            extensions.append('.jsx')
        if self.ts_var.get():
            extensions.append('.ts')
        if self.tsx_var.get():
            extensions.append('.tsx')
        
        # Config dosyaları
        if self.json_var.get():
            extensions.append('.json')
        if self.xml_var.get():
            extensions.append('.xml')
        if self.yaml_var.get():
            extensions.extend(['.yaml', '.yml'])
        if self.ini_var.get():
            extensions.extend(['.ini', '.cfg'])
        if self.toml_var.get():
            extensions.append('.toml')
        
        # Script dosyaları
        if self.sh_var.get():
            extensions.extend(['.sh', '.bash'])
        if self.py_var.get():
            extensions.append('.py')
        if self.bat_var.get():
            extensions.extend(['.bat', '.cmd'])
        if self.ps1_var.get():
            extensions.append('.ps1')
        
        # Programlama dilleri
        if self.cpp_var.get():
            extensions.extend(['.cpp', '.cxx'])
        if self.h_var.get():
            extensions.extend(['.h', '.hpp'])
        if self.c_var.get():
            extensions.append('.c')
        if self.java_var.get():
            extensions.append('.java')
        if self.php_var.get():
            extensions.append('.php')
        if self.rb_var.get():
            extensions.append('.rb')
        if self.go_var.get():
            extensions.append('.go')
        
        # Diğer
        if self.sql_var.get():
            extensions.append('.sql')
        if self.md_var.get():
            extensions.append('.md')
        if self.txt_var.get():
            extensions.append('.txt')
        if self.ui_var.get():
            extensions.append('.ui')
            
        # Custom extensions
        custom_exts = self.custom_extensions_entry.get().split(',')
        for ext in custom_exts:
            ext = ext.strip()
            if ext:
                if not ext.startswith('.'):
                    ext = '.' + ext
                if ext not in extensions:
                    extensions.append(ext.lower())
        
        return extensions
    
    def is_system_file(self, file_path):
        """Sistem dosyası olup olmadığını kontrol eder"""
        if not self.skip_system_files_var.get():
            return False
            
        file_name = os.path.basename(file_path).lower()
        
        # Kesinlikle atlanması gereken sistem dizinleri (Mutlak yollar)
        absolute_system_dirs = ['/usr/', '/opt/', '/lib/', '/var/', '/etc/', '/bin/', '/sbin/']
        for ad in absolute_system_dirs:
            if file_path.startswith(ad):
                return True

        # Proje içindeki ama genellikle istenmeyen dizinler
        third_party_dirs = ['node_modules', 'dist', 'build', 'vendor', 'bower_components', '.git', 
                           '.vscode', '__pycache__', '.pytest_cache', '.venv', 'env', 'venv',
                           'target', 'bin', 'obj', '.vs', '.idea', 'coverage', '.nyc_output']
        
        path_parts = file_path.lower().split(os.sep)
        if any(td in path_parts for td in third_party_dirs):
            return True
        
        # Sistem dosyaları (Sadece sistem dizinlerindeyse veya çok spesifikse)
        system_files = [
            'opensslv.h', 'opensslconf.h',
            'x509.h', 'x509v3.h', 'x509_vfy.h', 'x509_obj.h',
            'asn1.h', 'asn1t.h', 'asn1_mac.h'
        ]
        
        if file_name in system_files:
            return True
            
        # Qt MOC dosyalarını kontrol et
        if file_name.startswith('moc_') and file_name.endswith('.cpp'):
            return True
            
        # Binary/hex içerikli dosyaları kontrol et (Daha esnek)
        try:
            with open(file_path, 'rb') as f:
                chunk = f.read(1024)
                if not chunk:
                    return False
                
                # Binary karakter kontrolü (0-31 arası, \n \r \t hariç)
                binary_count = 0
                for byte in chunk:
                    if byte < 32 and byte not in [9, 10, 13]:
                        binary_count += 1
                
                # Eğer %15'ten fazlası binary ise muhtemelen binary dosyadır
                if binary_count > (len(chunk) * 0.15):
                    return True
        except:
            pass
            
        return False
    
    def get_language_extension(self, file_path):
        """Dosya uzantısına göre dil belirler"""
        ext = os.path.splitext(file_path)[1].lower()
        language_map = {
            # Web teknolojileri
            '.html': 'html',
            '.htm': 'html',
            '.css': 'css',
            '.js': 'javascript',
            '.jsx': 'jsx',
            '.ts': 'typescript',
            '.tsx': 'tsx',
            
            # Config dosyaları
            '.json': 'json',
            '.xml': 'xml',
            '.yaml': 'yaml',
            '.yml': 'yaml',
            '.ini': 'ini',
            '.cfg': 'ini',
            '.toml': 'toml',
            
            # Script dosyaları
            '.sh': 'bash',
            '.bash': 'bash',
            '.py': 'python',
            '.bat': 'batch',
            '.cmd': 'batch',
            '.ps1': 'powershell',
            
            # Programlama dilleri
            '.cpp': 'cpp',
            '.cxx': 'cpp',
            '.h': 'cpp',
            '.hpp': 'cpp',
            '.c': 'c',
            '.java': 'java',
            '.php': 'php',
            '.rb': 'ruby',
            '.go': 'go',
            
            # Diğer
            '.sql': 'sql',
            '.md': 'markdown',
            '.txt': 'text',
            '.ui': 'xml'
        }
        return language_map.get(ext, 'text')
    
    def start_extraction(self):
        if not self.folders:
            messagebox.showerror("Hata", "Lütfen en az bir klasör seçin!")
            return
        
        # Her çıkarma işlemi için yeni dosya adı oluştur
        self.output_file = self.generate_new_filename()
        
        # GUI'deki output_entry'yi güncelle
        self.output_entry.delete(0, tk.END)
        self.output_entry.insert(0, self.output_file)
        
        extensions = self.get_extensions()
        if not extensions:
            messagebox.showerror("Hata", "Lütfen en az bir dosya türü seçin!")
            return
        
        if self.scanning:
            return
        
        self.scanning = True
        self.scan_button.config(state='disabled', text="Çıkarılıyor...")
        self.results_text.delete(1.0, tk.END)
        
        thread = threading.Thread(target=self.extract_codes, args=(extensions,))
        thread.daemon = True
        thread.start()
    
    def extract_codes(self, extensions):
        try:
            self.update_status("Kod çıkarma başlatılıyor...")
            self.update_progress(0)
            
            # Collect files
            all_files = []
            skipped_files = []
            scan_all = '*' in extensions
            
            # Üçüncü taraf / build dizinleri (Dizin bazlı atlama için)
            third_party_dirs = ['node_modules', 'dist', 'build', 'vendor', 'bower_components', '.git', 
                               '.vscode', '__pycache__', '.pytest_cache', '.venv', 'env', 'venv',
                               'target', 'bin', 'obj', '.vs', '.idea', 'coverage', '.nyc_output']
            
            for folder in self.folders:
                self.log_result(f"Klasör taranıyor: {folder}")
                for root, dirs, files in os.walk(folder):
                    # Skip unwanted directories early
                    if self.skip_system_files_var.get():
                        dirs[:] = [d for d in dirs if d.lower() not in third_party_dirs]
                    
                    for file in files:
                        file_path = os.path.join(root, file)
                        
                        # Extension check
                        if not scan_all:
                            if not any(file.lower().endswith(ext) for ext in extensions):
                                continue
                        
                        if self.is_system_file(file_path):
                            skipped_files.append(file_path)
                            continue
                            
                        all_files.append(file_path)
            
            if skipped_files:
                self.log_result(f"Sistem dosyaları atlandı: {len(skipped_files)} dosya")
            
            if not all_files:
                self.log_result("Hiç dosya bulunamadı!")
                return
            
            self.log_result(f"Toplam {len(all_files)} dosya bulundu.")
            
            # Extract codes
            processed = 0
            format_type = self.output_format.get()
            
            if format_type == 'pdf':
                if FPDF is None:
                    messagebox.showerror("Hata", "fpdf2 kütüphanesi yüklü değil! Lütfen 'pip install fpdf2' komutu ile yükleyin.")
                    return
                
                pdf = FPDF()
                pdf.set_auto_page_break(auto=True, margin=15)
                pdf.add_page()
                
                pdf.set_font("Courier", size=10)
                
                # Header
                pdf.cell(200, 10, txt="KOD ÇIKARMA SONUÇLARI", ln=True, align='C')
                pdf.ln(5)
                pdf.set_font("Courier", size=8)
                pdf.cell(200, 5, txt=f"Tarih: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True)
                pdf.cell(200, 5, txt=f"Toplam Dosya: {len(all_files)}", ln=True)
                pdf.cell(200, 5, txt=f"Atlanan Dosya: {len(skipped_files)}", ln=True)
                pdf.ln(10)
                
                for i, file_path in enumerate(all_files):
                    try:
                        self.update_status(f"İşleniyor: {os.path.basename(file_path)}")
                        
                        # Add filename
                        if self.add_filename_var.get():
                            pdf.set_font("Courier", style='B', size=10)
                            pdf.cell(200, 10, txt=f"FILE: {os.path.basename(file_path)}", ln=True)
                            pdf.set_font("Courier", size=7)
                            pdf.cell(200, 5, txt=f"PATH: {file_path}", ln=True)
                            pdf.ln(2)
                        
                        # Read content
                        pdf.set_font("Courier", size=8)
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read()
                            pdf.multi_cell(0, 5, txt=content)
                        
                        pdf.ln(5)
                        if self.add_separator_var.get() and i < len(all_files) - 1:
                            pdf.line(10, pdf.get_y(), 200, pdf.get_y())
                            pdf.ln(5)
                        
                        processed += 1
                        progress = (processed / len(all_files)) * 100
                        self.update_progress(progress)
                        self.log_result(f"✓ {os.path.basename(file_path)} işlendi")
                    except Exception as e:
                        self.log_result(f"✗ Hata: {os.path.basename(file_path)} - {str(e)}")
                
                pdf.output(self.output_file)
            else:
                with open(self.output_file, 'w', encoding='utf-8') as output:
                    # Write header based on format
                    if format_type == 'md':
                        output.write("# Kod Çıkarma Sonuçları\n\n")
                        output.write(f"**Tarih:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                        output.write(f"**Toplam Dosya:** {len(all_files)}\n")
                        output.write(f"**Atlanan Dosya:** {len(skipped_files)}\n\n")
                        output.write("---\n\n")
                    else:
                        output.write("=" * 60 + "\n")
                        output.write("KOD ÇIKARMA SONUÇLARI\n")
                        output.write("=" * 60 + "\n")
                        output.write(f"Tarih: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                        output.write(f"Toplam Dosya: {len(all_files)}\n")
                        output.write(f"Atlanan Dosya: {len(skipped_files)}\n")
                        output.write("=" * 60 + "\n\n")
                    
                    for i, file_path in enumerate(all_files):
                        try:
                            self.update_status(f"İşleniyor: {os.path.basename(file_path)}")
                            
                            # Add filename if requested
                            if self.add_filename_var.get():
                                if format_type == 'md':
                                    output.write(f"\n## 📄 {os.path.basename(file_path)}\n\n")
                                    output.write(f"**Dosya Yolu:** `{file_path}`\n\n")
                                    output.write("```" + self.get_language_extension(file_path) + "\n")
                                else:
                                    output.write(f"\n// ===== {os.path.basename(file_path)} =====\n")
                            
                            # Read and write content
                            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                                content = f.read()
                                output.write(content)
                                if not content.endswith('\n'):
                                    output.write('\n')
                            
                            # Close code block if markdown
                            if format_type == 'md' and self.add_filename_var.get():
                                output.write("```\n\n")
                            
                            # Add separator if requested and not last file
                            if self.add_separator_var.get() and i < len(all_files) - 1:
                                if format_type == 'md':
                                    output.write("---\n\n")
                                else:
                                    output.write("\n" + "="*50 + "\n\n")
                            
                            processed += 1
                            progress = (processed / len(all_files)) * 100
                            self.update_progress(progress)
                            self.log_result(f"✓ {os.path.basename(file_path)} işlendi")
                            
                        except Exception as e:
                            self.log_result(f"✗ Hata: {os.path.basename(file_path)} - {str(e)}")
                            if self.add_filename_var.get():
                                if format_type == 'md':
                                    output.write(f"\n## ❌ HATA: {os.path.basename(file_path)}\n\n")
                                    output.write(f"**Hata:** {str(e)}\n\n")
                                else:
                                    output.write(f"\n// HATA: {os.path.basename(file_path)} - {str(e)}\n")
            
            self.update_status(f"Tamamlandı! {processed} dosya işlendi.")
            self.log_result(f"Kod çıkarma tamamlandı! Sonuçlar: {self.output_file}")
            
            # Dosyayı otomatik açma seçeneği
            if format_type == 'pdf':
                try:
                    if os.name == 'nt': # Windows
                        os.startfile(self.output_file)
                    elif os.name == 'posix': # Linux/Mac
                        import subprocess
                        subprocess.call(['xdg-open', self.output_file])
                except:
                    pass

            messagebox.showinfo("Başarılı", f"Kod çıkarma tamamlandı!\n{processed} dosya işlendi.\nSonuçlar: {self.output_file}")
            
        except Exception as e:
            self.log_result(f"Kritik hata: {str(e)}")
            messagebox.showerror("Hata", f"İşlem sırasında hata: {str(e)}")
        
        finally:
            self.scanning = False
            self.scan_button.config(state='normal', text="Kodları Çıkar")
            self.update_progress(0)
    
    def update_status(self, message):
        self.status_label.config(text=message)
        self.root.update()
    
    def update_progress(self, value):
        self.progress_var.set(value)
        self.root.update()
    
    def log_result(self, message):
        self.results_text.insert(tk.END, f"{message}\n")
        self.results_text.see(tk.END)
        self.root.update()
    
    def run(self):
        self.root.mainloop()

def main():
    try:
        app = CodeExtractor()
        app.run()
    except Exception as e:
        print(f"Uygulama başlatılırken hata: {e}")
        print("Komut satırı versiyonu kullanılıyor...")
        run_cli_version()

def run_cli_version():
    """Komut satırı versiyonu"""
    print("=== KOD ÇIKARICI (Komut Satırı Versiyonu) ===")
    
    # Klasör seçimi
    folders = []
    while True:
        folder = input("Taranacak klasör yolu (bitirmek için 'q'): ").strip()
        if folder.lower() == 'q':
            break
        if os.path.isdir(folder):
            folders.append(folder)
            print(f"✓ Klasör eklendi: {folder}")
        else:
            print(f"✗ Geçersiz klasör: {folder}")
    
    if not folders:
        print("Hiç klasör seçilmedi!")
        return
    
    # Çıktı dosyası
    output_file = input("Çıktı dosyası yolu (boş bırakılırsa Desktop'ta tarih damgalı dosya): ").strip()
    if not output_file:
        import random, string
        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
        
        # Tarih ve saat damgası
        now = datetime.now()
        timestamp = now.strftime("%Y%m%d_%H%M%S")
        random_chars = ''.join(random.choices(string.ascii_lowercase, k=3))
        
        # Dosya adı formatı: kodlar_YYYYMMDD_HHMMSS_abc.txt
        filename = f"kodlar_{timestamp}_{random_chars}.txt"
        output_file = os.path.join(desktop_path, filename)
        print(f"Otomatik çıktı dosyası: {output_file}")
    
    # Dosya türleri - varsayılan olarak en yaygın kod dosyaları
    extensions = ['.html', '.css', '.js', '.json', '.py', '.sh', '.md']
    print(f"Taranacak dosya türleri: {', '.join(extensions)}")
    
    # Seçenekler
    add_filename = input("Dosya adını ekle? (y/n): ").strip().lower() == 'y'
    add_separator = input("Dosyalar arası ayırıcı ekle? (y/n): ").strip().lower() == 'y'
    skip_system = input("Sistem dosyalarını atla? (y/n): ").strip().lower() == 'y'
    
    # Tarama
    print("\nKod çıkarma başlatılıyor...")
    all_files = []
    skipped_files = []
    
    def is_system_file_cli(file_path):
        """Komut satırı için sistem dosyası kontrolü"""
        if not skip_system:
            return False
            
        file_name = os.path.basename(file_path).lower()
        file_dir = os.path.dirname(file_path).lower()
        
        # Sistem dosyaları
        system_files = [
            'ssl.h', 'crypto.h', 'opensslv.h', 'opensslconf.h',
            'x509.h', 'x509v3.h', 'x509_vfy.h', 'x509_obj.h',
            'asn1.h', 'asn1t.h', 'asn1_mac.h',
            'bio.h', 'buffer.h', 'conf.h', 'err.h', 'evp.h',
            'hmac.h', 'md5.h', 'sha.h', 'rsa.h', 'dsa.h',
            'pkcs7.h', 'pkcs12.h', 'pem.h', 'rand.h',
            'bn.h', 'dh.h', 'engine.h', 'ui.h', 'txt_db.h',
            'safestack.h', 'stack.h', 'lhash.h', 'objects.h'
        ]
        
        if file_name in system_files:
            return True
            
        # Qt MOC dosyalarını kontrol et
        if file_name.startswith('moc_'):
            return True
            
        # Binary/hex içerikli dosyaları kontrol et
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read(1000)  # İlk 1000 karakteri oku
                
                # Hex değerleri kontrol et (0xb1, 0x58, 0x6c gibi)
                hex_patterns = ['0x', '0X']
                hex_count = sum(content.count(pattern) for pattern in hex_patterns)
                
                # Ardışık hex değerleri kontrol et
                hex_sequences = re.findall(r'0x[0-9a-fA-F]+,?\s*0x[0-9a-fA-F]+,?\s*0x[0-9a-fA-F]+', content)
                
                # Binary karakterler kontrol et
                binary_chars = sum(1 for c in content if ord(c) < 32 and c not in '\n\r\t')
                
                # Eğer çok fazla hex değeri veya binary karakter varsa
                if hex_count > 10 or len(hex_sequences) > 3 or binary_chars > 50:
                    return True
                    
        except:
            pass
            
        # Sistem klasörleri
        if any(keyword in file_dir for keyword in ['openssl', 'ssl', 'crypto', '/usr/', '/opt/']):
            return True
            
        return False
    
    for folder in folders:
        print(f"Klasör taranıyor: {folder}")
        for root, dirs, files in os.walk(folder):
            for file in files:
                if any(file.lower().endswith(ext) for ext in extensions):
                    file_path = os.path.join(root, file)
                    if is_system_file_cli(file_path):
                        skipped_files.append(file_path)
                        continue
                    all_files.append(file_path)
    
    if skipped_files:
        print(f"Sistem dosyaları atlandı: {len(skipped_files)} dosya")
    
    if not all_files:
        print("Hiç dosya bulunamadı!")
        return
    
    print(f"Toplam {len(all_files)} dosya bulundu.")
    
    # İşleme
    processed = 0
    with open(output_file, 'w', encoding='utf-8') as output:
        for i, file_path in enumerate(all_files):
            try:
                print(f"İşleniyor: {os.path.basename(file_path)}")
                
                # Add filename if requested
                if add_filename:
                    output.write(f"\n// ===== {os.path.basename(file_path)} =====\n")
                
                # Read and write content
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    output.write(content)
                    if not content.endswith('\n'):
                        output.write('\n')
                
                # Add separator if requested and not last file
                if add_separator and i < len(all_files) - 1:
                    output.write("\n" + "="*50 + "\n\n")
                
                processed += 1
                
            except Exception as e:
                print(f"Hata: {file_path} - {str(e)}")
                if add_filename:
                    output.write(f"\n// HATA: {os.path.basename(file_path)} - {str(e)}\n")
    
    print(f"\nKod çıkarma tamamlandı! {processed} dosya işlendi.")
    print(f"Sonuçlar: {output_file}")

if __name__ == "__main__":
    main()
