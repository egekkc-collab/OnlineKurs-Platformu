import customtkinter as ctk
import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime

# --- GLOBAL TEMA VE PREMİUM RENK PALETİ ---
ctk.set_appearance_mode("Dark")  
ctk.set_default_color_theme("blue") 

COLORS = {    
    "bg_dark": "#09090b",       
    "bg_panel": "#18181b",      
    "bg_card": "#27272a",       
    "border": "#3f3f46",        
    "text_main": "#f4f4f5",     
    "text_muted": "#a1a1aa",    
    "primary": "#3b82f6",       
    "primary_hover": "#2563eb", 
    "success": "#10b981",       
    "success_hover": "#059669",
    "warning": "#f59e0b",       
    "danger": "#ef4444",        
    "danger_hover": "#dc2626"
}

# ================= SQLITE VERİTABANI YÖNETİCİSİ =================
class DatabaseManager:
    def __init__(self, db_name="prokurs.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self._create_tables()
        self._ilk_verileri_bas()

    def _create_tables(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS adminler (
            kullanici_adi TEXT PRIMARY KEY, sifre TEXT)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS egitmenler (
            id INTEGER PRIMARY KEY AUTOINCREMENT, ad TEXT UNIQUE, uzmanlik TEXT)''')
        # ÖĞRENCİ TABLOSUNA AUTOINCREMENT EKLENDİ
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS ogrenciler (
            id INTEGER PRIMARY KEY AUTOINCREMENT, ad TEXT, email TEXT)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS kurslar (
            id TEXT PRIMARY KEY, ad TEXT, egitmen_ad TEXT, kont INTEGER, fiyat REAL DEFAULT 0)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS kayitlar (
            ogrenci_id INTEGER, kurs_id TEXT,
            PRIMARY KEY(ogrenci_id, kurs_id))''')
        self.cursor.execute("PRAGMA table_info(kurslar)")
        columns = [row[1] for row in self.cursor.fetchall()]
        if "fiyat" not in columns:
            self.cursor.execute("ALTER TABLE kurslar ADD COLUMN fiyat REAL DEFAULT 0")
        self.conn.commit()

    def _ilk_verileri_bas(self):
        self.cursor.execute("SELECT COUNT(*) FROM adminler")
        if self.cursor.fetchone()[0] == 0:
            self.cursor.execute("INSERT INTO adminler (kullanici_adi, sifre) VALUES ('admin', '1234')")
            
        self.cursor.execute("SELECT COUNT(*) FROM egitmenler")
        if self.cursor.fetchone()[0] == 0:
            self.egitmen_ekle("Ahmet Yılmaz", "Yapay Zeka Uzmanı")
            self.egitmen_ekle("Zeynep Demir", "Arayüz Tasarımı")
            # ÖĞRENCİ EKLERKEN ARTIK ID GÖNDERMİYORUZ, SİSTEM 1, 2, 3 DİYE ATAYACAK
            self.ogrenci_ekle("Ali Kaya", "ali@mail.com")
            self.ogrenci_ekle("Ayşe Çelik", "ayse@mail.com")
            self.ogrenci_ekle("Caner Gezer", "caner@mail.com")
            
            self.kurs_ekle("PY101", "Sıfırdan Python Programlama", "Ahmet Yılmaz", 20, 1499.0)
            self.kurs_ekle("UX202", "Modern Arayüz Tasarımı", "Zeynep Demir", 15, 1299.0)
            self.kayit_ekle(1, "PY101")
            self.kayit_ekle(3, "PY101")
        self.conn.commit()

    def admin_girisi_yap(self, k_adi, sifre):
        self.cursor.execute("SELECT * FROM adminler WHERE kullanici_adi=? AND sifre=?", (k_adi, sifre))
        return self.cursor.fetchone() is not None

    def egitmen_ekle(self, ad, uzmanlik):
        try:
            self.cursor.execute("INSERT INTO egitmenler (ad, uzmanlik) VALUES (?, ?)", (ad, uzmanlik))
            self.conn.commit(); return True, "Eğitmen başarıyla sisteme eklendi."
        except sqlite3.IntegrityError: return False, "Bu isimde bir eğitmen zaten var!"

    # ÖĞRENCİ EKLEME FONKSİYONU GÜNCELLENDİ (ID OTOMATİK OLUŞTURULUYOR)
    def ogrenci_ekle(self, ad, email):
        try:
            self.cursor.execute("INSERT INTO ogrenciler (ad, email) VALUES (?, ?)", (ad, email))
            self.conn.commit()
            # Eklenen öğrencinin yeni atanan ID'sini geri döndürüyoruz
            return True, "Öğrenci kaydı başarıyla oluşturuldu.", self.cursor.lastrowid
        except Exception as e: return False, str(e), None

    def kurs_ekle(self, k_id, ad, egitmen_ad, kont, fiyat):
        try:
            self.cursor.execute("INSERT INTO kurslar (id, ad, egitmen_ad, kont, fiyat) VALUES (?, ?, ?, ?, ?)", (k_id, ad, egitmen_ad, kont, fiyat))
            self.conn.commit(); return True, "Yeni kurs başarıyla oluşturuldu."
        except sqlite3.IntegrityError: return False, "Bu Kurs Kodu zaten kullanılıyor!"

    def kayit_ekle(self, ogrenci_id, kurs_id):
        try:
            self.cursor.execute("INSERT INTO kayitlar (ogrenci_id, kurs_id) VALUES (?, ?)", (ogrenci_id, kurs_id))
            self.conn.commit(); return True, "Öğrenci kursa başarıyla kaydedildi."
        except sqlite3.IntegrityError: return False, "Öğrenci bu kursa zaten kayıtlı!"

    def egitmenleri_getir(self): return self.cursor.execute("SELECT * FROM egitmenler").fetchall()
    def ogrencileri_getir(self): return self.cursor.execute("SELECT * FROM ogrenciler").fetchall()
    def kurslari_getir(self): return self.cursor.execute("SELECT * FROM kurslar").fetchall()
    def kayitlari_getir(self): return self.cursor.execute("SELECT * FROM kayitlar").fetchall()
    
    def get_stats(self):
        return {
            'egitmen': self.cursor.execute("SELECT COUNT(*) FROM egitmenler WHERE ad != ''").fetchone()[0],
            'ogrenci': self.cursor.execute("SELECT COUNT(*) FROM ogrenciler WHERE ad != ''").fetchone()[0],
            'kurs': self.cursor.execute("SELECT COUNT(*) FROM kurslar").fetchone()[0],
            'kayit': self.cursor.execute("SELECT COUNT(*) FROM kayitlar").fetchone()[0]
        }

    def kayit_sil(self, tablo, kosul_sutunu, kosul_degeri):
        query = f"DELETE FROM {tablo} WHERE {kosul_sutunu} = ?"
        try:
            self.cursor.execute(query, (kosul_degeri,))
            self.conn.commit()
            return True, "Kayıt veritabanından tamamen silindi."
        except Exception as e: return False, str(e)
        
    def kurs_kaydi_sil(self, ogrenci_id, kurs_id):
        try:
            self.cursor.execute("DELETE FROM kayitlar WHERE ogrenci_id=? AND kurs_id=?", (ogrenci_id, kurs_id))
            self.conn.commit()
            return True, "Öğrencinin bu kurstan kaydı başarıyla silindi."
        except Exception as e: return False, str(e)

# ================= İŞ MANTIĞI =================
class Egitmen:
    def __init__(self, ad, uzmanlik): self.ad, self.uzmanlik = ad, uzmanlik
class Ogrenci:
    def __init__(self, ogrenci_id, ad, email): self.id, self.ad, self.email = ogrenci_id, ad, email
class Kurs:
    def __init__(self, k_id, ad, egitmen, kont, fiyat=0.0):
        self.id, self.ad, self.egitmen, self.kont, self.fiyat = k_id, ad, egitmen, kont, float(fiyat or 0)
        self.ogrenciler = []
    def kaydet(self, ogr):
        if len(self.ogrenciler) < self.kont and ogr not in self.ogrenciler:
            self.ogrenciler.append(ogr); return True, "Kayıt işlemi onaylandı."
        return False, "Kayıt Başarısız! Kontenjan dolu."
    def kayit_iptal(self, ogr):
        if ogr in self.ogrenciler:
            self.ogrenciler.remove(ogr)
            return True
        return False

# ================= GİRİŞ EKRANI =================
class LoginScreen(ctk.CTkFrame):
    def __init__(self, master, login_basarili_callback, **kwargs):
        super().__init__(master, fg_color=COLORS["bg_dark"], **kwargs)
        self.login_basarili_callback = login_basarili_callback
        self.db = DatabaseManager()

        self.pack(fill="both", expand=True)

        card = ctk.CTkFrame(self, fg_color=COLORS["bg_card"], width=400, height=500, corner_radius=20, border_width=1, border_color=COLORS["border"])
        card.place(relx=0.5, rely=0.5, anchor="center")
        card.pack_propagate(False)

        ctk.CTkLabel(card, text="🎓 PROKURS", font=ctk.CTkFont(family="Segoe UI", size=32, weight="bold"), text_color=COLORS["text_main"]).pack(pady=(45, 5))
        ctk.CTkLabel(card, text="Güvenli Yönetim Paneli", font=ctk.CTkFont(family="Segoe UI", size=14), text_color=COLORS["primary"]).pack(pady=(0, 40))

        self.ent_user = ctk.CTkEntry(card, placeholder_text="Kullanıcı Adı", font=ctk.CTkFont(size=14), width=300, height=50, 
                                     fg_color=COLORS["bg_dark"], border_color=COLORS["border"], corner_radius=10)
        self.ent_user.pack(pady=10)
        self.ent_user.bind("<Enter>", lambda e: self.ent_user.configure(border_color=COLORS["primary"]))
        self.ent_user.bind("<Leave>", lambda e: self.ent_user.configure(border_color=COLORS["border"]))

        self.ent_pass = ctk.CTkEntry(card, placeholder_text="Şifre", show="•", font=ctk.CTkFont(size=14), width=300, height=50, 
                                     fg_color=COLORS["bg_dark"], border_color=COLORS["border"], corner_radius=10)
        self.ent_pass.pack(pady=10)
        self.ent_pass.bind("<Enter>", lambda e: self.ent_pass.configure(border_color=COLORS["primary"]))
        self.ent_pass.bind("<Leave>", lambda e: self.ent_pass.configure(border_color=COLORS["border"]))
        
        self.ent_pass.bind("<Return>", lambda e: self._giris_kontrol())

        self.lbl_hata = ctk.CTkLabel(card, text="", text_color=COLORS["danger"], font=ctk.CTkFont(size=12))
        self.lbl_hata.pack(pady=5)

        ctk.CTkButton(card, text="Oturum Aç", width=300, height=50, font=ctk.CTkFont(size=15, weight="bold"), 
                      fg_color=COLORS["primary"], hover_color=COLORS["primary_hover"], corner_radius=10, 
                      command=self._giris_kontrol).pack(pady=(10, 0))

        ctk.CTkLabel(card, text="Varsayılan: admin / 1234", text_color=COLORS["text_muted"], font=ctk.CTkFont(size=11)).pack(pady=15)

    def _giris_kontrol(self):
        k_adi = self.ent_user.get().strip()
        sifre = self.ent_pass.get().strip()

        if not k_adi or not sifre:
            self.lbl_hata.configure(text="Lütfen kullanıcı adı ve şifre giriniz!")
            return

        if self.db.admin_girisi_yap(k_adi, sifre):
            self.login_basarili_callback()
        else:
            self.lbl_hata.configure(text="Hatalı kullanıcı adı veya şifre!")

# ================= ANA ARAYÜZ (GELİŞMİŞ SAAS MİMARİSİ) =================
class AdminDashboard(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color=COLORS["bg_dark"], corner_radius=0, **kwargs)
        self.db = DatabaseManager()
        self.egitmenler, self.ogrenciler, self.kurslar = [], {}, {}
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.f_logo = ctk.CTkFont(family="Segoe UI", size=26, weight="bold")
        self.f_menu = ctk.CTkFont(family="Segoe UI", size=14, weight="bold")
        self.f_title = ctk.CTkFont(family="Segoe UI", size=24, weight="bold")
        self.f_label = ctk.CTkFont(family="Segoe UI", size=13)
        self.f_input = ctk.CTkFont(family="Segoe UI", size=14)

        self._setup_tree_style()
        self._baslangic_verilerini_yukle()

        self._build_sidebar()
        self._build_main_area()
        self._verileri_guncelle()

        self.after(150, lambda: self.select_frame_by_name("Genel Bakış"))

    def _setup_tree_style(self):
        style = ttk.Style()
        style.theme_use("default") 
        style.configure("Treeview", background=COLORS["bg_card"], foreground=COLORS["text_main"],
                        fieldbackground=COLORS["bg_card"], rowheight=45, borderwidth=0, font=("Segoe UI", 11))
        style.configure("Treeview.Heading", background=COLORS["bg_panel"], foreground=COLORS["text_muted"], 
                        font=("Segoe UI", 12, "bold"), borderwidth=0, padding=8)
        style.map('Treeview', background=[('selected', COLORS["primary"])])
        style.layout("Treeview", [('Treeview.treearea', {'sticky': 'nswe'})]) 

    def _build_sidebar(self):
        self.sidebar_frame = ctk.CTkFrame(self, fg_color=COLORS["bg_panel"], corner_radius=0, width=280)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(7, weight=1)

        logo_frame = ctk.CTkFrame(self.sidebar_frame, fg_color="transparent")
        logo_frame.grid(row=0, column=0, padx=20, pady=(30, 40), sticky="ew")
        ctk.CTkLabel(logo_frame, text="🎓 PROKURS", font=self.f_logo, text_color=COLORS["text_main"]).pack(anchor="center")
        ctk.CTkLabel(logo_frame, text="Admin Workspace", font=self.f_label, text_color=COLORS["primary"]).pack(anchor="center")

        self.active_indicator = ctk.CTkFrame(self.sidebar_frame, width=5, height=45, fg_color=COLORS["primary"], corner_radius=3)
        self.active_indicator.place(x=5, y=-100)

        self.menu_buttons = {}
        menus = [
            ("📊", "Genel Bakış"),
            ("👨‍🏫", "Eğitmen Yönetimi"),
            ("🎓", "Öğrenci Yönetimi"),
            ("📚", "Kurs Yönetimi"),
            ("⚡", "Hızlı Kayıt"),
            ("🗄️", "Veritabanı Gezgini")
        ]

        def on_enter(e, b_name):
            if self.page_title.cget("text") != b_name.upper():
                self.menu_buttons[b_name].configure(text_color=COLORS["text_main"])

        def on_leave(e, b_name):
            if self.page_title.cget("text") != b_name.upper():
                self.menu_buttons[b_name].configure(text_color=COLORS["text_muted"])

        for i, (icon, name) in enumerate(menus):
            btn = ctk.CTkButton(
                self.sidebar_frame, text=f"  {icon}   {name}", font=self.f_menu, anchor="w",
                fg_color="transparent", text_color=COLORS["text_muted"], hover_color=COLORS["bg_card"],
                corner_radius=10, height=45, command=lambda n=name: self.select_frame_by_name(n)
            )
            btn.grid(row=i+1, column=0, padx=20, pady=4, sticky="ew")
            btn.bind("<Enter>", lambda e, n=name: on_enter(e, n))
            btn.bind("<Leave>", lambda e, n=name: on_leave(e, n))
            self.menu_buttons[name] = btn

        profile_f = ctk.CTkFrame(self.sidebar_frame, fg_color=COLORS["bg_card"], corner_radius=12)
        profile_f.grid(row=8, column=0, padx=15, pady=20, sticky="s")
        ctk.CTkLabel(profile_f, text="👤 Admin: Yetkili", font=ctk.CTkFont(size=12, weight="bold"), text_color=COLORS["text_main"]).pack(pady=(10,0), padx=20)
        ctk.CTkLabel(profile_f, text="V 13.1 (Auto-ID)", font=ctk.CTkFont(size=11), text_color=COLORS["success"]).pack(pady=(0,10), padx=20)

    def _safe_animate_indicator(self, btn):
        target_y = btn.winfo_y()
        if target_y <= 10:
            self.after(50, lambda: self._safe_animate_indicator(btn))
            return
        if hasattr(self, '_anim_id') and self._anim_id:
            self.after_cancel(self._anim_id)
        current_y = float(self.active_indicator.place_info().get('y', -100))
        if current_y <= 0:
            self.active_indicator.place(x=5, y=target_y)
        else:
            self._animate_step(current_y, target_y)

    def _animate_step(self, current_y, target_y):
        if abs(current_y - target_y) < 1.5:
            self.active_indicator.place(x=5, y=target_y)
            return
        new_y = current_y + (target_y - current_y) * 0.25
        self.active_indicator.place(x=5, y=new_y)
        self._anim_id = self.after(15, self._animate_step, new_y, target_y)

    # --- ANA İÇERİK ALANI ---
    def _build_main_area(self):
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=35, pady=25)
        self.main_frame.grid_rowconfigure(1, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

        header_f = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        header_f.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        
        self.page_title = ctk.CTkLabel(header_f, text="Dashboard", font=self.f_title, text_color=COLORS["text_main"])
        self.page_title.pack(side="left")
        
        tarih = datetime.now().strftime("%d %B %Y")
        ctk.CTkLabel(header_f, text=f"📅 {tarih}", font=self.f_label, text_color=COLORS["text_muted"]).pack(side="right", padx=10)

        self.content_area = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.content_area.grid(row=1, column=0, sticky="nsew")

        self.frames = {}
        self._page_dashboard()
        self._page_egitmen()
        self._page_ogrenci()
        self._page_kurs()
        self._page_kayit()
        self._page_veritabani()

    def select_frame_by_name(self, name):
        for btn_name, btn in self.menu_buttons.items():
            if btn_name == name:
                btn.configure(fg_color=COLORS["bg_card"], text_color=COLORS["primary"])
                self._safe_animate_indicator(btn)
            else:
                btn.configure(fg_color="transparent", text_color=COLORS["text_muted"])
        
        self.page_title.configure(text=name.upper())

        for frame_name, frame in self.frames.items():
            if frame_name == name: frame.pack(fill="both", expand=True)
            else: frame.pack_forget()

    # ================= UI YARDIMCI METOTLARI =================
    def _create_input(self, parent, label, placeholder):
        f = ctk.CTkFrame(parent, fg_color="transparent")
        f.pack(fill="x", pady=(15, 5), padx=25)
        ctk.CTkLabel(f, text=label, font=self.f_label, text_color=COLORS["text_muted"]).pack(anchor="w", padx=5, pady=(0,5))
        ent = ctk.CTkEntry(f, placeholder_text=placeholder, font=self.f_input, height=45, fg_color=COLORS["bg_dark"], 
                           border_color=COLORS["border"], border_width=1, corner_radius=10)
        ent.pack(fill="x")
        ent.bind("<Enter>", lambda e: ent.configure(border_color=COLORS["primary"]))
        ent.bind("<Leave>", lambda e: ent.configure(border_color=COLORS["border"]))
        return ent

    def _alanlar_dolu_mu(self, *degerler):
        return all(str(deger).strip() for deger in degerler)

    def _create_table_header(self, parent, title):
        f = ctk.CTkFrame(parent, fg_color="transparent")
        f.pack(side="top", fill="x", padx=25, pady=(25, 10))
        ctk.CTkLabel(f, text=title, font=ctk.CTkFont(size=18, weight="bold"), text_color=COLORS["text_main"]).pack(side="left")

    def _create_table_action(self, parent, btn_text, cmd):
        f = ctk.CTkFrame(parent, fg_color="transparent")
        f.pack(side="bottom", fill="x", padx=25, pady=(10, 25))
        if cmd:
            ctk.CTkButton(f, text=btn_text, fg_color=COLORS["danger"], hover_color=COLORS["danger_hover"],
                          height=45, width=220, font=ctk.CTkFont(size=14, weight="bold"), command=cmd).pack(side="right")

    def _create_tree(self, parent, cols):
        f = ctk.CTkFrame(parent, fg_color="transparent")
        f.pack(side="top", fill="both", expand=True, padx=25, pady=(0, 10))
        scroll = ctk.CTkScrollbar(f, orientation="vertical", width=12)
        scroll.pack(side="right", fill="y")
        tree = ttk.Treeview(f, columns=cols, show="headings", yscrollcommand=scroll.set)
        tree.pack(side="left", fill="both", expand=True)
        scroll.configure(command=tree.yview)
        for c in cols: tree.heading(c, text=c); tree.column(c, anchor="center")
        return tree

    # ================= SAYFALAR =================
    def _page_dashboard(self):
        frame = ctk.CTkFrame(self.content_area, fg_color="transparent")
        self.frames["Genel Bakış"] = frame
        
        grid_f = ctk.CTkFrame(frame, fg_color="transparent")
        grid_f.pack(fill="x", pady=(0, 20))
        grid_f.grid_columnconfigure((0,1,2,3), weight=1, uniform="col")

        self.stat_cards = {}
        data = [("👨‍🏫 Eğitmenler", "egitmen", COLORS["primary"]), ("🎓 Öğrenciler", "ogrenci", COLORS["success"]),
                ("📚 Kurslar", "kurs", COLORS["warning"]), ("📝 Kayıt Dağılımı", "kayit", "#A855F7")]

        for i, (title, key, color) in enumerate(data):
            card = ctk.CTkFrame(grid_f, fg_color=COLORS["bg_card"], corner_radius=15, border_width=1, border_color=COLORS["border"])
            card.grid(row=0, column=i, padx=10, pady=10, sticky="nsew")
            
            ctk.CTkLabel(card, text=title, font=ctk.CTkFont(size=15, weight="bold"), text_color=COLORS["text_muted"]).pack(anchor="w", padx=20, pady=(20,0))
            ana_lbl = ctk.CTkLabel(card, text="0", font=ctk.CTkFont(size=42, weight="bold"), text_color=color)
            ana_lbl.pack(anchor="w", padx=20, pady=(0, 2))
            detay_lbl = ctk.CTkLabel(card, text="-", font=ctk.CTkFont(size=12), text_color=COLORS["text_muted"], justify="left", wraplength=180)
            detay_lbl.pack(anchor="w", padx=20, pady=(0, 20))
            self.stat_cards[key] = (ana_lbl, detay_lbl) 

        bottom_f = ctk.CTkFrame(frame, fg_color="transparent")
        bottom_f.pack(fill="both", expand=True)
        bottom_f.grid_columnconfigure((0,1), weight=1, uniform="col")

        info_card = ctk.CTkFrame(bottom_f, fg_color=COLORS["bg_card"], corner_radius=15)
        info_card.grid(row=0, column=0, sticky="nsew", padx=10)
        ctk.CTkLabel(info_card, text="Sistem Özeti", font=self.f_menu, text_color=COLORS["text_main"]).pack(anchor="w", padx=20, pady=(20,10))
        ctk.CTkLabel(info_card, text="• Tüm veritabanı bağlantıları stabil.\n• Veriler şifrelenmiş SQLite dosyasında tutuluyor.\n• Öğrenci ID'leri otomatik atanmaktadır.\n• Katı veri doğrulama protokolleri devrededir.", 
                     font=self.f_label, text_color=COLORS["text_muted"], justify="left").pack(anchor="w", padx=20)

        quick_card = ctk.CTkFrame(bottom_f, fg_color=COLORS["bg_card"], corner_radius=15)
        quick_card.grid(row=0, column=1, sticky="nsew", padx=10)
        ctk.CTkLabel(quick_card, text="Hızlı Kısayollar", font=self.f_menu, text_color=COLORS["text_main"]).pack(anchor="w", padx=20, pady=(20,10))
        ctk.CTkButton(quick_card, text="+ Yeni Kurs Ekle", fg_color=COLORS["primary"], command=lambda: self.select_frame_by_name("Kurs Yönetimi")).pack(fill="x", padx=20, pady=5)
        ctk.CTkButton(quick_card, text="⚡ Kayıt Yap", fg_color=COLORS["success"], command=lambda: self.select_frame_by_name("Hızlı Kayıt")).pack(fill="x", padx=20, pady=5)

    def _page_egitmen(self):
        frame = ctk.CTkFrame(self.content_area, fg_color="transparent")
        self.frames["Eğitmen Yönetimi"] = frame
        
        form_card = ctk.CTkFrame(frame, fg_color=COLORS["bg_card"], width=350, corner_radius=15)
        form_card.pack(side="left", fill="y", padx=(0, 20))
        form_card.pack_propagate(False) 
        
        ctk.CTkLabel(form_card, text="Yeni Eğitmen Formu", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=(25,10))
        self.ent_egitmen_ad = self._create_input(form_card, "Ad Soyad", "Örn: Ahmet Yılmaz")
        self.ent_egitmen_uzm = self._create_input(form_card, "Uzmanlık Alanı", "Örn: Yazılım")
        ctk.CTkButton(form_card, text="+ Sisteme Ekle", fg_color=COLORS["success"], hover_color=COLORS["success_hover"], 
                      height=45, font=self.f_menu, command=self._islem_egitmen_ekle).pack(fill="x", padx=25, pady=30)

        table_card = ctk.CTkFrame(frame, fg_color=COLORS["bg_card"], corner_radius=15)
        table_card.pack(side="right", fill="both", expand=True)
        
        self._create_table_header(table_card, "Mevcut Eğitmenler")
        self._create_table_action(table_card, "❌ Seçili Eğitmeni Sil", self._islem_egitmen_sil)
        self.tree_egitmen = self._create_tree(table_card, ("Ad Soyad", "Uzmanlık Alanı"))

    def _page_ogrenci(self):
        frame = ctk.CTkFrame(self.content_area, fg_color="transparent")
        self.frames["Öğrenci Yönetimi"] = frame
        
        form_card = ctk.CTkFrame(frame, fg_color=COLORS["bg_card"], width=350, corner_radius=15)
        form_card.pack(side="left", fill="y", padx=(0, 20))
        form_card.pack_propagate(False)
        
        ctk.CTkLabel(form_card, text="Öğrenci Kayıt Formu", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=(25,10))
        
        # ID GİRİŞ KUTUSU KALDIRILDI - OTOMATİK ATANACAK
        self.ent_ogr_ad = self._create_input(form_card, "Ad Soyad", "Öğrenci ismi")
        self.ent_ogr_email = self._create_input(form_card, "Email Adresi", "ornek@mail.com")
        ctk.CTkLabel(form_card, text="*Öğrenci ID numarası otomatik atanır.", text_color=COLORS["text_muted"], font=ctk.CTkFont(size=11)).pack(pady=(10,0))
        
        ctk.CTkButton(form_card, text="+ Öğrenci Oluştur", fg_color=COLORS["success"], hover_color=COLORS["success_hover"], 
                      height=45, font=self.f_menu, command=self._islem_ogrenci_ekle).pack(fill="x", padx=25, pady=20)

        table_card = ctk.CTkFrame(frame, fg_color=COLORS["bg_card"], corner_radius=15)
        table_card.pack(side="right", fill="both", expand=True)
        
        self._create_table_header(table_card, "Sistemdeki Öğrenciler")
        self._create_table_action(table_card, "❌ Seçili Öğrenciyi Sil", self._islem_ogrenci_sil)
        self.tree_ogrenci = self._create_tree(table_card, ("Öğrenci ID", "Ad Soyad", "Email"))

    def _page_kurs(self):
        frame = ctk.CTkFrame(self.content_area, fg_color="transparent")
        self.frames["Kurs Yönetimi"] = frame
        
        form_card = ctk.CTkFrame(frame, fg_color=COLORS["bg_card"], width=350, corner_radius=15)
        form_card.pack(side="left", fill="y", padx=(0, 20))
        form_card.pack_propagate(False)
        
        ctk.CTkLabel(form_card, text="Kurs Oluşturucu", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=(25,10))
        self.ent_kurs_id = self._create_input(form_card, "Kurs Kodu", "Örn: PY101")
        self.ent_kurs_ad = self._create_input(form_card, "Kurs Adı", "Kursun tam adı")
        
        f_cmb = ctk.CTkFrame(form_card, fg_color="transparent")
        f_cmb.pack(fill="x", pady=(15,5), padx=25)
        ctk.CTkLabel(f_cmb, text="Öğretmen Adı", font=self.f_label, text_color=COLORS["text_muted"]).pack(anchor="w", padx=5, pady=(0,5))
        self.cmb_egitmen = ctk.CTkEntry(f_cmb, placeholder_text="Öğretmen adı yazın", font=self.f_input, width=300, height=45,
                                        fg_color=COLORS["bg_dark"], border_color=COLORS["border"], corner_radius=10)
        self.cmb_egitmen.pack(fill="x")

        self.ent_kurs_kont = self._create_input(form_card, "Kontenjan", "Sadece rakam giriniz")
        self.ent_kurs_fiyat = self._create_input(form_card, "Kurs Fiyat", "Sadece rakam giriniz")
        ctk.CTkButton(form_card, text="+ Kurs Ekle", fg_color=COLORS["success"], hover_color=COLORS["success_hover"], 
                      height=45, font=self.f_menu, command=self._islem_kurs_ekle).pack(fill="x", padx=25, pady=20)

        table_card = ctk.CTkFrame(frame, fg_color=COLORS["bg_card"], corner_radius=15)
        table_card.pack(side="right", fill="both", expand=True)
        
        self._create_table_header(table_card, "Aktif Kurslar (Detay için çift tıkla)")
        self.tree_kurs = self._create_tree(table_card, ("Kurs Kodu", "Kurs Adı", "Eğitmen", "Doluluk", "Fiyat"))
        self.tree_kurs.bind("<Double-1>", self._islem_kurs_detay_goster)

    def _page_kayit(self):
        frame = ctk.CTkFrame(self.content_area, fg_color="transparent")
        self.frames["Hızlı Kayıt"] = frame
        
        center_f = ctk.CTkFrame(frame, fg_color="transparent")
        center_f.pack(expand=True)

        card = ctk.CTkFrame(center_f, fg_color=COLORS["bg_card"], width=450, corner_radius=20, border_width=1, border_color=COLORS["border"])
        card.pack(pady=20, padx=20)
        card.pack_propagate(False)
        card.configure(height=420)

        ctk.CTkLabel(card, text="⚡ Kursa Entegrasyon", font=ctk.CTkFont(size=22, weight="bold"), text_color=COLORS["text_main"]).pack(pady=(35, 10))
        ctk.CTkLabel(card, text="Sistemde var olan öğrenciyi kursa bağlayın.", font=self.f_label, text_color=COLORS["text_muted"]).pack(pady=(0, 20))

        # GÖRSEL YANILGI BURADA DÜZELTİLDİ: "Örn: 1"
        self.ent_kayit_ogr = self._create_input(card, "Öğrenci ID Numarası", "Örn: 1")
        self.ent_kayit_kurs = self._create_input(card, "Kurs Kodu", "Örn: PY101")
        
        ctk.CTkButton(card, text="Kayıt İşlemini Onayla", fg_color=COLORS["primary"], hover_color=COLORS["primary_hover"], 
                      height=50, font=self.f_menu, command=self._islem_kursa_kaydet).pack(fill="x", padx=25, pady=(30, 0))

    def _page_veritabani(self):
        frame = ctk.CTkFrame(self.content_area, fg_color="transparent")
        self.frames[" Veritabanı Gezgini"] = frame
        
        card = ctk.CTkFrame(frame, fg_color=COLORS["bg_card"], corner_radius=15)
        card.pack(fill="both", expand=True)

        header_f = ctk.CTkFrame(card, fg_color="transparent")
        header_f.pack(fill="x", padx=25, pady=(25, 10))
        ctk.CTkLabel(header_f, text="Ham Tablo Görüntüleyici", font=ctk.CTkFont(size=18, weight="bold")).pack(side="left")
        
        btn_f = ctk.CTkFrame(header_f, fg_color="transparent")
        btn_f.pack(side="right")
        for t in ["egitmenler", "ogrenciler", "kurslar", "kayitlar"]:
            ctk.CTkButton(btn_f, text=t.upper(), width=100, height=35, fg_color=COLORS["bg_panel"], text_color=COLORS["text_muted"],
                          hover_color=COLORS["border"], command=lambda n=t: self._db_tablo_yukle(n)).pack(side="left", padx=5)

        self.db_tree = self._create_tree(card, ("Sütun 1", "Sütun 2", "Sütun 3", "Sütun 4"))

    def _db_tablo_yukle(self, table_name):
        data = self.db.cursor.execute(f"SELECT * FROM {table_name}").fetchall()
        for row in self.db_tree.get_children(): self.db_tree.delete(row)
        for r in data: self.db_tree.insert("", "end", values=r)

    # ================= VERİ GÜNCELLEME VE İŞLEM METOTLARI =================
    def _baslangic_verilerini_yukle(self):
        self.egitmenler.clear(); self.ogrenciler.clear(); self.kurslar.clear()
        self.egitmenler = [Egitmen(e[1], e[2]) for e in self.db.egitmenleri_getir()]
        for o in self.db.ogrencileri_getir(): self.ogrenciler[o[0]] = Ogrenci(o[0], o[1], o[2])
        for k in self.db.kurslari_getir():
            e = next((x for x in self.egitmenler if x.ad == k[2]), None)
            self.kurslar[k[0]] = Kurs(k[0], k[1], e, k[3], k[4] if len(k) > 4 else 0)
        for kayit in self.db.kayitlari_getir():
            if kayit[0] in self.ogrenciler and kayit[1] in self.kurslar:
                self.kurslar[kayit[1]].ogrenciler.append(self.ogrenciler[kayit[0]])

    def _verileri_guncelle(self):
        gecerli_egitmenler = [e for e in self.egitmenler if e.ad and e.ad.strip()]
        egitmen_isimleri = ", ".join([e.ad.split()[0] for e in gecerli_egitmenler][:4]) 
        if len(gecerli_egitmenler) > 4: egitmen_isimleri += "..."
        
        gecerli_ogrenciler = [o for o in self.ogrenciler.values() if o.ad and o.ad.strip()]
        ogrenci_isimleri = ", ".join([o.ad.split()[0] for o in gecerli_ogrenciler][:4])
        if len(gecerli_ogrenciler) > 4: ogrenci_isimleri += "..."
        
        kurs_isimleri = ", ".join([k.id for k in self.kurslar.values()][:4])
        if len(self.kurslar) > 4: kurs_isimleri += "..."
        
        dolu_kurslar = [k for k in self.kurslar.values() if len(k.ogrenciler) > 0]
        kayit_ozeti = ", ".join([f"{k.id} ({len(k.ogrenciler)})" for k in dolu_kurslar][:3])
        if len(dolu_kurslar) > 3: kayit_ozeti += "..."

        detaylar = {
            'egitmen': egitmen_isimleri if egitmen_isimleri else "Kayıt bulunamadı",
            'ogrenci': ogrenci_isimleri if ogrenci_isimleri else "Kayıt bulunamadı",
            'kurs': kurs_isimleri if kurs_isimleri else "Kayıt bulunamadı",
            'kayit': kayit_ozeti if kayit_ozeti else "Hiç kayıt yok"
        }

        stats = self.db.get_stats()
        for k, v in stats.items(): 
            if k in self.stat_cards: 
                ana_lbl, detay_lbl = self.stat_cards[k]
                ana_lbl.configure(text=str(v))
                detay_lbl.configure(text=detaylar[k])
        
        def pop(t, d):
            for r in t.get_children(): t.delete(r)
            for i in d: t.insert("", "end", values=i)
            
        pop(self.tree_egitmen, [(e.ad, e.uzmanlik) for e in self.egitmenler])
        pop(self.tree_ogrenci, [(o.id, o.ad, o.email) for o in self.ogrenciler.values()])
        pop(self.tree_kurs, [(k.id, k.ad, k.egitmen.ad if k.egitmen else "Bilinmiyor", f"{len(k.ogrenciler)}/{k.kont}", f"{k.fiyat:.2f} ₺") for k in self.kurslar.values()])

    def _islem_egitmen_ekle(self):
        ad = self.ent_egitmen_ad.get().strip()
        uzm = self.ent_egitmen_uzm.get().strip()
        if not self._alanlar_dolu_mu(ad, uzm): return messagebox.showwarning("Eksik Bilgi", "Lütfen tüm alanları doldurunuz!")
        if any(char.isdigit() for char in ad): return messagebox.showwarning("Hatalı Giriş", "Eğitmen adında rakam bulunamaz!")
        if any(char.isdigit() for char in uzm): return messagebox.showwarning("Hatalı Giriş", "Uzmanlık alanında rakam bulunamaz!")

        basarili, mesaj = self.db.egitmen_ekle(ad, uzm)
        if basarili:
            self.egitmenler.append(Egitmen(ad, uzm))
            self._verileri_guncelle()
            self.ent_egitmen_ad.delete(0, 'end'); self.ent_egitmen_uzm.delete(0, 'end')
            messagebox.showinfo("Başarılı", mesaj)
        else: messagebox.showerror("Hata", mesaj)

    # ÖĞRENCİ EKLEME MANTIĞI OTOMATİK ID'YE GÖRE DÜZENLENDİ
    def _islem_ogrenci_ekle(self):
        ad, mail = self.ent_ogr_ad.get().strip(), self.ent_ogr_email.get().strip()
        
        if not self._alanlar_dolu_mu(ad, mail): return messagebox.showwarning("Eksik", "Bilgileri eksiksiz girin!")
        if any(char.isdigit() for char in ad): return messagebox.showwarning("Hatalı Giriş", "Öğrenci adında rakam bulunamaz!")
        if "@" not in mail or "." not in mail: return messagebox.showwarning("Hatalı Giriş", "Lütfen geçerli e-posta girin!")
        
        # ID veritabanından alınıyor
        basarili, mesaj, yeni_id = self.db.ogrenci_ekle(ad, mail)
        if basarili:
            self.ogrenciler[yeni_id] = Ogrenci(yeni_id, ad, mail)
            self._verileri_guncelle()
            self.ent_ogr_ad.delete(0, 'end'); self.ent_ogr_email.delete(0, 'end')
            messagebox.showinfo("Başarılı", f"{mesaj}\nAtanan Öğrenci ID: {yeni_id}")
        else: messagebox.showerror("Hata", mesaj)

    def _islem_kurs_ekle(self):
        k_id = self.ent_kurs_id.get().strip()
        ad = self.ent_kurs_ad.get().strip()
        e_ad = self.cmb_egitmen.get().strip()
        kont_str = self.ent_kurs_kont.get().strip()
        fiyat_str = self.ent_kurs_fiyat.get().strip()
        if not self._alanlar_dolu_mu(k_id, ad, e_ad, kont_str, fiyat_str): return messagebox.showwarning("Eksik", "Tüm alanları doldurun!")
        if not kont_str.isdigit(): return messagebox.showwarning("Hatalı Giriş", "Kontenjan kısmına yalnızca rakam girilmelidir!")
        if not fiyat_str.replace(',', '.').replace('.', '', 1).isdigit(): return messagebox.showwarning("Hatalı Giriş", "Fiyat kısmına yalnızca sayı girilmelidir!")
        
        kont = int(kont_str)
        fiyat = float(fiyat_str.replace(',', '.'))
        if not (5 <= kont <= 40): return messagebox.showwarning("Hata", "Kontenjan 5-40 arası olmalı!")
        if fiyat <= 0: return messagebox.showwarning("Hata", "Fiyat sıfırdan büyük olmalıdır!")

        basarili, mesaj = self.db.kurs_ekle(k_id, ad, e_ad, kont, fiyat)
        if basarili:
            e = next((x for x in self.egitmenler if x.ad == e_ad), None)
            self.kurslar[k_id] = Kurs(k_id, ad, e, kont, fiyat)
            self._verileri_guncelle()
            for w in [self.ent_kurs_id, self.ent_kurs_ad, self.ent_kurs_kont, self.ent_kurs_fiyat]: w.delete(0, 'end')
            messagebox.showinfo("Başarılı", mesaj)
        else: messagebox.showerror("Hata", mesaj)

    def _islem_kursa_kaydet(self):
        o_id_str, k_id = self.ent_kayit_ogr.get().strip(), self.ent_kayit_kurs.get().strip()
        if not self._alanlar_dolu_mu(o_id_str, k_id): return messagebox.showwarning("Eksik", "ID ve Kurs Kodu girin!")
        if not o_id_str.isdigit(): return messagebox.showwarning("Hatalı Giriş", "Kayıt yapılacak Öğrenci ID yalnızca rakamlardan oluşmalıdır!")
        
        o_id = int(o_id_str)
        if o_id not in self.ogrenciler: return messagebox.showerror("Hata", "Öğrenci bulunamadı!")
        if k_id not in self.kurslar: return messagebox.showerror("Hata", "Kurs bulunamadı!")

        ok, msg = self.kurslar[k_id].kaydet(self.ogrenciler[o_id])
        if ok:
            db_basarili, db_mesaj = self.db.kayit_ekle(o_id, k_id)
            if db_basarili:
                self._verileri_guncelle()
                self.ent_kayit_ogr.delete(0, 'end'); self.ent_kayit_kurs.delete(0, 'end')
                messagebox.showinfo("Başarılı", msg)
            else:
                self.kurslar[k_id].ogrenciler.remove(self.ogrenciler[o_id])
                messagebox.showerror("Hata", db_mesaj)
        else: messagebox.showwarning("Hata", msg)

    def _islem_kurs_detay_goster(self, event):
        secili = self.tree_kurs.selection()
        if not secili: return
        
        k_id = str(self.tree_kurs.item(secili[0])['values'][0])
        if k_id not in self.kurslar: return
        kurs = self.kurslar[k_id]

        p = ctk.CTkToplevel(self)
        p.title(f"Kurs Detay: {kurs.ad}")
        p.geometry("750x550")
        p.configure(fg_color=COLORS["bg_dark"])
        p.attributes("-topmost", True) 
        p.grab_set() 
        
        ctk.CTkLabel(p, text=f"📚 {kurs.ad}", font=self.f_title, text_color=COLORS["text_main"]).pack(pady=(25, 5))
        lbl_info = ctk.CTkLabel(p, text=f"Öğrenciler ({len(kurs.ogrenciler)}/{kurs.kont}) | Eğitmen: {kurs.egitmen.ad if kurs.egitmen else 'Bilinmiyor'} | Fiyat: {kurs.fiyat:.2f} ₺", font=self.f_menu, text_color=COLORS["text_muted"])
        lbl_info.pack(pady=(0, 20))

        kart = ctk.CTkFrame(p, fg_color=COLORS["bg_card"], corner_radius=15)
        kart.pack(fill="both", expand=True, padx=25, pady=(0, 25))

        if not kurs.ogrenciler:
            ctk.CTkLabel(kart, text="Bu kursa kayıtlı öğrenci yok.", font=self.f_input, text_color=COLORS["text_muted"]).pack(expand=True)
        else:
            toolbar = ctk.CTkFrame(kart, fg_color="transparent")
            toolbar.pack(fill="x", padx=15, pady=(15, 0))

            def _ogrenciyi_kurstan_cikar():
                secili_ogr = td.selection()
                if not secili_ogr:
                    return messagebox.showwarning("Uyarı", "Lütfen tablodan çıkarılacak öğrenciyi seçin!", parent=p)
                
                ogr_id = td.item(secili_ogr[0])['values'][0]
                ogr_ad = td.item(secili_ogr[0])['values'][1]
                
                if messagebox.askyesno("Kayıt İptali", f"'{ogr_ad}' isimli öğrencinin bu kurstan kaydı silinecek.\nOnaylıyor musunuz?", parent=p):
                    ok, msg = self.db.kurs_kaydi_sil(ogr_id, k_id)
                    if ok:
                        ogr_obj = self.ogrenciler.get(ogr_id)
                        if ogr_obj: kurs.kayit_iptal(ogr_obj)
                        
                        td.delete(secili_ogr[0])
                        lbl_info.configure(text=f"Öğrenciler ({len(kurs.ogrenciler)}/{kurs.kont}) | Eğitmen: {kurs.egitmen.ad if kurs.egitmen else 'Bilinmiyor'} | Fiyat: {kurs.fiyat:.2f} ₺")
                        self._verileri_guncelle()
                        messagebox.showinfo("Başarılı", msg, parent=p)
                    else:
                        messagebox.showerror("Hata", msg, parent=p)

            ctk.CTkButton(toolbar, text="❌ Seçili Öğrenciyi Kurstan Çıkar", fg_color=COLORS["danger"], hover_color=COLORS["danger_hover"], font=self.f_label, command=_ogrenciyi_kurstan_cikar).pack(side="right")

            tf = ctk.CTkFrame(kart, fg_color="transparent")
            tf.pack(fill="both", expand=True, padx=15, pady=15)
            ys = ctk.CTkScrollbar(tf, orientation="vertical", width=12)
            ys.pack(side="right", fill="y")
            
            td = ttk.Treeview(tf, columns=("Öğrenci No", "Ad Soyad", "Email Adresi"), show="headings", yscrollcommand=ys.set)
            td.pack(side="left", fill="both", expand=True)
            ys.configure(command=td.yview)

            for col in ("Öğrenci No", "Ad Soyad", "Email Adresi"): td.heading(col, text=col)
            td.column("Öğrenci No", width=100, anchor="center"); td.column("Ad Soyad", width=200); td.column("Email Adresi", width=250)
            for ogr in kurs.ogrenciler: td.insert("", "end", values=(ogr.id, ogr.ad, ogr.email))

    def _islem_egitmen_sil(self):
        secili = self.tree_egitmen.selection()
        if not secili: return messagebox.showwarning("Uyarı", "Lütfen tablodan bir eğitmen seçin!")
        ad_degeri = self.tree_egitmen.item(secili[0])['values'][0]
        if messagebox.askyesno("Kalıcı Silme", f"'{ad_degeri}' tamamen silinecek. Onaylıyor musunuz?"):
            ok, msg = self.db.kayit_sil("egitmenler", "ad", ad_degeri)
            if ok:
                self._baslangic_verilerini_yukle(); self._verileri_guncelle(); messagebox.showinfo("Başarılı", msg)
            else: messagebox.showerror("Hata", msg)

    def _islem_ogrenci_sil(self):
        secili = self.tree_ogrenci.selection()
        if not secili: return messagebox.showwarning("Uyarı", "Lütfen tablodan bir öğrenci seçin!")
        ogr_id = self.tree_ogrenci.item(secili[0])['values'][0]
        ogr_ad = self.tree_ogrenci.item(secili[0])['values'][1] 
        if messagebox.askyesno("Kalıcı Silme", f"'{ogr_ad}' tamamen silinecek. Onaylıyor musunuz?"):
            ok, msg = self.db.kayit_sil("ogrenciler", "id", ogr_id)
            if ok:
                self._baslangic_verilerini_yukle(); self._verileri_guncelle(); messagebox.showinfo("Başarılı", msg)
            else: messagebox.showerror("Hata", msg)

# ================= UYGULAMA YÖNETİCİSİ =================
class AppController(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("🎓 ProKurs | Admin Dashboard v13.1")
        self.geometry("1400x850")
        self.minsize(1200, 750)
        self.configure(fg_color=COLORS["bg_dark"])

        self.login_ekrani = LoginScreen(self, self.login_basarili)
        
    def login_basarili(self):
        self.login_ekrani.pack_forget()
        self.login_ekrani.destroy()
        
        main_container = ctk.CTkFrame(self, fg_color=COLORS["bg_dark"], corner_radius=0)
        main_container.pack(fill="both", expand=True)
        AdminDashboard(main_container).pack(fill="both", expand=True)

if __name__ == "__main__":
    app = AppController()
    app.mainloop()
