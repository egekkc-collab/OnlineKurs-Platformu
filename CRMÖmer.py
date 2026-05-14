import sys
import sqlite3
import random
from datetime import datetime

from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QTabWidget,
    QSpinBox,
    QMessageBox,
    QLabel,
    QComboBox,
    QHeaderView,
    QFrame
)

from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import Qt


# ==========================================================
# VERİTABANI
# ==========================================================
class CRMVeritabani:

    def __init__(self, db_adi="crm_mekanik_v12.db"):

        self.conn = sqlite3.connect(db_adi)
        self.cursor = self.conn.cursor()

        self.tablolari_olustur()
        self.verileri_yukle()

    # ==========================================================
    # TABLOLAR
    # ==========================================================
    def tablolari_olustur(self):

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS musteriler (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ad TEXT,
            soyad TEXT,
            tel TEXT UNIQUE,
            sehir TEXT
        )
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS stok (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            urun TEXT,
            miktar INTEGER,
            fiyat REAL
        )
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS satislar (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            m_tam_ad TEXT,
            u_ad TEXT,
            adet INTEGER,
            toplam REAL,
            tarih TEXT
        )
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS destek_talepleri (
            talep_id INTEGER PRIMARY KEY AUTOINCREMENT,
            m_tam_ad TEXT,
            aciklama TEXT,
            durum TEXT,
            tarih TEXT
        )
        """)

        self.conn.commit()

    # ==========================================================
    # ÖRNEK VERİLER
    # ==========================================================
    def verileri_yukle(self):

        self.cursor.execute("SELECT COUNT(*) FROM musteriler")

        if self.cursor.fetchone()[0] == 0:

            adlar = [
                "Ali", "Veli", "Ayşe", "Fatma", "Murat",
                "Gökhan", "Sibel", "Tülay", "Engin", "Serkan",
                "Burak", "Cem", "Derya", "Ebru", "Fatih",
                "Mehmet", "Can", "Hakan", "Oğuz", "Tolga",
                "Berk", "Yusuf", "Emre", "Kerem", "Samet",
                "Zeynep", "Elif", "Merve", "Gamze", "Buse",
                "Kaan", "Arda", "Onur", "Furkan", "Mete",
                "Deniz", "Aslı", "Naz", "İrem", "Sena",
                "Barış", "Uğur", "Levent", "Eren", "Doğukan",
                "Cansu", "Selin", "Nisa", "Ahmet", "Mustafa"
            ]

            soyadlar = [
                "Yılmaz", "Kaya", "Demir", "Çelik", "Şahin",
                "Öztürk", "Aras", "Kurt", "Aydın", "Koç",
                "Sarı", "Aksoy", "Yıldız", "Erdoğan", "Polat",
                "Bulut", "Aslan", "Kaplan", "Karaca", "Özdemir",
                "Çınar", "Taş", "Ekinci", "Bozkurt", "Keskin",
                "Tekin", "Avcı", "Kılıç", "Işık", "Duman",
                "Güneş", "Ergin", "Tunç", "Yavuz", "Korkmaz",
                "Akın", "Ateş", "Durmaz", "Karataş", "Eroğlu",
                "Özkan", "Sezer", "Kara", "Yücel", "Şimşek",
                "Acar", "Kocaman", "Türkmen", "Yalçın", "Doğan"
            ]

            sehirler = [
                "İstanbul",
                "Ankara",
                "İzmir",
                "Bursa",
                "Antalya"
            ]

            random.shuffle(adlar)
            random.shuffle(soyadlar)

            musteriler = []

            for i in range(50):

                tel = f"05{random.randint(30,55)}{random.randint(100,999)}{random.randint(10,99)}{random.randint(10,99)}"

                musteriler.append((
                    adlar[i],
                    soyadlar[i],
                    tel,
                    random.choice(sehirler)
                ))

            self.cursor.executemany("""
            INSERT OR IGNORE INTO musteriler
            (ad, soyad, tel, sehir)
            VALUES (?,?,?,?)
            """, musteriler)

        self.cursor.execute("SELECT COUNT(*) FROM stok")

        if self.cursor.fetchone()[0] == 0:

            stoklar = [

                ("Motor Yağı 5W-30", 50, 1450),
                ("Yağ Filtresi", 100, 250),
                ("Fren Balatası", 45, 950),
                ("Akü 72 Amper", 15, 2600),

                ("Hava Filtresi", 80, 300),
                ("Polen Filtresi", 60, 275),
                ("Far Ampulü", 120, 150),
                ("Triger Kayışı", 25, 1850),
                ("Debriyaj Seti", 18, 4200),
                ("Antifriz", 70, 450),
                ("Cam Suyu", 90, 120),
                ("Silecek Takımı", 55, 350),
                ("Lastik 17 İnç", 40, 3900),
                ("Jant Kapağı", 75, 200)

            ]

            self.cursor.executemany("""
            INSERT INTO stok
            (urun, miktar, fiyat)
            VALUES (?,?,?)
            """, stoklar)

        self.conn.commit()


# ==========================================================
# ANA UYGULAMA
# ==========================================================
class CRMApp(QMainWindow):

    def __init__(self):

        super().__init__()

        self.db = CRMVeritabani()

        self.setWindowTitle("MEKANİK CRM v12")
        self.resize(1300, 850)

        self.setStyleSheet("""

            QMainWindow {
                background-color: #f4f7f6;
            }

            QTabWidget::pane {
                border: 1px solid #d1d1d1;
                background: white;
                border-radius: 8px;
            }

            QTabBar::tab {
                background: #e2e2e2;
                padding: 15px 30px;
                font-weight: bold;
            }

            QTabBar::tab:selected {
                background: #2c3e50;
                color: white;
            }

            QPushButton {
                background-color: #3498db;
                color: white;
                border-radius: 5px;
                padding: 10px;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: #2980b9;
            }

            QLineEdit, QComboBox, QSpinBox {
                padding: 8px;
                border: 1px solid #bdc3c7;
                border-radius: 5px;
            }

            QHeaderView::section {
                background-color: #2c3e50;
                color: white;
                padding: 10px;
                font-weight: bold;
            }

        """)

        merkez = QWidget()
        self.setCentralWidget(merkez)

        self.ana_lay = QVBoxLayout(merkez)

        header = QFrame()

        h_lay = QHBoxLayout(header)

        title = QLabel("🛠️ MEKANİK CRM v12")
        title.setFont(QFont("Segoe UI", 16, QFont.Bold))

        h_lay.addWidget(title)

        self.ana_lay.addWidget(header)

        self.tabs = QTabWidget()

        self.ana_lay.addWidget(self.tabs)

        self.sayfa_m = QWidget()
        self.sayfa_s = QWidget()
        self.sayfa_satis = QWidget()
        self.sayfa_destek = QWidget()

        self.tabs.addTab(self.sayfa_m, "👥 MÜŞTERİLER")
        self.tabs.addTab(self.sayfa_s, "📦 STOK")
        self.tabs.addTab(self.sayfa_satis, "💰 SATIŞ")
        self.tabs.addTab(self.sayfa_destek, "🛠 DESTEK")

        self.m_paneli_kur()
        self.s_paneli_kur()
        self.satis_paneli_kur()
        self.destek_paneli_kur()

        self.m_listele()
        self.s_listele()
        self.satis_listele()
        self.destek_listele()

    # ==========================================================
    # MÜŞTERİ PANELİ
    # ==========================================================
    def m_paneli_kur(self):

        lay = QVBoxLayout(self.sayfa_m)

        frame = QFrame()

        f_lay = QHBoxLayout(frame)

        self.m_ad = QLineEdit()
        self.m_ad.setPlaceholderText("Ad")

        self.m_soyad = QLineEdit()
        self.m_soyad.setPlaceholderText("Soyad")

        self.m_tel = QLineEdit()
        self.m_tel.setPlaceholderText("Telefon")

        btn_ekle = QPushButton("👤 Müşteri Ekle")
        btn_ekle.setStyleSheet("background-color:#2ecc71;")
        btn_ekle.clicked.connect(self.m_ekle)

        btn_sil = QPushButton("🗑️ Sil")
        btn_sil.setStyleSheet("background-color:#e74c3c;")
        btn_sil.clicked.connect(self.m_sil)

        f_lay.addWidget(self.m_ad)
        f_lay.addWidget(self.m_soyad)
        f_lay.addWidget(self.m_tel)
        f_lay.addWidget(btn_ekle)
        f_lay.addWidget(btn_sil)

        lay.addWidget(frame)

        self.m_tablo = QTableWidget()

        self.m_tablo.setColumnCount(4)

        self.m_tablo.setHorizontalHeaderLabels([
            "ID",
            "Ad",
            "Soyad",
            "Telefon"
        ])

        self.m_tablo.setColumnHidden(0, True)

        self.m_tablo.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )

        lay.addWidget(self.m_tablo)

    # ==========================================================
    # STOK PANELİ
    # ==========================================================
    def s_paneli_kur(self):

        lay = QVBoxLayout(self.sayfa_s)

        btn_sil = QPushButton("🗑️ Ürün Sil")
        btn_sil.setStyleSheet("background-color:#e74c3c;")
        btn_sil.clicked.connect(self.stok_sil)

        lay.addWidget(btn_sil)

        self.s_tablo = QTableWidget()

        self.s_tablo.setColumnCount(3)

        self.s_tablo.setHorizontalHeaderLabels([
            "Ürün Adı",
            "Stok Miktarı",
            "Fiyat"
        ])

        self.s_tablo.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )

        lay.addWidget(self.s_tablo)

    # ==========================================================
    # SATIŞ PANELİ
    # ==========================================================
    def satis_paneli_kur(self):

        lay = QVBoxLayout(self.sayfa_satis)

        panel = QFrame()

        p_lay = QHBoxLayout(panel)

        self.c_m = QComboBox()
        self.c_u = QComboBox()

        self.s_adet = QSpinBox()
        self.s_adet.setRange(1, 100)

        btn = QPushButton("💸 Satış Yap")
        btn.clicked.connect(self.satis_yap)

        p_lay.addWidget(QLabel("Müşteri"))
        p_lay.addWidget(self.c_m)

        p_lay.addWidget(QLabel("Ürün"))
        p_lay.addWidget(self.c_u)

        p_lay.addWidget(QLabel("Adet"))
        p_lay.addWidget(self.s_adet)

        p_lay.addWidget(btn)

        lay.addWidget(panel)

        self.st_tablo = QTableWidget()

        self.st_tablo.setColumnCount(5)

        self.st_tablo.setHorizontalHeaderLabels([
            "Müşteri",
            "Ürün",
            "Adet",
            "Toplam",
            "Tarih"
        ])

        self.st_tablo.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )

        lay.addWidget(self.st_tablo)

    # ==========================================================
    # DESTEK PANELİ
    # ==========================================================
    def destek_paneli_kur(self):

        lay = QVBoxLayout(self.sayfa_destek)

        form = QHBoxLayout()

        self.c_m_destek = QComboBox()

        self.t_aciklama = QLineEdit()
        self.t_aciklama.setPlaceholderText("Şikayet / Talep")

        btn = QPushButton("🎫 Talep Aç")
        btn.clicked.connect(self.destek_ekle)

        form.addWidget(self.c_m_destek)
        form.addWidget(self.t_aciklama)
        form.addWidget(btn)

        lay.addLayout(form)

        self.d_tablo = QTableWidget()

        self.d_tablo.setColumnCount(5)

        self.d_tablo.setHorizontalHeaderLabels([
            "ID",
            "Müşteri",
            "Açıklama",
            "Durum",
            "Tarih"
        ])

        self.d_tablo.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )

        lay.addWidget(self.d_tablo)

    # ==========================================================
    # MÜŞTERİ EKLE
    # ==========================================================
    def m_ekle(self):

        ad = self.m_ad.text().strip()
        soyad = self.m_soyad.text().strip()
        tel = self.m_tel.text().strip()

        if not ad or not soyad or not tel:

            QMessageBox.warning(
                self,
                "Eksik Bilgi",
                "Tüm alanları doldurun!"
            )
            return

        if not ad.isalpha():

            QMessageBox.warning(
                self,
                "Hata",
                "Ad sadece harf içermelidir!"
            )
            return

        if not soyad.isalpha():

            QMessageBox.warning(
                self,
                "Hata",
                "Soyad sadece harf içermelidir!"
            )
            return

        if not tel.isdigit():

            QMessageBox.warning(
                self,
                "Hata",
                "Telefon sadece sayı içermelidir!"
            )
            return

        if len(tel) != 11:

            QMessageBox.warning(
                self,
                "Hata",
                "Telefon 11 haneli olmalıdır!"
            )
            return

        try:

            self.db.cursor.execute("""
            INSERT INTO musteriler
            (ad, soyad, tel, sehir)
            VALUES (?,?,?,?)
            """, (
                ad.capitalize(),
                soyad.upper(),
                tel,
                "İstanbul"
            ))

            self.db.conn.commit()

            self.m_ad.clear()
            self.m_soyad.clear()
            self.m_tel.clear()

            self.m_listele()

            QMessageBox.information(
                self,
                "Başarılı",
                "Müşteri eklendi."
            )

        except:

            QMessageBox.warning(
                self,
                "Hata",
                "Telefon numarası zaten kayıtlı!"
            )

    # ==========================================================
    # MÜŞTERİ SİL
    # ==========================================================
    def m_sil(self):

        secili = self.m_tablo.currentRow()

        if secili >= 0:

            musteri_id = self.m_tablo.item(secili, 0).text()

            self.db.cursor.execute("""
            DELETE FROM musteriler
            WHERE id=?
            """, (musteri_id,))

            self.db.conn.commit()

            self.m_listele()

    # ==========================================================
    # MÜŞTERİ LİSTELE
    # ==========================================================
    def m_listele(self):

        self.db.cursor.execute("""
        SELECT id, ad, soyad, tel
        FROM musteriler
        ORDER BY id DESC
        """)

        veriler = self.db.cursor.fetchall()

        self.m_tablo.setRowCount(0)

        for i, satir in enumerate(veriler):

            self.m_tablo.insertRow(i)

            for j, d in enumerate(satir):

                self.m_tablo.setItem(
                    i,
                    j,
                    QTableWidgetItem(str(d))
                )

        self.combo_guncelle()

    # ==========================================================
    # STOK LİSTELE
    # ==========================================================
    def s_listele(self):

        self.db.cursor.execute("""
        SELECT urun, miktar, fiyat
        FROM stok
        ORDER BY miktar DESC
        """)

        veriler = self.db.cursor.fetchall()

        self.s_tablo.setRowCount(0)

        for i, satir in enumerate(veriler):

            self.s_tablo.insertRow(i)

            for j, d in enumerate(satir):

                item = QTableWidgetItem(str(d))

                if j == 1:

                    miktar = int(d)

                    if miktar <= 20:

                        item.setBackground(QColor(255, 120, 120))

                    elif miktar <= 50:

                        item.setBackground(QColor(255, 230, 120))

                self.s_tablo.setItem(i, j, item)

    # ==========================================================
    # STOK SİL
    # ==========================================================
    def stok_sil(self):

        secili = self.s_tablo.currentRow()

        if secili >= 0:

            urun = self.s_tablo.item(secili, 0).text()

            self.db.cursor.execute("""
            DELETE FROM stok
            WHERE urun=?
            """, (urun,))

            self.db.conn.commit()

            self.s_listele()

    # ==========================================================
    # SATIŞ YAP
    # ==========================================================
    def satis_yap(self):

        musteri = self.c_m.currentText()
        urun = self.c_u.currentText()
        adet = self.s_adet.value()

        self.db.cursor.execute("""
        SELECT fiyat, miktar
        FROM stok
        WHERE urun=?
        """, (urun,))

        sonuc = self.db.cursor.fetchone()

        if sonuc and sonuc[1] >= adet:

            toplam = adet * sonuc[0]

            tarih = datetime.now().strftime("%d/%m/%Y %H:%M")

            self.db.cursor.execute("""
            INSERT INTO satislar
            (m_tam_ad, u_ad, adet, toplam, tarih)
            VALUES (?,?,?,?,?)
            """, (
                musteri,
                urun,
                adet,
                toplam,
                tarih
            ))

            self.db.cursor.execute("""
            UPDATE stok
            SET miktar = miktar - ?
            WHERE urun=?
            """, (
                adet,
                urun
            ))

            self.db.conn.commit()

            self.s_listele()
            self.satis_listele()

    # ==========================================================
    # SATIŞ LİSTELE
    # ==========================================================
    def satis_listele(self):

        self.db.cursor.execute("""
        SELECT m_tam_ad, u_ad, adet, toplam, tarih
        FROM satislar
        ORDER BY id DESC
        """)

        veriler = self.db.cursor.fetchall()

        self.st_tablo.setRowCount(0)

        for i, satir in enumerate(veriler):

            self.st_tablo.insertRow(i)

            for j, d in enumerate(satir):

                self.st_tablo.setItem(
                    i,
                    j,
                    QTableWidgetItem(str(d))
                )

    # ==========================================================
    # DESTEK EKLE
    # ==========================================================
    def destek_ekle(self):

        musteri = self.c_m_destek.currentText()

        aciklama = self.t_aciklama.text().strip()

        if aciklama:

            self.db.cursor.execute("""
            INSERT INTO destek_talepleri
            (m_tam_ad, aciklama, durum, tarih)
            VALUES (?,?,?,?)
            """, (
                musteri,
                aciklama,
                "Açık",
                datetime.now().strftime("%d/%m/%Y %H:%M")
            ))

            self.db.conn.commit()

            self.t_aciklama.clear()

            self.destek_listele()

    # ==========================================================
    # DESTEK LİSTELE
    # ==========================================================
    def destek_listele(self):

        self.db.cursor.execute("""
        SELECT *
        FROM destek_talepleri
        ORDER BY talep_id DESC
        """)

        veriler = self.db.cursor.fetchall()

        self.d_tablo.setRowCount(0)

        for i, satir in enumerate(veriler):

            self.d_tablo.insertRow(i)

            for j, d in enumerate(satir):

                self.d_tablo.setItem(
                    i,
                    j,
                    QTableWidgetItem(str(d))
                )

    # ==========================================================
    # COMBO GÜNCELLE
    # ==========================================================
    def combo_guncelle(self):

        self.c_m.clear()
        self.c_m_destek.clear()
        self.c_u.clear()

        self.db.cursor.execute("""
        SELECT ad, soyad
        FROM musteriler
        ORDER BY ad ASC
        """)

        for r in self.db.cursor.fetchall():

            isim = f"{r[0]} {r[1]}"

            self.c_m.addItem(isim)
            self.c_m_destek.addItem(isim)

        self.db.cursor.execute("""
        SELECT urun
        FROM stok
        WHERE miktar > 0
        """)

        for r in self.db.cursor.fetchall():

            self.c_u.addItem(r[0])


# ==========================================================
# PROGRAMI BAŞLAT
# ==========================================================
if __name__ == "__main__":

    app = QApplication(sys.argv)

    app.setStyle("Fusion")

    pencere = CRMApp()

    pencere.show()

    sys.exit(app.exec_())