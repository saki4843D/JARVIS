from commands.router import handle


def process_command(command, speak):

    response, should_exit = handle(command)

    speak(response)

    return should_exit