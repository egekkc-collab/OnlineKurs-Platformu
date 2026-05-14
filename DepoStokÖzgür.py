import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime

print("Depo ve Stok Veritabanı Başlatılıyor...")

# --- 1. VERİTABANI BAĞLANTISI VE KURULUMU ---
def db_baglan():
    return sqlite3.connect("depo_stok.db")

def veritabanini_kur():
    conn = db_baglan()
    cursor = conn.cursor()
    
    # Ürünler Tablosu
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS urunler (
            id TEXT PRIMARY KEY,
            ad TEXT,
            stok INTEGER,
            fiyat REAL
        )
    ''')
    
    # Siparişler Tablosu
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS siparisler (
            siparis_id INTEGER PRIMARY KEY AUTOINCREMENT,
            urun_id TEXT,
            adet INTEGER,
            toplam_tutar REAL,
            tarih TEXT,
            FOREIGN KEY (urun_id) REFERENCES urunler (id)
        )
    ''')
    
    # Eğer veritabanı boşsa hazır verileri ekle
    cursor.execute("SELECT COUNT(*) FROM urunler")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO urunler (id, ad, stok, fiyat) VALUES ('101', 'Gaming Laptop', 15, 35000.0)")
        cursor.execute("INSERT INTO urunler (id, ad, stok, fiyat) VALUES ('102', 'Kablosuz Mouse', 50, 450.0)")
        cursor.execute("INSERT INTO urunler (id, ad, stok, fiyat) VALUES ('103', 'Mekanik Klavye', 25, 1250.0)")
        conn.commit()
        
    conn.close()

