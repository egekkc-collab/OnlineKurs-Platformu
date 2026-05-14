import sys
import random
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QHBoxLayout, 
                             QVBoxLayout, QFormLayout, QLineEdit, QTextEdit, 
                             QPushButton, QTableWidget, QTableWidgetItem, 
                             QAbstractItemView, QSpinBox, QMessageBox, QGroupBox, 
                             QHeaderView, QLabel, QComboBox, QFrame)
from PyQt5.QtCore import QRegExp, Qt
from PyQt5.QtGui import QRegExpValidator, QColor, QFont, QLinearGradient, QPalette

# --- PREMIUM VIBRANT STYLE SHEET ---
STYLE_SHEET = """
    QMainWindow {
        background-color: #f5f7fa;
    }
    QGroupBox {
        font-family: 'Segoe UI';
        font-size: 14px;
        font-weight: bold;
        color: #444;
        border: 1px solid #d1d8e0;
        border-radius: 12px;
        margin-top: 20px;
        background-color: white;
        padding-top: 15px;
    }
    QGroupBox::title {
        subcontrol-origin: margin;
        subcontrol-position: top center;
        padding: 0 10px;
        background-color: #f5f7fa;
    }
    QLineEdit, QTextEdit, QSpinBox, QComboBox {
        border: 2px solid #edf2f7;
        border-radius: 8px;
        padding: 8px;
        background: #fdfdfd;
        selection-background-color: #3498db;
    }
    QLineEdit:focus {
        border: 2px solid #3498db;
        background: white;
    }
    QPushButton {
        background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #3498db, stop:1 #2980b9);
        color: white;
        border-radius: 10px;
        padding: 12px;
        font-size: 13px;
        font-weight: bold;
        border: none;
    }
    QPushButton:hover {
        background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #2980b9, stop:1 #3498db);
    }
    QPushButton#btn_sil {
        background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #e74c3c, stop:1 #c0392b);
    }
    QPushButton#btn_sil:hover {
        background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #c0392b, stop:1 #e74c3c);
    }
    QTableWidget {
        background-color: white;
        border: none;
        border-radius: 15px;
        gridline-color: #f1f2f6;
    }
    QHeaderView::section {
        background-color: #4b6cb7;
        color: white;
        padding: 10px;
        font-weight: bold;
        border: none;
    }
    QTableWidget::item {
        padding: 10px;
        border-bottom: 1px solid #f1f2f6;
    }
"""

# --- MODELLER ---
class SeyahatPlani:
    def __init__(self, s_id, yer, tarih, otel, fiyat, rota, akt, statu):
        self.seyahat_id = s_id
        self.gidis_yeri = yer
        self.tarih = tarih
        self.otel_adi = otel
        self.fiyat = fiyat
        self.rota = rota
        self.aktiviteler = akt
        self.statu = statu

