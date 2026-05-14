import customtkinter as ctk
import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime

# --- GLOBAL TEMA VE RENK PALETİ ---
ctk.set_appearance_mode("Dark")

COLORS = {
    "bg_main": "#140f0d",       
    "bg_surface": "#1f1815",    
    "bg_card": "#2a211d",       
    "border": "#3d302a",        
    "primary": "#d97706",       
    "primary_hover": "#b45309", 
    "text_main": "#fdf8f6",     
    "text_muted": "#a8a29e",    
    "success": "#10b981",       
    "warning": "#f59e0b",
    "danger": "#ef4444",
    "danger_hover": "#dc2626"
}

# ================= SQLITE VERİTABANI YÖNETİCİSİ =================
class TarifVeritabani:
    def __init__(self, db_name="yemek_tarif.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self._tablolari_kur()
        self._ornek_verileri_bas()

    def _tablolari_kur(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS kullanicilar (
            kullanici_id INTEGER PRIMARY KEY AUTOINCREMENT, ad TEXT)''')
        
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS tarifler (
            tarif_id INTEGER PRIMARY KEY AUTOINCREMENT, tarif_adi TEXT UNIQUE, kategori TEXT, hazirlama_suresi INTEGER)''')
        
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS malzemeler (
            id INTEGER PRIMARY KEY AUTOINCREMENT, tarif_id INTEGER, malzeme_adi TEXT, miktar TEXT,
            FOREIGN KEY(tarif_id) REFERENCES tarifler(tarif_id))''')
        
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS degerlendirmeler (
            id INTEGER PRIMARY KEY AUTOINCREMENT, kullanici_id INTEGER, tarif_id INTEGER, puan INTEGER,
            FOREIGN KEY(kullanici_id) REFERENCES kullanicilar(kullanici_id),
            FOREIGN KEY(tarif_id) REFERENCES tarifler(tarif_id))''')
        self.conn.commit()

    def _ornek_verileri_bas(self):
        self.cursor.execute("SELECT COUNT(*) FROM kullanicilar")
        if self.cursor.fetchone()[0] == 0:
            for ad in ["Ahmet Yılmaz", "Ayşe Kaya", "Caner Gezer", "Elif Demir", "Burak Şahin", "Zeynep Çelik"]:
                self.db_kullanici_ekle(ad)
            
            tarifler = [
                ("Mercimek Çorbası", "Çorba", 30),
                ("Fırın Sütlaç", "Tatlı", 45),
                ("Karnıyarık", "Ana Yemek", 60),
                ("Tiramisu", "Tatlı", 40),
                ("Mantı", "Hamur İşi", 90),
                ("Yaprak Sarma", "Zeytinyağlı", 120)
            ]
            for t_ad, t_kat, t_sure in tarifler:
                self.db_tarif_ekle(t_ad, t_kat, t_sure)
                
            # Malzemeler
            self.db_malzeme_ekle(1, "Kırmızı Mercimek", "1 Su Bardağı")
            self.db_malzeme_ekle(1, "Soğan", "1 Adet")
            self.db_malzeme_ekle(2, "Süt", "1 Litre")
            self.db_malzeme_ekle(2, "Pirinç", "Yarım Çay Bardağı")
            self.db_malzeme_ekle(3, "Patlıcan", "6 Adet")
            self.db_malzeme_ekle(3, "Kıyma", "300 Gram")
            
            # Değerlendirmeler
            self.db_degerlendirme_ekle(1, 1, 5) 
            self.db_degerlendirme_ekle(2, 2, 4) 
            self.db_degerlendirme_ekle(3, 3, 5) 
            
            self.conn.commit()

    # --- VERİ EKLEME/GÜNCELLEME İŞLEMLERİ ---
    def db_tarif_ekle(self, tarif_adi, kategori, hazirlama_suresi):
        try:
            self.cursor.execute("INSERT INTO tarifler (tarif_adi, kategori, hazirlama_suresi) VALUES (?, ?, ?)", 
                                (tarif_adi, kategori, hazirlama_suresi))
            self.conn.commit(); return True, "Tarif başarıyla eklendi."
        except sqlite3.IntegrityError: return False, "Bu isimde bir tarif zaten var!"

    def db_tarif_guncelle(self, tarif_id, yeni_ad, yeni_kat, yeni_sure):
        try:
            self.cursor.execute("UPDATE tarifler SET tarif_adi=?, kategori=?, hazirlama_suresi=? WHERE tarif_id=?", 
                                (yeni_ad, yeni_kat, yeni_sure, tarif_id))
            self.conn.commit(); return True, "Tarif başarıyla güncellendi."
        except sqlite3.IntegrityError: return False, "Bu tarif adı başka bir tarifte kullanılıyor!"

    def db_kullanici_ekle(self, ad):
        try:
            self.cursor.execute("INSERT INTO kullanicilar (ad) VALUES (?)", (ad,))
            self.conn.commit(); return True, "Kullanıcı başarıyla sisteme eklendi."
        except Exception as e: return False, str(e)

    def db_malzeme_ekle(self, t_id, m_adi, miktar):
        self.cursor.execute("SELECT * FROM malzemeler WHERE tarif_id=? AND LOWER(malzeme_adi)=?", (t_id, m_adi.lower()))
        if self.cursor.fetchone(): return False, "Bu malzeme tarifte zaten mevcut!"
        
        self.cursor.execute("INSERT INTO malzemeler (tarif_id, malzeme_adi, miktar) VALUES (?, ?, ?)", (t_id, m_adi, miktar))
        self.conn.commit(); return True, "Malzeme eklendi."

    def db_degerlendirme_ekle(self, k_id, t_id, puan):
        self.cursor.execute("SELECT * FROM degerlendirmeler WHERE kullanici_id=? AND tarif_id=?", (k_id, t_id))
        if self.cursor.fetchone(): return False, "Bu tarifi zaten değerlendirdiniz!"
        
        self.cursor.execute("INSERT INTO degerlendirmeler (kullanici_id, tarif_id, puan) VALUES (?, ?, ?)", (k_id, t_id, puan))
        self.conn.commit(); return True, "Değerlendirme kaydedildi."

    # --- VERİ SİLME İŞLEMLERİ ---
    def db_kayit_sil(self, tablo, kosul_sutunu, kosul_degeri):
        try:
            if tablo == 'tarifler':
                self.cursor.execute("DELETE FROM malzemeler WHERE tarif_id=?", (kosul_degeri,))
                self.cursor.execute("DELETE FROM degerlendirmeler WHERE tarif_id=?", (kosul_degeri,))
            elif tablo == 'kullanicilar':
                self.cursor.execute("DELETE FROM degerlendirmeler WHERE kullanici_id=?", (kosul_degeri,))

            self.cursor.execute(f"DELETE FROM {tablo} WHERE {kosul_sutunu} = ?", (kosul_degeri,))
            self.conn.commit()
            return True, "Kayıt başarıyla silindi."
        except Exception as e:
            return False, str(e)

    # --- VERİ ÇEKME İŞLEMLERİ ---
    def verileri_getir(self, tablo): return self.cursor.execute(f"SELECT * FROM {tablo}").fetchall()
    
    def malzemeleri_getir(self, t_id): 
        return self.cursor.execute("SELECT id, malzeme_adi, miktar FROM malzemeler WHERE tarif_id=?", (t_id,)).fetchall()
    
    def istatistikleri_getir(self):
        return {
            'tarif': self.cursor.execute("SELECT COUNT(*) FROM tarifler").fetchone()[0],
            'kullanici': self.cursor.execute("SELECT COUNT(*) FROM kullanicilar").fetchone()[0],
            'yorum': self.cursor.execute("SELECT COUNT(*) FROM degerlendirmeler").fetchone()[0]
        }
        
    def detayli_yorumları_getir(self):
        sorgu = """
        SELECT d.id, k.ad, t.tarif_adi, d.puan 
        FROM degerlendirmeler d
        JOIN kullanicilar k ON d.kullanici_id = k.kullanici_id
        JOIN tarifler t ON d.tarif_id = t.tarif_id
        ORDER BY d.id DESC
        """
        return self.cursor.execute(sorgu).fetchall()

