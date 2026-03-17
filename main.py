import os
import shutil
import stat
import fnmatch
from datetime import datetime

class FileManager:
    def __init__(self):
        self.current_path = os.getcwd()

    def get_current_path(self):
        return os.getcwd()

    def list_contents(self):
        """Просмотр содержимого текущего каталога"""
        print(f"\n--- Содержимое: {self.get_current_path()} ---")
        try:
            items = os.listdir('.')
            for item in items:
                item_type = "[DIR]" if os.path.isdir(item) else "[FILE]"
                print(f"{item_type} {item}")
        except PermissionError:
            print("Ошибка: Нет прав доступа к этой папке.")

    def create_directory(self, name):
        """Создание каталога"""
        try:
            os.mkdir(name)
            print(f"Каталог '{name}' создан.")
        except FileExistsError:
            print("Ошибка: Каталог уже существует.")
        except Exception as e:
            print(f"Ошибка: {e}")

    def create_file(self, name, content=""):
        """Создание файла"""
        try:
            with open(name, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Файл '{name}' создан.")
        except Exception as e:
            print(f"Ошибка: {e}")

    def view_file(self, name):
        """Просмотр файла"""
        try:
            with open(name, 'r', encoding='utf-8') as f:
                print(f"\n--- Содержимое {name} ---")
                print(f.read())
        except Exception as e:
            print(f"Ошибка чтения: {e}")

    def edit_file(self, name):
        """Редактирование файла (перезапись содержимого)"""
        print(f"Введите новое содержимое для {name} (нажмите Enter для подтверждения):")
        content = input()
        try:
            with open(name, 'w', encoding='utf-8') as f:
                f.write(content)
            print("Файл обновлен.")
        except Exception as e:
            print(f"Ошибка записи: {e}")

    def copy_item(self, source, destination):
        """Копирование файла или папки"""
        try:
            if os.path.isdir(source):
                shutil.copytree(source, destination)
            else:
                shutil.copy2(source, destination)
            print(f"Скопировано: {source} -> {destination}")
        except Exception as e:
            print(f"Ошибка копирования: {e}")

    def move_item(self, source, destination):
        """Перемещение/Переименование"""
        try:
            shutil.move(source, destination)
            print(f"Перемещено: {source} -> {destination}")
        except Exception as e:
            print(f"Ошибка перемещения: {e}")

    def delete_item(self, name):
        """Удаление файла или папки"""
        try:
            if os.path.isdir(name):
                shutil.rmtree(name)
            else:
                os.remove(name)
            print(f"Удалено: {name}")
        except Exception as e:
            print(f"Ошибка удаления: {e}")

    def get_properties(self, name):
        """Просмотр свойств (размер, дата изменения, права)"""
        try:
            stat_info = os.stat(name)
            print(f"\n--- Свойства: {name} ---")
            print(f"Размер: {stat_info.st_size} байт")
            print(f"Дата изменения: {datetime.fromtimestamp(stat_info.st_mtime)}")
            print(f"Права (oct): {oct(stat_info.st_mode)}")
        except Exception as e:
            print(f"Ошибка получения свойств: {e}")

    def change_permissions(self, name, mode):
        """Изменение прав доступа (chmod)"""
        try:
            # mode должен быть в восьмеричном формате, например 0o755
            os.chmod(name, mode)
            print(f"Права для {name} изменены на {oct(mode)}.")
        except Exception as e:
            print(f"Ошибка изменения прав (возможно, ОС не поддерживает): {e}")

    def search(self, pattern):
        """Поиск файлов по маске"""
        print(f"\n--- Поиск по маске '{pattern}' ---")
        found = False
        for root, dirs, files in os.walk('.'):
            for name in files:
                if fnmatch.fnmatch(name, pattern):
                    print(os.path.join(root, name))
                    found = True
            # Можно искать и папки, если нужно
            for name in dirs:
                if fnmatch.fnmatch(name, pattern):
                    print(os.path.join(root, name) + "/")
                    found = True
        if not found:
            print("Ничего не найдено.")

    def change_directory(self, path):
        """Переход в каталог"""
        try:
            os.chdir(path)
            self.current_path = os.getcwd()
            print(f"Переход в: {self.current_path}")
        except Exception as e:
            print(f"Ошибка перехода: {e}")

def main():
    fm = FileManager()
    
    while True:
        print(f"\n=== ФАЙЛОВЫЙ МЕНЕДЖЕР ===")
        print(f"Путь: {fm.get_current_path()}")
        print("1. Просмотреть содержимое")
        print("2. Создать папку")
        print("3. Создать файл")
        print("4. Просмотреть файл")
        print("5. Редактировать файл")
        print("6. Копировать")
        print("7. Переместить/Переименовать")
        print("8. Удалить")
        print("9. Свойства объекта")
        print("10. Изменить права доступа")
        print("11. Поиск")
        print("12. Перейти в папку (cd)")
        print("13. Выйти")
        
        choice = input("Выберите действие: ")
        
        if choice == '1':
            fm.list_contents()
        elif choice == '2':
            name = input("Имя папки: ")
            fm.create_directory(name)
        elif choice == '3':
            name = input("Имя файла: ")
            content = input("Содержимое (необязательно): ")
            fm.create_file(name, content)
        elif choice == '4':
            name = input("Имя файла: ")
            fm.view_file(name)
        elif choice == '5':
            name = input("Имя файла: ")
            fm.edit_file(name)
        elif choice == '6':
            src = input("Источник: ")
            dst = input("Назначение: ")
            fm.copy_item(src, dst)
        elif choice == '7':
            src = input("Источник: ")
            dst = input("Назначение (новый путь/имя): ")
            fm.move_item(src, dst)
        elif choice == '8':
            name = input("Имя для удаления: ")
            confirm = input(f"Вы уверены, что хотите удалить {name}? (yes/no): ")
            if confirm.lower() == 'yes':
                fm.delete_item(name)
        elif choice == '9':
            name = input("Имя объекта: ")
            fm.get_properties(name)
        elif choice == '10':
            name = input("Имя объекта: ")
            try:
                mode = int(input("Режим прав (например 755): "), 8)
                fm.change_permissions(name, mode)
            except ValueError:
                print("Неверный формат числа.")
        elif choice == '11':
            pattern = input("Маска поиска (например *.txt): ")
            fm.search(pattern)
        elif choice == '12':
            path = input("Путь к папке: ")
            fm.change_directory(path)
        elif choice == '13':
            print("Выход из программы.")
            break
        else:
            print("Неверный выбор.")

if __name__ == "__main__":
    main()