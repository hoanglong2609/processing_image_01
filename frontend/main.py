from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from api import api
from common import get_students, build_table, process_result, get_scores
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
ROLE = 0


class MyImage:
    base64_image = None
    path_image = None


def on_save_master(dialog, entries, screen, id=None):
    data = {}
    subjects = api.get('subject').json()

    for entry_key, value in entries.items():
        if entry_key == 'subject':
            cur_selection = list(value['object'].curselection())
            data['subject_ids'] = []
            for index, subject in enumerate(subjects):
                if index in cur_selection:
                    data['subject_ids'].append(subject['id'])
        else:
            data[entry_key] = value['object'].get()
    if screen == 'teacher' or screen == 'student':
        data['role'] = 1 if screen == 'teacher' else 0
        data['password'] = data['code']
        try:
            if id:
                data.pop('password', None)
                api.put(f'user/{id}', json=data)
                print(data)
            else:
                print(data)
                api.post(f'user/create', json=data)
        except:
            messagebox.showerror('info', 'create failed')
    else:
        try:
            if id:
                api.put(f'subject/{id}', json=data)
            else:
                api.post(f'subject/create', json=data)
        except:
            messagebox.showerror('info', 'create failed')

    dialog.destroy()
    master_page_detail(screen)


def dialog(screen, id=None):
    dialog = Toplevel()
    dialog.title('Dialog')
    dialog.geometry('340x350' if screen == 'subject' else '500x350')
    Label(dialog, **label_info).place(x=0, y=0, width=340 if screen == 'subject' else 500, height=350)

    default_data = None
    if id:
        if screen == 'subject':
            default_data = api.get(screen, {'id': id}).json()[0]
        else:
            default_data = api.get('user', {'id': id, 'role': 1 if screen == 'teacher' else 0}).json()[0]

    subjects = api.get('subject').json()
    if screen == 'subject':
        entries = {
            'name': {
                'object': Entry(dialog),
                'label': Label(dialog, text='name', **label_info),
                'place': {'width': 100, 'height': 25, 'x': 0, 'y': 50}
            },
            'password': {
                'object': Entry(dialog),
                'label': Label(dialog, text='password', **label_info),
                'place': {'width': 100, 'height': 25, 'x': 0, 'y': 100}
            }
        }
    else:
        entries = {
            'subject': {
                'object': Listbox(dialog, selectmode="multiple"),
                'label': Label(dialog, text='subject', **label_info),
                'place': {'width': 100, 'height': 25, 'x': 0, 'y': 0}
            },
            'code': {
                'object': Entry(dialog),
                'label': Label(dialog, text='code', **label_info),
                'place': {'width': 100, 'height': 25, 'x': 250, 'y': 0}
            },
            'name': {
                'object': Entry(dialog),
                'label': Label(dialog, text='name', **label_info),
                'place': {'width': 100, 'height': 25, 'x': 250, 'y': 100}
            },
            'mail': {
                'object': Entry(dialog),
                'label': Label(dialog, text='mail', **label_info),
                'place': {'width': 100, 'height': 25, 'x': 250, 'y': 200}
            }
        }

    for entry_key, value in entries.items():
        value['label'].place(**value['place'])
        if screen == 'subject':
            value['object'].place(
                width=200,
                height=25,
                x=value['place']['x'] + 100,
                y=value['place']['y']
            )
            if id:
                value['object'].insert(0, default_data[entry_key])
        else:
            value['object'].place(
                width=200,
                height=250 if entry_key == 'subject' else 25,
                x=0 if entry_key == 'subject' else value['place']['x'],
                y=50 if entry_key == 'subject' else value['place']['y'] + 50
            )
            if entry_key == 'subject':
                for index, subject in enumerate(subjects):
                    value['object'].insert(END, subject['name'])
                    if default_data and subject in default_data['subjects']:
                        value['object'].select_set(index)
            if id and entry_key != 'subject':
                value['object'].insert(0, default_data[entry_key])

    Button(
        dialog, **label_info, text='Save', command=lambda: on_save_master(dialog, entries, screen, id)
    ).place(x=250, y=300, height=25, width=100)


def master_page_detail(type):
    def handle_update(event):
        if table.item(table.focus()):
            id = table.item(table.focus())['values'][0]
            dialog(type, id)

    Label(window, **small_label_info).place(width=800, height=440, x=0, y=0)
    if type == 'subject':
        data = api.get(type).json()
        header_table = (
            {'name': 'id', 'text': 'Id', 'width': 80},
            {'name': type, 'text': type, 'width': 170}
        )
    else:
        data = api.get('user', {'role': 1 if type == 'teacher' else 0}).json()
        header_table = (
            {'name': 'id', 'text': 'Id', 'width': 40},
            {'name': 'code', 'text': 'code', 'width': 40},
            {'name': 'name', 'text': 'name', 'width': 130}
        )
    table = build_table(window, header_table, data, {'width': 760, 'height': 360, 'x': 20, 'y': 20})

    table.bind('<Double-1>', handle_update)

    Button(window, text='Add new', command=lambda: dialog(type)).place(
        width=70, height=25, x=700, y=400
    )
    Button(window, text='Back', command=master_page).place(
        width=70, height=25, x=600, y=400
    )


