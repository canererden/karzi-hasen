import datetime
import sqlite3
import sys

from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from dateutil.relativedelta import relativedelta


class LoginDialog(QDialog):
    # noinspection PyArgumentList
    def __init__(self):
        super(LoginDialog, self).__init__()
        uic.loadUi('gui\\LoginDialog.ui', self)
        self.conn = sqlite3.connect('database.db')
        self.cursor = self.conn.cursor()
        self.btn_giris.clicked.connect(self.login)
        self.kullanici_tc = ""
        self.kullanici_sifre = ""

    def login(self):
        self.kullanici_tc = self.input_tc.text()
        self.kullanici_sifre = self.input_pass.text()
        dogru_tc = self.cursor.execute("select TC from uyeler").fetchall()
        dogru_tc_listesi = [x[0] for x in dogru_tc]
        if int(self.kullanici_tc) in dogru_tc_listesi:
            dogru_sifre = self.cursor.execute(
                "select sifre from uyeler where TC=?", (self.kullanici_tc,)).fetchone()[0]
            if self.kullanici_sifre == dogru_sifre:
                self.accept()
            else:
                QMessageBox.warning(self, 'Şifre Hatalı!',
                                    'TC Kimlik Sistemde Kayıtlı Ancak Şifre Hatalı Bilgi için: cerden@sakarya.edu.tr')
        else:
            QMessageBox.warning(self, 'TC Hatalı!',
                                'TC Kimlik Numarası Sistemde Kayıtlı Değil! Bilgi için: cerden@sakarya.edu.tr')


class InsertDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super(InsertDialog, self).__init__(*args, **kwargs)
        uic.loadUi('gui\\InsertDialog.ui', self)
        self.conn = sqlite3.connect('database.db')
        self.cursor = self.conn.cursor()
        self.btn_uye_ekle.clicked.connect(self.uye_ekle)

    def uye_ekle(self):
        tc_no, isim, soyisim, telefon, email, adres = self.tc_input.text(), self.isim_input.text(
        ), self.soyisim_input.text(), self.telefon_input.text(), self.email_input.text(), self.adres_input.text()
        role = "Uye"
        sifre = "uye54"
        try:
            self.cursor.execute(
                "INSERT INTO uyeler (TC, isim,soyisim,telefon,email,adres,role,sifre) VALUES (?, ?,?,?,?,?,?,?)", (
                    tc_no, isim, soyisim, telefon, email, adres, role, sifre))
            self.conn.commit()
            self.cursor.close()
            self.conn.close()
            QMessageBox.information(
                QMessageBox(), 'Başarılı', 'Yeni üye sisteme eklenmiştir.')
            self.close()
        except Exception:
            QMessageBox.warning(
                QMessageBox(), 'Hata', 'Üye sisteme eklenemedi. Lütfen tüm bilgileri giriniz.')


class SearchDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super(SearchDialog, self).__init__(*args, **kwargs)
        uic.loadUi('gui\\SearchDialog.ui', self)


class AboutDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super(AboutDialog, self).__init__(*args, **kwargs)
        uic.loadUi('gui\\AboutDialog.ui', self)


