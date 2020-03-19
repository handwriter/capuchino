import sqlite3
import sys

from PyQt5.QtWidgets import QApplication, QWidget, QTableWidgetItem, QLineEdit
from PyQt5 import uic
from design import Ui_Form as Design


class MyWidget(QWidget, Design):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.con = sqlite3.connect("coffee.sqlite")
        self.titles = None
        self.update_result()
        self.pushButton.clicked.connect(self.adds)
        self.pushButton_2.clicked.connect(self.edits)

    def update_result(self):
        cur = self.con.cursor()
        # Получили результат запроса, который ввели в текстовое поле
        result = cur.execute("Select * from Info").fetchall()
        # Заполнили размеры таблицы
        self.tableWidget.setRowCount(len(result))
        self.tableWidget.setColumnCount(len(result[0]))
        self.titles = [description[0] for description in cur.description]
        # Заполнили таблицу полученными элементами
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))

    def adds(self):
        self.con = sqlite3.connect("coffee.sqlite")
        self.ex = AddForm()
        self.ex.show()
        self.update_result()

    def edits(self):
        self.con = sqlite3.connect("coffee.sqlite")
        if not self.tableWidget.currentItem() is None:
            self.ex = EditForm(self.tableWidget.currentItem())
            self.ex.show()
            self.update_result()


class EditForm(QWidget):
    def __init__(self, item):
        print(item.row())
        super().__init__()
        uic.loadUi('addEditCoffeeForm.ui', self)
        self.con = sqlite3.connect("coffee.sqlite")
        cur = self.con.cursor()
        print('z')
        result = cur.execute("""SELECT * FROM Info
                                WHERE ROWID = ?""", (item.row(),)).fetchall()
        print('m')
        self.lineEdit_2.setText(str(result[0][1]))
        self.lineEdit_3.setText(str(result[0][2]))
        print('k')
        self.lineEdit_4.setText(str(result[0][3]))
        self.lineEdit_5.setText(str(result[0][4]))
        self.lineEdit_6.setText(str(result[0][5]))
        self.lineEdit_7.setText(str(result[0][6]))
        print('d')
        self.pushButton.clicked.connect(self.accept)
        self.row = item.row()

    def accept(self):
        try:
            cur = self.con.cursor()
            result = cur.execute("""UPDATE Info
                                    SET name = ?, degree = ?, style = ?, description = ?, price = ?, vol = ?
                                    WHERE ROWID = ?""",
                                 (self.lineEdit_2.text(), self.lineEdit_3.text(),
                                  self.lineEdit_4.text(), self.lineEdit_5.text(), self.lineEdit_6.text(),
                                  self.lineEdit_7.text(), self.row,)).fetchall()
            self.close()
            self.con.commit()
        except:
            self.label_8.setText("Error")


class AddForm(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('addEditCoffeeForm.ui', self)
        self.pushButton.clicked.connect(self.accept)
        self.con = sqlite3.connect("coffee.sqlite")

    def accept(self):
        try:
            cur2 = self.con.cursor()
            result2 = cur2.execute("""SELECT * FROM Info""").fetchall()[-1][0]
            cur = self.con.cursor()
            result = cur.execute(
                """INSERT INTO Info(ID,name,degree,style,description,price,vol) VALUES(?,?,?,?,?,?,?)""",
                (result2 + 1, self.lineEdit_2.text(), self.lineEdit_3.text(),
                 self.lineEdit_4.text(), self.lineEdit_5.text(), self.lineEdit_6.text(),
                 self.lineEdit_7.text(),)).fetchall()
            self.close()
            self.con.commit()
        except:
            self.label_8.setText("Error")


app = QApplication(sys.argv)
ex = MyWidget()
ex.show()
sys.exit(app.exec_())
