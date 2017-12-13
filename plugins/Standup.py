from plugins import Plugin

import json
from time import sleep

class Standup(Plugin.Plugin):
    def __init__(self, bot, msg):
        Plugin.Plugin.__init__(self, bot, msg)

    def get_help(self):
        return str('!standup [<what am I doing>]. Bez parametru vypíše statusy všech přihlášených uživatelů. Parametr <what am I doing> uloží status pro uživatele, který ho napsal')

    def execute(self):
        message = self.msg['body'][1:].split()
        msg_type = len(message)

        standup_status={}

        try:
            with open('standup.data', 'r') as infile:
                standup_status = json.load(infile)
        except Exception as e:
            print(e)

        if msg_type == 1:
            for key, value in standup_status.items():
                # if key in MUC users
                self.bot.send_message(mto=self.msg['from'].bare,
                        mbody='%s : %s' % (key, value),
                        mtype='groupchat')
                sleep(self.bot.message_delay)    # we don't want to spam
        elif msg_type == 2:
            if message[1] in standup_status:
                user = message[1]
                status = standup_status[message[1]]
                self.bot.send_message(mto=self.msg['from'].bare,
                        mbody='%s : %s' % (user, status),
                        mtype='groupchat')
            else:
                self.bot.send_message(mto=self.msg['from'].bare,
                        mbody='No standup status for %s' % message[1],
                        mtype='groupchat')
        else:
            standup_status[message[1]] = ' '.join(message[2:])
            with open('standup.data', 'w') as outfile:
                json.dump(standup_status, outfile)
            
            self.bot.send_message(mto=self.msg['from'].bare,
                    mbody='Standup status stored for %s' % message[1],
                    mtype='groupchat')


