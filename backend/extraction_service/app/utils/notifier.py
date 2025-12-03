from EventNotifier import Notifier

class Notification:
    def __init__(self):
        self.on_data_ready = Notifier()

    def notification(self,msg:str, data:dict):
        self.on_data_ready.notify(msg , data)


def listener(data):
    print(f"Received data: {data}")