class AidatEkleDialog(QDialog):
    def __init__(self, uye_id, *args, **kwargs):
        super(AidatEkleDialog, self).__init__(*args, **kwargs)
        uic.loadUi('gui\\AidatEkleDialog.ui', self)
        now = QDate.currentDate()
        self.uye_id = uye_id
        self.aidat_text.setText(
            "{} no'lu üyeye aidat ekleniyor...".format(self.uye_id))
        self.conn = sqlite3.connect('database.db')
        self.cursor = self.conn.cursor()
        self.aidat_tarihi.setDate(now)

        self.btn_aidat_ekle.clicked.connect(self.aidat_ekle)
        self.btn_mail.clicked.connect(self.ekle_mail)

    def aidat_ekle(self):
        aidat_miktari = int(self.input_miktar.text())
        aidat_tarihi = self.aidat_tarihi.date()
        try:
            self.cursor.execute("INSERT INTO yatirimlar (_id, yatirimTarih, yatirimMiktari) VALUES (?,?,?)",
                                (self.uye_id, aidat_tarihi.toPyDate(), aidat_miktari))
            self.conn.commit()
            self.cursor.close()
            self.conn.close()
            QMessageBox.information(
                QMessageBox(), 'Başarılı', 'Aidat Eklenmiştir.')
            self.close()
        except Exception:
            QMessageBox.warning(
                QMessageBox(), 'Hata', 'Aidat Eklenemedi.')

    def ekle_mail(self):
        # TODO Ekle Mail hazırlanacak.
        aidat_miktari = int(self.input_miktar.text())
        aidat_tarihi = self.aidat_tarihi.date()
        try:
            self.cursor.execute("INSERT INTO yatirimlar (_id, yatirimTarih, yatirimMiktari) VALUES (?,?,?)",
                                (self.uye_id, aidat_tarihi.toPyDate(), aidat_miktari))
            self.conn.commit()
            self.cursor.close()
            self.conn.close()
            QMessageBox.information(
                QMessageBox(), 'Başarılı', 'Aidat Eklenmiştir.')
            self.close()
        except Exception:
            QMessageBox.warning(
                QMessageBox(), 'Hata', 'Aidat Eklenemedi.')


class OdemeEkleDialog(QDialog):
    def __init__(self, uye_id, *args, **kwargs):
        super(OdemeEkleDialog, self).__init__(*args, **kwargs)
        uic.loadUi('gui\\OdemeEkleDialog.ui', self)
        now = QDate.currentDate()
        self.uye_id = uye_id
        self.odeme_text.setText(
            "{} no'lu üyeye ödeme ekleniyor...".format(self.uye_id))
        self.conn = sqlite3.connect('database.db')
        self.cursor = self.conn.cursor()
        self.odeme_tarihi.setDate(now)
        borc_listesi = self.cursor.execute(
            'select taksit_id, taksitTarih, taksitMiktar from taksitler where uye_id = ? '
            'and taksitOdeme < taksitMiktar',
            (self.uye_id,)).fetchall()
        for borc in borc_listesi:
            self.comboBox.addItem(str(borc))
        if borc_listesi:
            # TODO burası borcu olmayanlar için hatalı çalışıyor.
            self.comboBox.setCurrentIndex(0)
            self.taksitler = eval(self.comboBox.currentText())
            self.taksit_id = self.taksitler[0]
            self.taksit_tarih = datetime.datetime.strptime(self.taksitler[1], '%Y-%m-%d').date()
            self.taksit_miktar = self.taksitler[2]
            self.comboBox.currentIndexChanged.connect(self.selectionchange)
            self.btn_odeme_ekle.clicked.connect(self.odeme_ekle)
        else:
            QMessageBox.warning(QMessageBox(), 'Hata', 'Üyeye ait borç bulunmamaktadır.')
            self.close()

    def odeme_ekle(self):
        odeme_tarihi = self.odeme_tarihi.date()
        try:
            self.conn = sqlite3.connect('database.db')
            self.cursor = self.conn.cursor()
            self.cursor.execute("update taksitler set taksitOdeme = ?, odemeTarihi=? where taksit_id =?",
                                (self.taksit_miktar, odeme_tarihi.toPyDate(), self.taksit_id))
            self.conn.commit()
            self.cursor.close()
            self.conn.close()
            QMessageBox.information(QMessageBox(), 'Başarılı', 'Ödeme Eklenmiştir.')
            self.close()
        except Exception:
            QMessageBox.warning(QMessageBox(), 'Hata', 'Ödeme Eklenemedi.')

    def selectionchange(self):
        self.taksitler = eval(self.comboBox.currentText())
        self.taksit_id = self.taksitler[0]
        self.taksit_tarih = datetime.datetime.strptime(self.taksitler[1], '%Y-%m-%d').date()
        self.taksit_miktar = self.taksitler[2]


