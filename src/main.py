import json
import logging

from termcolor import colored

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

def main():
    # Create an instance of the LLM
    llm = LLM(model="gpt-3.5-turbo")

    # User task
    user_task = input(colored("[?] Please enter the user task: ", "cyan"))

    # Infer the commands
    commands = llm.infer(user_task)

    print(colored(f"Commands: {commands}", "green"))

    global PREVIOUS_COMMANDS
    for command in commands:
        PREVIOUS_COMMANDS.append(command)

    # Create an instance of the Automation class
    automation = Automation()

    # Run the commands
    results = automation.run_commands(commands)

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