def master_page():
    Label(window, **small_label_info).place(width=800, height=440, x=0, y=0)
    Label(window, text='Master page', bg='#333333', fg="#FF3399", font=("Arial", 30)).place(
        x=0, y=0, width=800, height=50
    )
    buttons = {
        'subject': {
            'object': Button(window, text='subject', **label_info, command=lambda: master_page_detail('subject')),
            'place': {'width': 150, 'height': 50, 'x': 325, 'y': 60}
        },
        'student': {
            'object': Button(window, text='student', **label_info, command=lambda: master_page_detail('student')),
            'place': {'width': 150, 'height': 50, 'x': 325, 'y': 160}
        },
        'teacher': {
            'object': Button(window, text='teacher', **label_info, command=lambda: master_page_detail('teacher')),
            'place': {'width': 150, 'height': 50, 'x': 325, 'y': 260}
        }
    }

    for key, value in buttons.items():
        value['object'].place(**value['place'])

    Button(window, text='Back', **label_info, command=home_screen).place(**{'width': 150, 'height': 50, 'x': 325, 'y': 360})


def on_process_result(base64_image, is_grading, subject_combobox):
    subjects = api.get('subject').json()
    subject_name = subject_combobox.get()
    subject_id = list(filter(lambda x: x['name'] == subject_name, subjects))[0]['id']
    process_result(base64_image, is_grading, subject_id)


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

    def login_subject_screen(event):
        def on_login_subject():
            subject_name = subject_combobox.get()
            subject_id = list(filter(lambda x: x['name'] == subject_name, subjects))[0]['id']
            response = api.post('subject/login', json={'id': subject_id, 'password': password_entry.get()}).json()
            dialog.destroy()
            if response['code'] == 200:
                sub_btn['state'] = 'normal'
            else:
                messagebox.showerror('login', 'wrong password')

        dialog = Toplevel()
        dialog.title('Dialog')
        dialog.geometry('250x200')
        Label(dialog, **label_info).place(x=0, y=0, width=340, height=250)
        Label(dialog, **label_info, text='Enter subject password').place(x=0, y=0, width=250, height=50)
        password_entry = Entry(dialog, show="*", font=("Arial", 16))
        password_entry.place(**{'width': 200, 'height': 25, 'x': 20, 'y': 50})
        Button(dialog, text='Submit', command=on_login_subject).place(x=50, y=125, width=100, height=25)

    subject_combobox = ttk.Combobox(window)
    subjects = api.get('subject').json()
    subject_combobox['value'] = list(map(lambda x: x['name'], subjects))
    subject_combobox.place(width=150, height=25, x=210, y=12)
    subject_combobox.bind('<<ComboboxSelected>>', login_subject_screen)

    Button(
        window, text='Choose', bg="#FF3399", fg="#FFFFFF", font=("Arial", 12), command=on_open_file_dialog
    ).place(width=70, height=25, x=110, y=12)
    Button(
        window, text='Back', bg="#FF3399", fg="#FFFFFF", font=("Arial", 12), command=home_screen
    ).place(width=70, height=25, x=570, y=12)
    sub_btn = Button(
        window, text='Create result' if not is_grading else 'Grading', bg="#FF3399", fg="#FFFFFF", font=("Arial", 12),
        state='disabled',
        command=lambda: on_process_result(MyImage.base64_image, is_grading, subject_combobox)
    )
    sub_btn.place(
        width=100, height=25, x=670, y=10
    )
    # file_input = filedialog.askopenfilename(filetypes=[('Jpg Files', '*.jpg'), ('PNG Files', '*.png')])


