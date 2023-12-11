import random
import sys
import sqlite3
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow
import math

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        uic.loadUi('window.ui', self)
        connect = sqlite3.connect('physics')
        self.cur = connect.cursor()
        self.Item_btn.clicked.connect(self.Item)
        self.title_btn.clicked.connect(self.go_task)
        self.submit.clicked.connect(self.check)
        self.th = self.cur.execute("""SELECT theme FROM themes""").fetchall()
        self.th = [i[0] for i in self.th]
        for i in self.th:
            self.Items.addItem(i)

    def Item(self):
        self.title.clear()
        self.selected_item = self.Items.currentText()
        self.th = self.cur.execute(f"""SELECT Тема FROM tasks 
                WHERE Раздел = (SELECT themes.ID from themes WHERE theme = '{self.selected_item}')""").fetchall()
        for i in self.th:
            self.title.addItem(i[0])

    def go_task(self):
        self.current = self.title.currentText()
        self.curr_title = self.cur.execute(f"""SELECT exersise FROM exersises 
        WHERE exersises.theme = 
        (SELECT tasks.ID FROM tasks WHERE Тема = '{self.current}')""").fetchall()
        self.curr_title = [i[0] for i in self.curr_title]
        self.a = self.curr_title[random.randrange(len(self.curr_title))]
        self.ex = self.cur.execute(f"""SELECT explanation from exersises 
        WHERE exersise = '{self.a}'""").fetchall()[0][0]
        self.formul = self.cur.execute(f"""SELECT formula FROM exersises WHERE 
        exersise = '{self.a}'""").fetchall()[0][0]
        self.values = self.cur.execute(f"""SELECT exersises.variables FROM exersises 
                WHERE exersise = '{self.a}'""").fetchall()[0]
        self.values = self.values[0].split('@')
        self.values = [i.split(';') for i in self.values]
        self.s = {}
        for i in range(len(self.values)):
            val_1 = random.randrange(int(self.values[i][1]), int(self.values[i][2]) + 1,
                                   int(self.values[i][3]))
            self.s[self.values[i][0]] = val_1
        for i in self.values:
            self.a = self.a.replace('{' + i[0] + '}', str(self.s[i[0]]))
            self.formul = self.formul.replace(i[0], str(self.s[i[0]]))
        self.task.setPlainText(self.a)
        self.vari = eval(str(self.formul))
        self.correct = round(eval(self.formul), 2)

    def check(self):
        self.answer_1 = round(float(self.answer.text()), 2)
        if self.answer_1 == self.correct:
            self.corr.setText(f'Молодец! Всё правильно.')
        else:
            self.corr.setText(f'Неверно. Правильный ответ - {self.correct}.')
        if self.let_explain.isChecked():
            self.explanation.setPlainText(self.ex)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec())