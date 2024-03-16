import logging
import subprocess as sp

from termcolor import colored

class Automation:
    def __init__(self):
        """
        Constructor for the Automation class, that is responsible for running the commands.

        Args:
            None

        Returns:
            None
        """
        self.script_name = "auto_llm.ps1"
    
    def run_commands(self, commands: list) -> str:
        """
        Method to run the list of commands.

        Args:
            commands (list): The list of commands that are to be run.

        Returns:
            str: The result of running the commands.
        """
        ret_code = 1
        while ret_code != 0:
            # Write the commands to a PowerShell script
            with open(self.script_name, "w") as f:
                for command in commands:
                    f.write(f"{command.strip()}\n")

            # Run the PowerShell script
            result = sp.run(["powershell.exe", f".\\{self.script_name}"], capture_output=True, text=True)

            ret_code = result.returncode

            logging.info(f"Return code: {ret_code}")

            if ret_code != 0:
                logging.error(colored(f"Error: {result.stderr}\nTrying again...", "red"))

        # Return the result
        return result.stdout or result.stderr
    
    