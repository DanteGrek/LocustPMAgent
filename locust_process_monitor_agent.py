import psutil
import socket
import pickle


def _get_cpu_and_memory():
    return {"cpu": psutil.cpu_percent(interval=0.2), "memory": psutil.virtual_memory().percent}


class LocustProcessMonitorAgent(object):

    def __init__(self, port=9090):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(('', port))
        self.conn = None

    def wait_client(self):
        self.sock.listen(1)
        self.conn, addr = self.sock.accept()
        print 'connected:', addr

    def launch_process_monitor_agent(self):
        while True:
            self.wait_client()
            data = self.conn.recv(1024)
            if data == 'locust client':
                try:
                    while True:
                        self.conn.send(pickle.dumps(_get_cpu_and_memory()))
                        print "send"
                except Exception:
                    print "can not send charts!!!"
                    self.close_connection()

    def close_connection(self):
        self.conn.close()


if __name__ == '__main__':
    lpma = LocustProcessMonitorAgent()
    lpma.launch_process_monitor_agent()