# ================= PROJE 6: İSTENEN SINIFLAR =================
class Malzeme:
    def __init__(self, malzeme_adi, miktar):
        self.malzeme_adi = malzeme_adi
        self.miktar = miktar

class Tarif:
    def __init__(self, tarif_id, tarif_adi, kategori, hazirlama_suresi):
        self.tarif_id = tarif_id
        self.tarif_adi = tarif_adi
        self.kategori = kategori
        self.hazirlama_suresi = hazirlama_suresi

    def tarif_ekle(self, db_manager):
        return db_manager.db_tarif_ekle(self.tarif_adi, self.kategori, self.hazirlama_suresi)

    def tarif_guncelle(self, db_manager, yeni_ad, yeni_kat, yeni_sure):
        return db_manager.db_tarif_guncelle(self.tarif_id, yeni_ad, yeni_kat, yeni_sure)

class Kullanici:
    def __init__(self, kullanici_id, ad):
        self.kullanici_id = kullanici_id
        self.ad = ad

    def tarif_degerlendir(self, db_manager, tarif_id, puan):
        return db_manager.db_degerlendirme_ekle(self.kullanici_id, tarif_id, puan)

# ================= ANA ARAYÜZ =================
class YemekTarifApp(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color=COLORS["bg_main"], corner_radius=0, **kwargs)
        self.db = TarifVeritabani()
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.pack(fill="both", expand=True)
        
        self.font_logo = ctk.CTkFont(family="Segoe UI", size=24, weight="bold")
        self.font_title = ctk.CTkFont(family="Segoe UI", size=24, weight="bold")
        self.font_nav = ctk.CTkFont(family="Segoe UI", size=15, weight="bold")
        self.font_h2 = ctk.CTkFont(family="Segoe UI", size=18, weight="bold")
        self.font_label = ctk.CTkFont(family="Segoe UI", size=13)
        self.font_normal = ctk.CTkFont(family="Segoe UI", size=13)
        
        self._setup_tree_style()
        self._build_sidebar()
        self._build_main_area()
        self._verileri_guncelle()

        self.after(150, lambda: self.select_tab("Ana Sayfa"))

    def _setup_tree_style(self):
        style = ttk.Style()
        style.theme_use("default") 
        style.configure("Treeview", background=COLORS["bg_surface"], foreground=COLORS["text_main"],
                        fieldbackground=COLORS["bg_surface"], rowheight=45, borderwidth=0, font=("Segoe UI", 11))
        style.configure("Treeview.Heading", background=COLORS["bg_card"], foreground=COLORS["text_muted"], 
                        font=("Segoe UI", 12, "bold"), borderwidth=0, padding=8)
        style.map('Treeview', background=[('selected', COLORS["primary"])])
        style.layout("Treeview", [('Treeview.treearea', {'sticky': 'nswe'})]) 

    def _build_sidebar(self):
        self.sidebar_frame = ctk.CTkFrame(self, fg_color=COLORS["bg_surface"], corner_radius=0, width=280)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(7, weight=1)

        logo_frame = ctk.CTkFrame(self.sidebar_frame, fg_color="transparent")
        logo_frame.grid(row=0, column=0, padx=20, pady=(30, 40), sticky="ew")
        ctk.CTkLabel(logo_frame, text="🍲 Yemek Tarifleri", font=self.font_logo, text_color=COLORS["primary"]).pack(anchor="center")
        ctk.CTkLabel(logo_frame, text="Yönetim Paneli", font=self.font_label, text_color=COLORS["text_muted"]).pack(anchor="center")

        self.active_indicator = ctk.CTkFrame(self.sidebar_frame, width=5, height=45, fg_color=COLORS["primary"], corner_radius=3)
        self.active_indicator.place(x=5, y=-100)

        self.nav_buttons = {}
        menus = [
            ("📊", "Ana Sayfa"),
            ("📝", "Tarif Yönetimi"),
            ("👤", "Kullanıcı Yönetimi"),
            ("⭐", "Değerlendirmeler")
        ]

        def on_enter(e, b_name):
            if self.page_title.cget("text") != b_name.upper():
                self.nav_buttons[b_name].configure(text_color=COLORS["text_main"])

        def on_leave(e, b_name):
            if self.page_title.cget("text") != b_name.upper():
                self.nav_buttons[b_name].configure(text_color=COLORS["text_muted"])

        for i, (icon, name) in enumerate(menus):
            btn = ctk.CTkButton(
                self.sidebar_frame, text=f"  {icon}   {name}", font=self.font_nav, anchor="w",
                fg_color="transparent", text_color=COLORS["text_muted"], hover_color=COLORS["bg_card"],
                corner_radius=10, height=45, command=lambda n=name: self.select_tab(n)
            )
            btn.grid(row=i+1, column=0, padx=20, pady=4, sticky="ew")
            btn.bind("<Enter>", lambda e, n=name: on_enter(e, n))
            btn.bind("<Leave>", lambda e, n=name: on_leave(e, n))
            self.nav_buttons[name] = btn

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

    def _build_main_area(self):
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=35, pady=25)
        self.main_frame.grid_rowconfigure(1, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

        header_f = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        header_f.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        
        self.page_title = ctk.CTkLabel(header_f, text="DASHBOARD", font=self.font_title, text_color=COLORS["text_main"])
        self.page_title.pack(side="left")
        
        tarih = datetime.now().strftime("%d %B %Y")
        ctk.CTkLabel(header_f, text=f"📅 {tarih}", font=self.font_label, text_color=COLORS["text_muted"]).pack(side="right", padx=10)

        self.content_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.content_frame.grid(row=1, column=0, sticky="nsew")
        
        self.pages = {}
        self._page_anasayfa()
        self._page_tarif_yonetimi()
        self._page_kullanici_yonetimi()
        self._page_degerlendirmeler()

    def select_tab(self, name):
        for btn_name, btn in self.nav_buttons.items():
            if btn_name == name:
                btn.configure(fg_color=COLORS["bg_card"], text_color=COLORS["primary"])
                self._safe_animate_indicator(btn)
            else:
                btn.configure(fg_color="transparent", text_color=COLORS["text_muted"])

        self.page_title.configure(text=name.upper())

        for page_name, page in self.pages.items():
            if page_name == name: page.pack(fill="both", expand=True)
            else: page.pack_forget()
            
        self._verileri_guncelle()

    def _create_input(self, parent, placeholder):
        ent = ctk.CTkEntry(parent, placeholder_text=placeholder, font=self.font_normal, height=45, 
                           fg_color=COLORS["bg_main"], border_color=COLORS["border"], corner_radius=10)
        ent.pack(fill="x", pady=8, padx=2)
        ent.bind("<Enter>", lambda e: ent.configure(border_color=COLORS["primary"]))
        ent.bind("<Leave>", lambda e: ent.configure(border_color=COLORS["border"]))
        return ent

    def _create_tree(self, parent, cols):
        f = ctk.CTkFrame(parent, fg_color="transparent")
        f.pack(fill="both", expand=True, pady=10)
        scroll = ctk.CTkScrollbar(f, orientation="vertical", width=12)
        scroll.pack(side="right", fill="y")
        tree = ttk.Treeview(f, columns=cols, show="headings", yscrollcommand=scroll.set)
        tree.pack(side="left", fill="both", expand=True)
        scroll.configure(command=tree.yview)
        for c in cols: tree.heading(c, text=c); tree.column(c, anchor="center")
        return tree

    # ================= SAYFALAR =================
    def _page_anasayfa(self):
        page = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        self.pages["Ana Sayfa"] = page
        
        grid_f = ctk.CTkFrame(page, fg_color="transparent")
        grid_f.pack(fill="x", pady=(0, 20))
        grid_f.grid_columnconfigure((0,1,2), weight=1, uniform="col")

        self.stat_lbls = {}
        stats = [("📜 Sistemdeki Tarif", "tarif"), ("👤 Kayıtlı Kullanıcı", "kullanici"), ("⭐ Toplam Değerlendirme", "yorum")]
        
        for i, (title, key) in enumerate(stats):
            card = ctk.CTkFrame(grid_f, fg_color=COLORS["bg_surface"], corner_radius=15, border_width=1, border_color=COLORS["border"])
            card.grid(row=0, column=i, padx=10, sticky="nsew")
            
            ctk.CTkLabel(card, text=title, font=self.font_h2, text_color=COLORS["text_muted"]).pack(pady=(25, 5))
            
            ana_lbl = ctk.CTkLabel(card, text="0", font=ctk.CTkFont(size=54, weight="bold"), text_color=COLORS["primary"])
            ana_lbl.pack(pady=(0, 10))
            
            scroll_f = ctk.CTkScrollableFrame(card, fg_color="transparent", height=150)
            scroll_f.pack(fill="both", expand=True, padx=10, pady=(0, 20))
            
            detay_lbl = ctk.CTkLabel(scroll_f, text="-", font=ctk.CTkFont(size=13, weight="bold"), text_color=COLORS["text_main"], justify="center")
            detay_lbl.pack(expand=True)
            
            self.stat_lbls[key] = (ana_lbl, detay_lbl) 

    # ---> YENİDEN TASARLANAN TARİF VE MALZEME SAYFASI <---
    def _page_tarif_yonetimi(self):
        page = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        self.pages["Tarif Yönetimi"] = page
        
        left_pane = ctk.CTkFrame(page, fg_color="transparent")
        left_pane.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        right_pane = ctk.CTkFrame(page, fg_color="transparent")
        right_pane.pack(side="right", fill="both", expand=True, padx=(10, 0))

        # ---- SOL PANEL: TARİF YÖNETİMİ ----
        tarif_form_f = ctk.CTkFrame(left_pane, fg_color=COLORS["bg_surface"], corner_radius=15)
        tarif_form_f.pack(fill="x", pady=(0, 15), ipadx=15, ipady=15)
        ctk.CTkLabel(tarif_form_f, text="📝 Tarif Formu", font=self.font_h2, text_color=COLORS["primary"]).pack(anchor="w", pady=(5,15))
        
        self.ent_t_ad = self._create_input(tarif_form_f, "Tarif Adı")
        self.ent_t_kat = self._create_input(tarif_form_f, "Kategori (Örn: Çorba)")
        self.ent_t_sure = self._create_input(tarif_form_f, "Hazırlama Süresi (Sadece Dakika)")
        
        t_btn_f = ctk.CTkFrame(tarif_form_f, fg_color="transparent")
        t_btn_f.pack(fill="x", pady=(10,0))
        ctk.CTkButton(t_btn_f, text="Yeni Ekle", fg_color=COLORS["success"], height=40, command=self._islem_tarif_ekle).pack(side="left", expand=True, padx=2)
        ctk.CTkButton(t_btn_f, text="Güncelle", fg_color=COLORS["warning"], text_color="black", height=40, command=self._islem_tarif_guncelle).pack(side="right", expand=True, padx=2)

        tarif_list_f = ctk.CTkFrame(left_pane, fg_color=COLORS["bg_surface"], corner_radius=15)
        tarif_list_f.pack(fill="both", expand=True, ipadx=15, ipady=15)
        ctk.CTkLabel(tarif_list_f, text="Mevcut Tarifler (Malzeme Listesi için Seçin)", font=self.font_h2).pack(anchor="w")
        
        self.tree_tarif = self._create_tree(tarif_list_f, ("ID", "Tarif Adı", "Kategori", "Süre"))
        self.tree_tarif.column("ID", width=40)
        self.tree_tarif.bind("<<TreeviewSelect>>", self._tarif_detay_goster)
        
        ctk.CTkButton(tarif_list_f, text="🗑️ Seçili Tarifi Sil", fg_color=COLORS["danger"], hover_color=COLORS["danger_hover"], height=40, command=self._islem_tarif_sil).pack(fill="x", pady=(10,0))

        # ---- SAĞ PANEL: MALZEME YÖNETİMİ ----
        self.malzeme_pane = ctk.CTkFrame(right_pane, fg_color=COLORS["bg_surface"], corner_radius=15)
        self.malzeme_pane.pack(fill="both", expand=True, ipadx=15, ipady=15)
        
        # Başlangıçta tarif seçilmediği için görünen mesaj
        self.lbl_secili_tarif = ctk.CTkLabel(self.malzeme_pane, text="👈 Malzeme Ekle/Çıkar İşlemleri İçin\nSoldan Bir Tarif Seçin.", font=self.font_h2, text_color=COLORS["text_muted"])
        self.lbl_secili_tarif.pack(expand=True)
        
        # Tarif seçilince görünecek asıl içerik
        self.malzeme_icerik = ctk.CTkFrame(self.malzeme_pane, fg_color="transparent")
        
        self.lbl_malzeme_baslik = ctk.CTkLabel(self.malzeme_icerik, text="Malzemeler", font=self.font_h2, text_color=COLORS["text_main"])
        self.lbl_malzeme_baslik.pack(anchor="w", pady=(0, 10))

        self.tree_malzeme = self._create_tree(self.malzeme_icerik, ("ID", "Malzeme Adı", "Miktar"))
        self.tree_malzeme.column("ID", width=40)

        # MALZEME EKLE / ÇIKAR ALANI 
        m_action_f = ctk.CTkFrame(self.malzeme_icerik, fg_color="transparent")
        m_action_f.pack(fill="x", pady=(10,0))
        
        self.ent_m_ad = ctk.CTkEntry(m_action_f, placeholder_text="Malzeme Adı", height=40, width=170, fg_color=COLORS["bg_main"], border_color=COLORS["border"], corner_radius=8)
        self.ent_m_ad.pack(side="left", padx=(0,5))
        
        self.ent_m_mik = ctk.CTkEntry(m_action_f, placeholder_text="Miktar", height=40, width=100, fg_color=COLORS["bg_main"], border_color=COLORS["border"], corner_radius=8)
        self.ent_m_mik.pack(side="left", padx=(0,10))
        
        ctk.CTkButton(m_action_f, text="➕ Ekle", fg_color=COLORS["success"], height=40, width=80, command=self._islem_malzeme_ekle).pack(side="left", padx=(0, 5))
        ctk.CTkButton(m_action_f, text="🗑️ Çıkar", fg_color=COLORS["danger"], hover_color=COLORS["danger_hover"], height=40, width=80, command=self._islem_malzeme_sil).pack(side="left")

        self.secili_tarif_id = None

    def _tarif_detay_goster(self, event):
        secili = self.tree_tarif.selection()
        if not secili: return
        
        item = self.tree_tarif.item(secili[0])['values']
        self.secili_tarif_id = item[0]
        tarif_adi = item[1]
        
        # Formu otomatik doldur (Güncelleme işlemi için kolaylık)
        self.ent_t_ad.delete(0, 'end'); self.ent_t_ad.insert(0, tarif_adi)
        self.ent_t_kat.delete(0, 'end'); self.ent_t_kat.insert(0, item[2])
        self.ent_t_sure.delete(0, 'end'); self.ent_t_sure.insert(0, str(item[3]).replace(" dk", ""))

        # Sağ tarafta malzemeleri aç
        self.lbl_secili_tarif.pack_forget()
        self.malzeme_icerik.pack(fill="both", expand=True)
        self.lbl_malzeme_baslik.configure(text=f"📋 {tarif_adi} Malzemeleri")
        
        self._malzemeleri_listele(self.secili_tarif_id)

    def _malzemeleri_listele(self, t_id):
        for r in self.tree_malzeme.get_children(): self.tree_malzeme.delete(r)
        malzemeler = self.db.malzemeleri_getir(t_id)
        for m in malzemeler: self.tree_malzeme.insert("", "end", values=(m[0], m[1], m[2]))

    def _page_kullanici_yonetimi(self):
        page = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        self.pages["Kullanıcı Yönetimi"] = page

        form_f = ctk.CTkFrame(page, fg_color=COLORS["bg_surface"], corner_radius=15, width=400)
        form_f.pack(side="left", fill="y", padx=(0, 20), ipadx=15, ipady=15)
        form_f.pack_propagate(False)
        
        ctk.CTkLabel(form_f, text="👤 Kullanıcı Kaydı", font=self.font_h2).pack(pady=(5,15))
        self.ent_k_ad = self._create_input(form_f, "Kullanıcı Adı") 
        ctk.CTkButton(form_f, text="Kullanıcı Ekle", fg_color=COLORS["primary"], hover_color=COLORS["primary_hover"], height=45, font=self.font_nav, command=self._islem_kullanici_ekle).pack(fill="x", pady=20)

        list_f = ctk.CTkFrame(page, fg_color=COLORS["bg_surface"], corner_radius=15)
        list_f.pack(side="right", fill="both", expand=True, ipadx=15, ipady=15)
        ctk.CTkLabel(list_f, text="Sistemdeki Tüm Kullanıcılar", font=self.font_h2).pack(anchor="w")
        self.tree_kullanici = self._create_tree(list_f, ("Kullanıcı ID", "Ad"))
        self.tree_kullanici.column("Kullanıcı ID", width=100, anchor="center")
        
        f = ctk.CTkFrame(list_f, fg_color="transparent")
        f.pack(side="bottom", fill="x", pady=(0, 10))
        ctk.CTkButton(f, text="❌ Seçili Kullanıcıyı Sil", fg_color=COLORS["danger"], hover_color=COLORS["danger_hover"], height=40, width=200, font=ctk.CTkFont(size=14, weight="bold"), command=self._islem_kullanici_sil).pack(side="right")

    def _page_degerlendirmeler(self):
        page = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        self.pages["Değerlendirmeler"] = page

        form_f = ctk.CTkFrame(page, fg_color=COLORS["bg_surface"], corner_radius=15, width=400)
        form_f.pack(side="left", fill="y", padx=(0, 20), ipadx=15, ipady=15)
        form_f.pack_propagate(False)

        ctk.CTkLabel(form_f, text="⭐ Tarif Puanla", font=self.font_h2).pack(pady=(5,15))
        
        self.cmb_puan_kull = ctk.CTkComboBox(form_f, values=[], height=45, fg_color=COLORS["bg_main"], border_color=COLORS["border"])
        self.cmb_puan_kull.pack(fill="x", pady=10)
        self.cmb_puan_kull.set("Kullanıcı Seçin")

        self.cmb_puan_tarif = ctk.CTkComboBox(form_f, values=[], height=45, fg_color=COLORS["bg_main"], border_color=COLORS["border"])
        self.cmb_puan_tarif.pack(fill="x", pady=10)
        self.cmb_puan_tarif.set("Tarif Seçin")

        self.ent_puan = self._create_input(form_f, "Puan (1-5 Arası)")
        ctk.CTkButton(form_f, text="Puanı Gönder", fg_color=COLORS["success"], height=45, font=self.font_nav, command=self._islem_puan_ekle).pack(fill="x", pady=20)

        list_f = ctk.CTkFrame(page, fg_color=COLORS["bg_surface"], corner_radius=15)
        list_f.pack(side="right", fill="both", expand=True, ipadx=15, ipady=15)
        ctk.CTkLabel(list_f, text="Son Değerlendirmeler", font=self.font_h2).pack(anchor="w")
        self.tree_yorum = self._create_tree(list_f, ("ID", "Kullanıcı", "Tarif", "Puan"))
        self.tree_yorum.column("ID", width=40)
        
        f = ctk.CTkFrame(list_f, fg_color="transparent")
        f.pack(side="bottom", fill="x", pady=(0, 10))
        ctk.CTkButton(f, text="❌ Seçili Puanı Sil", fg_color=COLORS["danger"], hover_color=COLORS["danger_hover"], height=40, width=200, font=ctk.CTkFont(size=14, weight="bold"), command=self._islem_degerlendirme_sil).pack(side="right")


    # ================= İŞLEMLER VE OOP BAĞLANTISI =================
    def _verileri_guncelle(self):
        stats = self.db.istatistikleri_getir()
        tarifler_db = self.db.verileri_getir("tarifler")
        kull_db = self.db.verileri_getir("kullanicilar")
        yorumlar = self.db.detayli_yorumları_getir()

        tarif_detay = "\n".join([t[1] for t in tarifler_db])
        kull_detay = "\n".join([k[1] for k in kull_db])
        yorum_detay = "\n".join([f"{y[1]} - {y[3]}⭐" for y in yorumlar])

        detaylar_dict = {
            'tarif': tarif_detay if tarif_detay else "Kayıt Yok",
            'kullanici': kull_detay if kull_detay else "Kayıt Yok",
            'yorum': yorum_detay if yorum_detay else "Kayıt Yok"
        }

        for k, v in stats.items():
            if k in self.stat_lbls:
                ana_lbl, detay_lbl = self.stat_lbls[k]
                ana_lbl.configure(text=str(v))
                detay_lbl.configure(text=detaylar_dict[k])

        def tabloyu_doldur(tree, veri_listesi):
            for r in tree.get_children(): tree.delete(r)
            for v in veri_listesi: tree.insert("", "end", values=v)

        tabloyu_doldur(self.tree_tarif, [(t[0], t[1], t[2], f"{t[3]} dk") for t in tarifler_db])
        tabloyu_doldur(self.tree_kullanici, [(k[0], k[1]) for k in kull_db])

        yildizli_yorumlar = [(y[0], y[1], y[2], "⭐" * y[3]) for y in yorumlar]
        tabloyu_doldur(self.tree_yorum, yildizli_yorumlar)

        self.cmb_puan_kull.configure(values=[f"{k[0]} - {k[1]}" for k in kull_db])
        self.cmb_puan_tarif.configure(values=[f"{t[0]} - {t[1]}" for t in tarifler_db])

    def _isim_mi(self, metin):
        if not metin: return False
        return not any(char.isdigit() for char in metin)

    def _islem_tarif_ekle(self):
        ad = self.ent_t_ad.get().strip()
        kat = self.ent_t_kat.get().strip()
        sure_str = self.ent_t_sure.get().strip()

        if not ad or not kat or not sure_str: return messagebox.showwarning("Eksik", "Tüm alanları doldurun!")
        if not self._isim_mi(ad): return messagebox.showwarning("Hata", "Tarif adı rakam içeremez!")
        if not self._isim_mi(kat): return messagebox.showwarning("Hata", "Kategori rakam içeremez!")
        if not sure_str.isdigit(): return messagebox.showwarning("Hata", "Süre sadece rakamlardan oluşmalıdır!")

        yeni_tarif = Tarif(None, ad, kat, int(sure_str)) 
        basarili, mesaj = yeni_tarif.tarif_ekle(self.db)
        
        if basarili:
            self._verileri_guncelle()
            self.ent_t_ad.delete(0, 'end'); self.ent_t_kat.delete(0, 'end'); self.ent_t_sure.delete(0, 'end')
        else: messagebox.showerror("Hata", mesaj)

    def _islem_tarif_guncelle(self):
        if not self.secili_tarif_id:
            return messagebox.showwarning("Uyarı", "Lütfen önce tablodan güncellenecek tarifi seçin!")
            
        ad = self.ent_t_ad.get().strip()
        kat = self.ent_t_kat.get().strip()
        sure_str = self.ent_t_sure.get().strip()

        if not ad or not kat or not sure_str: return messagebox.showwarning("Eksik", "Tüm alanları doldurun!")
        if not self._isim_mi(ad): return messagebox.showwarning("Hata", "Tarif adı rakam içeremez!")
        if not self._isim_mi(kat): return messagebox.showwarning("Hata", "Kategori rakam içeremez!")
        if not sure_str.isdigit(): return messagebox.showwarning("Hata", "Süre sadece rakamlardan oluşmalıdır!")

        secili_tarif = Tarif(self.secili_tarif_id, ad, kat, int(sure_str))
        basarili, mesaj = secili_tarif.tarif_guncelle(self.db, ad, kat, int(sure_str))
        
        if basarili:
            self._verileri_guncelle()
            messagebox.showinfo("Başarılı", mesaj)
        else: messagebox.showerror("Hata", mesaj)

    def _islem_kullanici_ekle(self):
        ad = self.ent_k_ad.get().strip()
        if not ad: return messagebox.showwarning("Eksik", "Ad alanı zorunludur!")
        if not self._isim_mi(ad): return messagebox.showwarning("Hata", "İsim rakam içeremez!")

        ok, msg = self.db.db_kullanici_ekle(ad)
        if ok:
            self._verileri_guncelle()
            self.ent_k_ad.delete(0, 'end')
        else: messagebox.showerror("Hata", msg)

    def _islem_malzeme_ekle(self):
        if not self.secili_tarif_id: return messagebox.showwarning("Uyarı", "Lütfen önce tablodan bir tarif seçin!")
        
        ad = self.ent_m_ad.get().strip()
        mik = self.ent_m_mik.get().strip()
        
        if not ad or not mik: return messagebox.showwarning("Eksik", "Malzeme adı ve miktarı giriniz!")
        if not self._isim_mi(ad): return messagebox.showwarning("Hata", "Malzeme adı rakam içeremez!")
        
        yeni_malzeme = Malzeme(ad, mik)
        ok, msg = self.db.db_malzeme_ekle(self.secili_tarif_id, yeni_malzeme.malzeme_adi, yeni_malzeme.miktar)
        
        if ok:
            self._malzemeleri_listele(self.secili_tarif_id)
            self.ent_m_ad.delete(0, 'end'); self.ent_m_mik.delete(0, 'end')
        else: messagebox.showerror("Hata", msg)

    def _islem_puan_ekle(self):
        kull_secim = self.cmb_puan_kull.get()
        tarif_secim = self.cmb_puan_tarif.get()
        puan_str = self.ent_puan.get().strip()

        if "Seçin" in kull_secim or "Seçin" in tarif_secim or not puan_str:
            return messagebox.showwarning("Eksik", "Lütfen tüm seçimleri ve puanı eksiksiz doldurun.")
        if not puan_str.isdigit() or not (1 <= int(puan_str) <= 5):
            return messagebox.showwarning("Hata", "Puan sadece 1 ile 5 arasında bir rakam olmalıdır!")

        k_id = int(kull_secim.split(" - ")[0])
        t_id = int(tarif_secim.split(" - ")[0])
        puan = int(puan_str)

        aktif_kullanici = Kullanici(k_id, kull_secim.split(" - ")[1])
        basarili, msg = aktif_kullanici.tarif_degerlendir(self.db, t_id, puan)
        
        if basarili:
            self._verileri_guncelle()
            self.ent_puan.delete(0, 'end')
            messagebox.showinfo("Başarılı", msg)
        else: messagebox.showerror("Hata", msg)

    # --- SİLME İŞLEMLERİ ---
    def _islem_tarif_sil(self):
        secili = self.tree_tarif.selection()
        if not secili: return messagebox.showwarning("Uyarı", "Lütfen tablodan silinecek tarifi seçin!")
        
        t_id = self.tree_tarif.item(secili[0])['values'][0]
        t_ad = self.tree_tarif.item(secili[0])['values'][1]
        
        if messagebox.askyesno("Tarif Sil", f"'{t_ad}' tarifi silinecek.\nBuna bağlı tüm malzemeler ve puanlamalar da silinir. Onaylıyor musunuz?"):
            ok, msg = self.db.db_kayit_sil("tarifler", "tarif_id", t_id)
            if ok:
                self._verileri_guncelle()
                if self.secili_tarif_id == t_id:
                    self.secili_tarif_id = None
                    self.malzeme_icerik.pack_forget()
                    self.lbl_secili_tarif.pack(expand=True)
                messagebox.showinfo("Başarılı", msg)
            else: messagebox.showerror("Hata", msg)

    def _islem_malzeme_sil(self):
        secili = self.tree_malzeme.selection()
        if not secili: return messagebox.showwarning("Uyarı", "Lütfen tablodan çıkarılacak malzemeyi seçin!")
        
        m_id = self.tree_malzeme.item(secili[0])['values'][0]
        if messagebox.askyesno("Malzeme Çıkar", "Seçili malzeme bu tariften çıkarılacak. Onaylıyor musunuz?"):
            ok, msg = self.db.db_kayit_sil("malzemeler", "id", m_id)
            if ok:
                self._malzemeleri_listele(self.secili_tarif_id)
            else: messagebox.showerror("Hata", msg)

    def _islem_kullanici_sil(self):
        secili = self.tree_kullanici.selection()
        if not secili: return messagebox.showwarning("Uyarı", "Lütfen tablodan bir kullanıcı seçin!")
        
        k_id = self.tree_kullanici.item(secili[0])['values'][0]
        k_ad = self.tree_kullanici.item(secili[0])['values'][1]
        
        if messagebox.askyesno("Kullanıcı Sil", f"'{k_ad}' kullanıcısı ve yaptığı tüm puanlamalar silinecek. Onaylıyor musunuz?"):
            ok, msg = self.db.db_kayit_sil("kullanicilar", "kullanici_id", k_id)
            if ok:
                self._verileri_guncelle()
                messagebox.showinfo("Başarılı", msg)
            else: messagebox.showerror("Hata", msg)

    def _islem_degerlendirme_sil(self):
        secili = self.tree_yorum.selection()
        if not secili: return messagebox.showwarning("Uyarı", "Lütfen tablodan bir değerlendirme seçin!")
        
        d_id = self.tree_yorum.item(secili[0])['values'][0]
        if messagebox.askyesno("Puan Sil", "Bu değerlendirme kalıcı olarak silinecek. Onaylıyor musunuz?"):
            ok, msg = self.db.db_kayit_sil("degerlendirmeler", "id", d_id)
            if ok:
                self._verileri_guncelle()
            else: messagebox.showerror("Hata", msg)


# ================= UYGULAMA ÇALIŞTIRICI =================
if __name__ == "__main__":
    app = ctk.CTk()
    app.title("Yemek Tarif Platformu v5.0")
    app.geometry("1400x850")
    app.minsize(1200, 750)
    YemekTarifApp(app)
    app.mainloop()