# Auto LLM

This is an experimental project to automate the usage of a PC using LLMs (Large Language Models) like GPT-3. The idea is to use the LLM to automate the usage of a PC, for example, to automatically change the wallpaper, open a program, or even write code.

## How it works

The project is divided into two parts: the LLM and the automation. The LLM is responsible for understanding the user's commands and generating the necessary code to automate the PC. The automation part is responsible for executing the code generated by the LLM.

## How to use

First, please export the following environment variables:

```bash
# So that the python script doesn't crash
export PYTHONPATH=$(pwd)
```

After that, you can run the following commands:

```bash
# Init Venv
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the main script
python src/main.py
```

## How to contribute

If you want to contribute to this project, please open an issue or a pull request. We are open to new ideas and suggestions.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
