# 📁 Dosya Tarayıcı ve Kod Çıkarıcı Uygulamaları

Bu proje, SQL, C++ (.cpp) ve Header (.h) dosyalarını tarayıp içeriklerini çıkaran iki farklı uygulama içerir:

1. **📊 Dosya Tarayıcı**: Detaylı raporlama ile dosya tarama
2. **💻 Kod Çıkarıcı**: Sadece kod bloklarını düz metin olarak çıkarma

## 🎯 **Kod Çıkarıcı (Ana Uygulama)**

Sadece kod bloklarını almak ve düz metin dosyasına aktarmak için tasarlanmış basit ve etkili uygulama.

### ✨ Özellikler

- 🎯 **Sadece Kod İçeriği**: Dosya başlıkları ve metadata olmadan sadece kod
- 📁 **Çoklu Klasör Desteği**: Birden fazla klasörü aynı anda tarayabilir
- ⚙️ **Esnek Seçenekler**: Dosya adı ekleme ve ayırıcı seçenekleri
- 🛡️ **Sistem Dosyalarını Atla**: OpenSSL, Qt MOC, binary/hex dosyaları otomatik atlanır
- 📝 **Markdown Desteği**: Kodları güzel formatlanmış .md dosyasına çıkarır
- 🎨 **Syntax Highlighting**: Dosya türüne göre kod renklendirme
- 🖥️ **Modern GUI**: Kullanıcı dostu arayüz
- 📊 **İlerleme Takibi**: Gerçek zamanlı ilerleme çubuğu
- 🔄 **Threading**: Arka planda çalışır, arayüz donmaz

### 🚀 Kullanım

#### GUI Versiyonu
```bash
python3 code_extractor.py
```

#### Komut Satırı Versiyonu
```bash
python3 simple_extract.py
```

### 📋 Çıktı Formatı

#### Markdown Formatı (.md)
```markdown
# Kod Çıkarma Sonuçları

**Tarih:** 2024-01-15 14:30:25
**Toplam Dosya:** 3
**Atlanan Dosya:** 2

---

## 📄 example.cpp

**Dosya Yolu:** `/path/to/example.cpp`

```cpp
#include <iostream>
int main() {
    std::cout << "Hello World!" << std::endl;
    return 0;
}
```

---

## 📄 query.sql

**Dosya Yolu:** `/path/to/query.sql`

```sql
SELECT * FROM users WHERE active = 1;
```
```

#### Text Formatı (.txt)
```
// ===== example.cpp =====
#include <iostream>
int main() {
    std::cout << "Hello World!" << std::endl;
    return 0;
}

==================================================

// ===== query.sql =====
SELECT * FROM users WHERE active = 1;
```

## 📊 **Dosya Tarayıcı (Detaylı Versiyon)**

Detaylı raporlama ve metadata ile dosya tarama için tasarlanmış uygulama.

### ✨ Özellikler

- 📝 **Detaylı Raporlama**: Her dosya için dosya yolu, boyut ve metadata
- 🎨 **Modern Arayüz**: Emoji destekli, renkli tasarım
- ⚙️ **Dosya Türü Filtreleme**: Hangi dosya türlerinin taranacağını seçebilirsiniz
- 🗑️ **Toplu İşlemler**: Tüm klasörleri tek tıkla temizleyebilirsiniz

### 🚀 Kullanım

```bash
python3 file_scanner.py
```

### 📋 Çıktı Formatı

```
================================================================================
DOSYA TARAMA SONUÇLARI
================================================================================
Tarama Tarihi: 2024-01-15 14:30:25
Taranan Klasörler: /path/to/folder1, /path/to/folder2
Taranan Dosya Türleri: .sql, .cpp, .h
================================================================================

============================================================
DOSYA: /path/to/folder1/example.cpp
BOYUT: 1024 bytes
TÜR: .cpp
============================================================

#include <iostream>
int main() {
    std::cout << "Hello World!" << std::endl;
    return 0;
}
```

## 🛠️ Gereksinimler

- Python 3.6 veya üzeri
- tkinter (GUI için)
- Ubuntu/Debian sistemlerde: `sudo apt install python3-tk`

## 📦 Kurulum

1. Dosyaları bilgisayarınıza indirin
2. Terminal/Komut İstemcisini açın
3. Dosyaların bulunduğu klasöre gidin
4. Gerekirse tkinter'ı yükleyin:
   ```bash
   sudo apt update && sudo apt install python3-tk -y
   ```

## 🎮 Kullanım Kılavuzu

### Kod Çıkarıcı (Önerilen)

