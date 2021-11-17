from datetime import datetime, timedelta
import time


class ANTIDDOSTG:
    timeout = 5

    limit = 20

    ddos_ban_time = 360  # Ban time in secs
    autoban = True

    log = False

    service_status = False

    ddosers = []
    messages_ddos = None
    callbacks_ddos = {}

    def __init__(self, timeout=5, autoban = True, autobantime = 360, limit=10):
        self.timeout = timeout
        self.limit = limit
        self.autoban = autoban
        self.ddos_ban_time = autobantime
        self.messages_ddos = {}

    def ddos_message(self, message):
        if self.isddoser(message.chat.id):
            return False
        try:
            msg = self.messages_ddos[message.chat.id]
            for i in msg:
                if i[0] == message.text:
                    return False
            self.messages_ddos[message.chat.id].append([message.text,
                                                        datetime.now() + timedelta(seconds=self.timeout)])

            if len(self.messages_ddos[message.chat.id]) >= self.limit and self.autoban:
                self.ddosers.append({message.chat.id: datetime.now() + timedelta(seconds=self.ddos_ban_time)})
                if self.log:
                    print(f"[AD-TG] ANTIDDOSTG has baned {message.chat.id} for {self.ddos_ban_time} sec.")
            return True
        except Exception as e:
            self.messages_ddos.update({message.chat.id: [[message.text, datetime.now() + timedelta(seconds=self.timeout)]]})
            return True

    def ddos_callback(self, callback_query):
        if self.isddoser(callback_query.message.chat.id):
            return False
        try:
            msg = self.messages_ddos[callback_query.message.chat.id]
            for i in msg:
                if i[0] == callback_query.data:
                    return False
            self.messages_ddos[callback_query.message.chat.id].append([callback_query.data,
                                                        datetime.now() + timedelta(seconds=self.timeout)])

            if len(self.messages_ddos[callback_query.message.chat.id]) >= self.limit and self.autoban:
                self.ddosers.append({callback_query.message.chat.id: datetime.now() + timedelta(seconds=self.ddos_ban_time)})
                if self.log:
                    print(f"[AD-TG] ANTIDDOSTG has baned {callback_query.message.chat.id} for {self.ddos_ban_time} sec.")
            return True
        except Exception as e:
            self.messages_ddos.update({callback_query.message.chat.id: [[callback_query.data, datetime.now() + timedelta(seconds=self.timeout)]]})
            return True

    def start_service(self):
        print(f"[AD-TG] ANTIDDOSTG service has started!")
        self.service_status = True
        while self.service_status:
            try:
                if self.log:
                    print(f"[AD-TG] Check started.")
                for i in self.messages_ddos:
                    for x in range(len(self.messages_ddos[i])):
                        if self.messages_ddos[i][x][1] < datetime.now():
                            self.messages_ddos[i].pop(x)
                for i in self.callbacks_ddos:
                    for x in range(len(self.callbacks_ddos[i])):
                        if self.callbacks_ddos[i][x][1] < datetime.now():
                            self.callbacks_ddos[i].pop(x)
                for i in self.ddosers:
                    for x in i.items():
                        if x[1] < datetime.now():
                            self.ddosers.remove(i)
            except:
                continue
            time.sleep(0.5)

    def shoutdown_service(self):
        self.service_status = False


    def start_log(self):
        self.log = True

    def stop_log(self):
        self.log = False

    def isddoser(self, uid):
        for i in self.ddosers:
            for id in i:
                if id == uid:
                    return True
        return False