class BorcVerDialog(QDialog):
    def __init__(self, uye_id, *args, **kwargs):
        super(BorcVerDialog, self).__init__(*args, **kwargs)
        uic.loadUi('gui\\BorcVerDialog.ui', self)
        self.now = QDate.currentDate()
        self.uye_id = uye_id
        self.borc_ver_text.setText(
            "{} no'lu üyeye borç ekleniyor...".format(self.uye_id))
        self.conn = sqlite3.connect('database.db')
        self.cursor = self.conn.cursor()
        self.borc_tarihi.setDate(self.now)
        self.vade_tarihi.setDate(self.now.addDays(270))

        self.btn_borc_ver.clicked.connect(self.borc_ver)

    def borc_ver(self):
        borc_miktari = int(self.input_miktar.text())
        borc_tarihi = self.borc_tarihi.date()
        vade_tarihi = self.vade_tarihi.date()
        r = relativedelta(vade_tarihi.toPyDate(), borc_tarihi.toPyDate())
        k = r.months * (r.years + 1)
        miktar_listesi = [0] * k
        tarih_listesi = []
        odeme_listesi = [0] * k
        for i in range(k):
            miktar_listesi[i] = int(borc_miktari / k)
        for i in range(0, borc_miktari % k):
            miktar_listesi[-(i + 1)] += 1
        for i, borc in enumerate(miktar_listesi):
            tarih = QDate(borc_tarihi.toPyDate() + relativedelta(months=i + 1))
            tarih_listesi.append(tarih)
        try:
            self.cursor.execute(
                "INSERT INTO borclar (_id, borcAlinma, borcVade, borcMiktar, borcEklenme) VALUES (?,?,?,?,?)",
                (self.uye_id, borc_tarihi.toPyDate(), vade_tarihi.toPyDate(), borc_miktari, self.now.toPyDate()))
            self.conn.commit()
            son_borc_id = self.cursor.execute(
                "SELECT borclar.borc_id from borclar where borc_id = (select max(borc_id) from borclar)").fetchone()[0]
            for i in range(len(odeme_listesi)):
                self.cursor.execute(
                    "INSERT INTO taksitler (borc_id,uye_id,taksitTarih,taksitMiktar,taksitOdeme) VALUES (?,?,?,?,?)",
                    (son_borc_id, self.uye_id, tarih_listesi[i].toPyDate(), miktar_listesi[i], odeme_listesi[i]))
            self.conn.commit()
            self.cursor.close()
            self.conn.close()
            QMessageBox.information(
                QMessageBox(), 'Başarılı', 'Borç Eklenmiştir.')
            self.close()
        except Exception:
            QMessageBox.warning(
                QMessageBox(), 'Hata', 'Borç Eklenemedi.')


class DeleteDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super(DeleteDialog, self).__init__(*args, **kwargs)
        uic.loadUi('gui\\DeleteDialog.ui', self)
        self.conn = sqlite3.connect('database.db')
        self.cursor = self.conn.cursor()
        self.btn_uye_sil.clicked.connect(self.uye_sil)

    def uye_sil(self):
        tc_no = self.tc_input.text()
        try:
            self.cursor.execute('delete from uyeler where TC={}'.format(tc_no))
            self.conn.commit()
            self.cursor.close()
            self.conn.close()
            QMessageBox.information(
                QMessageBox(), 'Başarılı', 'Yeni üye sistemden silinmiştir.')
            self.close()
        except Exception:
            QMessageBox.warning(
                QMessageBox(), 'Hata', 'Üye sisteme silinemedi. Lütfen tüm bilgileri giriniz.')


