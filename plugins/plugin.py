class Plugin:
    def __init__(self, bot, msg):
        self.bot = bot
        self.msg = msg

    # this is executed when a command is called
    def execute(self):
        raise NotImplementedError()

    # returns a string with parameter description for specific plugin
    def get_help():
        raise NotImplementedError()


