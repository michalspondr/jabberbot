from plugins import plugin

class Help(plugin.Plugin):
    def __init__(self, bot, msg):
        plugin.Plugin.__init__(self, bot, msg)

    def execute(self):
        self.bot.send_message(mto=self.msg['from'].bare,
                mbody=self.get_help(),
                mtype='groupchat')

    def get_help(self):
        return '!help [nazev_pluginu] - bez parametru vrátí seznam všech dostupných pluginů, s parametrem vypíše nápovědu k tomuto pluginu'
