import logging
import subprocess as sp

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
        result = sp.run("powershell -c '" + command.replace("'", "\"") + "'", shell=True, check=True, stdout=sp.PIPE, stderr=sp.PIPE)

        if result.returncode != 0:
            logging.error(f"Error: {result.stderr.decode('utf-8')}")
            return {
                "success": False,
                "message": result.stderr.decode("utf-8")
            }
        
        return {
            "success": True,
            "message": result.stdout.decode("utf-8")
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
            ok_dict["success"] = False

            while not ok_dict["success"]:
                result = self.run(command)
                ok_dict["success"] = result["success"]
                ok_dict["message"] = result["message"]

            results.append(result)
        
        return results
    
    