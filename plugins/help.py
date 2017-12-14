from plugins import plugin

class Help(plugin.Plugin):
    def __init__(self, bot, msg):
        plugin.Plugin.__init__(self, bot, msg)

    def execute(self):
        self.bot.send_message(mto=self.msg['from'].bare,
                mbody='Až to bude hotový, bude tady help',
                mtype='groupchat')

