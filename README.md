# 🎓 PROKURS - EĞİTİM YÖNETİM SİSTEMİ

Profesyonel ve kullanıcı dostu bir Eğitim ve Kurs Yönetim Platformu. CustomTkinter ile geliştirilmiş, SQLite veritabanı desteğine sahip, modern, hızlı ve karanlık (dark) temalı lüks bir masaüstü arayüzü sunmaktadır.



# 🔐 Güvenli Giriş ve Kimlik Doğrulama
<img width="1187" height="751" alt="image" src="https://github.com/user-attachments/assets/a577d035-1523-418f-b955-8374aee6389e" />

- ✨ **İnteraktif Tasarım** - Tıklandığında rengi değişen (Focus) giriş kutuları ve şifre gizleme (•) özelliği
  
- 🛡️ **Yönetici Paneli** - Sisteme yetkisiz erişimleri engelleyen, sadece adminlerin girebildiği korumalı ana ekran
  
- ⚠️ **Akıllı Bildirimler** - Boş alan bırakıldığında veya hatalı şifre girildiğinde anlık olarak beliren uyarı metinleri


# 📊 Dashboard ve İstatistikler

 <img width="1914" height="1014" alt="image" src="https://github.com/user-attachments/assets/f1495ecb-0a4f-479c-a5ec-31d86e679f5d" />

- 📈 **Sistem Özeti** - Eğitmen, öğrenci ve kurs sayılarının anlık takibi
- 💸 **Otomatik Ciro Hesabı** - Kayıtlı öğrenci sayısı ve kurs fiyatına göre anlık toplam gelir hesaplaması
- 🎯 **Dinamik Kartlar** - Yapılan tüm işlemlerin saniyeler içinde istatistik ekranına yansıması
- 📅 **Tarih Entegrasyonu** - Sistemin kullanıldığı günün anlık tarih gösterimi


# 👨‍🏫 Eğitmen Yönetimi

<img width="1904" height="999" alt="image" src="https://github.com/user-attachments/assets/bb3a1ed2-41d4-4d10-8b28-016ce1a31b58" />

-  **Hızlı Eğitmen Kaydı** - Sol taraftaki özel form arayüzü sayesinde "Ad Soyad" ve "Uzmanlık Alanı" girilerek sisteme anında yeni eğitmen ekleme
- 📋 **Dinamik Eğitmen Tablosu** - Sistemde kayıtlı olan tüm uzman kadroyu geniş, okunabilir ve modern bir liste halinde görüntüleme
- 🗑️ **Tek Tıkla Kayıt Silme** - Sağ taraftaki listeden herhangi bir eğitmeni seçip alt kısımdaki kırmızı butonla sistemden kalıcı olarak çıkarma
- 🛡️ **Akıllı Form Doğrulaması** - Form alanlarının boş bırakılmasını veya isim/uzmanlık alanına yanlışlıkla rakam girilmesini engelleyen arka plan güvenlik kontrolü
- ✨ **Görsel Geri Bildirim** - Eğitmen eklendiğinde veya silindiğinde anında beliren, başarılı/başarısız durumuna göre renk değiştiren bilgi mesajları


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