# --- ANA PENCERE ---
class SeyahatApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Seyahat Master v3.0 - Renkli Dashboard")
        self.setMinimumSize(1250, 850)
        self.setStyleSheet(STYLE_SHEET)
        
        self.planlar = []
        self.init_data()
        self.init_ui()

    def init_data(self):
        sehirler = ["Barselona", "Venedik", "Prag", "Atina", "Bali", "New York", "Kapadokya", "Phuket"]
        oteller = ["Lüks Palas", "Zümrüt Resort", "Sakin Bahçe", "Royal Otel", "Butik Han"]
        statuler = ["Planlandı", "Tamamlandı", "İptal Edildi"]
        for i in range(1, 31):
            self.planlar.append(SeyahatPlani(
                i, random.choice(sehirler), f"{random.randint(1,28)}.{random.randint(6,12)}.2026",
                random.choice(oteller), random.randint(4000, 45000),
                "Merkez -> Turistik Yerler", "Gezi, Gastronomi, Fotoğraf", random.choice(statuler)
            ))

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        # --- SOL PANEL ---
        left_panel = QVBoxLayout()
        
        # Logo/Başlık Alanı
        title_frame = QFrame()
        title_frame.setStyleSheet("background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #1e3c72, stop:1 #2a5298); border-radius: 15px;")
        title_layout = QVBoxLayout(title_frame)
        main_title = QLabel("TRAVEL PLANNER")
        main_title.setStyleSheet("color: white; font-size: 24px; font-weight: 900; letter-spacing: 2px;")
        main_title.setAlignment(Qt.AlignCenter)
        title_layout.addWidget(main_title)
        left_panel.addWidget(title_frame)

        # Form Alanı
        form_group = QGroupBox("PLAN DETAYLARI")
        form_layout = QFormLayout()
        form_layout.setSpacing(15)

        v_harf = QRegExpValidator(QRegExp("[a-zA-ZğüşıöçĞÜŞİÖÇ ]+"))
        v_sayi = QRegExpValidator(QRegExp("[0-9.]+"))

        self.txt_id = QLineEdit(); self.txt_id.setReadOnly(True); self.txt_id.setPlaceholderText("ID")
        self.txt_yer = QLineEdit(); self.txt_yer.setValidator(v_harf)
        self.txt_tarih = QLineEdit(); self.txt_tarih.setPlaceholderText("GG.AA.YYYY"); self.txt_tarih.setValidator(v_sayi)
        self.txt_otel = QLineEdit(); self.txt_otel.setValidator(v_harf)
        self.txt_fiyat = QSpinBox(); self.txt_fiyat.setRange(0, 2000000); self.txt_fiyat.setSuffix(" ₺")
        self.cmb_statu = QComboBox(); self.cmb_statu.addItems(["Planlandı", "Tamamlandı", "İptal Edildi"])
        self.txt_rota = QLineEdit()
        self.txt_aktivite = QTextEdit(); self.txt_aktivite.setMaximumHeight(70)

        form_layout.addRow("📌 ID:", self.txt_id)
        form_layout.addRow("🌍 Gidiş Yeri:", self.txt_yer)
        form_layout.addRow("📅 Tarih:", self.txt_tarih)
        form_layout.addRow("🏨 Otel Adı:", self.txt_otel)
        form_layout.addRow("💰 Fiyat:", self.txt_fiyat)
        form_layout.addRow("🚦 Durum:", self.cmb_statu)
        form_layout.addRow("🛣️ Rota:", self.txt_rota)
        form_layout.addRow("📝 Aktiviteler:", self.txt_aktivite)
        form_group.setLayout(form_layout)
        left_panel.addWidget(form_group)

        # Butonlar
        btn_layout = QHBoxLayout()
        self.btn_ekle = QPushButton("KAYDET")
        self.btn_guncelle = QPushButton("GÜNCELLE")
        self.btn_sil = QPushButton("SİL")
        self.btn_sil.setObjectName("btn_sil")
        
        btn_layout.addWidget(self.btn_ekle); btn_layout.addWidget(self.btn_guncelle); btn_layout.addWidget(self.btn_sil)
        left_panel.addLayout(btn_layout)

        # Bütçe Kartı
        self.stat_card = QFrame()
        self.stat_card.setStyleSheet("background: white; border: 2px solid #3498db; border-radius: 15px;")
        stat_layout = QVBoxLayout(self.stat_card)
        self.lbl_total = QLabel("TOPLAM HARCAMA\n0 ₺")
        self.lbl_total.setAlignment(Qt.AlignCenter)
        self.lbl_total.setStyleSheet("color: #2c3e50; font-size: 20px; font-weight: bold;")
        stat_layout.addWidget(self.lbl_total)
        left_panel.addWidget(self.stat_card)
        
        left_panel.addStretch()

        # --- SAĞ PANEL ---
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(["ID", "Destinasyon", "Tarih", "Konaklama", "Bütçe", "Durum", "Güzergah"])
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        
        main_layout.addLayout(left_panel, 1)
        main_layout.addWidget(self.table, 3)

        # Sinyaller
        self.btn_ekle.clicked.connect(self.ekle_plan)
        self.btn_guncelle.clicked.connect(self.guncelle_plan)
        self.btn_sil.clicked.connect(self.sil_plan)
        self.table.itemClicked.connect(self.satir_sec)

        self.listele()

    def listele(self):
        self.table.setRowCount(0)
        toplam = 0
        for p in self.planlar:
            row = self.table.rowCount()
            self.table.insertRow(row)
            
            # ID ve Temel Bilgiler
            self.table.setItem(row, 0, QTableWidgetItem(str(p.seyahat_id)))
            self.table.setItem(row, 1, QTableWidgetItem(p.gidis_yeri))
            self.table.setItem(row, 2, QTableWidgetItem(p.tarih))
            self.table.setItem(row, 3, QTableWidgetItem(p.otel_adi))
            
            # Fiyat Renklendirme
            f_item = QTableWidgetItem(f"{p.fiyat:,} ₺")
            f_item.setFont(QFont("Segoe UI", 10, QFont.Bold))
            if p.fiyat > 30000: f_item.setForeground(QColor("#e67e22"))
            elif p.fiyat < 10000: f_item.setForeground(QColor("#27ae60"))
            self.table.setItem(row, 4, f_item)
            
            # Durum Renklendirme
            s_item = QTableWidgetItem(p.statu)
            if p.statu == "Planlandı": s_item.setForeground(QColor("#3498db"))
            elif p.statu == "Tamamlandı": s_item.setForeground(QColor("#2ecc71"))
            else: s_item.setForeground(QColor("#95a5a6"))
            self.table.setItem(row, 5, s_item)
            
            self.table.setItem(row, 6, QTableWidgetItem(p.rota))
            toplam += p.fiyat

        self.lbl_total.setText(f"TOPLAM HARCAMA\n{toplam:,} ₺")

    def satir_sec(self):
        idx = self.table.currentRow()
        if idx >= 0:
            p_id = int(self.table.item(idx, 0).text())
            p = next(x for x in self.planlar if x.seyahat_id == p_id)
            self.txt_id.setText(str(p.seyahat_id))
            self.txt_yer.setText(p.gidis_yeri); self.txt_tarih.setText(p.tarih)
            self.txt_otel.setText(p.otel_adi); self.txt_fiyat.setValue(p.fiyat)
            self.cmb_statu.setCurrentText(p.statu); self.txt_rota.setText(p.rota)
            self.txt_aktivite.setPlainText(p.aktiviteler)

    def ekle_plan(self):
        if not self.txt_yer.text(): return
        yeni_id = max([p.seyahat_id for p in self.planlar], default=0) + 1
        self.planlar.append(SeyahatPlani(yeni_id, self.txt_yer.text(), self.txt_tarih.text(),
                                        self.txt_otel.text(), self.txt_fiyat.value(),
                                        self.txt_rota.text(), self.txt_aktivite.toPlainText(),
                                        self.cmb_statu.currentText()))
        self.listele(); self.temizle()

    def guncelle_plan(self):
        if not self.txt_id.text(): return
        p_id = int(self.txt_id.text())
        for p in self.planlar:
            if p.seyahat_id == p_id:
                p.gidis_yeri = self.txt_yer.text(); p.tarih = self.txt_tarih.text()
                p.otel_adi = self.txt_otel.text(); p.fiyat = self.txt_fiyat.value()
                p.statu = self.cmb_statu.currentText(); p.rota = self.txt_rota.text()
                p.aktiviteler = self.txt_aktivite.toPlainText()
        self.listele()

    def sil_plan(self):
        if not self.txt_id.text(): return
        self.planlar = [p for p in self.planlar if p.seyahat_id != int(self.txt_id.text())]
        self.listele(); self.temizle()

    def temizle(self):
        for w in [self.txt_id, self.txt_yer, self.txt_tarih, self.txt_otel, self.txt_rota]: w.clear()
        self.txt_fiyat.setValue(0); self.txt_aktivite.clear(); self.cmb_statu.setCurrentIndex(0)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    win = SeyahatApp()
    win.show()
    sys.exit(app.exec_())