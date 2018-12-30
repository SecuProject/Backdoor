import argparse


def mg_arg():
    parser = argparse.ArgumentParser(description='Backdoor server fonction')

    parser.add_argument('-l', '--logName', help='Set the server logging file', type=str, default="logFile.log")
    parser.add_argument('-nv', '--notverbose', action="store_true", default=False, help="Disable verbose mode")

    parser.add_argument('-p', '--LPORT', help='Set port to listen on', type=int, default=5001)
    
    args = parser.parse_args()
    return args
