import os

# определяем функции для каждой команды
def create_folder(folder_name):
    try:
        os.mkdir(folder_name)
        print(f"Папка {folder_name} создана.")
    except FileExistsError:
        print(f"Папка {folder_name} уже существует.")

def delete_folder(folder_name):
    try:
        os.rmdir(folder_name)
        print(f"Папка {folder_name} создана.")
    except FileNotFoundError:
        print(f"Папка {folder_name} не найдена.")

def change_directory(directory):
    try:
        os.chdir(directory)
        print("Текущяя директория:", os.getcwd())
    except FileNotFoundError:
        print("Директория не найдена.")

def read_file(file_name):
    try:
        with open(file_name, 'r') as f:
            contents = f.read()
            print(contents)
    except FileNotFoundError:
        print(f"Файл {file_name} не найден.")

def edit_file(file_name):
    try:
        with open(file_name, 'w') as f:
            new_contents = input("Введите новые данные: ")
            f.write(new_contents)
            print(f"Файл {file_name} успешно отредактирован.")
    except FileNotFoundError:
        print(f"Файл {file_name} не найден.")

def move_file(original_path, new_path):
    try:
        os.rename(original_path, new_path)
        print("Файл успешно перемещён.")
    except FileNotFoundError:
        print("Файл не найден.")

def rename_file(original_name, new_name):
    try:
        os.rename(original_name, new_name)
        print(f"Файл {original_name} переименован в {new_name}.")
    except FileNotFoundError:
        print(f"Файл {original_name} не найден.")

# display available commands to user
print(f'''Доступные комманды:
          - создать папку
          - удалить папку
          - сменить директорию
          - чтение файла
          - редактирование файла
          - перемещение файла
          - переименование файла
          ''')


# get input from user and execute corresponding function
while True:
    command = input("Введите команду: ")
    if command == "создать папку" or command == "mkdir":
        folder_name = input("Введите название папки: ")
        create_folder(folder_name)
    elif command == "удалить папку" or command == "rm":
        folder_name = input("Введите название папки: ")
        delete_folder(folder_name)
    elif command == "сменить директорию" or command == "cd":
        directory = input("Введите директорию: ")
        change_directory(directory)
    elif command == "чтение файла" or command == "cat":
        file_name = input("Введите имя файла: ")
        read_file(file_name)
    elif command == "редактирование файла" or command == "vi":
        file_name = input("Введите имя файла: ")
        edit_file(file_name)
    elif command == "перемещение файла" or command == "mv":
        original_path = input("Введите текущий путь: ")
        new_path = input("Введите новый путь: ")
        move_file(original_path, new_path)
    elif command == "переименование файла" or command == "rename":
        original_name = input("Введите текущее название файла: ")
        new_name = input("Введите новое название файла: ")
        rename_file(original_name, new_name)
    else:
        print("Некорректная команда.")
