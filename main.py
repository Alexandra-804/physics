import random
import sys
import sqlite3
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        uic.loadUi('window.ui', self)
        connect = sqlite3.connect('physics')
        self.cur = connect.cursor()
        self.Item_btn.clicked.connect(self.Item)
        self.title_btn.clicked.connect(self.go_task)
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
        print(self.curr_title)
        self.a = self.curr_title[random.randrange(len(self.curr_title))]
        self.values = self.cur.execute(f"""SELECT exersises.variables FROM exersises 
                WHERE exersise = '{self.a}'""").fetchall()[0]
        self.values = self.values[0].split('@')
        self.values = [i.split(';') for i in self.values]
        print(self.values)
        self.s = {}
        for i in range(len(self.values)):
            v_1 = random.randrange(int(self.values[i][1]), int(self.values[i][2]) + 1,
                                   int(self.values[i][3]))
            self.s[self.values[i][0]] = v_1
        print(self.s)
        for k in self.s:
            print(k)
            print(self.s[k])
            self.a.replace(k, str(self.s[k]))
        self.task.setPlainText(self.a)





if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec())