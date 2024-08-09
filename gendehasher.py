import hashlib
import time
import os
import shutil
import re
from colorama import Fore

# хранит к себе пароли
password_list = []

# логотип формата ASCII
logo = """

  /$$$$$$                      /$$$$$$$            /$$   /$$                     /$$                          
 /$$__  $$                    | $$__  $$          | $$  | $$                    | $$                          
| $$  \__/  /$$$$$$  /$$$$$$$ | $$  \ $$  /$$$$$$ | $$  | $$  /$$$$$$   /$$$$$$$| $$$$$$$   /$$$$$$   /$$$$$$ 
| $$ /$$$$ /$$__  $$| $$__  $$| $$  | $$ /$$__  $$| $$$$$$$$ |____  $$ /$$_____/| $$__  $$ /$$__  $$ /$$__  $$
| $$|_  $$| $$$$$$$$| $$  \ $$| $$  | $$| $$$$$$$$| $$__  $$  /$$$$$$$|  $$$$$$ | $$  \ $$| $$$$$$$$| $$  \__/
| $$  \ $$| $$_____/| $$  | $$| $$  | $$| $$_____/| $$  | $$ /$$__  $$ \____  $$| $$  | $$| $$_____/| $$      
|  $$$$$$/|  $$$$$$$| $$  | $$| $$$$$$$/|  $$$$$$$| $$  | $$|  $$$$$$$ /$$$$$$$/| $$  | $$|  $$$$$$$| $$      
 \______/  \_______/|__/  |__/|_______/  \_______/|__/  |__/ \_______/|_______/ |__/  |__/ \_______/|__/      
                                                                                                                                                                                                                                                                                                    
"""

# Данная функция очищает экран терминала
def clear_screen():
    os.system("cls || clear")

# Данная функция выводит логотип по центру экрана
def printcenter(text):
    size = shutil.get_terminal_size().columns
    for line in text.split("\n"):
        print(' ' * (round((size/2)-len(line)/2)), line)

# Данная функция выполняет перебор паролей
def bruteforce(hash_str: str, salt: str = None):
    # SHA256
    if len(hash_str) == 64:
        for password in password_list:
            if hashlib.sha256(password.encode()).hexdigest() == hash_str:
                return (hash_str, password)
            if salt is not None and (hashlib.sha256(password.encode() + salt.encode()).hexdigest() == hash_str or hashlib.sha256(hashlib.sha256(password.encode()).hexdigest().encode() + salt.encode()).hexdigest() == hash_str):
                return (hash_str, password)
    # SHA512
    elif len(hash_str) == 128:
        for password in password_list:
            if hashlib.sha512(password.encode()).hexdigest() == hash_str:
                return (hash_str, password)
            if salt is not None and (hashlib.sha512(password.encode() + salt.encode()).hexdigest() == hash_str or hashlib.sha512(hashlib.sha512(password.encode()).hexdigest().encode() + salt.encode()).hexdigest() == hash_str):
                return (hash_str, password)
    return None

