# import csv
# def y():
#     filename='StudentDetails\StudentDetails.csv'
#     with open(filename, 'r') as f:
#         reader=csv.reader(f)
#         first_row=next(reader)
#     with open(filename, 'w',newline='') as f:
#         writer=csv.writer(f)
#         writer.writerow(first_row)
#     f.close()
# import the new login page file
from tkinter import * 
def login():
    # create a new window
    login_window = Toplevel(root)
    login_window.title("Login")

    # create the username label and entry
    username_label = Label(login_window, text="Username")
    username_label.pack()
    username_entry = Entry(login_window)
    username_entry.pack()

    # create the password label and entry
    password_label = Label(login_window, text="Password")
    password_label.pack()
    password_entry = Entry(login_window, show="*")
    password_entry.pack()

    # create the login button
    login_button = Button(login_window, text="Login")
    login_button.pack()
