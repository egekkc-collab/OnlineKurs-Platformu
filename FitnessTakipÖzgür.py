import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime
import random

print("FitTrack Veritabanı ve Sistem Başlatılıyor...")

# --- 1. RENK PALETİ VE STİL AYARLARI ---
BLUE_ANGELS = "#0033A0"  
SPORTY_YELLOW = "#FFD100" 
WHITE = "#FFFFFF"
TEXT_DARK = "#1A1A1A"     
BTN_GREEN = "#21D03A"     
BTN_GREEN_HOVER = "#1B9E2B"
BTN_RED = "#FF3333"       
BTN_RED_HOVER = "#CC0000"
BTN_DARK = "#0A1931"      

# --- SABİT 50 SPOR LİSTESİ ---
POPULER_50_SPOR = [
    "1. Koşu", "2. Yüzme", "3. Bisiklet", "4. Ağırlık Antrenmanı", "5. Pilates", 
    "6. Yoga", "7. Futbol", "8. Basketbol", "9. Voleybol", "10. Tenis", 
    "11. Masa Tenisi", "12. Boks", "13. Kickboks", "14. CrossFit", "15. Halter", 
    "16. Jimnastik", "17. Kürek", "18. Atletizm", "19. Güreş", "20. Judo", 
    "21. Karate", "22. Taekwondo", "23. Eskrim", "24. Okçuluk", "25. Badminton", 
    "26. Golf", "27. Hentbol", "28. Su Topu", "29. Buz Pateni", "30. Kayak", 
    "31. Snowboard", "32. Dağcılık", "33. Tırmanış", "34. Sörf", "35. Yelken", 
    "36. Binicilik", "37. Triatlon", "38. Maraton", "39. Zumba", "40. Aerobik", 
    "41. Step", "42. Dans", "43. Squash", "44. Rugby", "45. Amerikan Futbolu", 
    "46. Beyzbol", "47. Kriket", "48. İp Atlama", "49. Kalistenik", "50. MMA"
]

# --- SAMİMİ MOTİVASYON MESAJLARI ---
ZAYIF_MESAJLAR = [
    "Biraz daha kalori alarak o güzel kasları besleyebiliriz! 💪",
    "Metabolizman harika çalışıyor! Sağlıklı atıştırmalıklarla enerjini artırmaya ne dersin? 🥜",
    "Kilo almak, vermek kadar sabır ister. Antrenman ve beslenmene güven! 🥑"
]
NORMAL_MESAJLAR = [
    "Harika görünüyorsun! Formunu korumaya aynen devam! 🌟",
    "VKİ değerin tam da olması gerektiği gibi. Sadece sporun tadını çıkar! 🏃‍♂️",
    "Mükemmel denge! Disiplinin her halinden belli oluyor. 👏"
]
KILOLU_MESAJLAR = [
    "Hedeflerine ulaşmak için harika bir yoldasın, pes etmek yok! 🔥",
    "Her antrenman seni en iyi versiyonuna bir adım daha yaklaştırıyor. Devam! 🏋️‍♂️",
    "Küçük adımlar büyük değişimler getirir. Kendine inan, yapabilirsin! ✨"
]
OBEZ_MESAJLAR = [
    "Bu yola çıkma cesaretin bile en büyük başarı! Adım adım hedefe ilerliyoruz. 🧗‍♂️",
    "Sağlığın için attığın her adım çok değerli. Biz buradayız, sen sadece başla! 💙",
    "Kendini kimseyle kıyaslama, sadece dünkü senden daha iyi ol. Birlikte başaracağız! 🚀"
]

# --- 2. VERİTABANI BAĞLANTISI VE KURULUMU ---
def db_baglan():
    return sqlite3.connect("fittrack_pro.db")

