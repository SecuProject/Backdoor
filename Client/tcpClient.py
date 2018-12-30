import tools
import mgArg


def main():
    default_server_ip = "127.0.0.1" 

    args = mgArg.mg_arg(default_server_ip)
    tools.set_log(args.logName, args.notverbose)
    
    while True:
        secure_communication = tools.SecureCommunication(args.RHOST, args.RPORT) 
        secure_communication.secure_connect()
        tools.echo_service(secure_communication, args.RHOST, args.logName)
        secure_communication.clean_socket()


if __name__ == "__main__":
    main()
