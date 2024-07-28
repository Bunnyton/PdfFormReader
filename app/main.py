import os.path

import PyPDF2
import re
import pprint

from db.sql import Sql
from db.create_db import create_db


def extract_form_data(pdf_path):
    # Открываем PDF файл
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        res = dict()
        res['Организация'] = dict()
        res['Сотрудники'] = dict()
        for key, val in reader.get_fields().items():
            if '/V' in val.keys():
                if key == 'ОГРН' or key == 'ИНН' or key == 'КПП' or key == 'Почтовый адрес' or key == 'Электронная почта' or key == 'Название организации':
                    res['Организация'][key] = val['/V']
                elif key == 'Тип организации':
                    if val['/V'] == '/0':
                        res['Организация'][key] = 'Государственная'
                    else:
                        res['Организация'][key] = 'Коммерческая'
                elif key == 'орядковый номер':  # почему-то так считывает название поля
                    pass
                else:
                    numsearch = re.findall(r'\d+', key)
                    if numsearch:
                        num = numsearch[0]
                        if num not in res['Сотрудники'].keys():
                            res['Сотрудники'][num] = {'Фамилия': None,
                                                      'Имя': None,
                                                      'Отчество': None,
                                                      'Должность': None,
                                                      'Электронная почта': None,
                                                      'Номер телефона': None}
                        res['Сотрудники'][num][key.replace(num, '')] = val['/V']
        return res


def get_pdf_files(path):
    if not os.path.exists(path):
        raise ValueError(f"Путь {path} не существует")
    if os.path.isdir(path):
        return ['/'.join([path, f]).replace('//', '/') for f in os.listdir(path) if f.endswith('.pdf') and os.path.isfile(os.path.join(path, f))]
    else:
        return [path]

if __name__ == "__main__":
    pdf_path = r"C:\Users\Антон\Мои документы\практика"
    #pdf_path = str(input('Введите путь до pdf форм(ы):'))

    create_db()
    sql = Sql()

    pdf_files = get_pdf_files(pdf_path)

    for pdf_file in pdf_files:
        form_data = extract_form_data(pdf_file)
        # pprint.pprint(form_data)
        sql.insert_workers(form_data)

    pprint.pprint(sql.get_workers())