class OdemeleriGosterDialog(QDialog):
    def __init__(self, *args, **kwargs):
        # TODO Ödemeleri göster taksitleri gösterecek şekilde ayarlanacak.
        super(OdemeleriGosterDialog, self).__init__(*args, **kwargs)
        uic.loadUi('gui\\OdemeleriGosterDialog.ui', self)
        self.showNormal()
        self.setWindowFlags(Qt.Window)
        self.conn = sqlite3.connect('database.db')
        self.cursor = self.conn.cursor()
        self.tableWidget.setSelectionBehavior(QTableView.SelectRows)
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.goster()

    def goster(self):
        query = 'select uyeler._id, uyeler.isim || " " || uyeler.soyisim as \'isim soyisim\', taksitler.taksitTarih, taksitler.taksitMiktar, taksitler.taksitOdeme, taksitler.odemeTarihi from uyeler inner join taksitler on taksitler.uye_id=uyeler._id order by uyeler._id, taksitler.odemeTarihi desc'
        borclular = self.cursor.execute(query).fetchall()
        for row_number, row_data in enumerate(borclular):
            self.tableWidget.insertRow(row_number)
            for column_number in range(len(row_data)):
                data = row_data[column_number]
                if data is None:
                    data = 0
                self.tableWidget.setItem(
                    row_number, column_number, QTableWidgetItem(str(data)))
        self.conn.commit()
        self.conn.close()


class YatirimlariGosterDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super(YatirimlariGosterDialog, self).__init__(*args, **kwargs)
        uic.loadUi('gui\\YatirimlariGosterDialog.ui', self)
        self.showNormal()
        self.setWindowFlags(Qt.Window)
        self.tableWidget.setSelectionBehavior(QTableView.SelectRows)
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)

        year = QDate.currentDate().year()
        self.comboBox.activated[str].connect(self.onChange)

    def onChange(self, text):
        # TODO tarihleri daha güzel gösterebilir.
        self.conn = sqlite3.connect('database.db')
        year = int(text)
        query = """select uyeler._id, uyeler.isim || " " || uyeler.soyisim as 'isim soyisim', 
        (select sum(yatirimlar.yatirimMiktari) from yatirimlar where uyeler._id=yatirimlar._id),
        (select yatirimlar.yatirimMiktari from yatirimlar where uyeler._id=yatirimlar._id and 
        strftime('%Y',yatirimlar.yatirimTarih)=:Year and strftime('%m',yatirimlar.yatirimTarih)='01'),
        (select yatirimlar.yatirimMiktari from yatirimlar where uyeler._id=yatirimlar._id and 
        strftime('%Y',yatirimlar.yatirimTarih)=:Year and strftime('%m',yatirimlar.yatirimTarih)='02'),
        (select yatirimlar.yatirimMiktari from yatirimlar where uyeler._id=yatirimlar._id and 
        strftime('%Y',yatirimlar.yatirimTarih)=:Year and strftime('%m',yatirimlar.yatirimTarih)='03'),
        (select yatirimlar.yatirimMiktari from yatirimlar where uyeler._id=yatirimlar._id and 
        strftime('%Y',yatirimlar.yatirimTarih)=:Year and strftime('%m',yatirimlar.yatirimTarih)='04'),
        (select yatirimlar.yatirimMiktari from yatirimlar where uyeler._id=yatirimlar._id and 
        strftime('%Y',yatirimlar.yatirimTarih)=:Year and strftime('%m',yatirimlar.yatirimTarih)='05'),
        (select yatirimlar.yatirimMiktari from yatirimlar where uyeler._id=yatirimlar._id and 
        strftime('%Y',yatirimlar.yatirimTarih)=:Year and strftime('%m',yatirimlar.yatirimTarih)='06'),
        (select yatirimlar.yatirimMiktari from yatirimlar where uyeler._id=yatirimlar._id and 
        strftime('%Y',yatirimlar.yatirimTarih)=:Year and strftime('%m',yatirimlar.yatirimTarih)='07'),
        (select yatirimlar.yatirimMiktari from yatirimlar where uyeler._id=yatirimlar._id and 
        strftime('%Y',yatirimlar.yatirimTarih)=:Year and strftime('%m',yatirimlar.yatirimTarih)='08'),
        (select yatirimlar.yatirimMiktari from yatirimlar where uyeler._id=yatirimlar._id and 
        strftime('%Y',yatirimlar.yatirimTarih)=:Year and strftime('%m',yatirimlar.yatirimTarih)='09'),
        (select yatirimlar.yatirimMiktari from yatirimlar where uyeler._id=yatirimlar._id and 
        strftime('%Y',yatirimlar.yatirimTarih)=:Year and strftime('%m',yatirimlar.yatirimTarih)='10'),
        (select yatirimlar.yatirimMiktari from yatirimlar where uyeler._id=yatirimlar._id and 
        strftime('%Y',yatirimlar.yatirimTarih)=:Year and strftime('%m',yatirimlar.yatirimTarih)='11'),
        (select yatirimlar.yatirimMiktari from yatirimlar where uyeler._id=yatirimlar._id and 
        strftime('%Y',yatirimlar.yatirimTarih)=:Year and strftime('%m',yatirimlar.yatirimTarih)='12')         
        from uyeler"""
        result = self.conn.execute(query, {'Year': str(year)})
        self.tableWidget.setRowCount(0)
        for row_number, row_data in enumerate(result):
            self.tableWidget.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.tableWidget.setItem(
                    row_number, column_number, QTableWidgetItem(str(data)))
                if data and column_number > 2:
                    self.tableWidget.item(
                        row_number, column_number).setForeground(Qt.green)
                if (data is None) and column_number > 2:
                    self.tableWidget.setItem(
                        row_number, column_number, QTableWidgetItem('0'))
        self.conn.commit()
        self.conn.close()


