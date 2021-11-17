from aiogram.types import Message, callback_query
from datetime import datetime, timedelta
import time


class ANTIDDOSTG:
    timeout = 5

    service_status = False

    ddosers = []
    messages_ddos = {}
    callbacks_ddos = {}

    def __init__(self, timeout=5):
        self.timeout = timeout

    def ddos_message(self, message: Message):
        try:
            msg = self.messages_ddos[message.chat.id]
        except:
            self.messages_ddos.update({message.chat.id: [[message.text,
                                                               datetime.now() + timedelta(seconds=self.timeout)]]})
            return True
        if msg is not None:
            for i in msg:
                if i[0] == message.text:
                    return False
            self.messages_ddos.update({message.chat.id:
                                        self.messages_ddos[message.chat.id].append([message.text,
                                        datetime.now() + timedelta(seconds=self.timeout)])})
        else:
            self.messages_ddos.update({message.chat.id: [message.text,
                                                         datetime.now() + timedelta(seconds=self.timeout)]})
        return True

    def ddos_callback(self, callback: callback_query):
        try:
            msg = self.messages_ddos[callback.message.chat.id]
        except:
            self.messages_ddos.update({callback.message.chat.id: [[callback.data,
                                                          datetime.now() + timedelta(seconds=self.timeout)]]})
            return True
        if msg is not None:
            for i in msg:
                if i[0] == callback.data:
                    return False
            self.messages_ddos.update({callback.message.chat.id:
                                           self.messages_ddos[callback.message.chat.id].append([callback.message.text,
                                                                                       datetime.now() + timedelta(
                                                                                           seconds=self.timeout)])})
        else:
            self.messages_ddos.update({callback.message.chat.id: [callback.data,
                                                         datetime.now() + timedelta(seconds=self.timeout)]})
        return True

    def start_service(self):
        self.service_status = True
        while self.service_status:
            for i in self.messages_ddos:
                for x in range(len(self.messages_ddos[i])):
                    if self.messages_ddos[i][x][1] < datetime.now():
                        self.messages_ddos[i].pop(x)
            for i in self.callbacks_ddos:
                for x in range(len(self.callbacks_ddos[i])):
                    if self.callbacks_ddos[i][x][1] < datetime.now():
                        self.callbacks_ddos[i].pop(x)
            time.sleep(0.5)

    def shoutdown_service(self):
        self.service_status = False


