import tools
import mgArg


def main():
    default_server_ip = "127.0.0.1" 

    args = mgArg.mg_arg(default_server_ip)
    tools.set_log(args.logName, args.notverbose)
    
    while True:
        secureCommunication = tools.secureCommunication(args.RHOST, args.RPORT) 
        secureCommunication.secure_connect()
        tools.echo_service(secureCommunication, args.RHOST, args.logName)
        secureCommunication.clean_socket()


if __name__ == "__main__":
    main()
