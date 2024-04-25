main_menu = '''\nГлавное меню:
    1. Открыть файл
    2. Сохранить файл
    3. Показать контакты
    4. Добавить контакт
    5. Найти контакт
    6. Изменить контакт
    7. Удалить контакт
    8. Выход\n'''

input_choice = 'Выберите пункт меню: '
input_index = 'Введите индекс контакта: '
input_search = 'Что будем искать: '
input_change = 'Какой контакт будем менять: '
input_delete = 'Какой контакт будем удалять: '
input_new_contact = 'Введите данные нового контакта: '
new_contact = {'name': 'Введите имя: ',
               'phone': 'Введите номер телефона: ',
               'comment': 'Введите комментарий: '}
change_contact = 'Введите новые данные или оставьте пустым, чтоб не менять: '

load_successful = 'Телефонная книга успешно открыта!'
save_successful = 'Телефонная книга успешно сохранена!'
pb_empty = 'Телефонная книга пуста или не загружена!'
no_saved_book = 'В телефонной книге есть не сохраненные изменения Сохранить? '
goodbye = 'Хорошего дня!'


def delete_contact(name: str) -> str:
    return f'Контакт {name} успешно удален!'


def confirm_delete(name: str) -> str:
    return f'Вы точно хотите удалить контакт {name}?'


def new_contact_successful(name: str):
    return f'Контакт {name} успешно добавлен'


def change_successful(name: str) -> str:
    return f'Контакт {name} успешно изменен!'


def empty_search(word) -> str:
    return f'Контакты содержащие слово "{word}" не найдены'