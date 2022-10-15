from telegram import Update
from telegram.ext import CommandHandler, CallbackContext

    
class TelegramCommand:
    def __init__(self, name, handler, aliases=[], description=""):
        self.name = name
        self.handler = handler
        self.aliases = aliases
        self.description = description


class TelegramCommandsBin:
    def __init__(self):
        self.commands = []

    def add(self, cmd: TelegramCommand):
        self.commands.append(cmd)

    def setup_handlers(self, bot_application):
        def add_handler_to_bot_application(command_name, function):
            bot_application.add_handler(CommandHandler(command_name, function))

        for cmd in self.commands:
            add_handler_to_bot_application(cmd.name, cmd.handler)
            for a in cmd.aliases:
                add_handler_to_bot_application(a, cmd.handler)

    async def show_commands_list(self, update: Update, context: CallbackContext):

        text = ["Available commands:"]
        for cmd in self.commands:
            text.append(f"/{cmd.name} - {cmd.description}")
        final = "\n".join(text)
        await update.message.reply_text(final)

    def __iter__(self):
        return iter(self.commands)

    def __getitem__(self, item):
        return self.commands[item]


"""

Usage:

commands = TelegramCommandsBin()
commands.add(TelegramCommand("last", last_answers, description="show last day saved in database"))
commands.add(TelegramCommand("stats", make_stats, description="show basic stats"))
commands.add(TelegramCommand("delete", delete_last_day, aliases=["del"], description="delete last item from database"))
commands.add(TelegramCommand("edit", edit_last_answer, description="edit specific answer in last day. format: /edit key new_value"))

"""