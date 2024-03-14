import logging

from termcolor import colored
try:
    from classes.LLM import LLM
    from classes.Automation import Automation
except ModuleNotFoundError:
    logging.error(colored("Please set the PYTHONPATH environment variable to the project root directory.", "red"))

def main():
    # Create an instance of the LLM
    llm = LLM(model="gpt-3.5-turbo")

    # User task
    user_task = input(colored("[?] Please enter the user task: ", "cyan"))

    # Infer the commands
    commands = llm.infer(user_task)

    # Create an instance of the Automation class
    automation = Automation()

    # Run the commands
    results = automation.run_commands(commands)

    print(colored(f"Results: {results}", "green"))

if __name__ == "__main__":
    # Set logging level to info
    logging.basicConfig(level=logging.INFO)

    try:
        main()
    except Exception as e:
        logging.error(colored(f"Error: {e}", "red"))
