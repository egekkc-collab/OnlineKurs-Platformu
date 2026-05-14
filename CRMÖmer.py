import sys
import sqlite3
import random
from datetime import datetime

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton, QTableWidget, QTableWidgetItem,
    QStackedWidget, QSpinBox, QMessageBox, QLabel, QComboBox,
    QHeaderView, QFrame, QGraphicsDropShadowEffect
)
from PyQt5.QtGui import QFont, QColor, QIcon
from PyQt5.QtCore import Qt, QSize

# ==========================================================
# DATABASE (Mantık Aynı Kaldı)
# ==========================================================
class CRMVeritabani:
    def __init__(self):
        self.conn = sqlite3.connect("crm_final.db")
        self.cursor = self.conn.cursor()
        self.tablolar()
        self.ornek_veri()

    def tablolar(self):
        self.cursor.execute("CREATE TABLE IF NOT EXISTS musteriler(id INTEGER PRIMARY KEY AUTOINCREMENT, ad TEXT, soyad TEXT, tel TEXT UNIQUE, sehir TEXT)")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS stok(id INTEGER PRIMARY KEY AUTOINCREMENT, urun TEXT, miktar INTEGER, fiyat REAL)")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS satislar(id INTEGER PRIMARY KEY AUTOINCREMENT, musteri TEXT, urun TEXT, adet INTEGER, toplam REAL, tarih TEXT)")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS destek(id INTEGER PRIMARY KEY AUTOINCREMENT, musteri TEXT, aciklama TEXT, durum TEXT, tarih TEXT)")
        self.conn.commit()

    def ornek_veri(self):
        self.cursor.execute("SELECT COUNT(*) FROM musteriler")
        if self.cursor.fetchone()[0] == 0:
            adlar = ["Ali","Veli","Ayşe","Fatma","Murat","Can"]
            soyadlar = ["Yılmaz","Kaya","Demir","Çelik"]
            for _ in range(50):
                self.cursor.execute("INSERT INTO musteriler(ad,soyad,tel,sehir) VALUES (?,?,?,?)", 
                                   (random.choice(adlar), random.choice(soyadlar), f"05{random.randint(30,55)}{random.randint(10000000,99999999)}", "İstanbul"))
        
        self.cursor.execute("SELECT COUNT(*) FROM stok")
        if self.cursor.fetchone()[0] == 0:
            urunler = [("Motor Yağı",50,1450), ("Yağ Filtresi",80,250), ("Akü",20,2600), ("Lastik",60,3900)]
            self.cursor.executemany("INSERT INTO stok(urun,miktar,fiyat) VALUES (?,?,?)", urunler)
        self.conn.commit()

