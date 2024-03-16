import json
import asyncio
import logging
import edge_tts

from uuid import uuid4
from termcolor import colored
from playsound import playsound

try:
    from classes.LLM import LLM
    from classes.Automation import Automation
except ModuleNotFoundError:
    logging.error(colored("Please set the PYTHONPATH environment variable to the project root directory.", "red"))

def print_ascii_art():
    print(colored(r"""
    
                _        _      _      __  __ 
     /\        | |      | |    | |    |  \/  |
    /  \  _   _| |_ ___ | |    | |    | \  / |
   / /\ \| | | | __/ _ \| |    | |    | |\/| |
  / ____ \ |_| | || (_) | |____| |____| |  | |
 /_/    \_\__,_|\__\___/|______|______|_|  |_|
                                              
""", "green"))
    
PREVIOUS_COMMANDS = []

async def say(text: str) -> None:
    communicate = edge_tts.Communicate(text, "en-GB-SoniaNeural")
    filename = f"assets/{str(uuid4())}.mp3"
    await communicate.save(filename)

    playsound(filename)

def main() -> None:
    # Create an instance of the LLM
    llm = LLM(model="gpt-3.5-turbo")

    # User task
    user_task = input(colored("[?] Please enter the user task: ", "cyan"))

    if user_task == "exit":
        raise KeyboardInterrupt
    elif user_task == "help":
        print(colored("Commands: 'exit', 'help'", "green"))
        return

    # Generate the commands
    commands = llm.infer(user_task)

    print(colored(f"Commands: {commands}", "green"))

    global PREVIOUS_COMMANDS
    for command in commands:
        PREVIOUS_COMMANDS.append(command)

    # Create an instance of the Automation class
    automation = Automation()

    # Run the commands
    results = automation.run_commands(commands)

    explanation = llm.explain_commands(commands)

    try:
        loop = asyncio.get_event_loop_policy().new_event_loop()
        loop.run_until_complete(say(explanation))
    except Exception as e:
        logging.error(colored(f"Error: {e}", "red"))
    finally:
        loop.close()

    print(colored(f"Results: {results}", "green"))

if __name__ == "__main__":
    # Print the ASCII art
    print_ascii_art()

    # Set logging level to info
    logging.basicConfig(level=logging.INFO)

    try:
        while True:
            main()
    except KeyboardInterrupt:
        logging.info(colored("Exiting...", "green"))
        with open("previous_commands.json", "w") as file:
            json.dump(PREVIOUS_COMMANDS, file)
    except Exception as e:
        logging.error(colored(f"Error: {e}", "red"))
        with open("previous_commands.json", "w") as file:
            json.dump(PREVIOUS_COMMANDS, file)
