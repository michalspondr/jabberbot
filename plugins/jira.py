from plugins import plugin

class Jira(plugin.Plugin):
    def __init__(self, bot, msg):
        plugin.Plugin.__init__(self, bot, msg)

    def execute(self):
        pass

    def get_help():
        return 'Converts JIRA cases to their links'