# ==========================================================
# MODERN UI COMPONENTS
# ==========================================================
class CRMApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db = CRMVeritabani()
        self.setWindowTitle("Apex CRM v2.0 - Dashboard")
        self.resize(1280, 850)

        # GENEL STİL (QSS)
        self.setStyleSheet("""
            QMainWindow { background-color: #F8FAFC; }
            
            /* Sidebar */
            #Sidebar { 
                background-color: #1E293B; 
                min-width: 220px; 
                max-width: 220px; 
            }
            
            #SideButton {
                background-color: transparent;
                color: #94A3B8;
                border: none;
                padding: 15px;
                text-align: left;
                font-size: 14px;
                font-weight: bold;
                border-radius: 8px;
                margin: 5px 10px;
            }
            #SideButton:hover { background-color: #334155; color: white; }
            #SideButton:checked { background-color: #2563EB; color: white; }

            /* Kart Yapısı */
            #ContentCard {
                background-color: white;
                border-radius: 12px;
                border: 1px solid #E2E8F0;
            }

            /* Tablo */
            QTableWidget {
                border: none;
                background-color: white;
                alternate-background-color: #F8FAFC;
                selection-background-color: #DBEAFE;
                selection-color: #2563EB;
            }
            QHeaderView::section {
                background-color: white;
                padding: 12px;
                border: none;
                border-bottom: 2px solid #E2E8F0;
                font-weight: bold;
                color: #64748B;
            }

            /* Giriş Alanları */
            QLineEdit, QComboBox, QSpinBox {
                border: 1px solid #E2E8F0;
                border-radius: 8px;
                padding: 10px;
                background: white;
            }
            QLineEdit:focus { border: 2px solid #2563EB; }

            /* Butonlar */
            #PrimaryBtn {
                background-color: #2563EB;
                color: white;
                font-weight: bold;
                border-radius: 8px;
                padding: 12px;
            }
            #PrimaryBtn:hover { background-color: #1D4ED8; }
            
            #DangerBtn {
                background-color: #EF4444;
                color: white;
                border-radius: 8px;
                padding: 12px;
            }
        """)

        self.init_ui()
        self.load_all()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # --- SIDEBAR ---
        sidebar = QFrame()
        sidebar.setObjectName("Sidebar")
        side_layout = QVBoxLayout(sidebar)
        
        logo = QLabel("APEX CRM")
        logo.setStyleSheet("color: white; font-size: 24px; font-weight: 900; margin: 20px 10px;")
        side_layout.addWidget(logo)

        self.btn_m = QPushButton(" Müşteriler"); self.btn_m.setCheckable(True); self.btn_m.setChecked(True)
        self.btn_s = QPushButton(" Stok Yönetimi"); self.btn_s.setCheckable(True)
        self.btn_sat = QPushButton(" Satış Paneli"); self.btn_sat.setCheckable(True)
        self.btn_sup = QPushButton(" Destek Merkezi"); self.btn_sup.setCheckable(True)

        for btn in [self.btn_m, self.btn_s, self.btn_sat, self.btn_sup]:
            btn.setObjectName("SideButton")
            btn.setCursor(Qt.PointingHandCursor)
            side_layout.addWidget(btn)
        
        side_layout.addStretch()
        
        # --- CONTENT AREA ---
        self.content_stack = QStackedWidget()
        
        # Sayfaları Tanımla
        self.page_customer = self.create_customer_page()
        self.page_stock = self.create_stock_page()
        self.page_sales = self.create_sales_page()
        self.page_support = self.create_support_page()

        self.content_stack.addWidget(self.page_customer)
        self.content_stack.addWidget(self.page_stock)
        self.content_stack.addWidget(self.page_sales)
        self.content_stack.addWidget(self.page_support)

        # Navigasyon Bağlantıları
        self.btn_m.clicked.connect(lambda: self.switch_page(0))
        self.btn_s.clicked.connect(lambda: self.switch_page(1))
        self.btn_sat.clicked.connect(lambda: self.switch_page(2))
        self.btn_sup.clicked.connect(lambda: self.switch_page(3))

        main_layout.addWidget(sidebar)
        main_layout.addWidget(self.content_stack)

    def switch_page(self, index):
        buttons = [self.btn_m, self.btn_s, self.btn_sat, self.btn_sup]
        for i, btn in enumerate(buttons):
            btn.setChecked(i == index)
        self.content_stack.setCurrentIndex(index)

    # ---------------- SAYFA TASARIMLARI ----------------

    def create_customer_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(30, 30, 30, 30)

        title = QLabel("Müşteri Veritabanı")
        title.setStyleSheet("font-size: 28px; font-weight: bold; color: #1E293B;")
        layout.addWidget(title)

        # Form Kartı
        form_card = QFrame(); form_card.setObjectName("ContentCard")
        form_layout = QHBoxLayout(form_card)
        
        self.ad = QLineEdit(); self.ad.setPlaceholderText("Ad")
        self.soyad = QLineEdit(); self.soyad.setPlaceholderText("Soyad")
        self.tel = QLineEdit(); self.tel.setPlaceholderText("Telefon (05xx)")
        
        btn_add = QPushButton("Müşteri Ekle"); btn_add.setObjectName("PrimaryBtn")
        btn_add.clicked.connect(self.add_customer)
        
        btn_del = QPushButton("Seçileni Sil"); btn_del.setObjectName("DangerBtn")
        btn_del.clicked.connect(self.del_customer)

        form_layout.addWidget(self.ad); form_layout.addWidget(self.soyad); form_layout.addWidget(self.tel)
        form_layout.addWidget(btn_add); form_layout.addWidget(btn_del)
        
        layout.addWidget(form_card)

        # Tablo
        self.tbl_m = QTableWidget()
        self.tbl_m.setColumnCount(4)
        self.tbl_m.setHorizontalHeaderLabels(["ID", "Ad", "Soyad", "Telefon"])
        self.tbl_m.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tbl_m.setColumnHidden(0, True)
        
        layout.addWidget(self.tbl_m)
        return page

    def create_stock_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(30,30,30,30)
        
        title = QLabel("Stok ve Envanter")
        title.setStyleSheet("font-size: 28px; font-weight: bold;")
        layout.addWidget(title)

        self.tbl_s = QTableWidget()
        self.tbl_s.setColumnCount(3)
        self.tbl_s.setHorizontalHeaderLabels(["Ürün Adı", "Stok Miktarı", "Birim Fiyat"])
        self.tbl_s.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        layout.addWidget(self.tbl_s)
        return page

    def create_sales_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(30,30,30,30)

        title = QLabel("Yeni Satış İşlemi")
        title.setStyleSheet("font-size: 28px; font-weight: bold;")
        layout.addWidget(title)

        form_card = QFrame(); form_card.setObjectName("ContentCard")
        form_lay = QHBoxLayout(form_card)
        
        self.cmb_m = QComboBox(); self.cmb_u = QComboBox()
        self.adet = QSpinBox(); self.adet.setRange(1, 500)
        btn_sell = QPushButton("Satışı Onayla"); btn_sell.setObjectName("PrimaryBtn")
        btn_sell.clicked.connect(self.sell)

        form_lay.addWidget(QLabel("Müşteri:"))
        form_lay.addWidget(self.cmb_m)
        form_lay.addWidget(QLabel("Ürün:"))
        form_lay.addWidget(self.cmb_u)
        form_lay.addWidget(QLabel("Adet:"))
        form_lay.addWidget(self.adet)
        form_lay.addWidget(btn_sell)

        layout.addWidget(form_card)

        self.tbl_sat = QTableWidget()
        self.tbl_sat.setColumnCount(5)
        self.tbl_sat.setHorizontalHeaderLabels(["Müşteri", "Ürün", "Adet", "Toplam", "Tarih"])
        self.tbl_sat.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.tbl_sat)
        
        return page

    def create_support_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(30,30,30,30)
        
        title = QLabel("Destek ve Talepler")
        title.setStyleSheet("font-size: 28px; font-weight: bold;")
        layout.addWidget(title)

        form_card = QFrame(); form_card.setObjectName("ContentCard")
        form_lay = QVBoxLayout(form_card)
        
        self.cmb_sup = QComboBox()
        self.txt_sup = QLineEdit(); self.txt_sup.setPlaceholderText("Sorun açıklaması...")
        btn_sup = QPushButton("Talep Oluştur"); btn_sup.setObjectName("PrimaryBtn")
        btn_sup.clicked.connect(self.add_support)

        form_lay.addWidget(self.cmb_sup); form_lay.addWidget(self.txt_sup); form_lay.addWidget(btn_sup)
        layout.addWidget(form_card)

        self.tbl_sup = QTableWidget()
        self.tbl_sup.setColumnCount(4)
        self.tbl_sup.setHorizontalHeaderLabels(["Müşteri", "Açıklama", "Durum", "Tarih"])
        self.tbl_sup.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.tbl_sup)
        
        return page

    # ---------------- FONKSİYONLAR (VERİ) ----------------

    def add_customer(self):
        if not self.ad.text().isalpha() or len(self.tel.text()) < 10:
            return QMessageBox.warning(self, "Hata", "Lütfen geçerli bilgiler girin!")
        
        self.db.cursor.execute("INSERT INTO musteriler(ad,soyad,tel,sehir) VALUES (?,?,?,?)", 
                             (self.ad.text(), self.soyad.text(), self.tel.text(), "İstanbul"))
        self.db.conn.commit()
        self.load_all()
        self.ad.clear(); self.soyad.clear(); self.tel.clear()

    def del_customer(self):
        r = self.tbl_m.currentRow()
        if r >= 0:
            cid = self.tbl_m.item(r, 0).text()
            self.db.cursor.execute("DELETE FROM musteriler WHERE id=?", (cid,))
            self.db.conn.commit()
            self.load_all()

    def sell(self):
        m = self.cmb_m.currentText()
        u = self.cmb_u.currentText()
        a = self.adet.value()
        self.db.cursor.execute("SELECT fiyat, miktar FROM stok WHERE urun=?", (u,))
        res = self.db.cursor.fetchone()
        if res and res[1] >= a:
            toplam = res[0] * a
            self.db.cursor.execute("INSERT INTO satislar VALUES(NULL,?,?,?,?,?)", (m, u, a, toplam, datetime.now().strftime("%d/%m/%Y")))
            self.db.cursor.execute("UPDATE stok SET miktar=miktar-? WHERE urun=?", (a, u))
            self.db.conn.commit()
            self.load_all()
            QMessageBox.information(self, "Başarılı", f"{toplam} TL tutarında satış yapıldı.")

    def add_support(self):
        if self.txt_sup.text():
            self.db.cursor.execute("INSERT INTO destek VALUES(NULL,?,?,?,?)", 
                                 (self.cmb_sup.currentText(), self.txt_sup.text(), "Açık", datetime.now().strftime("%d/%m/%Y")))
            self.db.conn.commit()
            self.load_all()
            self.txt_sup.clear()

    def load_all(self):
        # Müşteriler
        self.db.cursor.execute("SELECT id, ad, soyad, tel FROM musteriler ORDER BY id DESC")
        self.fill_table(self.tbl_m, self.db.cursor.fetchall())
        
        # Stok
        self.db.cursor.execute("SELECT urun, miktar, fiyat FROM stok")
        self.fill_table(self.tbl_s, self.db.cursor.fetchall())
        
        # Satışlar
        self.db.cursor.execute("SELECT musteri, urun, adet, toplam, tarih FROM satislar ORDER BY id DESC")
        self.fill_table(self.tbl_sat, self.db.cursor.fetchall())

        # Destek
        self.db.cursor.execute("SELECT musteri, aciklama, durum, tarih FROM destek ORDER BY id DESC")
        self.fill_table(self.tbl_sup, self.db.cursor.fetchall())

        # ComboBox Güncellemeleri
        self.cmb_m.clear(); self.cmb_sup.clear(); self.cmb_u.clear()
        self.db.cursor.execute("SELECT ad || ' ' || soyad FROM musteriler")
        musteriler = [r[0] for r in self.db.cursor.fetchall()]
        self.cmb_m.addItems(musteriler); self.cmb_sup.addItems(musteriler)
        
        self.db.cursor.execute("SELECT urun FROM stok")
        self.cmb_u.addItems([r[0] for r in self.db.cursor.fetchall()])

    def fill_table(self, table, data):
        table.setRowCount(0)
        for i, row in enumerate(data):
            table.insertRow(i)
            for j, val in enumerate(row):
                item = QTableWidgetItem(str(val))
                item.setTextAlignment(Qt.AlignCenter)
                table.setItem(i, j, item)

# ==========================================================
# RUN
# ==========================================================
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setFont(QFont("Segoe UI", 10))
    w = CRMApp()
    w.show()
    sys.exit(app.exec_())
