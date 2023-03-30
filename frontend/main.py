from tkinter import *
from tkinter import messagebox
from api import api
from common import get_students, build_table, process_result
from tkinter import filedialog
from PIL import Image, ImageTk
import base64

window = Tk()
window.title("Login form")
window.geometry('800x440')
window.configure(bg='#333333')
size = {'width': 800, 'height': 440}
image_size = {'width': 700, 'height': 390}
label_info = {'bg': '#333333', 'fg': "#FFFFFF", 'font': ("Arial", 16)}
small_label_info = {'bg': '#333333', 'fg': "#FFFFFF", 'font': ("Arial", 12)}
testing_image = None


class MyImage:
    base64_image = None
    path_image = None


def on_process_result(base64_image, is_grading):
    process_result(base64_image, is_grading)


def on_open_file_dialog():
    global testing_image
    file_input = filedialog.askopenfilename(
        initialdir="../backend", filetypes=[('PNG Files', '*.png'), ('Jpg Files', '*.jpg'), ("all files", "*.*")]
    )

    # convert image to base64
    with open(file_input, "rb") as img_file:
        MyImage.base64_image = base64.b64encode(img_file.read())

    image = Image.open(file_input)
    image = image.resize((image_size['width'], image_size['height']), Image.ANTIALIAS)
    testing_image = ImageTk.PhotoImage(image)
    Label(window, image=testing_image).place(**image_size, x=60, y=50)


def processing_page(is_grading):
    Label(window, **small_label_info).place(width=800, height=440, x=0, y=0)
    Label(window, text='Choose File', **small_label_info).place(width=100, height=30, x=10, y=10)
    Button(
        window, text='Choose', bg="#FF3399", fg="#FFFFFF", font=("Arial", 12), command=on_open_file_dialog
    ).place(width=70, height=25, x=110, y=12)
    Button(
        window, text='Create result', bg="#FF3399", fg="#FFFFFF", font=("Arial", 12),
        command=lambda: on_process_result(MyImage.base64_image, is_grading)
    ).place(
        width=100, height=25, x=670, y=10
    )
    # file_input = filedialog.askopenfilename(filetypes=[('Jpg Files', '*.jpg'), ('PNG Files', '*.png')])


def subject_page():
    def filter_students(event):
        item = subject_table.item(subject_table.focus())
        row = item['values']
        students = get_students({'subject': row[0]})
        students_table = build_table(
            window, header_student_table, students, {'width': 450, 'height': 400, 'x': 300, 'y': 20}
        )

    Label(window, **label_info).place(width=800, height=440, x=0, y=0)
    Button(window, text='Back', command=home_screen).place(width=70, height=30, x=700, y=405)
    # subject_table = ttk.Treeview(window)
    header_subject_table = (
        {'name': 'id', 'text': 'Id', 'width': 80},
        {'name': 'subject', 'text': 'subject', 'width': 170}
    )

    header_student_table = (
        {'name': 'id', 'text': 'Id', 'width': 80},
        {'name': 'code', 'text': 'code', 'width': 170},
        {'name': 'student', 'text': 'student', 'width': 200}
    )

    subjects = api.get('subject').json()
    students = get_students()

    subject_table = build_table(window, header_subject_table, subjects, {'width': 250, 'height': 380, 'x': 20, 'y': 20})
    students_table = build_table(window, header_student_table, students, {'width': 450, 'height': 380, 'x': 300, 'y': 20})

    subject_table.bind('<Double-1>', filter_students)

    # auto focus
    subject_table.focus(subject_table.get_children()[0])
    subject_table.selection_set(subject_table.get_children()[0])


def home_screen():
    Label(window, width=800, height=440, **label_info).pack()
    Label(window, **label_info).place(width=800, height=440, x=0, y=0)
    Label(window, text='Home page', bg='#333333', fg="#FF3399", font=("Arial", 30)).place(
        x=0, y=0, width=800, height=50
    )
    buttons = {
        'create result': {
            'object': Button(window, text='create result', **label_info, command=lambda: processing_page(False)),
            'place': {'width': 150, 'height': 50, 'x': 325, 'y': 150}
        },
        'grading': {
            'object': Button(window, text='grading', **label_info, command=lambda: processing_page(True)),
            'place': {'width': 150, 'height': 50, 'x': 325, 'y': 250}
        },
        'subject': {
            'object': Button(window, text='subject', **label_info, command=subject_page),
            'place': {'width': 150, 'height': 50, 'x': 325, 'y': 350}
        }
    }

    for key, value in buttons.items():
        value['object'].place(**value['place'])


def login():
    data = api.post(
        'user/login', json={'code': username_entry.get(), 'password': password_entry.get()}
    )

    if data.json()['code'] == 200:
        home_screen()
    else:
        messagebox.showerror(title="Error", message="Invalid login.")


# Creating login page
login_label = Label(
    window, text="Login", bg='#333333', fg="#FF3399", font=("Arial", 30))
username_label = Label(
    window, text="Username", bg='#333333', fg="#FFFFFF", font=("Arial", 16))
