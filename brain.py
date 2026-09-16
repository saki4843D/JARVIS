from commands.router import handle
from memory.conversation import add_message


def process_command(command, speak):

    # Save the user's message
    add_message("user", command)

    # Process the command
    response, should_exit = handle(command)

    # Save Jarvis's response
    add_message("assistant", response)

    speak(response)

    return should_exit