1. **Uygulamayı başlat**: `python3 code_extractor.py`
2. **Klasör ekle**: "Klasör Ekle" butonu ile taranacak klasörleri seç
3. **Dosya türlerini seç**: Checkbox'lardan istediğinizi seçin
4. **Çıktı formatını seç**:
   - 📝 **Markdown (.md)**: Güzel formatlanmış, syntax highlighting ile
   - 📄 **Text (.txt)**: Basit text formatı
5. **Seçenekleri ayarla**:
   - ✅ "Dosya adını ekle": Her dosyanın başına dosya adını ekler
   - ✅ "Dosyalar arası ayırıcı ekle": Dosyalar arasına çizgi ekler
   - ✅ "Sistem dosyalarını atla": OpenSSL, Qt MOC, binary/hex dosyalarını atlar
6. **Çıktı dosyası seç**: "Dosya Seç" butonu ile sonuç dosyasını belirle
7. **Kodları çıkar**: "Kodları Çıkar" butonu ile işlemi başlat

### Basit Test

Hızlı test için:
```bash
python3 simple_extract.py
```

Bu komut `test_files` klasöründeki dosyaları tarar ve `extracted_codes.txt` dosyasına yazar.

## 📁 Desteklenen Dosya Türleri

- **SQL Dosyaları**: `.sql`
- **C++ Kaynak Dosyaları**: `.cpp`
- **C++ Header Dosyaları**: `.h`

## 🎨 Arayüz Özellikleri

### Kod Çıkarıcı
- **Basit ve Temiz**: Sadece gerekli özellikler
- **Hızlı**: Minimum arayüz elemanı
- **Esnek**: Seçeneklerle özelleştirilebilir

### Dosya Tarayıcı
- **Modern Tasarım**: Emoji destekli, renkli arayüz
- **Kullanıcı Dostu**: Hover efektleri ve cursor değişimleri
- **Responsive**: Farklı ekran boyutlarına uyumlu

## 🔧 Güvenlik

- Dosya okuma hatalarını yakalar
- Encoding sorunlarını otomatik çözer
- Güvenli dosya yolları
- Thread-safe işlemler

## ⚡ Performans

- Çoklu thread desteği
- Bellek dostu dosya okuma
- Gerçek zamanlı ilerleme takibi
- Optimize edilmiş dosya tarama

## 🐛 Sorun Giderme

### Uygulama Açılmıyor
- Python'un yüklü olduğundan emin olun: `python3 --version`
- tkinter'ı yükleyin: `sudo apt install python3-tk`

### Dosyalar Okunamıyor
- Dosya izinlerini kontrol edin
- Dosyaların başka bir uygulama tarafından kullanılmadığından emin olun

### Çıktı Dosyası Oluşturulamıyor
- Hedef klasörün yazma izinlerini kontrol edin
- Disk alanının yeterli olduğundan emin olun

### GUI Çalışmıyor
- Basit test için: `python3 simple_extract.py`
- Komut satırı versiyonu her zaman çalışır

### Sistem Dosyaları İşleniyor
- "Sistem dosyalarını atla" seçeneğini işaretleyin
- OpenSSL, x509, ssl, crypto, Qt MOC, binary/hex dosyaları otomatik atlanır
- Sadece kendi yazdığınız kod dosyaları işlenir

## 📝 Dosya Yapısı

```
abc/
├── code_extractor.py        # Ana kod çıkarıcı (GUI)
├── simple_extract.py        # Basit kod çıkarıcı (CLI)
├── file_scanner.py          # Detaylı dosya tarayıcı (GUI)
├── file_scanner_simple.py   # Basit dosya tarayıcı (GUI)
├── README.md               # Bu dosya
├── requirements.txt        # Gereksinimler
├── extracted_codes.txt     # Test çıktısı
└── test_files/            # Test dosyaları
    ├── example.cpp
    ├── header.h
    └── database.sql
```

## 📝 Lisans

Bu uygulama açık kaynak kodludur ve özgürce kullanılabilir.

## 🤝 Katkıda Bulunma

Geliştirmeler için pull request gönderebilirsiniz.

## 📞 Destek

Herhangi bir sorun yaşarsanız:
1. README dosyasındaki sorun giderme bölümünü kontrol edin
2. Terminal çıktılarını kontrol edin
3. Basit test versiyonunu deneyin: `python3 simple_extract.py`

---

**💡 İpucu**: Kod çıkarıcı, sadece kod bloklarını almak istediğinizde idealdir. Detaylı raporlama istiyorsanız dosya tarayıcıyı kullanın.
