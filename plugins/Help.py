from plugins import Plugin

class Help(Plugin.Plugin):
    def __init__(self, bot, msg):
        Plugin.Plugin.__init__(self, bot, msg)

    def execute(self):
        self.bot.send_message(mto=self.msg['from'].bare,
                mbody='Až to bude hotový, bude tady help',
                mtype='groupchat')