# --- 2. GUI (ARAYÜZ) SINIFI ---
class DepoStokGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Depo ve Stok Yönetim Otomasyonu (Dark Red Edition)")
        self.root.geometry("950x600")
        
        # --- RENK PALETİ ---
        self.BG_MAIN = "#121212"      # Ana arka plan (Koyu Siyah)
        self.BG_SEC = "#1e1e1e"       # İkincil arka plan
        self.FG_MAIN = "#ffffff"      # Ana yazı rengi (Beyaz)
        self.RED_ACCENT = "#d32f2f"   # Kırmızı vurgu
        self.RED_HOVER = "#ff6659"    # Açık kırmızı (Hover için)
        self.ENTRY_BG = "#2c2c2c"     # Girdi kutusu arka planı
        
        self.root.configure(bg=self.BG_MAIN)

        # Tema Ayarları
        self.stil_ayarla()

        self.arayuzu_ciz()
        self.verileri_guncelle()

    def stil_ayarla(self):
        style = ttk.Style()
        # Temayı clam olarak ayarlıyoruz ki renkler değişebilsin
        if "clam" in style.theme_names():
            style.theme_use("clam") 

        # Sekme (Notebook) Stilleri
        style.configure("TNotebook", background=self.BG_MAIN, borderwidth=0)
        style.configure("TNotebook.Tab", background=self.BG_SEC, foreground=self.FG_MAIN, 
                        padding=[15, 8], font=("Segoe UI", 10, "bold"), borderwidth=0)
        style.map("TNotebook.Tab", 
                  background=[("selected", self.RED_ACCENT)], 
                  foreground=[("selected", self.FG_MAIN)])

        # Veritabanı Tablosu (Treeview) Stilleri
        style.configure("Treeview", 
                        background=self.BG_SEC, 
                        foreground=self.FG_MAIN, 
                        fieldbackground=self.BG_SEC, 
                        rowheight=30, 
                        borderwidth=0, 
                        font=("Segoe UI", 10))
        style.map('Treeview', background=[('selected', self.RED_ACCENT)])
        
        style.configure("Treeview.Heading", 
                        background=self.RED_ACCENT, 
                        foreground=self.FG_MAIN, 
                        font=("Segoe UI", 11, "bold"),
                        borderwidth=0)
        style.map("Treeview.Heading", background=[('active', self.RED_HOVER)])

    def arayuzu_ciz(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=20, pady=20)

        # SEKMELER
        self.tab_urunler = tk.Frame(self.notebook, bg=self.BG_MAIN)
        self.notebook.add(self.tab_urunler, text=" 📦 Ürünler & Ekleme ")
        self.ciz_tab_urunler()

        self.tab_stok = tk.Frame(self.notebook, bg=self.BG_MAIN)
        self.notebook.add(self.tab_stok, text=" 🔄 Stok Güncelle ")
        self.ciz_tab_stok()

        self.tab_siparis = tk.Frame(self.notebook, bg=self.BG_MAIN)
        self.notebook.add(self.tab_siparis, text=" 🛒 Sipariş Oluştur ")
        self.ciz_tab_siparis()

        self.tab_gecmis = tk.Frame(self.notebook, bg=self.BG_MAIN)
        self.notebook.add(self.tab_gecmis, text=" 📜 Sipariş Geçmişi ")
        self.ciz_tab_gecmis()

    # --- ÖZEL BUTON VE ENTRY OLUŞTURUCULAR ---
    def ozel_buton(self, parent, text, command, bg_color=None):
        bg = bg_color if bg_color else self.RED_ACCENT
        btn = tk.Button(parent, text=text, command=command, bg=bg, fg=self.FG_MAIN, 
                        font=("Segoe UI", 11, "bold"), relief="flat", padx=10, pady=5, 
                        cursor="hand2", activebackground=self.RED_HOVER, activeforeground=self.FG_MAIN)
        return btn

    def ozel_entry(self, parent):
        return tk.Entry(parent, width=25, bg=self.ENTRY_BG, fg=self.FG_MAIN, 
                        insertbackground=self.FG_MAIN, font=("Segoe UI", 11), relief="flat")

    # --- SEKME ÇİZİMLERİ ---
    def ciz_tab_urunler(self):
        sol_frame = tk.Frame(self.tab_urunler, bg=self.BG_MAIN)
        sol_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        tk.Label(sol_frame, text="Mevcut Ürünler (Veritabanı)", bg=self.BG_MAIN, fg=self.RED_ACCENT, font=("Segoe UI", 13, "bold")).pack(anchor="w", pady=(0, 10))

        sutunlar = ("ID", "Ad", "Stok", "Fiyat")
        self.tablo_urunler = ttk.Treeview(sol_frame, columns=sutunlar, show="headings")
        self.tablo_urunler.heading("ID", text="Ürün ID")
        self.tablo_urunler.heading("Ad", text="Ürün Adı")
        self.tablo_urunler.heading("Stok", text="Stok")
        self.tablo_urunler.heading("Fiyat", text="Fiyat (TL)")
        
        self.tablo_urunler.column("ID", width=80, anchor="center")
        self.tablo_urunler.column("Ad", width=200)
        self.tablo_urunler.column("Stok", width=80, anchor="center")
        self.tablo_urunler.column("Fiyat", width=120, anchor="center")
        self.tablo_urunler.pack(fill="both", expand=True)

        # --- YENİ EKLENEN SİLME BUTONU ---
        self.ozel_buton(sol_frame, "🗑️ SEÇİLİ ÜRÜNÜ SİL", self.islem_urun_sil, bg_color="#b71c1c").pack(pady=10, anchor="e")

        sag_frame = tk.Frame(self.tab_urunler, bg=self.BG_SEC, padx=20, pady=20)
        sag_frame.pack(side="right", fill="y", padx=10, pady=10)

        tk.Label(sag_frame, text="YENİ ÜRÜN EKLE", bg=self.BG_SEC, fg=self.RED_ACCENT, font=("Segoe UI", 12, "bold")).pack(pady=(0, 15))

        tk.Label(sag_frame, text="Ürün ID:", bg=self.BG_SEC, fg=self.FG_MAIN, font=("Segoe UI", 10)).pack(anchor="w", pady=(10, 2))
        self.ent_u_id = self.ozel_entry(sag_frame)
        self.ent_u_id.pack()

        tk.Label(sag_frame, text="Ürün Adı:", bg=self.BG_SEC, fg=self.FG_MAIN, font=("Segoe UI", 10)).pack(anchor="w", pady=(10, 2))
        self.ent_u_ad = self.ozel_entry(sag_frame)
        self.ent_u_ad.pack()

        tk.Label(sag_frame, text="Başlangıç Stoğu:", bg=self.BG_SEC, fg=self.FG_MAIN, font=("Segoe UI", 10)).pack(anchor="w", pady=(10, 2))
        self.ent_u_stok = self.ozel_entry(sag_frame)
        self.ent_u_stok.pack()

        tk.Label(sag_frame, text="Birim Fiyatı (TL):", bg=self.BG_SEC, fg=self.FG_MAIN, font=("Segoe UI", 10)).pack(anchor="w", pady=(10, 2))
        self.ent_u_fiyat = self.ozel_entry(sag_frame)
        self.ent_u_fiyat.pack()

        self.ozel_buton(sag_frame, "SİSTEME EKLE", self.islem_urun_ekle).pack(pady=30, fill="x")

    def ciz_tab_stok(self):
        merkez_frame = tk.Frame(self.tab_stok, bg=self.BG_MAIN)
        merkez_frame.pack(expand=True)

        frame = tk.Frame(merkez_frame, bg=self.BG_SEC, padx=40, pady=40)
        frame.pack()
        
        tk.Label(frame, text="MANUEL STOK GİRİŞİ", bg=self.BG_SEC, fg=self.RED_ACCENT, font=("Segoe UI", 14, "bold")).grid(row=0, column=0, columnspan=3, pady=(0, 20))

        tk.Label(frame, text="Ürün Seç:", bg=self.BG_SEC, fg=self.FG_MAIN, font=("Segoe UI", 11)).grid(row=1, column=0, pady=10, sticky="w")
        self.cb_stok_urun = ttk.Combobox(frame, state="readonly", width=35, font=("Segoe UI", 11))
        self.cb_stok_urun.grid(row=1, column=1, pady=10, padx=10, columnspan=2)

        tk.Label(frame, text="Miktar:", bg=self.BG_SEC, fg=self.FG_MAIN, font=("Segoe UI", 11)).grid(row=2, column=0, pady=10, sticky="w")
        self.ent_stok_miktar = self.ozel_entry(frame)
        self.ent_stok_miktar.grid(row=2, column=1, pady=10, padx=10, sticky="w", columnspan=2)

        self.ozel_buton(frame, "▲ STOK ARTIR (+)", lambda: self.islem_stok_guncelle("+"), bg_color="#2e7d32").grid(row=3, column=1, pady=30, sticky="ew", padx=5)
        self.ozel_buton(frame, "▼ STOK AZALT (-)", lambda: self.islem_stok_guncelle("-")).grid(row=3, column=2, pady=30, sticky="ew", padx=5)

    def ciz_tab_siparis(self):
        merkez_frame = tk.Frame(self.tab_siparis, bg=self.BG_MAIN)
        merkez_frame.pack(expand=True)

        frame = tk.Frame(merkez_frame, bg=self.BG_SEC, padx=40, pady=40)
        frame.pack()
        
        tk.Label(frame, text="SİPARİŞ OLUŞTURMA", bg=self.BG_SEC, fg=self.RED_ACCENT, font=("Segoe UI", 14, "bold")).grid(row=0, column=0, columnspan=2, pady=(0, 20))

        tk.Label(frame, text="Ürün Seç:", bg=self.BG_SEC, fg=self.FG_MAIN, font=("Segoe UI", 11)).grid(row=1, column=0, pady=10, sticky="w")
        self.cb_siparis_urun = ttk.Combobox(frame, state="readonly", width=35, font=("Segoe UI", 11))
        self.cb_siparis_urun.grid(row=1, column=1, pady=10, padx=10)

        tk.Label(frame, text="Adet:", bg=self.BG_SEC, fg=self.FG_MAIN, font=("Segoe UI", 11)).grid(row=2, column=0, pady=10, sticky="w")
        self.ent_siparis_adet = self.ozel_entry(frame)
        self.ent_siparis_adet.grid(row=2, column=1, pady=10, padx=10, sticky="w")

        self.ozel_buton(frame, "SİPARİŞİ ONAYLA", self.islem_siparis_olustur).grid(row=3, column=0, columnspan=2, pady=30, sticky="ew")

    def ciz_tab_gecmis(self):
        tk.Label(self.tab_gecmis, text="Tüm Sipariş Geçmişi", bg=self.BG_MAIN, fg=self.RED_ACCENT, font=("Segoe UI", 14, "bold")).pack(pady=15)

        sutunlar = ("SiparisID", "UrunAd", "Adet", "ToplamTutar", "Tarih")
        self.tablo_gecmis = ttk.Treeview(self.tab_gecmis, columns=sutunlar, show="headings")
        
        self.tablo_gecmis.heading("SiparisID", text="Sipariş ID")
        self.tablo_gecmis.heading("UrunAd", text="Ürün Adı")
        self.tablo_gecmis.heading("Adet", text="Adet")
        self.tablo_gecmis.heading("ToplamTutar", text="Toplam Tutar (TL)")
        self.tablo_gecmis.heading("Tarih", text="Tarih & Saat")
        
        self.tablo_gecmis.column("SiparisID", anchor="center", width=80)
        self.tablo_gecmis.column("UrunAd", width=200)
        self.tablo_gecmis.column("Adet", anchor="center", width=80)
        self.tablo_gecmis.column("ToplamTutar", anchor="center", width=120)
        self.tablo_gecmis.column("Tarih", anchor="center", width=150)
        
        self.tablo_gecmis.pack(fill="both", expand=True, padx=20, pady=(0, 20))

    # --- MANTIKSAL İŞLEMLER VE VERİTABANI SORGULARI ---
    def verileri_guncelle(self):
        for item in self.tablo_urunler.get_children():
            self.tablo_urunler.delete(item)
            
        conn = db_baglan()
        cursor = conn.cursor()
        
        cursor.execute("SELECT id, ad, stok, fiyat FROM urunler")
        urunler_db = cursor.fetchall()
        
        urun_listesi_combo = []
        for u in urunler_db:
            self.tablo_urunler.insert("", "end", values=(u[0], u[1], u[2], f"{u[3]:.2f}"))
            urun_listesi_combo.append(f"{u[0]} - {u[1]} (Stok: {u[2]})")

        self.cb_stok_urun['values'] = urun_listesi_combo
        self.cb_siparis_urun['values'] = urun_listesi_combo
        self.cb_stok_urun.set('')
        self.cb_siparis_urun.set('')

        for item in self.tablo_gecmis.get_children():
            self.tablo_gecmis.delete(item)
            
        cursor.execute('''
            SELECT s.siparis_id, u.ad, s.adet, s.toplam_tutar, s.tarih 
            FROM siparisler s 
            JOIN urunler u ON s.urun_id = u.id 
            ORDER BY s.siparis_id DESC
        ''')
        siparisler_db = cursor.fetchall()
        
        for s in siparisler_db:
            self.tablo_gecmis.insert("", "end", values=(s[0], s[1], s[2], f"{s[3]:.2f}", s[4]))
            
        conn.close()

    def islem_urun_ekle(self):
        u_id = self.ent_u_id.get().strip()
        ad = self.ent_u_ad.get().strip().title()

        if not u_id.isdigit():
            messagebox.showerror("Hata", "Ürün ID sadece sayılardan oluşmalıdır (Örn: 104)!")
            return
        if int(u_id) < 100:
            messagebox.showerror("Hata", "Sistematik düzen için Ürün ID 100 veya daha büyük bir sayı olmalıdır!")
            return

        if not ad:
            messagebox.showerror("Hata", "Ürün Adı boş bırakılamaz!")
            return
        if len(ad) > 30:
            messagebox.showerror("Hata", "Ürün Adı çok uzun! En fazla 30 karakter kullanabilirsiniz.")
            return
        if not any(harf.isalpha() for harf in ad):
            messagebox.showerror("Hata", "Ürün Adı sadece sayı veya sembolden oluşamaz, en az bir harf içermelidir!")
            return

        try:
            stok = int(self.ent_u_stok.get())
            fiyat = float(self.ent_u_fiyat.get())
            
            if stok < 0 or stok > 100000:
                messagebox.showerror("Hata", "Stok miktarı 0 ile 100.000 arasında olmalıdır!")
                return
                
            if fiyat <= 0 or fiyat > 1000000:
                messagebox.showerror("Hata", "Fiyat 0'dan büyük olmalı ve 1.000.000 TL'yi geçmemelidir!")
                return

            conn = db_baglan()
            cursor = conn.cursor()
            
            cursor.execute("SELECT id FROM urunler WHERE id = ?", (u_id,))
            if cursor.fetchone():
                messagebox.showerror("Hata", "Bu ID'ye sahip bir ürün zaten mevcut!")
                conn.close()
                return

            cursor.execute("INSERT INTO urunler (id, ad, stok, fiyat) VALUES (?, ?, ?, ?)", (u_id, ad, stok, fiyat))
            conn.commit()
            conn.close()
            
            self.ent_u_id.delete(0, tk.END)
            self.ent_u_ad.delete(0, tk.END)
            self.ent_u_stok.delete(0, tk.END)
            self.ent_u_fiyat.delete(0, tk.END)
            
            self.verileri_guncelle()
            messagebox.showinfo("Başarılı", f"'{ad}' sisteme eklendi!")

        except ValueError:
            messagebox.showerror("Hata", "Lütfen stok için tam sayı, fiyat için geçerli bir sayı giriniz!")

    # --- YENİ EKLENEN SİLME FONKSİYONU ---
    def islem_urun_sil(self):
        secilen = self.tablo_urunler.selection()
        if not secilen:
            messagebox.showwarning("Uyarı", "Lütfen tablodan silmek istediğiniz ürünü seçin!")
            return

        # Seçili satırdan ürün ID ve adını alıyoruz
        item = self.tablo_urunler.item(secilen[0])
        u_id = str(item['values'][0])
        u_ad = item['values'][1]

        cevap = messagebox.askyesno("Onay", f"'{u_ad}' adlı ürünü silmek istediğinize emin misiniz?\n\n(Not: Varsa bu ürüne ait sipariş geçmişi de silinecektir.)")
        
        if cevap:
            conn = db_baglan()
            cursor = conn.cursor()
            
            # 1. Önce siparişler tablosundaki bu ürüne ait bağlantılı siparişleri siliyoruz (DB bozulmasın diye)
            cursor.execute("DELETE FROM siparisler WHERE urun_id = ?", (u_id,))
            
            # 2. Sonra ürünü siliyoruz
            cursor.execute("DELETE FROM urunler WHERE id = ?", (u_id,))
            
            conn.commit()
            conn.close()
            
            self.verileri_guncelle()
            messagebox.showinfo("Başarılı", f"'{u_ad}' başarıyla silindi!")

    def islem_stok_guncelle(self, islem_turu):
        secim = self.cb_stok_urun.get()
        if not secim:
            messagebox.showwarning("Uyarı", "Lütfen ürün seçin!")
            return

        u_id = secim.split(" - ")[0]

        try:
            miktar = int(self.ent_stok_miktar.get())
            if miktar <= 0: raise ValueError()

            conn = db_baglan()
            cursor = conn.cursor()
            cursor.execute("SELECT stok FROM urunler WHERE id = ?", (u_id,))
            mevcut_stok = cursor.fetchone()[0]

            if islem_turu == "+":
                yeni_stok = mevcut_stok + miktar
                cursor.execute("UPDATE urunler SET stok = ? WHERE id = ?", (yeni_stok, u_id))
                mesaj = f"Stok artırıldı. Yeni stok: {yeni_stok}"
                basarili = True
            else:
                if mevcut_stok >= miktar:
                    yeni_stok = mevcut_stok - miktar
                    cursor.execute("UPDATE urunler SET stok = ? WHERE id = ?", (yeni_stok, u_id))
                    mesaj = f"Stok azaltıldı. Yeni stok: {yeni_stok}"
                    basarili = True
                else:
                    mesaj = f"Hata: Yeterli stok yok! (Mevcut: {mevcut_stok})"
                    basarili = False

            if basarili:
                conn.commit()
                self.ent_stok_miktar.delete(0, tk.END)
                self.verileri_guncelle()
                messagebox.showinfo("Başarılı", mesaj)
            else:
                messagebox.showerror("Hata", mesaj)
                
            conn.close()

        except ValueError:
            messagebox.showerror("Hata", "Lütfen miktar olarak geçerli bir tam sayı giriniz!")

    def islem_siparis_olustur(self):
        secim = self.cb_siparis_urun.get()
        if not secim:
            messagebox.showwarning("Uyarı", "Lütfen ürün seçin!")
            return

        u_id = secim.split(" - ")[0]

        try:
            adet = int(self.ent_siparis_adet.get())
            if adet <= 0: raise ValueError()

            conn = db_baglan()
            cursor = conn.cursor()
            
            cursor.execute("SELECT ad, stok, fiyat FROM urunler WHERE id = ?", (u_id,))
            urun_ad, mevcut_stok, fiyat = cursor.fetchone()

            if mevcut_stok >= adet:
                yeni_stok = mevcut_stok - adet
                cursor.execute("UPDATE urunler SET stok = ? WHERE id = ?", (yeni_stok, u_id))
                
                tutar = adet * fiyat
                tarih_str = datetime.now().strftime("%Y-%m-%d %H:%M")
                
                cursor.execute("INSERT INTO siparisler (urun_id, adet, toplam_tutar, tarih) VALUES (?, ?, ?, ?)", 
                               (u_id, adet, tutar, tarih_str))
                siparis_no = cursor.lastrowid
                
                conn.commit()
                self.ent_siparis_adet.delete(0, tk.END)
                self.verileri_guncelle()
                messagebox.showinfo("Sipariş Başarılı", f"Sipariş No: {siparis_no}\nÜrün: {urun_ad}\nToplam: {tutar:.2f} TL")
            else:
                messagebox.showerror("Stok Yetersiz", f"İptal edildi! İstenen: {adet}, Mevcut Stok: {mevcut_stok}")

            conn.close()

        except ValueError:
            messagebox.showerror("Hata", "Lütfen sipariş adedine tam sayı giriniz!")

# --- 4. ÇALIŞTIRMA ---
if __name__ == "__main__":
    try:
        veritabanini_kur()
        root = tk.Tk()
        app = DepoStokGUI(root)
        print("Arayüz başarıyla başlatıldı ve silme özelliği aktif!")
        root.mainloop()
    except Exception as e:
        print(f"BİR HATA OLUŞTU: {e}")