username_entry = Entry(window, font=("Arial", 16))
password_entry = Entry(window, show="*", font=("Arial", 16))
username_entry.insert(0, '20160320')
password_entry.insert(0, '20160320')
password_label = Label(
    window, text="Password", bg='#333333', fg="#FFFFFF", font=("Arial", 16))
login_button = Button(
    window, text="Login", bg="#FF3399", fg="#FFFFFF", font=("Arial", 16), command=login)

# Placing widgets on the screen
login_label.place(width=100, height=50, x=350, y=50)
username_label.place(width=100, height=50, x=250, y=150)
username_entry.place(width=200, height=30, x=350, y=160)
password_label.place(width=100, height=50, x=250, y=200)
password_entry.place(width=200, height=30, x=350, y=210)
login_button.place(width=100, height=50, x=350, y=300)

window.mainloop()

# SETTING = {'width': 800, 'height': 440, 'bg': '#333333'}
#
#
# class SampleApp(Tk):
#
#     def __init__(self, *args, **kwargs):
#         Tk.__init__(self, *args, **kwargs)
#
#         self.title_font = Font(family='Helvetica', size=18, weight="bold", slant="italic")
#
#         # the container is where we'll stack a bunch of frames
#         # on top of each other, then the one we want visible
#         # will be raised above the others
#         container = Frame(self, **SETTING)
#         # container.pack(side="top", fill="both", expand=True)
#         container.pack()
#         container.grid_rowconfigure(0, weight=2)
#         container.grid_columnconfigure(0, weight=2)
#
#         self.frames = {}
#         for F in (LoginPage, PageHome, SubjectPage):
#             page_name = F.__name__
#             frame = F(parent=container, controller=self)
#             self.frames[page_name] = frame
#
#             # put all of the pages in the same location;
#             # the one on the top of the stacking order
#             # will be the one that is visible.
#             frame.grid(row=0, column=0, sticky="nsew")
#
#         self.show_frame("LoginPage")
#
#     def show_frame(self, page_name):
#         '''Show a frame for the given page name'''
#         frame = self.frames[page_name]
#         frame.tkraise()
#
#
# class LoginPage(Frame):
#
#     def __init__(self, parent, controller):
#         Frame.__init__(self, parent, **SETTING)
#         self.controller = controller
#
#         # Creating widgets
#         login_label = Label(
#             self, text="Login", bg='#333333', fg="#FF3399", font=("Arial", 30))
#         username_label = Label(
#             self, text="Username", bg='#333333', fg="#FFFFFF", font=("Arial", 16))
#         username_entry = Entry(self, font=("Arial", 16))
#         password_entry = Entry(self, show="*", font=("Arial", 16))
#         username_entry.insert(0, '20160320')
#         password_entry.insert(0, '20160320')
#         password_label = Label(
#             self, text="Password", bg='#333333', fg="#FFFFFF", font=("Arial", 16))
#         login_button = Button(
#             self, text="Login", bg="#FF3399", fg="#FFFFFF", font=("Arial", 16),
#             command=lambda: self.login(username_entry.get(), password_entry.get())
#         )
#
#         # Placing widgets on the screen
#         login_label.grid(row=0, column=0, columnspan=2, sticky="news", pady=40)
#         username_label.grid(row=1, column=0)
#         username_entry.grid(row=1, column=1, pady=20)
#         password_label.grid(row=2, column=0)
#         password_entry.grid(row=2, column=1, pady=20)
#         login_button.grid(row=3, column=0, columnspan=2, pady=30)
#
#     def login(self, code, password):
#         data = api.post(
#             'user/login', json={'code': code, 'password': password}
#         )
#         if data.json()['code'] == 200:
#             self.controller.show_frame('PageHome')
#         else:
#             messagebox.showerror(title="Error", message="Invalid login.")
#
#
# class PageHome(Frame):
#     color = {'bg': '#333333', 'fg': "#FFFFFF"}
#     color_btn = {'bg': '#FF3399', 'fg': "#FFFFFF"}
#
#     def __init__(self, parent, controller):
#         Frame.__init__(self, parent, **SETTING)
#         self.controller = controller
#         label = Label(self, text="Home page", font=controller.title_font, **self.color)
#         grading = Button(self, text="Grading", **self.color_btn, command=lambda: controller.show_frame("StartPage"))
#         subjects = Button(self, text="Subjects", **self.color_btn, command=lambda: controller.show_frame("SubjectPage"))
#
#         label.grid(row=0, column=1, pady=20, padx=100)
#         grading.grid(row=1, column=1, pady=20, padx=100)
#         subjects.grid(row=2, column=1, pady=20, padx=100)
#
#
# class SubjectPage(Frame):
#
#     def __init__(self, parent, controller):
#         Frame.__init__(self, parent, **SETTING)
#         self.controller = controller
#         label = Label(self, text="Subjects", font=controller.title_font)
#         label.pack(side="top", fill="x", pady=10)
#         Label(self, text='test').place(x=10, y=10, width=100, height=30)
#         # button = Button(self, text="Go to the start page",
#         #                    command=lambda: controller.show_frame("StartPage"))
#         # button.pack()
#
#
# if __name__ == "__main__":
#     app = SampleApp()
#     app.title("Login form")
#     # app.geometry('800x440')
#     app.configure(bg='#333333')
#     app.mainloop()
