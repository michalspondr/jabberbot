#!/usr/bin/python3

# Simple jabber bot
# Just for my studying purposes
# In the future it could help us with our projects

from sleekxmpp import ClientXMPP    # install python3-sleekxmpp
import logging
from optparse import OptionParser

#load plugins
from plugins.help import Help
from plugins.standup import Standup
from plugins.jira import Jira

plugins = [Help, Standup, Jira]

class MUCBot(ClientXMPP):
    def __init__(self, jid, password, room, nick, message_delay):
        ClientXMPP.__init__(self, jid, password)

        self.room = room
        self.nick = nick

        self.message_delay = message_delay

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
                Standup(self, msg).execute()
            else:
                Help(self, msg).execute()

        except Exception as e:
            print(e)

def parseOptions():
    # Setup the command line arguments
    optp = OptionParser()

    # Output verbosity options
    optp.add_option('-q', '--quiet', help='set logging to ERROR',
                    action='store_const', dest='loglevel',
                    const=logging.ERROR, default=logging.INFO)
    optp.add_option('-d', '--debug', help='set logging to DEBUG',
                    action='store_const', dest='loglevel',
                    const=logging.DEBUG, default=logging.INFO)
    optp.add_option('-v', '--verbose', help='set logging to COMM',
                    action='store_const', dest='loglevel',
                    const=5, default=logging.INFO)

    optp.add_option('-s', '--no-spam', dest="nospam",
                    help='time interval between sending multi-row messages')

    # JID and password options
    optp.add_option("-j", "--jid", dest="jid",
                    help="JID to use")
    optp.add_option("-p", "--password", dest="password",
                    help="password to use")
    optp.add_option("-r", "--room", dest="room",
                    help="MUC room to join")
    optp.add_option("-n", "--nick", dest="nick",
                    help="MUC nickname")
    opts, args = optp.parse_args()

    # Setup logging
    logging.basicConfig(level=opts.loglevel,
                        format='%(levelname)-8s %(message)s')

    if opts.jid is None:
        opts.jid = raw_input("Username: ")
    if opts.password is None:
        opts.password = getpass.getpass("Password: ")
    if opts.room is None:
        opts.room = raw_input("MUC room: ")
    if opts.nick is None:
        opts.nick = raw_input("MUC nickname: ")

    if opts.nospam is None:
        opts.nospam = 0
    try:
        opts.nospam = int(opts.nospam)
    except ValueError:
        opts.nospam = 0

    return opts


if __name__ == '__main__':
    # parse options from command line (or enter them manually)
    opts = parseOptions()

    # prepare bot and run it
    xmpp = MUCBot(opts.jid, opts.password, opts.room, opts.nick, opts.nospam)
#   xmpp.register_plugin('xep_0030')    # Service Discovery
    xmpp.register_plugin('xep_0045')    # MUC
    xmpp.register_plugin('xep_0199')    # XMPP ping

    if xmpp.connect():
        xmpp.process(block=True)
    else:
        print('Unable to connect')

