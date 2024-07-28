from datetime import datetime, timezone

from app.db.models.model import (
    Worker,
    Organization
)
from app.db.session import get_session, session_merge


class Sql:
    def insert_worker(self, info):
        with get_session() as session:
            if not info['Номер телефона'] is None:
                is_comm_org = True
                if info['Организация']['Тип организации'] == 'Государственная':
                    is_comm_org = False

                org = session_merge(session,
                                    Organization(name=info['Организация']['Название организации'], ogrn=info['Организация']['ОГРН'],
                                                 kpp=info['Организация']['КПП'],
                                                 inn=info['Организация']['ИНН'],
                                                 is_comm_org=is_comm_org,
                                                 mail_address=info['Организация']['Почтовый адрес'],
                                                 email=info['Организация']['Электронная почта']),
                                    Organization.ogrn == info['Организация']['ОГРН'])
                if org:
                    session.flush()
                    session_merge(session,
                                  Worker(last_name=info['Фамилия'], first_name=info['Имя'], patronymic=info['Отчество'],
                                         post=info['Должность'], email=info['Электронная почта'],
                                         phone=info['Номер телефона'], organization_ogrn=org.ogrn),
                                  Worker.phone == info['Номер телефона'])
                else:
                    raise Exception("У сотрудника не указана организация - " + str(info))

                session.commit()
            else:
                raise Exception("У сотрудника не указан номер телефона - " + str(info))

    def insert_workers(self, info):
        for worker_num in info['Сотрудники'].keys():
            worker_info = {'Организация': info['Организация'], **info['Сотрудники'][worker_num]}
            try:
                self.insert_worker(worker_info)
            except Exception as e:
                print(str(e))

    def get_workers(self):
        with get_session() as session:
            workers = session.query(Worker).all()
            workers_info = list()
            for worker in workers:
                workers_info.append({'Фамилия': worker.last_name,
                                     'Имя': worker.first_name,
                                     'Отчество': worker.patronymic,
                                     'Должность': worker.post,
                                     'Электронная почта': worker.email,
                                     'Номер телефона': worker.phone,
                                     'Организация': worker.organization.name})
            return workers_info