# основной код программы
def main():
    global password_list
    clear_screen()
    print()
    printcenter(f"{Fore.YELLOW}{logo}")
    wordlist = input(f"{Fore.RED} [»] {Fore.LIGHTBLUE_EX} Название/Путь к Wordlist: {Fore.WHITE}")
    if not os.path.isfile(wordlist):
        clear_screen()
        printcenter(f"{Fore.YELLOW}{logo}")
        printcenter(f"{Fore.LIGHTBLUE_EX}[ERROR] {Fore.WHITE} Не удалось загрузить Wordlist, попробуйте еще раз.")
        time.sleep(5)
        print()
        main()
    else:
        clear_screen()
        printcenter(f"{Fore.YELLOW}{logo}")
        printcenter(f"{Fore.LIGHTBLUE_EX}[LOG] {Fore.WHITE} Загрузка Wordlist, ожидайте..")
        with open(wordlist, 'r', encoding="latin-1") as f:
            password_list = [password.strip() for password in f]
            clear_screen()
            printcenter(f"{Fore.YELLOW}{logo}")
            printcenter(f"{Fore.LIGHTBLUE_EX}             [LOG]{Fore.WHITE} Загружено {Fore.RED}{len(password_list)} {Fore.WHITE}паролей.")
            print()
            printcenter(f"{Fore.LIGHTBLUE_EX}[INFO] {Fore.WHITE} Введите Hash, затем Salt. {Fore.YELLOW}Если нет Salt, оставьте поле пустым.")
            print()
            
        while True:
            hash_str = input(f"{Fore.RED} [»] {Fore.LIGHTBLUE_EX} Введите Hash: {Fore.WHITE}")
            if len(hash_str) < 32 or len(hash_str) > 128:

                clear_screen()
                printcenter(f"{Fore.YELLOW}{logo}")
                printcenter(f"{Fore.LIGHTBLUE_EX}[ERROR] {Fore.WHITE} Неверный Hash.")
                time.sleep(5)
                print()
                main()
            print()
            salt = input(f"{Fore.RED} [»] {Fore.LIGHTBLUE_EX} Введите Salt: {Fore.WHITE}")
            start = time.perf_counter()
            
            if salt.strip() != "":
                final = bruteforce(hash_str, salt)
            else:
                final = bruteforce(hash_str)
            end = time.perf_counter()

            if final is None:
                clear_screen()
                printcenter(f"{Fore.YELLOW}{logo}")
                printcenter(f"{Fore.LIGHTBLUE_EX}[LOG]{Fore.WHITE} Неверный Hash/Salt или пароль не найден.")
                time.sleep(15)
                main()
            if final[0] == hash_str:
                clear_screen()
                printcenter(f"{Fore.YELLOW}{logo}")
                printcenter(f"{Fore.LIGHTBLUE_EX}[LOG]{Fore.WHITE} Возможный пароль найден -> {Fore.RED}{final[1]} {Fore.RESET}({Fore.LIGHTBLUE_EX}{end-start:.3f} секунд{Fore.RESET})")
                print()
                print()
                printcenter(f"{Fore.YELLOW}(1) {Fore.WHITE} Расшифровать другой hash {Fore.YELLOW}(2){Fore.WHITE} Главное меню {Fore.YELLOW}(3){Fore.WHITE} Выход")
                print()
                option = input(f"{Fore.RED} [»] {Fore.LIGHTBLUE_EX} Выберите опцию: {Fore.WHITE}")
                if option == "1":
                    continue
                elif option == "2":
                    main_menu()
                elif option == "3":
                    clear_screen()
                    exit()
                else:
                    clear_screen()
                    printcenter(f"{Fore.YELLOW}{logo}")
                    printcenter(f"{Fore.LIGHTBLUE_EX}[ERROR] {Fore.WHITE} Вы должны выбрать допустимый вариант!")
                    time.sleep(5)
                    main()

# Функция для разделения hash и salt
def divider(content: str) -> str:
    hash_str = re.search(r"[^$SHA]\w{127}", content)
    if hash_str is None:
        hash_str = re.search(r"[^$SHA]\w{63}", content)
        if hash_str is None:
            return None
    hash_str = hash_str.group()
    salt = ''.join(item for item in content.split('$') if item != hash_str and len(item) < len(hash_str) and not item.lower().startswith('sha'))
    if salt:
        return f"{hash_str}:{salt}"
    else:
        return f"{hash_str} {Fore.RED}(Нет Salt)"

# функция главного меню + преобразования необработанного хэша
def main_menu():
    while True:
        clear_screen()
        print()
        printcenter(f"{Fore.YELLOW}{logo}")
        print(Fore.LIGHTBLUE_EX + "1) Преобразовать необработанный хеш в хеш:соль")
        print(Fore.LIGHTBLUE_EX + "2) Использовать оптимизированный GenDeHasher")
        opt = input("> ")

        if opt == "1":
            print()
            printcenter(f"{Fore.YELLOW}{logo}")
            raw = input(Fore.LIGHTWHITE_EX + "\nНеобработанный хеш: " + Fore.LIGHTBLUE_EX)
            divided = divider(raw)
            if divided:
                print(Fore.LIGHTWHITE_EX + "Разделено:\n" + Fore.LIGHTGREEN_EX + divided)
            else:
                print("Неверный формат хеша.")
            print()
            print(Fore.YELLOW + "Нажмите Enter, чтобы продолжить...")
            input()
            pass
        
        elif opt == "2":
            main()
        else:
            clear_screen()
            printcenter(f"{Fore.YELLOW}{logo}")
            printcenter(f"{Fore.LIGHTBLUE_EX}[ОШИБКА] {Fore.WHITE}Вы должны выбрать допустимый вариант!")
            time.sleep(5)
            main()
            continue

if __name__ == "__main__":
    main_menu()