def subject_page():
    def filter_students(event):
        item = subject_table.item(subject_table.focus())
        row = item['values']
        students = get_students({'subject': row[0], 'role': 0})
        students_table = build_table(
            window, header_student_table, students, {'width': 450, 'height': 400, 'x': 300, 'y': 20}
        )
        students_table.bind('<Double-1>', filter_scores)

    def filter_scores(event):
        dialog = Toplevel()
        dialog.title('score')
        dialog.geometry('340x350')
        item_sub = subject_table.item(subject_table.focus())
        item_stu = students_table.item(students_table.focus())
        sub = item_sub['values']
        stu = item_stu['values']
        scores = get_scores({'subject': sub[0], 'student': stu[0]})
        header_score_table = (
            {'name': 'id', 'text': 'Id', 'width': 100},
            {'name': 'code', 'text': 'code', 'width': 100},
            {'name': 'score', 'text': 'score', 'width': 100}
        )
        scores_table = build_table(
            dialog, header_score_table, scores, {'width': 300, 'height': 300, 'x': 20, 'y': 20})

        # scores_table = build_table(dialog, )

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
    students = get_students({'role': 0})

    subject_table = build_table(window, header_subject_table, subjects, {'width': 250, 'height': 380, 'x': 20, 'y': 20})
    students_table = build_table(window, header_student_table, students, {'width': 450, 'height': 380, 'x': 300, 'y': 20})

    subject_table.bind('<Double-1>', filter_students)
    students_table.bind('<Double-1>', filter_scores)

    # auto focus
    subject_table.focus(subject_table.get_children()[0])
    subject_table.selection_set(subject_table.get_children()[0])


def home_screen():
    # Label(window, width=800, height=440, **label_info).pack()
    Label(window, **label_info).place(width=800, height=440, x=0, y=0)
    Label(window, text='Home page', bg='#333333', fg="#FF3399", font=("Arial", 30)).place(
        x=0, y=0, width=800, height=50
    )
    if ROLE == 1:
        buttons = {
            'master': {
                'object': Button(window, text='master', **label_info, command=master_page),
                'place': {'width': 150, 'height': 50, 'x': 325, 'y': 60}
            },
            'create result': {
                'object': Button(window, text='create result', **label_info, command=lambda: processing_page(False)),
                'place': {'width': 150, 'height': 50, 'x': 325, 'y': 160}
            },
            'grading': {
                'object': Button(window, text='grading', **label_info, command=lambda: processing_page(True)),
                'place': {'width': 150, 'height': 50, 'x': 325, 'y': 260}
            },
            'subject': {
                'object': Button(window, text='subject', **label_info, command=subject_page),
                'place': {'width': 150, 'height': 50, 'x': 325, 'y': 360}
            }
        }
    else:
        buttons = {
            'subject': {
                'object': Button(window, text='subject', **label_info, command=subject_page),
                'place': {'width': 150, 'height': 50, 'x': 325, 'y': 150}
            }
        }
    for key, value in buttons.items():
        value['object'].place(**value['place'])


def login():
    global ROLE
    data = api.post(
        'user/login', json={'code': username_entry.get(), 'password': password_entry.get()}
    )

    if data.json()['code'] == 200:
        ROLE = data.json()['data']['role']
        home_screen()
    else:
        messagebox.showerror(title="Error", message="Invalid login.")


def get_password(code_entry, gmail_entry):
    api.get('user/forgot', {'code': code_entry.get(), 'gmail': gmail_entry.get()})
    messagebox.showinfo('info', 'check your mail')


def forgot():
    dialog = Toplevel()
    dialog.title('Dialog')
    dialog.geometry('320x250')
    Label(dialog, text='code').place(x=0, y=0, width=100, height=50)
    Label(dialog, text='gmail').place(x=0, y=50, width=100, height=50)
    code_entry = Entry(dialog)
    code_entry.place(x=100, y=12, width=200, height=25)
    gmail_entry = Entry(dialog)
    gmail_entry.place(x=100, y=62, width=200, height=25)
    Button(
        dialog, text='get password', command=lambda: get_password(code_entry, gmail_entry)
    ).place(x=50, y=162, width=200, height=25)


# Creating login page
login_label = Label(
    window, text="Login", bg='#333333', fg="#FF3399", font=("Arial", 30))
username_label = Label(
    window, text="Username", bg='#333333', fg="#FFFFFF", font=("Arial", 16))
username_entry = Entry(window, font=("Arial", 16))
password_entry = Entry(window, show="*", font=("Arial", 16))
username_entry.insert(0, 'admin')
password_entry.insert(0, 'admin')
password_label = Label(
    window, text="Password", bg='#333333', fg="#FFFFFF", font=("Arial", 16))
login_button = Button(
    window, text="Login", bg="#FF3399", fg="#FFFFFF", font=("Arial", 16), command=login)
forgot_button = Button(
    window, text="Forgot", bg="#FF3399", fg="#FFFFFF", font=("Arial", 16), command=forgot)

# Placing widgets on the screen
login_label.place(width=100, height=50, x=350, y=50)
username_label.place(width=100, height=50, x=250, y=150)
username_entry.place(width=200, height=30, x=350, y=160)
password_label.place(width=100, height=50, x=250, y=200)
password_entry.place(width=200, height=30, x=350, y=210)
login_button.place(width=100, height=50, x=350, y=300)
forgot_button.place(width=100, height=50, x=350, y=360)

window.mainloop()