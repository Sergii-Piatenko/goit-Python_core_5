import os
import re
import shutil
import sys


def delete_folder(path):

    important_folders = ('images', 'video', 'documents',
                         'audio', 'archives', 'unknown extensions')

    get_items = os.listdir(path)

    for folder in get_items:
        if not folder in important_folders:
            shutil.rmtree(os.path.join(path, folder))


def normalize(file_name):

    result = ''
    name, extension = os.path.splitext(file_name)

    for letter in name:
        if letter.isdigit() or re.findall(r'[A-z]', letter):
            result += letter
        else:
            for key, value in TRANS.items():
                if not re.findall(r'[А-яёЁґҐ]', letter):
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
    unknown_extensions = True
    name_file = os.path.basename(path)
    file_path = os.path.dirname(path)
    end_folder = os.path.split(file_path)[-1]

    if re.findall(r'[А-яёЁґҐ]+', name_file):
        name_file = normalize(name_file)

    for folder, extension in folders.items():

        if os.path.join(path_root, folder) in path:
            unknown_extensions = False
            continue

        if path.upper().endswith(extension):

            folder_destination = os.path.join(path_root, folder)
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
            unknown_extensions = False

    if unknown_extensions:
        folder_destination = os.path.join(path_root, 'unknown extensions')
        try:
            os.mkdir(os.path.join(folder_destination), mode=0o777, dir_fd=None)
            shutil.move(path, os.path.join(folder_destination, name_file))
        except FileExistsError:
            shutil.move(path, os.path.join(folder_destination, name_file))


def search_for_items(path, reset=True):

    global list_files

    if reset:
        list_files = []

    get_items = os.listdir(path)

    for item in get_items:

        if os.path.isdir(os.path.join(path, item)):
            search_for_items(os.path.join(path, item), reset=False)

        else:
            list_files.append(os.path.join(path, item))

    return list_files


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

    path_root = path
    path_files = search_for_items(path)
    for item in path_files:
        sorted_files(item)

    delete_folder(path_root)

else:
    print('Not correct path')
