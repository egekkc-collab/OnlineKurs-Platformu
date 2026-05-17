# 🎓 PROKURS - EĞİTİM YÖNETİM SİSTEMİ

Profesyonel ve kullanıcı dostu bir Eğitim ve Kurs Yönetim Platformu. CustomTkinter ile geliştirilmiş, SQLite veritabanı desteğine sahip, modern, hızlı ve karanlık (dark) temalı lüks bir masaüstü arayüzü sunmaktadır.


# 📋 Özellikler

# 🔐 Güvenli Giriş ve Kimlik Doğrulama
<img width="1187" height="751" alt="image" src="https://github.com/user-attachments/assets/a577d035-1523-418f-b955-8374aee6389e" />
- ✨ **İnteraktif Tasarım** - Tıklandığında rengi değişen (Focus) giriş kutuları ve şifre gizleme (•) özelliği
- 🛡️ **Yönetici Paneli** - Sisteme yetkisiz erişimleri engelleyen, sadece adminlerin girebildiği korumalı ana ekran
- ⚠️ **Akıllı Bildirimler** - Boş alan bırakıldığında veya hatalı şifre girildiğinde anlık olarak beliren uyarı metinleri


# 📊 Dashboard ve İstatistikler
- 📈 **Sistem Özeti** - Eğitmen, öğrenci ve kurs sayılarının anlık takibi
- 💸 **Otomatik Ciro Hesabı** - Kayıtlı öğrenci sayısı ve kurs fiyatına göre anlık toplam gelir hesaplaması
- 🎯 **Dinamik Kartlar** - Yapılan tüm işlemlerin saniyeler içinde istatistik ekranına yansıması
- 📅 **Tarih Entegrasyonu** - Sistemin kullanıldığı günün anlık tarih gösterimi

<img width="1440" height="900" alt="Dashboard Goruntusu" src="https://github.com/user-attachments/assets/ornek-link-buraya-gelecek-1" />

# 📚 Kurs Yönetimi ve Kayıt İşlemleri
- ➕ **Kurs Oluşturma** - Kurs kodu, adı, eğitmeni, kontenjanı ve fiyatı ile yeni sınıf açma
- 🔍 **Canlı Arama (Live Search)** - Tuşa basıldığı anda binlerce kurs arasından anında filtreleme
- 📋 **Detaylı Görünüm** - Listedeki kursa çift tıklayarak o kursa özel öğrenci listesini inceleme
- ⚡ **Hızlı Kayıt (Entegrasyon)** - Sadece öğrenci ID ve kurs kodu girerek tek tıkla öğrenciyi kursa bağlama
- ❌ **Kurstan Çıkarma** - Detay penceresinden seçili öğrencinin kurs ilişiğini kesme

<img width="1440" height="900" alt="Kurs Yonetimi Goruntusu" src="https://github.com/user-attachments/assets/ornek-link-buraya-gelecek-2" />

# 👨‍🏫 Eğitmen ve Öğrenci Yönetimi
- ➕ **Eğitmen Ekle** - Ad, soyad ve uzmanlık alanı ile sisteme eğitmen kaydı
- 🎓 **Öğrenci Ekle** - Ad ve email ile kayıt; sistem tarafından otomatik Öğrenci ID ataması
- 🗑️ **Kalıcı Silme** - Seçili öğrenciyi veya eğitmeni sistemden tamamen kaldırma
- 🛡️ **Veri Doğrulama** - Yanlış email formatını veya isim yerine rakam girilmesini engelleyen mantıksal güvenlik kontrolleri

<img width="1440" height="900" alt="Ogrenci Yonetimi Goruntusu" src="https://github.com/user-attachments/assets/ornek-link-buraya-gelecek-3" />

# 🗄️ Sistem ve Veritabanı Araçları
- 💾 **Veritabanı Gezgini** - Arka planda çalışan ham SQLite tablolarını (egitmenler, ogrenciler, kurslar, kayitlar) doğrudan uygulama arayüzünden görüntüleyebilme
- ⚙️ **Otomatik Kurulum** - Sistem ilk açıldığında veritabanı yoksa kendi kendini inşa etme ve test verileri oluşturma



# 🎨 Tasarım Özellikleri
- 🌙 **Lüks Koyu Tema** - Göz yormayan, profesyonel CustomTkinter görünümü
- 🔵 **Mavi ve Yeşil Vurgular** - İşlem başarı durumuna göre renklenen bildirim metinleri ve butonlar
- ✨ **Animasyonlu Elementler** - Üzerine gelince (hover) belirginleşen, butonlar ve dinamik renk değiştiren giriş kutuları
- 📍 **Kayan Navigasyon** - Hangi sayfada olduğunuzu gösteren hareketli sol menü belirteci (indikatör)
- 📱 **Responsive Tablolar (Treeview)** - Ekran boyutuna göre kendini ayarlayan, kaydırma çubuğuna (Scrollbar) sahip veri tabloları



# 🖥️ Teknolojiler

| Teknoloji | Kullanım Alanı |
|-----------|----------------|
| Python 3.x | Ana programlama dili |
| CustomTkinter | Modern GUI Framework (Karanlık tema ve yuvarlak hatlı arayüz) |
| SQLite3 | Yerel, sunucusuz veritabanı yönetimi |
| Tkinter (ttk) | Veri tablolarının (Treeview) oluşturulması |
