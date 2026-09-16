from commands.plugins.greetings import GreetingsPlugin


plugins = [
    GreetingsPlugin(),
]


def handle(command):

    for plugin in plugins:

        if plugin.can_handle(command):

            return plugin.handle(command)

    return None