from api import api
import urllib.parse
from tkinter import ttk
from tkinter import *


def get_students(conditions: dict = None):
    url = 'user'
    if conditions:
        url = f'{url}/?{urllib.parse.urlencode(conditions)}'

    students = api.get(url).json()
    students = list(
        map(lambda x: {'id': x['id'], 'code': x['code'], 'name': x['name']}, students)
    )

    return students


def get_scores(conditions: dict = None):
    url = 'score'
    if conditions:
        url = f'{url}/?{urllib.parse.urlencode(conditions)}'

    scores = api.get(url).json()
    scores = list(
        map(lambda x: {'id': x['id'], 'code': x['code'], 'score': x['score']}, scores)
    )

    return scores


def bind_data_to_table(window, cols, rows):
    table = ttk.Treeview(window)

    table['columns'] = list(map(lambda x: x['name'], cols))

    table.column("#0", width=0, stretch=NO)
    for col in cols:
        table.column(col['name'], anchor=CENTER, width=col['width'])

    # table.heading("#0", text="", stretch=CENTER)
    for col in cols:
        table.heading(col['name'], anchor=CENTER, text=col['text'])

    for row in rows:
        table.insert(parent='', index='end', text='', values=list(row.values()))

    return table


def build_table(window, cols, rows, place: dict):
    table = bind_data_to_table(window, cols, rows)
    table.place(**place)
    return table


def process_result(image, is_grading=True, subject_id=None):
    data = api.post(
        'processing_image/base64_img',
        json={
            'image': image.decode("utf-8"),
            'is_result': not is_grading,
            'subject': subject_id
        }
    )

    print(data.json())
