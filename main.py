import re
import csv
from logger_n2 import logger


@logger('contacts_upd.log')
def read_file(file_name):
    with open(file_name, encoding='utf-8') as f:
        rows = csv.reader(f, delimiter=',')
        contacts_list = list(rows)
    return contacts_list


@logger('contacts_upd.log')
def format_full_name(contacts_list):
    pattern = r'^([А-ЯЁа-яё]+)\s*(\,?)([А-ЯЁа-яё]+)\s*(\,?)([А-ЯЁа-яё]*)(\,?)(\,?)(\,?)'
    substitution = r'\1\2\8\3\4\7\5\6'
    contacts_list_updated = []
    for card in contacts_list:
        card_as_string = ','.join(card)
        formatted_card = re.sub(pattern, substitution, card_as_string)
        card_as_list = formatted_card.split(',')
        contacts_list_updated.append(card_as_list)
    return contacts_list_updated


@logger('contacts_upd.log')
def format_number(contacts_list):
    pattern = r'(\+7|8)?[\s\-\(]*(\d{3})[\s\-\)]*(\d{3})[\s\-]*(\d{2})[\s\-]*(\d{2})' \
              r'(\s*)(\(*)(доб)*(\.*)(\s*)(\d+)*(\)*)'
    substitution = r'+7(\2)\3-\4-\5\6\8\9\11'
    contacts_list_updated = []
    for card in contacts_list:
        card_as_string = ','.join(card)
        formatted_card = re.sub(pattern, substitution, card_as_string)
        card_as_list = formatted_card.split(',')
        contacts_list_updated.append(card_as_list)
    return contacts_list_updated


@logger('contacts_upd.log')
def join_duplicates(contacts_list):
    dict_ = {}
    contacts_list_updated = []
    for i in contacts_list:
        if i[0]+i[1] not in dict_:
            dict_[i[0]+i[1]] = i
        else:
            dict_[i[0]+i[1]] = [y if x == '' else x for x, y in zip(dict_[i[0]+i[1]], i)]
    for card in dict_.values():
        contacts_list_updated.append(card)
    return contacts_list_updated


@logger('contacts_upd.log')
def write_file(contacts_list):
    with open('phonebook.csv', 'w', encoding='utf-8', newline='') as f:
        datawriter = csv.writer(f, delimiter=',')
        datawriter.writerows(contacts_list)


if __name__ == '__main__':
    contacts = read_file('phonebook_raw.csv')
    contacts = format_full_name(contacts)
    contacts = format_number(contacts)
    contacts = join_duplicates(contacts)
    write_file(contacts)
