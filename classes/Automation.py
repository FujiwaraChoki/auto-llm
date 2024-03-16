import logging
import subprocess as sp

import subprocess as sp
import logging

class Automation:
    def __init__(self):
        """
        Constructor for the Automation class, that is responsible for running the commands.

        Args:
            None

        Returns:
            None
        """
        pass

    def run(self, command: str) -> dict:
        """
        Method to run the command.

        Args:
            command (str): The command that is to be run.

        Returns:
            dict: The result of the command.
        """

        logging.info(f"Running the command: {command}")

        # Send the command to the powershell
        result = sp.run(command, shell=True, text=True, capture_output=True)

        # Capture output and error streams
        stdout, stderr = result.stdout, result.stderr

        # Check if the command was successful
        if not stderr:
            return {
                "success": True,
                "message": stdout
            }
        else:
            return {
                "success": False,
                "message": stderr
            }
    
    def run_commands(self, commands: list) -> list:
        """
        Method to run the list of commands.

        Args:
            commands (list): The list of commands that are to be run.

        Returns:
            list: The list of results for the commands.
        """
        results = []
        ok_dict = {}

        for command in commands:
            result = self.run(command)
            ok_dict["success"] = result["success"]
            ok_dict["message"] = result["message"]

            results.append(result)
        
        return results
    
    