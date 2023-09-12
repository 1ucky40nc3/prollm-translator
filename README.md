# Prompt-LLM Translator 🌟🚀

A Gradio Chat App for a LLM assisted Translator

## Installation

Dependencies:
- [Python](https://www.python.org/)

Install the Python dependencies using the following commands:
```bash
python -m pip install virtualenv
python -m venv venv
```
If you are using windows:
```bash
venv\Scripts\activate
```
On linux-based systems:
```bash
source venv/bin/activate
```
Install the requirements:
```bash
python -m pip install -r requirements.txt
```
Install for development:
```bash
python -m pip install -e .
```

### Set up your Local Environment

Copy and rename [`.env.template`](.env.template) to `.env`:
```bash
cp .env.template .env
```
Insert your secrets and other configuration in the [`.env`](.env) file.



## Usage

### Manual Usage

You can start the gradio app manually with the following commands:
```bash
# Use the file
python src/gradio_chat/app.py
# Use the command
gradio-chat
```
It is also possible to use the Pro-LLM Translator individually:
```bash
# Use the file
python src/prollm_translator/main.py
# Use the command
prollm-translator
```

### Docker Compose

You can also use the gradio app with the provided docker compose setup. Just follow the commands below:
```bash
docker compose build
docker compose up
```