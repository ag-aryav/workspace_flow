from PyQt5.QtWidgets import *
from PyQt5 import uic
import tkinter as tk
from tkinter import messagebox
import requests
import urllib

# urllib.parse.quote("not_full_parameter_only_value")


class Login:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("WorkspaceFlow Login")
        self.root.geometry("300x150")

        self.label1 = tk.Label(self.root, text="username", font=("Ariel", 8))
        self.label1.pack()

        self.username = tk.Entry(self.root, width=100)
        self.username.pack()

        self.label2 = tk.Label(self.root, text="password", font=("Ariel", 8))
        self.label2.pack()

        self.password = tk.Entry(self.root, width=100, show="•")
        self.password.pack()

        self.login_button = tk.Button(self.root, width=100, text='Login', command=self.login)
        self.login_button.pack()

        self.root.mainloop()

    def login(self):
        response = requests.get("https://script.google.com/macros/s/AKfycbyNW6ouAPsSeyK5zJcj8xSmnvnBjoNSrfp-ZNmkr35549qF_JNdvC33jCM8FSl18O4/exec?job=users")
        users = response.json()['data']
        usernames = {}
        for i in users:
            if i[0] == 'Name':
                continue

            else:
                usernames[i[0]] = str(i[1])
        try:
            if usernames[self.username.get()] == self.password.get():
                self.root.destroy()
                workspace_app = QApplication([])
                window = Workspace()
                workspace_app.exec_()
            else:
                messagebox.showinfo("", "incorrect PASSWORD")

        except Exception as E:
            print(E)
            messagebox.showinfo("", "ERROR OCCURED")


class Workspace(QMainWindow):
    def __init__(self):
        super(Workspace, self).__init__()
        uic.loadUi("WorkspaceFlow.ui", self)
        self.show()

        self.savedb_button.clicked.connect(self.newHidingPlace)
        self.RefreshButton.clicked.connect(self.refreshHPs)
        self.viewHP.setColumnWidth(0, 200)
        self.viewHP.setColumnWidth(1, 200)
        self.viewHP.setColumnWidth(2, 400)
        self.refreshHPs()

    def refreshHPs(self):
        response = requests.get("https://script.google.com/macros/s/AKfycbyNW6ouAPsSeyK5zJcj8xSmnvnBjoNSrfp-ZNmkr35549qF_JNdvC33jCM8FSl18O4/exec?job=view_hp")
        HPs = response.json()['data']
        self.viewHP.setRowCount(len(HPs))
        row = 0
        for i in range(1, len(HPs)):
            self.viewHP.setItem(row, 0, QTableWidgetItem(HPs[i][0]))
            self.viewHP.setItem(row, 1, QTableWidgetItem(HPs[i][1]))
            self.viewHP.setItem(row, 2, QTableWidgetItem(HPs[i][2]))
            row += 1

        qtmessagebox = QMessageBox()
        qtmessagebox.setText("Refreshed")
        qtmessagebox.exec_()

    def newHidingPlace(self):
        hiding_place = urllib.parse.quote(self.HPName.text())
        hiding_place_image = urllib.parse.quote(self.HPLink.text())
        HPDescription = urllib.parse.quote(self.Description.toPlainText())
        # urllib.parse.quote("not_full_parameter_only_value")
        data_line = str([hiding_place, hiding_place_image, HPDescription])
        response = requests.get(f"https://script.google.com/macros/s/AKfycbyNW6ouAPsSeyK5zJcj8xSmnvnBjoNSrfp-ZNmkr35549qF_JNdvC33jCM8FSl18O4/exec?job=add&data={data_line}")
        print(response.json)
        qtmessagebox = QMessageBox()
        qtmessagebox.setText("Saved to cloud.")
        qtmessagebox.exec_()


def main():
    Login()


if __name__ == '__main__':
    main()
