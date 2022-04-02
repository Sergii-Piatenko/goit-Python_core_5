import os
import re
import shutil
import sys


def delete_empty_folder(path):

    for i in path:
        os.rmdir(i)


def normalize(file_name):

    result = ''
    name, extension = os.path.splitext(file_name)

    for letter in name:

        for key, value in TRANS.items():

            if letter.isdigit():
                result += letter
                break

            elif re.findall(r'[A-z]', letter):
                result += letter
                break

            elif not re.findall(r'[А-яёЁіІїЇґҐ]', letter):
                result += '_'
                break

            elif ord(letter) == key:
                result += value
                break

    return result + extension


def sorted_files(path):

    folders = {'images': ('JPEG', 'PNG', 'JPG', 'SVG'),
               'video': ('AVI', 'MP4', 'MOV', 'MKV'),
               'documents': ('DOC', 'DOCX', 'TXT', 'PDF', 'XLS', 'XLSX', 'PPTX', 'PPT'),
               'audio': ('MP3', 'OGG', 'WAV', 'AMR'),
               'archives': ('ZIP', 'GZ', 'TAR', 'RAR'), }

    for folder, extension in folders.items():

        if path.upper().endswith(extension):

            name_file = os.path.basename(path)
            file_path = os.path.dirname(path)
            end_folder = os.path.split(file_path)[-1]

            if re.findall(r'[А-яёЁґҐ]+', name_file):
                name_file = normalize(name_file)

            if end_folder == folder:
                folder_destination = file_path
                shutil.move(path, os.path.join(
                    folder_destination, name_file))
            else:
                folder_destination = os.path.join(file_path, folder)
                try:
                    os.mkdir(folder_destination, mode=0o777, dir_fd=None)
                    shutil.move(path, os.path.join(
                        folder_destination, name_file))
                except FileExistsError:
                    shutil.move(path, os.path.join(
                        folder_destination, name_file))

            if folder == 'archives':
                unpack_archive(os.path.join(
                    folder_destination, name_file))


def search_for_items(path, reset=True):

    global list_files, empty_folders

    if reset:
        list_files = []
        empty_folders = []

    get_items = os.listdir(path)

    for item in get_items:

        if os.path.isdir(os.path.join(path, item)):

            if not os.listdir(os.path.join(path, item)):
                empty_folders.append(os.path.join(path, item))
            search_for_items(os.path.join(path, item), reset=False)

        else:
            list_files.append(os.path.join(path, item))

    return [list_files, empty_folders]


def unpack_archive(path):

    name_file = os.path.basename(path)
    file_path = os.path.dirname(path)
    name = os.path.splitext(name_file)[0]
    shutil.unpack_archive(path, os.path.join(file_path, name))


CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
TRANSLATION = ("a", "b", "v", "h", "d", "e", "e", "zh", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "kh", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ja", "je", "i", "i", "g")

TRANS = {}

for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION):

    TRANS[ord(c)] = l
    TRANS[ord(c.upper())] = l.upper()

path = sys.argv[1]

if os.path.exists(path):

    path_files, path_empty_folders = search_for_items(path)
    for item in path_files:
        sorted_files(item)

    if path_empty_folders:
        delete_empty_folder(path_empty_folders)

else:
    print('Not correct path')
