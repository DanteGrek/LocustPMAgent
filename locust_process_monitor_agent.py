import psutil
import socket
import pickle


def _get_cpu_and_memory():
    return {"cpu": psutil.cpu_percent(interval=0.2), "memory": psutil.virtual_memory().percent}


class LocustProcessMonitorAgent(object):

    def __init__(self, port=9999):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(('', port))
        self.conn = None

    def wait_client(self):
        print "agent wait for client connection"
        self.sock.listen(1)
        self.conn, addr = self.sock.accept()
        print 'connected:', addr

    def launch_process_monitor_agent(self):
        while True:
            self.wait_client()
            try:
                while True:
                    data = self.conn.recv(1024)
                    if data == 'locust client':
                        self.conn.send(pickle.dumps(_get_cpu_and_memory()))
                        print "send"
                    elif data == 'done':
                        self.close_connection()
                        print "client closed connection"
                        break
                    else:
                        self.close_connection()
                        print "connection is close"
                        break
            except Exception:
                print "can not send charts!!!"
            finally:
                self.close_connection()

    def close_connection(self):
        self.conn.close()


if __name__ == '__main__':
    lpma = LocustProcessMonitorAgent()
    lpma.launch_process_monitor_agent()
