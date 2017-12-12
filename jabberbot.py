#!/usr/bin/python3

# Simple jabber bot
# Just for my studying purposes
# In the future it could help us with our projects

from sleekxmpp import ClientXMPP    # install python3-sleekxmpp
import json
from time import sleep

class MUCBot(ClientXMPP):
    def __init__(self, jid, password, room, nick):
        ClientXMPP.__init__(self, jid, password)

        self.room = room
        self.nick = nick

        self.add_event_handler('session_start', self.start)
        self.add_event_handler('groupchat_message', self.muc_message)

    def start(self, event):
        self.get_roster()
        self.send_presence()
        self.plugin['xep_0045'].joinMUC(self.room, self.nick, wait=True)

    def muc_message(self, msg):
#        if msg['mucnick'] != self.nick and self.nick in msg['body']:
#            self.send_message(mto=msg['from'].bare,
#                              mbody='Co chceš, %s?' % msg['mucnick'],
#                              mtype='groupchat')

        if msg['mucnick'] != self.nick and msg['body'].startswith('!'):
            self.process_command(msg)

    def process_command(self, msg):
        try:
            command = msg['body'][1:].split()[0]
            if command == 'test':
                self.send_message(mto=msg['from'].bare,
                                  mbody='%s : Funguju' % msg['mucnick'],
                                  mtype='groupchat')
            elif command == 'standup':
                self.standup(msg)
            else:
                self.help(msg)

        except Exception as e:
            print(e)

    def standup(self, msg):
        message = msg['body'][1:].split()
        msg_type = len(message)

        standup_status={}

        try:
            with open('standup.data', 'r') as infile:
                standup_status = json.load(infile)
        except Exception as e:
            print(e)

        if msg_type == 1:
            for key, value in standup_status.items():
                self.send_message(mto=msg['from'].bare,
                        mbody='%s : %s' % (key, value),
                        mtype='groupchat')
                sleep(1)    # we don't want spam
        elif msg_type == 2:
            if message[1] in standup_status:
                user = message[1]
                status = standup_status[message[1]]
                self.send_message(mto=msg['from'].bare,
                        mbody='%s : %s' % (user, status),
                        mtype='groupchat')
            else:
                self.send_message(mto=msg['from'].bare,
                        mbody='No standup status for %s' % message[1],
                        mtype='groupchat')
        else:
            standup_status[message[1]] = ' '.join(message[2:])
            with open('standup.data', 'w') as outfile:
                json.dump(standup_status, outfile)
            
            self.send_message(mto=msg['from'].bare,
                    mbody='Standup status stored for %s' % message[1],
                    mtype='groupchat')

    def help(self, msg):
        self.send_message(mto=msg['from'].bare,
                mbody='Až to bude hotový, bude tady help',
                mtype='groupchat')


if __name__ == '__main__':
    xmpp = MUCBot('jid@server.xx', 'boticka', 'room@chat.jabb.im', 'bot')
#   xmpp.register_plugin('xep_0030')    # Service Discovery
    xmpp.register_plugin('xep_0045')    # MUC
    xmpp.register_plugin('xep_0199')    # XMPP ping

    if xmpp.connect():
        xmpp.process(block=True)
    else:
        print('Unable to connect')