def veritabanini_kur():
    conn = db_baglan()
    cursor = conn.cursor()
    
    # Sporcular tablosunu CİNSİYET sütunu ile oluştur
    cursor.execute('''CREATE TABLE IF NOT EXISTS sporcular (
            id INTEGER PRIMARY KEY AUTOINCREMENT, ad TEXT, kilo REAL, boy REAL, cinsiyet TEXT DEFAULT 'Belirtmek İstemiyorum')''')
            
    # Eski sürümden kalan veritabanı varsa "cinsiyet" sütununu hata vermeden eklemek için ufak bir yama (Migration)
    try:
        cursor.execute("ALTER TABLE sporcular ADD COLUMN cinsiyet TEXT DEFAULT 'Belirtmek İstemiyorum'")
    except sqlite3.OperationalError:
        pass # Eğer sütun zaten varsa (ikinci açılışta vs.) hata vermesini engeller ve geçer.
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS antrenmanlar (
            id INTEGER PRIMARY KEY AUTOINCREMENT, sporcu_id INTEGER, 
            tur TEXT, sure REAL, kalori REAL, tarih TEXT,
            FOREIGN KEY (sporcu_id) REFERENCES sporcular (id))''')
            
    cursor.execute("SELECT COUNT(*) FROM sporcular")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO sporcular (ad, kilo, boy, cinsiyet) VALUES ('Ahmet Yılmaz', 85.0, 1.82, 'Erkek')")
        ahmet_id = cursor.lastrowid
        bugun = datetime.now().strftime("%Y-%m-%d %H:%M")
        cursor.execute("INSERT INTO antrenmanlar (sporcu_id, tur, sure, kalori, tarih) VALUES (?, ?, ?, ?, ?)",
                       (ahmet_id, "14. CrossFit", 45, 600, bugun))
        
    conn.commit()
    conn.close()

# --- 3. OOP SINIFLARI ---
class Sporcu:
    def __init__(self, s_id, ad, kilo, boy, cinsiyet):
        self.id = s_id
        self.ad = ad
        self.kilo = kilo
        self.boy = boy
        self.cinsiyet = cinsiyet

    def vki_hesapla(self):
        return round(self.kilo / (self.boy ** 2), 2)

# --- 4. ANA GUI (ARAYÜZ) SINIFI ---
class FitTrackApp:
    def __init__(self, root):
        self.root = root
        self.root.title("FITTRACK - Fitness Takip Sistemi")
        self.root.geometry("1150x700")
        self.root.configure(bg=BLUE_ANGELS) 
        
        self.aktif_sporcu = None
        self.stilleri_ayarla()
        self.arayuzu_hazirla()
        self.combo_listesini_guncelle()

    def stilleri_ayarla(self):
        style = ttk.Style()
        style.theme_use("clam")
        
        style.configure("Treeview", background=WHITE, foreground=TEXT_DARK, 
                        rowheight=35, fieldbackground=WHITE, font=("Segoe UI", 11, "bold"), borderwidth=0)
        style.map('Treeview', background=[('selected', SPORTY_YELLOW)], foreground=[('selected', TEXT_DARK)])
        
        style.configure("Treeview.Heading", background=BTN_DARK, foreground=SPORTY_YELLOW, 
                        font=("Impact", 13), borderwidth=0, padding=5)
                        
        style.configure("TNotebook", background=BLUE_ANGELS, borderwidth=0)
        style.configure("TNotebook.Tab", font=("Impact", 12), padding=[15, 5], background=WHITE, foreground=BLUE_ANGELS)
        style.map("TNotebook.Tab", background=[("selected", SPORTY_YELLOW)], foreground=[("selected", TEXT_DARK)])

    def btn_hover(self, btn, hover_color, normal_color):
        btn.bind("<Enter>", lambda e: btn.config(bg=hover_color))
        btn.bind("<Leave>", lambda e: btn.config(bg=normal_color))

    def arayuzu_hazirla(self):
        ust_frame = tk.Frame(self.root, bg=BLUE_ANGELS, height=90)
        ust_frame.pack(fill="x", padx=20, pady=(10, 0))

        logo_frame = tk.Frame(ust_frame, bg=BLUE_ANGELS)
        logo_frame.pack(side="left", pady=10)
        tk.Label(logo_frame, text="⚡", font=("Segoe UI Emoji", 30), fg=SPORTY_YELLOW, bg=BLUE_ANGELS).pack(side="left")
        tk.Label(logo_frame, text="FIT", font=("Impact", 32), fg=WHITE, bg=BLUE_ANGELS).pack(side="left")
        tk.Label(logo_frame, text="TRACK", font=("Impact", 32), fg=SPORTY_YELLOW, bg=BLUE_ANGELS).pack(side="left")

        sag_menu = tk.Frame(ust_frame, bg=BLUE_ANGELS)
        sag_menu.pack(side="right", pady=20)
        
        btn_db = tk.Button(sag_menu, text="🗄️ SİSTEM DB", bg=BTN_DARK, fg=SPORTY_YELLOW, 
                           font=("Impact", 12), relief="flat", padx=15, pady=5,
                           cursor="hand2", command=self.veritabani_penceresi)
        btn_db.pack(side="left", padx=(0, 25))
        self.btn_hover(btn_db, WHITE, BTN_DARK)
        
        tk.Label(sag_menu, text="AKTİF SPORCU:", font=("Impact", 14), fg=WHITE, bg=BLUE_ANGELS).pack(side="left", padx=10)
        self.cb_profil = ttk.Combobox(sag_menu, state="readonly", width=20, font=("Helvetica", 12, "bold"))
        self.cb_profil.pack(side="left", padx=5)
        self.cb_profil.bind("<<ComboboxSelected>>", self.profil_degistir_event)

        btn_yeni_profil = tk.Button(sag_menu, text="+ YENİ ÜYE", bg=SPORTY_YELLOW, fg=TEXT_DARK, 
                                    font=("Impact", 12), relief="flat", padx=15, pady=5,
                                    cursor="hand2", command=self.yeni_profil_penceresi)
        btn_yeni_profil.pack(side="left", padx=15)
        self.btn_hover(btn_yeni_profil, WHITE, SPORTY_YELLOW)

        ana_govde = tk.Frame(self.root, bg=BLUE_ANGELS)
        ana_govde.pack(fill="both", expand=True, padx=20, pady=15)

        self.kart = tk.Frame(ana_govde, bg=WHITE, highlightbackground=SPORTY_YELLOW, highlightthickness=4)
        self.kart.pack(side="left", fill="y", padx=(0, 20), ipadx=10)
        
        tk.Label(self.kart, text="SPORCU KİMLİĞİ", font=("Impact", 20), fg=BLUE_ANGELS, bg=WHITE, pady=15).pack(fill="x")
        tk.Frame(self.kart, height=3, bg=SPORTY_YELLOW).pack(fill="x")

        icerik = tk.Frame(self.kart, bg=WHITE, padx=15, pady=10)
        icerik.pack(fill="both", expand=True)

        self.lbl_ad = tk.Label(icerik, text="AD SOYAD: -", font=("Impact", 18), fg=TEXT_DARK, bg=WHITE)
        self.lbl_ad.pack(anchor="w", pady=(0, 10))
        
        # --- CİNSİYET BİLGİSİ ---
        self.lbl_cinsiyet = tk.Label(icerik, text="CİNSİYET: -", font=("Helvetica", 13, "bold"), fg=TEXT_DARK, bg=WHITE)
        self.lbl_cinsiyet.pack(anchor="w", pady=2)

        self.lbl_kilo = tk.Label(icerik, text="KİLO: -", font=("Helvetica", 13, "bold"), fg=TEXT_DARK, bg=WHITE)
        self.lbl_kilo.pack(anchor="w", pady=2)
        
        self.lbl_boy = tk.Label(icerik, text="BOY: -", font=("Helvetica", 13, "bold"), fg=TEXT_DARK, bg=WHITE)
        self.lbl_boy.pack(anchor="w", pady=2)
        
        tk.Frame(icerik, height=2, bg="#EEEEEE").pack(fill="x", pady=15)
        
        tk.Label(icerik, text="VÜCUT KİTLE İNDEKSİ", font=("Impact", 14), fg="gray", bg=WHITE).pack()
        self.lbl_vki = tk.Label(icerik, text="-", font=("Impact", 45), fg=SPORTY_YELLOW, bg=WHITE)
        self.lbl_vki.pack(pady=0)
        
        self.lbl_vki_durum = tk.Label(icerik, text="DURUM: -", font=("Impact", 14), fg=TEXT_DARK, bg=WHITE)
        self.lbl_vki_durum.pack(pady=2)
        
        self.lbl_vki_mesaj = tk.Label(icerik, text="", font=("Helvetica", 10, "italic"), fg="#555555", bg=WHITE, wraplength=250, justify="center")
        self.lbl_vki_mesaj.pack(pady=(5, 5))

        btn_guncelle = tk.Button(self.kart, text="✏️ PROFİLİ GÜNCELLE", bg=SPORTY_YELLOW, fg=TEXT_DARK, 
                            font=("Impact", 12), relief="flat", pady=8,
                            cursor="hand2", command=self.profil_guncelle_penceresi)
        btn_guncelle.pack(fill="x", side="bottom")
        self.btn_hover(btn_guncelle, WHITE, SPORTY_YELLOW)

        btn_sil = tk.Button(self.kart, text="🗑️ PROFİLİ SİL", bg=BTN_RED, fg=WHITE, 
                            font=("Impact", 12), relief="flat", pady=8,
                            cursor="hand2", command=self.profili_sil)
        btn_sil.pack(fill="x", side="bottom")
        self.btn_hover(btn_sil, BTN_RED_HOVER, BTN_RED)

        sag_frame = tk.Frame(ana_govde, bg=BLUE_ANGELS)
        sag_frame.pack(side="right", fill="both", expand=True)

        form_kart = tk.Frame(sag_frame, bg=WHITE, highlightbackground=SPORTY_YELLOW, highlightthickness=4)
        form_kart.pack(fill="x", pady=(0, 15))
        
        tk.Label(form_kart, text="YENİ ANTRENMAN GİR", font=("Impact", 18), fg=BLUE_ANGELS, bg=WHITE).pack(anchor="w", padx=20, pady=(15, 5))
        
        form_icerik = tk.Frame(form_kart, bg=WHITE)
        form_icerik.pack(fill="x", padx=20, pady=(0, 15))

        tk.Label(form_icerik, text="BRANŞ:", bg=WHITE, font=("Impact", 12)).grid(row=0, column=0, padx=(0, 5))
        
        self.cb_spor = ttk.Combobox(form_icerik, values=POPULER_50_SPOR, state="readonly", width=22, font=("Helvetica", 11, "bold"))
        self.cb_spor.grid(row=0, column=1, padx=(5, 15))
        self.cb_spor.set(POPULER_50_SPOR[0])

        tk.Label(form_icerik, text="SÜRE (dk):", bg=WHITE, font=("Impact", 12)).grid(row=0, column=2, padx=(5, 5))
        self.ent_sure = tk.Entry(form_icerik, width=6, font=("Helvetica", 13, "bold"), relief="solid", bd=2, bg="#F0F0F0")
        self.ent_sure.grid(row=0, column=3, padx=5, ipady=3)

        tk.Label(form_icerik, text="KALORİ:", bg=WHITE, font=("Impact", 12)).grid(row=0, column=4, padx=(15, 5))
        self.ent_kalori = tk.Entry(form_icerik, width=6, font=("Helvetica", 13, "bold"), relief="solid", bd=2, bg="#F0F0F0")
        self.ent_kalori.grid(row=0, column=5, padx=5, ipady=3)

        btn_kaydet = tk.Button(form_icerik, text="➕ KAYDET", bg=BTN_GREEN, fg=WHITE, 
                               font=("Impact", 12), relief="flat", padx=15, pady=5,
                               cursor="hand2", command=self.antrenman_kaydet)
        btn_kaydet.grid(row=0, column=6, padx=(20, 0))
        self.btn_hover(btn_kaydet, BTN_GREEN_HOVER, BTN_GREEN)

        tablo_kart = tk.Frame(sag_frame, bg=WHITE, highlightbackground=SPORTY_YELLOW, highlightthickness=4)
        tablo_kart.pack(fill="both", expand=True)

        self.tablo = ttk.Treeview(tablo_kart, columns=("Tur", "Sure", "Kalori", "Tarih"), show="headings")
        self.tablo.heading("Tur", text="🏆 BRANŞ")
        self.tablo.heading("Sure", text="⏱️ SÜRE")
        self.tablo.heading("Kalori", text="🔥 YAKILAN KALORİ")
        self.tablo.heading("Tarih", text="📅 TARİH")
        
        self.tablo.column("Tur", width=180) 
        self.tablo.column("Sure", width=80, anchor="center")
        self.tablo.column("Kalori", width=100, anchor="center")
        self.tablo.column("Tarih", width=150, anchor="center")
        self.tablo.pack(fill="both", expand=True, padx=2, pady=2)

    def veritabani_penceresi(self):
        db_win = tk.Toplevel(self.root)
        db_win.title("Sistem Veritabanı Görüntüleyici")
        db_win.geometry("950x550")
        db_win.configure(bg=BLUE_ANGELS)
        db_win.grab_set()

        baslik = tk.Frame(db_win, bg=BTN_DARK, height=60)
        baslik.pack(fill="x")
        tk.Label(baslik, text="🗄️ SİSTEM VERİTABANI YÖNETİMİ", font=("Impact", 18), fg=SPORTY_YELLOW, bg=BTN_DARK, pady=10).pack()

        notebook = ttk.Notebook(db_win)
        notebook.pack(fill="both", expand=True, padx=15, pady=15)

        # 1. SEKME: SPORCULAR TABLOSU
        sekme1 = tk.Frame(notebook, bg=WHITE)
        notebook.add(sekme1, text="👤 Tüm Sporcular (Kullanıcılar)")

        tree_sporcular = ttk.Treeview(sekme1, columns=("ID", "Ad", "Cinsiyet", "Kilo", "Boy", "VKI"), show="headings")
        tree_sporcular.heading("ID", text="SPORCU ID")
        tree_sporcular.heading("Ad", text="AD SOYAD")
        tree_sporcular.heading("Cinsiyet", text="CİNSİYET")
        tree_sporcular.heading("Kilo", text="KİLO (kg)")
        tree_sporcular.heading("Boy", text="BOY (m)")
        tree_sporcular.heading("VKI", text="V.K.İ.")
        
        tree_sporcular.column("ID", width=80, anchor="center")
        tree_sporcular.column("Ad", width=200)
        tree_sporcular.column("Cinsiyet", width=150, anchor="center")
        tree_sporcular.column("Kilo", width=80, anchor="center")
        tree_sporcular.column("Boy", width=80, anchor="center")
        tree_sporcular.column("VKI", width=100, anchor="center")
        tree_sporcular.pack(fill="both", expand=True, padx=2, pady=2)

        # 2. SEKME: ANTRENMANLAR TABLOSU
        sekme2 = tk.Frame(notebook, bg=WHITE)
        notebook.add(sekme2, text="⚡ Tüm Antrenman Kayıtları")

        tree_antrenman = ttk.Treeview(sekme2, columns=("ID", "Ad", "Tur", "Sure", "Kalori", "Tarih"), show="headings")
        tree_antrenman.heading("ID", text="SPORCU ID")
        tree_antrenman.heading("Ad", text="SPORCU ADI")
        tree_antrenman.heading("Tur", text="BRANŞ")
        tree_antrenman.heading("Sure", text="SÜRE (dk)")
        tree_antrenman.heading("Kalori", text="KALORİ (kcal)")
        tree_antrenman.heading("Tarih", text="TARİH")
        
        tree_antrenman.column("ID", width=100, anchor="center")
        tree_antrenman.column("Ad", width=180)
        tree_antrenman.column("Tur", width=150)
        tree_antrenman.column("Sure", width=80, anchor="center")
        tree_antrenman.column("Kalori", width=100, anchor="center")
        tree_antrenman.column("Tarih", width=150, anchor="center")
        tree_antrenman.pack(fill="both", expand=True, padx=2, pady=2)

        conn = db_baglan()
        cursor = conn.cursor()

        # Sporcuları Çek
        cursor.execute("SELECT id, ad, kilo, boy, cinsiyet FROM sporcular ORDER BY id ASC")
        for row in cursor.fetchall():
            s_id, s_ad, s_kilo, s_boy, s_cins = row
            vki = round(s_kilo / (s_boy ** 2), 2)
            tree_sporcular.insert("", "end", values=(s_id, s_ad, s_cins, s_kilo, s_boy, vki))

        # Antrenmanları Çek
        sorgu = '''
            SELECT s.id, s.ad, a.tur, a.sure, a.kalori, a.tarih 
            FROM antrenmanlar a 
            JOIN sporcular s ON a.sporcu_id = s.id 
            ORDER BY a.id DESC
        '''
        cursor.execute(sorgu)
        for row in cursor.fetchall():
            tree_antrenman.insert("", "end", values=(row[0], row[1], row[2], row[3], row[4], row[5]))

        conn.close()

    def profil_guncelle_penceresi(self):
        if not self.aktif_sporcu:
            messagebox.showwarning("Hata", "Güncellenecek bir profil seçili değil!")
            return
            
        self.guncelle_win = tk.Toplevel(self.root)
        self.guncelle_win.title("Profili Güncelle")
        self.guncelle_win.geometry("350x400")
        self.guncelle_win.configure(bg=WHITE)
        self.guncelle_win.grab_set()

        baslik = tk.Frame(self.guncelle_win, bg=BTN_DARK, height=50)
        baslik.pack(fill="x")
        tk.Label(baslik, text="PROFİLİ GÜNCELLE", font=("Impact", 16), fg=SPORTY_YELLOW, bg=BTN_DARK, pady=10).pack()

        f = tk.Frame(self.guncelle_win, bg=WHITE, padx=30, pady=20)
        f.pack(fill="both", expand=True)

        tk.Label(f, text="YENİ KİLO (kg):", font=("Impact", 12), bg=WHITE).pack(anchor="w", pady=(5, 2))
        self.e_guncel_kilo = tk.Entry(f, font=("Helvetica", 12, "bold"), bg="#F0F0F0", relief="solid", bd=2)
        self.e_guncel_kilo.pack(fill="x", ipady=5, pady=(0, 10))
        self.e_guncel_kilo.insert(0, str(self.aktif_sporcu.kilo)) 

        tk.Label(f, text="YENİ BOY (m):", font=("Impact", 12), bg=WHITE).pack(anchor="w", pady=(5, 2))
        self.e_guncel_boy = tk.Entry(f, font=("Helvetica", 12, "bold"), bg="#F0F0F0", relief="solid", bd=2)
        self.e_guncel_boy.pack(fill="x", ipady=5, pady=(0, 10))
        self.e_guncel_boy.insert(0, str(self.aktif_sporcu.boy)) 
        
        # CİNSİYET GÜNCELLEME
        tk.Label(f, text="CİNSİYET:", font=("Impact", 12), bg=WHITE).pack(anchor="w", pady=(5, 2))
        self.cb_guncel_cinsiyet = ttk.Combobox(f, values=["Erkek", "Kadın", "Belirtmek İstemiyorum"], state="readonly", font=("Helvetica", 11, "bold"))
        self.cb_guncel_cinsiyet.pack(fill="x", pady=(0, 20))
        
        # Mevcut Cinsiyeti ComboBox'ta seçili hale getir
        if self.aktif_sporcu.cinsiyet in ["Erkek", "Kadın", "Belirtmek İstemiyorum"]:
            self.cb_guncel_cinsiyet.set(self.aktif_sporcu.cinsiyet)
        else:
            self.cb_guncel_cinsiyet.set("Belirtmek İstemiyorum")

        btn_kaydet = tk.Button(f, text="DEĞİŞİKLİKLERİ KAYDET", bg=SPORTY_YELLOW, fg=TEXT_DARK, 
                                      font=("Impact", 12), relief="flat", pady=8, command=self.profil_guncelle_kaydet)
        btn_kaydet.pack(fill="x")
        self.btn_hover(btn_kaydet, BTN_DARK, SPORTY_YELLOW)

    def profil_guncelle_kaydet(self):
        try:
            yeni_kilo = float(self.e_guncel_kilo.get())
            yeni_boy = float(self.e_guncel_boy.get())
            yeni_cinsiyet = self.cb_guncel_cinsiyet.get()

            if not (30 <= yeni_kilo <= 250) or not (0.5 <= yeni_boy <= 2.5): 
                raise ValueError("Mantıksız değerler")

            conn = db_baglan()
            cursor = conn.cursor()
            cursor.execute("UPDATE sporcular SET kilo = ?, boy = ?, cinsiyet = ? WHERE id = ?", (yeni_kilo, yeni_boy, yeni_cinsiyet, self.aktif_sporcu.id))
            conn.commit()
            conn.close()
            
            self.aktif_sporcu.kilo = yeni_kilo
            self.aktif_sporcu.boy = yeni_boy
            self.aktif_sporcu.cinsiyet = yeni_cinsiyet
            self.ekrani_yenile()
            self.guncelle_win.destroy()
            
            messagebox.showinfo("Başarılı", "Profil başarıyla güncellendi. Yeni hedeflere hazırız! 🚀")
        except ValueError:
            messagebox.showwarning("Hata", "Lütfen mantıklı sayılar girin! (Örn boy: 1.80)")

    def yeni_profil_penceresi(self):
        self.win = tk.Toplevel(self.root)
        self.win.title("Yeni Üye")
        self.win.geometry("350x520")
        self.win.configure(bg=WHITE)
        self.win.grab_set()

        baslik = tk.Frame(self.win, bg=BTN_DARK, height=60)
        baslik.pack(fill="x")
        tk.Label(baslik, text="YENİ ÜYE EKLE", font=("Impact", 18), fg=SPORTY_YELLOW, bg=BTN_DARK, pady=10).pack()

        f = tk.Frame(self.win, bg=WHITE, padx=30, pady=10)
        f.pack(fill="both", expand=True)

        tk.Label(f, text="AD:", font=("Impact", 12), bg=WHITE).pack(anchor="w", pady=(5, 2))
        self.e_ad = tk.Entry(f, font=("Helvetica", 12, "bold"), bg="#F0F0F0", relief="solid", bd=2)
        self.e_ad.pack(fill="x", ipady=5, pady=(0, 10))

        tk.Label(f, text="SOYAD:", font=("Impact", 12), bg=WHITE).pack(anchor="w", pady=(5, 2))
        self.e_soyad = tk.Entry(f, font=("Helvetica", 12, "bold"), bg="#F0F0F0", relief="solid", bd=2)
        self.e_soyad.pack(fill="x", ipady=5, pady=(0, 10))
        
        # --- CİNSİYET SEÇİMİ EKLENDİ ---
        tk.Label(f, text="CİNSİYET:", font=("Impact", 12), bg=WHITE).pack(anchor="w", pady=(5, 2))
        self.cb_cinsiyet = ttk.Combobox(f, values=["Erkek", "Kadın", "Belirtmek İstemiyorum"], state="readonly", font=("Helvetica", 11, "bold"))
        self.cb_cinsiyet.pack(fill="x", pady=(0, 10))
        self.cb_cinsiyet.current(2) # Varsayılan olarak Belirtmek İstemiyorum seçili gelsin

        tk.Label(f, text="KİLO (kg):", font=("Impact", 12), bg=WHITE).pack(anchor="w", pady=(5, 2))
        self.e_kilo = tk.Entry(f, font=("Helvetica", 12, "bold"), bg="#F0F0F0", relief="solid", bd=2)
        self.e_kilo.pack(fill="x", ipady=5, pady=(0, 10))

        tk.Label(f, text="BOY (Örn: 1.85):", font=("Impact", 12), bg=WHITE).pack(anchor="w", pady=(5, 2))
        self.e_boy = tk.Entry(f, font=("Helvetica", 12, "bold"), bg="#F0F0F0", relief="solid", bd=2)
        self.e_boy.pack(fill="x", ipady=5, pady=(0, 15))

        btn_profil_kaydet = tk.Button(f, text="SİSTEME KAYDET", bg=SPORTY_YELLOW, fg=TEXT_DARK, 
                                      font=("Impact", 14), relief="flat", pady=10, command=self.yeni_profil_kaydet)
        btn_profil_kaydet.pack(fill="x")
        self.btn_hover(btn_profil_kaydet, BTN_DARK, SPORTY_YELLOW)

    def yeni_profil_kaydet(self):
        ad = self.e_ad.get().strip().title()
        soyad = self.e_soyad.get().strip().title()
        cinsiyet = self.cb_cinsiyet.get()
        
        if len(ad) < 2 or len(soyad) < 2:
            messagebox.showwarning("Uyarı", "Ad ve soyad en az 2 karakter olmalıdır!")
            return
            
        if len(ad) > 20 or len(soyad) > 20:
            messagebox.showwarning("Sınır Aşıldı", "Ad veya soyad çok uzun! Maksimum 20 karakter girebilirsin. 😅")
            return

        tam_ad = f"{ad} {soyad}"
        
        try:
            kilo = float(self.e_kilo.get())
            boy = float(self.e_boy.get())

            if any(c.isdigit() for c in tam_ad): raise ValueError("İsim Hatası")
            if not (30 <= kilo <= 250) or not (0.5 <= boy <= 2.5): raise ValueError("Fizik Hatası")

            conn = db_baglan()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO sporcular (ad, kilo, boy, cinsiyet) VALUES (?, ?, ?, ?)", (tam_ad, kilo, boy, cinsiyet))
            yeni_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            self.combo_listesini_guncelle()
            self.cb_profil.set(f"{yeni_id} - {tam_ad}")
            self.aktif_sporcu = Sporcu(yeni_id, tam_ad, kilo, boy, cinsiyet)
            self.ekrani_yenile()
            self.win.destroy()
        except ValueError as e:
            hata_mesaji = str(e)
            if hata_mesaji == "İsim Hatası":
                messagebox.showwarning("Hata", "İsim veya soyisimde rakam bulunamaz!")
            else:
                messagebox.showwarning("Hata", "Lütfen tüm alanları doğru doldurun! (Boy için nokta kullanın örn: 1.85)")

    def profili_sil(self):
        if not self.aktif_sporcu: return
        cevap = messagebox.askyesno("DİKKAT!", f"{self.aktif_sporcu.ad} profilini ve tüm antrenman geçmişini silmek istediğinize emin misiniz?")
        if cevap:
            conn = db_baglan()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM antrenmanlar WHERE sporcu_id = ?", (self.aktif_sporcu.id,))
            cursor.execute("DELETE FROM sporcular WHERE id = ?", (self.aktif_sporcu.id,))
            conn.commit()
            conn.close()
            
            self.aktif_sporcu = None
            self.combo_listesini_guncelle()

    def combo_listesini_guncelle(self):
        conn = db_baglan()
        cursor = conn.cursor()
        # cinsiyet sütununu da veritabanından çekiyoruz
        cursor.execute("SELECT id, ad, kilo, boy, cinsiyet FROM sporcular")
        kayitlar = cursor.fetchall()
        conn.close()

        liste = [f"{kayit[0]} - {kayit[1]}" for kayit in kayitlar]
        self.cb_profil['values'] = liste
        
        if kayitlar:
            if not self.aktif_sporcu or not any(str(self.aktif_sporcu.id) in s for s in liste):
                self.cb_profil.current(0)
                ilk = kayitlar[0]
                self.aktif_sporcu = Sporcu(ilk[0], ilk[1], ilk[2], ilk[3], ilk[4])
        else:
            self.cb_profil.set('')
            self.aktif_sporcu = None
            
        self.ekrani_yenile()

    def profil_degistir_event(self, event):
        secim = self.cb_profil.get()
        if not secim: return
        secili_id = int(secim.split(" - ")[0])
        
        conn = db_baglan()
        cursor = conn.cursor()
        cursor.execute("SELECT id, ad, kilo, boy, cinsiyet FROM sporcular WHERE id = ?", (secili_id,))
        kayit = cursor.fetchone()
        conn.close()

        if kayit:
            self.aktif_sporcu = Sporcu(kayit[0], kayit[1], kayit[2], kayit[3], kayit[4])
            self.ekrani_yenile()

    def ekrani_yenile(self):
        for item in self.tablo.get_children(): self.tablo.delete(item)

        if not self.aktif_sporcu: 
            self.lbl_ad.config(text="AD SOYAD: -")
            self.lbl_cinsiyet.config(text="CİNSİYET: -")
            self.lbl_kilo.config(text="KİLO: -")
            self.lbl_boy.config(text="BOY: -")
            self.lbl_vki.config(text="-")
            self.lbl_vki_durum.config(text="DURUM: -", fg=TEXT_DARK)
            self.lbl_vki_mesaj.config(text="")
            return
        
        self.lbl_ad.config(text=f"{self.aktif_sporcu.ad}")
        self.lbl_cinsiyet.config(text=f"CİNSİYET: {self.aktif_sporcu.cinsiyet}")
        self.lbl_kilo.config(text=f"KİLO: {self.aktif_sporcu.kilo} kg")
        self.lbl_boy.config(text=f"BOY: {self.aktif_sporcu.boy} m")
        
        vki = self.aktif_sporcu.vki_hesapla()
        self.lbl_vki.config(text=f"{vki}")
        
        if vki < 18.5:
            durum_metni = "ZAYIF"
            renk = "#17A2B8" 
            mesaj = random.choice(ZAYIF_MESAJLAR)
        elif 18.5 <= vki < 25.0:
            durum_metni = "NORMAL"
            renk = BTN_GREEN 
            mesaj = random.choice(NORMAL_MESAJLAR)
        elif 25.0 <= vki < 30.0:
            durum_metni = "FAZLA KİLOLU"
            renk = "#FD7E14" 
            mesaj = random.choice(KILOLU_MESAJLAR)
        else:
            durum_metni = "OBEZ"
            renk = BTN_RED 
            mesaj = random.choice(OBEZ_MESAJLAR)
            
        self.lbl_vki_durum.config(text=f"DURUM: {durum_metni}", fg=renk)
        self.lbl_vki_mesaj.config(text=mesaj)

        conn = db_baglan()
        cursor = conn.cursor()
        cursor.execute("SELECT tur, sure, kalori, tarih FROM antrenmanlar WHERE sporcu_id = ? ORDER BY id DESC", (self.aktif_sporcu.id,))
        antrenman_kayitlari = cursor.fetchall()
        conn.close()

        for kayit in antrenman_kayitlari:
            self.tablo.insert("", "end", values=(kayit[0], f"{int(kayit[1])} dk", f"{int(kayit[2])} kcal", kayit[3]))

    def antrenman_kaydet(self):
        if not self.aktif_sporcu: return messagebox.showwarning("Hata", "Önce bir sporcu seç!")
        try:
            sure = float(self.ent_sure.get())
            kalori = float(self.ent_kalori.get())
            tur = self.cb_spor.get()
            
            if sure <= 0 or kalori <= 0 or not tur: 
                raise ValueError("Eksik veya negatif değer")
                
            if sure > 1440:
                messagebox.showerror("Mantık Hatası", "Bir insan aralıksız 24 saatten (1440 dk) fazla antrenman yapamaz! Sen bir Cyborg musun yoksa? 🤖")
                return

            if kalori > 10000:
                messagebox.showerror("Mantık Hatası", "Bir antrenmanda 10.000'den fazla kalori yakılması imkansızdır. Lütfen mantıklı bir değer girin!")
                return
                
            tarih_str = datetime.now().strftime("%Y-%m-%d %H:%M")
            conn = db_baglan()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO antrenmanlar (sporcu_id, tur, sure, kalori, tarih) VALUES (?, ?, ?, ?, ?)",
                           (self.aktif_sporcu.id, tur, sure, kalori, tarih_str))
            conn.commit()
            conn.close()
            
            self.ent_sure.delete(0, tk.END)
            self.ent_kalori.delete(0, tk.END)
            self.ekrani_yenile()
        except ValueError:
            messagebox.showerror("Hata", "Süre ve kalori rakam olmalı, branş boş olamaz!")

# --- ÇALIŞTIR ---
if __name__ == "__main__":
    veritabanini_kur()
    root = tk.Tk()
    app = FitTrackApp(root)
    root.mainloop()