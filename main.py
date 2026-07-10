from brain import process_command
from speak import speak
from listen import listen


def main():
    speak("Hello Sathwik. I am Jarvis.")

    while True:

        command = listen()

        if command == "":
            continue

        should_exit = process_command(command, speak)

        if should_exit:
            break


if __name__ == "__main__":
    main()