class MainWindow(QMainWindow):
    def __init__(self, tc_no, sifre):
        super(MainWindow, self).__init__()
        uic.loadUi('gui\\mainwindow.ui', self)
        self.conn = sqlite3.connect('database.db')
        self.cursor = self.conn.cursor()
        self.tc_no = tc_no
        self.sifre = sifre
        self.id_no, self.tc_no, self.isim, self.soyisim, self.telefon, self.email, self.adres, self.role, self.sifre = self.cursor.execute(
            "select * from uyeler where TC={}".format(int(self.tc_no))).fetchone()
        self.uye_bilgileri.setText(
            " {} {}\n Telefon: {}\n e-mail: {}".format(self.isim, self.soyisim, self.telefon, self.email))

        if self.role == 'Admin':
            self.btn_ac_adduser.triggered.connect(self.insert)
            self.btn_ac_delete.triggered.connect(self.delete)
            self.btn_ac_borc_ekle.triggered.connect(self.borc_ver)
            self.btn_ac_yatirim_ekle.triggered.connect(self.aidat_ekle)
            self.btn_ac_odeme_ekle.triggered.connect(self.odeme_ekle)
        else:
            self.btn_ac_adduser.triggered.connect(self.uye_giris)
            self.btn_ac_delete.triggered.connect(self.uye_giris)
            self.btn_ac_borc_ekle.triggered.connect(self.uye_giris)
            self.btn_ac_yatirim_ekle.triggered.connect(self.uye_giris)
            self.btn_ac_odeme_ekle.triggered.connect(self.uye_giris)

        self.btn_ac_refresh.triggered.connect(self.loaddata)
        self.btn_ac_yatirimlari_goster.triggered.connect(
            self.yatirimlari_goster)
        self.btn_ac_odemeleri_goster.triggered.connect(self.odemeleri_goster)
        self.btn_ac_gelistirici.triggered.connect(self.about)
        self.btn_ac_exit.triggered.connect(self.exit)

    def uye_giris(self):
        error_dialog = QErrorMessage()
        error_dialog.setWindowTitle("Hata")
        error_dialog.showMessage('Üyelere izin verilmemektedir.')
        error_dialog.exec_()

    def loaddata(self):
        toplam_yatirim = 0
        toplam_borc = 0
        kalan_borc = 0
        self.conn = sqlite3.connect('database.db')
        self.cursor = self.conn.cursor()
        self.tableWidget.setRowCount(0)
        result = self.cursor.execute(
            "select uyeler._id, uyeler.isim || ' ' || uyeler.soyisim, (select sum(yatirimlar.yatirimMiktari) from yatirimlar where yatirimlar._id=uyeler._id), (select sum(borclar.borcMiktar) from borclar where borclar._id=uyeler._id), (select sum(borclar.borcMiktar) from borclar where uyeler._id=borclar._id) - (select sum(taksitOdeme) from taksitler where taksitler.uye_id=uyeler._id) from uyeler")

        result_list = result.fetchall()
        for row_number, row_data in enumerate(result_list):
            self.tableWidget.insertRow(row_number)
            uye_id = row_data[0]
            taksitler = self.cursor.execute(
                "select strftime('%d/%m/%Y', taksitTarih)|| '--' || sum(taksitMiktar) from taksitler where uye_id=? and taksitMiktar>taksitOdeme group by taksitler.taksitTarih",
                (uye_id,)).fetchall()
            taksit_list = [x[0] for x in taksitler]
            for taksit in taksit_list:
                row_data = row_data + (taksit,)

            try:
                yatirim = int(row_data[2])
            except:
                yatirim = 0
            try:
                borc = int(row_data[3])
            except:
                borc = 0
            try:
                kalan = int(row_data[4])
            except:
                kalan = 0
            for column_number in range(len(row_data)):
                data = row_data[column_number]
                if data is None:
                    data = 0
                self.tableWidget.setItem(
                    row_number, column_number, QTableWidgetItem(str(data)))
            toplam_yatirim += yatirim
            toplam_borc += borc
            kalan_borc += kalan

        self.kasa_bilgileri.setText(
            " Toplam Yatırım: {} \n Toplam Verilen Borç: {} \n Toplam Kalan Borç: {}\n Mevcut Kasa: {}".format(
                toplam_yatirim, toplam_borc, kalan_borc,
                toplam_yatirim - kalan_borc))
        self.conn.commit()
        self.conn.close()

    def insert(self):
        dlg = InsertDialog()
        dlg.exec_()

    def delete(self):
        dlg = DeleteDialog()
        dlg.exec_()

    def yatirimlari_goster(self):
        self.w = YatirimlariGosterDialog()
        self.w.show()

    def odemeleri_goster(self):
        self.w = OdemeleriGosterDialog()
        self.w.show()

    def borc_ver(self):
        if self.tableWidget.selectionModel().selectedRows():
            indexes = self.tableWidget.selectionModel().selectedRows()
            uye_no = indexes[0].data()
            dlg = BorcVerDialog(uye_id=uye_no)
            dlg.exec_()
        else:
            error_dialog = QErrorMessage()
            error_dialog.setWindowTitle("Hata")
            error_dialog.showMessage('Üye seçilmedi! Lütfen bir üye seçiniz')
            error_dialog.exec_()

    def aidat_ekle(self):
        if self.tableWidget.selectionModel().selectedRows():
            indexes = self.tableWidget.selectionModel().selectedRows()
            uye_no = indexes[0].data()
            dlg = AidatEkleDialog(uye_id=uye_no)
            dlg.exec_()
        else:
            error_dialog = QErrorMessage()
            error_dialog.setWindowTitle("Hata")
            error_dialog.showMessage('Üye seçilmedi! Lütfen bir üye seçiniz')
            error_dialog.exec_()

    def odeme_ekle(self):
        if self.tableWidget.selectionModel().selectedRows():
            indexes = self.tableWidget.selectionModel().selectedRows()
            uye_no = indexes[0].data()
            dlg = OdemeEkleDialog(uye_id=uye_no)
            dlg.exec_()
        else:
            error_dialog = QErrorMessage()
            error_dialog.setWindowTitle("Hata")
            error_dialog.showMessage('Üye seçilmedi! Lütfen bir üye seçiniz')
            error_dialog.exec_()

    def about(self):
        dlg = AboutDialog()
        dlg.exec_()

    def exit(self):
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    passdlg = LoginDialog()
    passdlg.show()
    if (passdlg.exec_() == QDialog.Accepted):
        giris_yapan_tc = passdlg.input_tc.text()
        giris_yapan_pass = passdlg.input_pass.text()
        window = MainWindow(tc_no=giris_yapan_tc, sifre=giris_yapan_pass)
        window.show()
        window.loaddata()
    sys.exit(app.exec_())
