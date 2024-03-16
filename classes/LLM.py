import re
import json
import logging

from typing import List
from g4f.client import Client
from g4f.Provider import FreeGpt

class LLM:
    def __init__(self, model: str = "CodeLlama-34b-Instruct-hf") -> None:
        """
        Constructor for the LLM class, that is responsible for text generation of the commands.

        Args:
            model (str): The model that is to be used for the text generation.
                Check https://github.com/xtekky/gpt4free?tab=readme-ov-file#models
                for the list of available models.

        Returns:
            None
        """
        self.client = Client()

        self.model = model

        # List of objects, each object is a dictionary with the following keys:
        # - user_task: The user task that is to be converted into commands.
        # - commands: The list of commands that are inferred from the user task.
        self.history = []

        self.system_prompt = "You are a form of LLM, that generates commands in a JSON Array format, based on a user provided task. The user task is a string, and the commands are a list of strings. The user task is the input, and the commands are the output."

    def extract_commands(self, text: str) -> List[str]:
        """
        Method to extract the commands from the generated text.

        Args:
            text (str): The generated text from the LLM.

        Returns:
            List[str]: The list of commands that are extracted from the generated text.
        """
        if str(text).startswith("["):
            # The text is already in the JSON Array format
            return json.loads(text)
        # Extract the JSON Array from the generated text
        commands = re.findall(r"\[.*\]", text)

        return commands

    def infer(self, user_task: str) -> List[str]:
        """
        Method to infer the commands from the user task.

        Args:
            user_task (str): The user task that is to be converted into commands.

        Returns:
            List[str]: The list of commands that are inferred from the user task.
        """
        logging.info(f"Inferring LLM for the user task: {user_task}")

        messages = [
            {
                "role": "system",
                "content": self.system_prompt
            }
        ]

        for obj in self.history:
            msg = f"User Task: {obj['user_task']}\nList of Commands you generated: {obj['commands']}"
            messages.append({
                "role": "user",
                "content": msg
            })

        messages.append({
            "role": "user",
            "content": f"""
            As stated earlier, you are a form of LLM, that generates commands in a JSON Array format, based on a user provided task. The user task is a string, and the commands are a list of strings. The user task is the input, and the commands are the output.

            You are now to generate a JSON Array of commands, to execute on a Windows Machine using PowerShell, that achieve the following task:
            {user_task}

            The commands should be in the following format:
            [
                "command1",
                "command2",
                "command3"
            ]

            If you need to generate a script, make sure to make it multiple commands, and not a single command.

            If access to the file system is required, only work in the current working directory, so never mention a path that has a directory in it, always directly reference the files.

            NEVER use placeholders. Always use actual values, if you don't know them, use the Environment Variables that reference them on Windows.

            The commands should be in the format of a JSON Array, and should be valid commands to execute on a Windows Machine.

            You MUST ONLY SEND the JSON Array of commands, and nothing else. Do NOT provide any additional information or context in the response, other than the JSON Array of commands."""
        })

        # Generate text response
        generation = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            provider=FreeGpt
        )

        logging.info(f"Generated LLM Response with length of {len(generation.choices[0].message.content)} characters.")
        print(generation.choices[0].message.content)
        # Extract the commands from the generated text
        commands = self.extract_commands(generation.choices[0].message.content)

        # Add the user task and the commands to the history
        self.history.append({
            "user_task": user_task,
            "commands": commands
        })

        return commands
