
import os
import shutil
import stat
import time
import sys
from datetime import datetime
import subprocess

class FileManager:
    def __init__(self):
        self.current_path = os.getcwd()
        self.clipboard = None  # для копирования/вырезания
        self.clipboard_operation = None  # 'copy' или 'cut'
        
    def clear_screen(self):
        """Очистка экрана"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def show_help(self):
        """Показать справку"""
        self.clear_screen()
        print("=" * 60)
        print("СПРАВКА ПО ФАЙЛОВОМУ МЕНЕДЖЕРУ".center(60))
        print("=" * 60)
        print("РАБОТА С КАТАЛОГАМИ:")
        print("  cd <путь>          - перейти в каталог")
        print("  mkdir <имя>         - создать каталог")
        print("  rmdir <имя>         - удалить пустой каталог")
        print("  rm -r <имя>         - удалить каталог с содержимым")
        print("  mvdir <ист> <назн>   - переместить/переименовать каталог")
        print("  cpdir <ист> <назн>   - копировать каталог")
        print("  ls                   - просмотр содержимого")
        print("  finddir <имя>        - поиск каталогов")
        print("  chmoddir <имя> <права> - изменить права доступа")
        print()
        print("РАБОТА С ФАЙЛАМИ:")
        print("  touch <имя>          - создать файл")
        print("  cat <имя>            - просмотр файла")
        print("  edit <имя>           - редактировать файл")
        print("  mv <ист> <назн>       - переместить/переименовать файл")
        print("  cp <ист> <назн>       - копировать файл")
        print("  rm <имя>             - удалить файл")
        print("  find <имя>           - поиск файлов")
        print("  chmod <имя> <права>   - изменить права доступа")
        print("  attrib <имя>         - показать атрибуты файла")
        print()
        print("ОБЩИЕ КОМАНДЫ:")
        print("  pwd                  - показать текущий путь")
        print("  ls -l                - подробный список")
        print("  ls -a                - показать скрытые файлы")
        print("  clear                - очистить экран")
        print("  help                 - показать эту справку")
        print("  exit                 - выход из программы")
        print("=" * 60)
        input("Нажмите Enter для продолжения...")
    
    def list_directory(self, show_all=False, long_format=False):
        """Просмотр содержимого каталога"""
        try:
            items = os.listdir(self.current_path)
            
            if not show_all:
                items = [item for item in items if not item.startswith('.')]
            
            if long_format:
                self._list_long_format(items)
            else:
                self._list_short_format(items)
                
        except PermissionError:
            print("Ошибка: Нет прав доступа к каталогу")
        except Exception as e:
            print(f"Ошибка при чтении каталога: {e}")
    
    def _list_short_format(self, items):
        """Краткий формат списка"""
        print(f"\nСодержимое каталога: {self.current_path}")
        print("-" * 60)
        
        # Сортируем: сначала каталоги, потом файлы
        dirs = []
        files = []
        
        for item in sorted(items):
            full_path = os.path.join(self.current_path, item)
            if os.path.isdir(full_path):
                dirs.append(f"[{item}]")
            else:
                files.append(item)
        
        # Выводим в несколько колонок
        all_items = dirs + files
        if all_items:
            col_width = max(len(item) for item in all_items) + 2
            cols = 80 // col_width
            for i, item in enumerate(all_items):
                print(item.ljust(col_width), end='')
                if (i + 1) % cols == 0:
                    print()
            print()
        else:
            print("Каталог пуст")
    
    def _list_long_format(self, items):
        """Подробный формат списка"""
        print(f"\nПодробное содержимое каталога: {self.current_path}")
        print("-" * 70)
        print(f"{'Права':10} {'Размер':>8} {'Дата':12} {'Имя':20}")
        print("-" * 70)
        
        for item in sorted(items):
            full_path = os.path.join(self.current_path, item)
            try:
                stat_info = os.stat(full_path)
                
                # Права доступа
                if os.path.isdir(full_path):
                    mode = 'd'
                else:
                    mode = '-'
                
                mode += 'r' if stat_info.st_mode & stat.S_IRUSR else '-'
                mode += 'w' if stat_info.st_mode & stat.S_IWUSR else '-'
                mode += 'x' if stat_info.st_mode & stat.S_IXUSR else '-'
                mode += 'r' if stat_info.st_mode & stat.S_IRGRP else '-'
                mode += 'w' if stat_info.st_mode & stat.S_IWGRP else '-'
                mode += 'x' if stat_info.st_mode & stat.S_IXGRP else '-'
                mode += 'r' if stat_info.st_mode & stat.S_IROTH else '-'
                mode += 'w' if stat_info.st_mode & stat.S_IWOTH else '-'
                mode += 'x' if stat_info.st_mode & stat.S_IXOTH else '-'
                
                # Размер
                size = stat_info.st_size
                if size < 1024:
                    size_str = f"{size}B"
                elif size < 1024 * 1024:
                    size_str = f"{size/1024:.1f}K"
                else:
                    size_str = f"{size/(1024*1024):.1f}M"
                
                # Дата
                mod_time = datetime.fromtimestamp(stat_info.st_mtime)
                date_str = mod_time.strftime("%d.%m.%Y")
                
                # Имя
                name = item
                if os.path.isdir(full_path):
                    name = f"[{name}]"
                
                print(f"{mode:10} {size_str:>8} {date_str:12} {name:20}")
                
            except Exception as e:
                print(f"{'?'*10:10} {'?':>8} {'?':12} {item:20}")
    
    def change_directory(self, path):
        """Сменить текущий каталог"""
        try:
            if path == "..":
                new_path = os.path.dirname(self.current_path)
            elif path.startswith("/") or (os.name == 'nt' and path[1:3] == ':\\'):
                new_path = path
            else:
                new_path = os.path.join(self.current_path, path)
            
            new_path = os.path.abspath(new_path)
            
            if os.path.exists(new_path) and os.path.isdir(new_path):
                self.current_path = new_path
                print(f"Текущий каталог: {self.current_path}")
            else:
                print("Ошибка: Каталог не существует")
        except Exception as e:
            print(f"Ошибка при смене каталога: {e}")
    
    def make_directory(self, name):
        """Создать каталог"""
        try:
            path = os.path.join(self.current_path, name)
            os.mkdir(path)
            print(f"Каталог '{name}' создан")
        except FileExistsError:
            print("Ошибка: Каталог уже существует")
        except Exception as e:
            print(f"Ошибка при создании каталога: {e}")
    
    def remove_directory(self, name, recursive=False):
        """Удалить каталог"""
        try:
            path = os.path.join(self.current_path, name)
            if recursive:
                shutil.rmtree(path)
                print(f"Каталог '{name}' и его содержимое удалены")
            else:
                os.rmdir(path)
                print(f"Пустой каталог '{name}' удален")
        except FileNotFoundError:
            print("Ошибка: Каталог не найден")
        except OSError:
            print("Ошибка: Каталог не пуст. Используйте 'rm -r' для рекурсивного удаления")
        except Exception as e:
            print(f"Ошибка при удалении каталога: {e}")
    
    def copy_directory(self, src, dst):
        """Копировать каталог"""
        try:
            src_path = os.path.join(self.current_path, src)
            dst_path = os.path.join(self.current_path, dst)
            
            if os.path.exists(dst_path):
                print("Ошибка: Целевой каталог уже существует")
                return
            
            shutil.copytree(src_path, dst_path)
            print(f"Каталог '{src}' скопирован в '{dst}'")
        except Exception as e:
            print(f"Ошибка при копировании каталога: {e}")
    
    def move_directory(self, src, dst):
        """Переместить/переименовать каталог"""
        try:
            src_path = os.path.join(self.current_path, src)
            dst_path = os.path.join(self.current_path, dst)
            
            shutil.move(src_path, dst_path)
            print(f"Каталог '{src}' перемещен/переименован в '{dst}'")
        except Exception as e:
            print(f"Ошибка при перемещении каталога: {e}")
    
    def create_file(self, name):
        """Создать файл"""
        try:
            path = os.path.join(self.current_path, name)
            with open(path, 'w') as f:
                pass
            print(f"Файл '{name}' создан")
        except Exception as e:
            print(f"Ошибка при создании файла: {e}")
    
    def view_file(self, name):
        """Просмотр файла"""
        try:
            path = os.path.join(self.current_path, name)
            if not os.path.exists(path):
                print("Ошибка: Файл не найден")
                return
            
            # Определяем размер файла
            size = os.path.getsize(path)
            if size > 1024 * 1024:  # > 1MB
                print("Файл слишком большой для просмотра (> 1MB)")
                answer = input("Все равно открыть? (y/n): ")
                if answer.lower() != 'y':
                    return
            
            # Читаем и отображаем файл
            self.clear_screen()
            print(f"Просмотр файла: {name}")
            print("-" * 60)
            
            with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                print(content)
            
            print("-" * 60)
            input("Нажмите Enter для продолжения...")
            
        except Exception as e:
            print(f"Ошибка при просмотре файла: {e}")
    
    def edit_file(self, name):
        """Редактирование файла (используем системный редактор)"""
        try:
            path = os.path.join(self.current_path, name)
            
            if not os.path.exists(path):
                print("Файл не существует. Создать? (y/n): ")
                if input().lower() == 'y':
                    self.create_file(name)
            
            # Используем блокнот на Windows или nano/nano на Unix
            if os.name == 'nt':
                os.system(f'notepad "{path}"')
            else:
                # Пытаемся использовать доступные редакторы
                editors = ['nano', 'vim', 'vi', 'gedit']
                editor_found = False
                
                for editor in editors:
                    if shutil.which(editor):
                        os.system(f'{editor} "{path}"')
                        editor_found = True
                        break
                
                if not editor_found:
                    print("Не найден текстовый редактор")
                    
        except Exception as e:
            print(f"Ошибка при редактировании файла: {e}")
    
    def copy_file(self, src, dst):
        """Копировать файл"""
        try:
            src_path = os.path.join(self.current_path, src)
            dst_path = os.path.join(self.current_path, dst)
            
            shutil.copy2(src_path, dst_path)
            print(f"Файл '{src}' скопирован в '{dst}'")
        except Exception as e:
            print(f"Ошибка при копировании файла: {e}")
    
    def move_file(self, src, dst):
        """Переместить/переименовать файл"""
        try:
            src_path = os.path.join(self.current_path, src)
            dst_path = os.path.join(self.current_path, dst)
            
            shutil.move(src_path, dst_path)
            print(f"Файл '{src}' перемещен/переименован в '{dst}'")
        except Exception as e:
            print(f"Ошибка при перемещении файла: {e}")
    
    def remove_file(self, name):
        """Удалить файл"""
        try:
            path = os.path.join(self.current_path, name)
            os.remove(path)
            print(f"Файл '{name}' удален")
        except Exception as e:
            print(f"Ошибка при удалении файла: {e}")
    
    def search_files(self, pattern):
        """Поиск файлов"""
        print(f"Поиск файлов по шаблону: {pattern}")
        print("-" * 60)
        found = 0
        
        for root, dirs, files in os.walk(self.current_path):
            for file in files:
                if pattern.lower() in file.lower():
                    full_path = os.path.join(root, file)
                    rel_path = os.path.relpath(full_path, self.current_path)
                    print(f"  {rel_path}")
                    found += 1
        
        print("-" * 60)
        print(f"Найдено файлов: {found}")
        input("Нажмите Enter для продолжения...")
    
    def search_directories(self, pattern):
        """Поиск каталогов"""
        print(f"Поиск каталогов по шаблону: {pattern}")
        print("-" * 60)
        found = 0
        
        for root, dirs, files in os.walk(self.current_path):
            for directory in dirs:
                if pattern.lower() in directory.lower():
                    full_path = os.path.join(root, directory)
                    rel_path = os.path.relpath(full_path, self.current_path)
                    print(f"  {rel_path}")
                    found += 1
        
        print("-" * 60)
        print(f"Найдено каталогов: {found}")
        input("Нажмите Enter для продолжения...")
    
    def change_permissions(self, name, permissions, is_dir=False):
        """Изменить права доступа"""
        try:
            path = os.path.join(self.current_path, name)
            
            if not os.path.exists(path):
                print("Ошибка: Путь не найден")
                return
            
            # Преобразуем права из строки (например "755" в число)
            try:
                perm = int(permissions, 8)
                os.chmod(path, perm)
                
                type_str = "каталога" if is_dir else "файла"
                print(f"Права {type_str} '{name}' изменены на {permissions}")
                
                # Показываем новые права
                stat_info = os.stat(path)
                print(f"Новые права (восьмеричные): {oct(stat_info.st_mode)[-3:]}")
                
            except ValueError:
                print("Ошибка: Неверный формат прав. Используйте восьмеричные числа (например, 755)")
                
        except Exception as e:
            print(f"Ошибка при изменении прав: {e}")
    
    def show_attributes(self, name):
        """Показать атрибуты файла/каталога"""
        try:
            path = os.path.join(self.current_path, name)
            
            if not os.path.exists(path):
                print("Ошибка: Путь не найден")
                return
            
            stat_info = os.stat(path)
            
            print(f"\nАтрибуты для: {name}")
            print("=" * 50)
            
            # Тип
            if os.path.isdir(path):
                print("Тип: Каталог")
            elif os.path.isfile(path):
                print("Тип: Файл")
            elif os.path.islink(path):
                print("Тип: Символическая ссылка")
            
            # Размер
            size = stat_info.st_size
            print(f"Размер: {size} байт")
            
            # Права доступа (восьмеричные)
            mode = stat_info.st_mode
            print(f"Права доступа: {oct(mode)[-3:]}")
            
            # Временные метки
            print(f"Создан: {datetime.fromtimestamp(stat_info.st_ctime)}")
            print(f"Изменен: {datetime.fromtimestamp(stat_info.st_mtime)}")
            print(f"Доступ: {datetime.fromtimestamp(stat_info.st_atime)}")
            
            # Владелец (на Unix системах)
            if os.name != 'nt':
                import pwd
                import grp
                try:
                    user = pwd.getpwuid(stat_info.st_uid).pw_name
                    group = grp.getgrgid(stat_info.st_gid).gr_name
                    print(f"Владелец: {user}")
                    print(f"Группа: {group}")
                except:
                    print(f"UID: {stat_info.st_uid}")
                    print(f"GID: {stat_info.st_gid}")
            
            print("=" * 50)
            input("Нажмите Enter для продолжения...")
            
        except Exception as e:
            print(f"Ошибка при получении атрибутов: {e}")
    
    def run(self):
        """Основной цикл программы"""
        self.clear_screen()
        print("=" * 60)
        print("ФАЙЛОВЫЙ МЕНЕДЖЕР v1.0".center(60))
        print("=" * 60)
        print("Введите 'help' для получения справки")
        print("-" * 60)
        
        while True:
            try:
                # Показываем текущий путь
                print(f"\n[{self.current_path}]")
                command = input("> ").strip()
                
                if not command:
                    continue
                
                # Разбираем команду
                parts = command.split()
                cmd = parts[0].lower()
                
                if cmd == "exit":
                    print("До свидания!")
                    break
                
                elif cmd == "clear":
                    self.clear_screen()
                
                elif cmd == "help":
                    self.show_help()
                
                elif cmd == "pwd":
                    print(self.current_path)
                
                elif cmd == "ls":
                    show_all = False
                    long_format = False
                    
                    if len(parts) > 1:
                        if "-a" in parts[1:]:
                            show_all = True
                        if "-l" in parts[1:]:
                            long_format = True
                    
                    self.list_directory(show_all, long_format)
                
                elif cmd == "cd":
                    if len(parts) > 1:
                        self.change_directory(parts[1])
                    else:
                        print("Использование: cd <путь>")
                
                elif cmd == "mkdir":
                    if len(parts) > 1:
                        self.make_directory(parts[1])
                    else:
                        print("Использование: mkdir <имя>")
                
                elif cmd == "rmdir":
                    if len(parts) > 1:
                        self.remove_directory(parts[1])
                    else:
                        print("Использование: rmdir <имя>")
                
                elif cmd == "rm" and len(parts) > 2 and parts[1] == "-r":
                    self.remove_directory(parts[2], recursive=True)
                
                elif cmd == "cpdir":
                    if len(parts) > 2:
                        self.copy_directory(parts[1], parts[2])
                    else:
                        print("Использование: cpdir <источник> <назначение>")
                
                elif cmd == "mvdir":
                    if len(parts) > 2:
                        self.move_directory(parts[1], parts[2])
                    else:
                        print("Использование: mvdir <источник> <назначение>")
                
                elif cmd == "touch":
                    if len(parts) > 1:
                        self.create_file(parts[1])
                    else:
                        print("Использование: touch <имя>")
                
                elif cmd == "cat":
                    if len(parts) > 1:
                        self.view_file(parts[1])
                    else:
                        print("Использование: cat <имя>")
                
                elif cmd == "edit":
                    if len(parts) > 1:
                        self.edit_file(parts[1])
                    else:
                        print("Использование: edit <имя>")
                
                elif cmd == "cp":
                    if len(parts) > 2:
                        self.copy_file(parts[1], parts[2])
                    else:
                        print("Использование: cp <источник> <назначение>")
                
                elif cmd == "mv":
                    if len(parts) > 2:
                        self.move_file(parts[1], parts[2])
                    else:
                        print("Использование: mv <источник> <назначение>")
                
                elif cmd == "rm" and len(parts) > 1 and parts[1] != "-r":
                    self.remove_file(parts[1])
                
                elif cmd == "find":
                    if len(parts) > 1:
                        self.search_files(parts[1])
                    else:
                        print("Использование: find <шаблон>")
                
                elif cmd == "finddir":
                    if len(parts) > 1:
                        self.search_directories(parts[1])
                    else:
                        print("Использование: finddir <шаблон>")
                
                elif cmd == "chmod" and len(parts) > 2:
                    self.change_permissions(parts[1], parts[2], is_dir=False)
                
                elif cmd == "chmoddir" and len(parts) > 2:
                    self.change_permissions(parts[1], parts[2], is_dir=True)
                
                elif cmd == "attrib":
                    if len(parts) > 1:
                        self.show_attributes(parts[1])
                    else:
                        print("Использование: attrib <имя>")
                
                else:
                    print(f"Неизвестная команда: {cmd}")
                    print("Введите 'help' для списка команд")
                    
            except KeyboardInterrupt:
                print("\nИспользуйте 'exit' для выхода")
            except Exception as e:
                print(f"Ошибка: {e}")

def main():
    """Точка входа"""
    fm = FileManager()
    
    try:
        fm.run()
    except KeyboardInterrupt:
        print("\nДо свидания!")
    except Exception as e:
        print(f"Критическая ошибка: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
