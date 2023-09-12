# Copyright 2023 Louis Wendler
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import logging
import argparse

import gradio as gr

from gradio_chat.models import ChatHistory, Update
from gradio_chat.utils import (
    timestamp,
    load_frontend_from_cache,
    load_chats_from_cache,
    load_settings,
    pprint_dcls,
    pprint_dict,
    list_chat_ids,
    find_chat_by_id,
    set_chat_by_id,
    update_chat_by_id,
    del_chat_by_id,
    empty_chat,
    list_setting_ids,
    find_setting_by_id
)
from gradio_chat.parser import argument_parser

from prollm_translator.llm import openai_chat_completion
from prollm_translator.prompts import base


logger = logging.getLogger(__name__)


# We work with global variables here.
# TODO: Use states instead of global variables
chats = None
settings = None


def message_fn(
    message: str, 
    chat_history: ChatHistory, 
    setting_id: str
) -> tuple[str, ChatHistory]:
    setting = find_setting_by_id(setting_id, settings)
    
    source_lang_short = "en"
    target_lang_short = "ja"
    google_translation = "同意します"
    system_prompt = base.prompt(
        source_lang_short=source_lang_short,
        target_lang_short=target_lang_short,
        google_translation=google_translation
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": message}
    ]

    completion_iter = openai_chat_completion(
        messages,
        return_chat_completion=True
    )
    bot_message = []
    for output, completion in completion_iter:
        if output is not None:
            bot_message.append(output)
    bot_message = "".join(bot_message)
    chat_history.append((message, bot_message))
    return "", chat_history


def select_chat_event(choice: str, chat_id: str, chat_history: ChatHistory) -> tuple[str, Update, Update]:
    set_chat_by_id(chat_id, chat_history, chats)
    chat = find_chat_by_id(choice, chats)
    return chat.id, gr.update(value=chat.history), gr.update(value=chat.id)


def add_chat_event(chat_id: str, chat_history: ChatHistory) -> tuple[str, ChatHistory, Update]:
    set_chat_by_id(chat_id, chat_history, chats)
    chat = empty_chat()
    chats.append(chat)
    choices = list_chat_ids(chats)
    return chat.id, chat.history, gr.update(choices=choices, value=chat.id)


def delete_chat_event(chat_id: str) -> tuple[str, ChatHistory, Update]:
    del_chat_by_id(chat_id, chats)
    if len(chats) == 0:
        logger.info("Creating empty chat because we deleted all chats")
        chat = empty_chat()
        chats.append(chat)
    chat = chats[0]
    choices = list_chat_ids(chats)
    return chat.id, chat.history, gr.update(choices=choices, value=chat.id)


def clear_chat_event() -> None:
    return None


def select_setting_event(choice: str) -> str:
    print(f"Selected setting: {choice}")
    return choice


def rename_chat_event(new_id: str, chat_id: str) -> tuple[str, Update]:
    chat = find_chat_by_id(chat_id, chats)
    chat.id = new_id
    update_chat_by_id(chat_id, chat, chats)
    choices = list_chat_ids(chats)
    return chat.id, gr.update(choices=choices, value=chat.id)





def app(args: argparse.Namespace) -> None:
    global chats
    global settings

    frontend = load_frontend_from_cache(args.frontend, args.cache_dir)
    logger.info(f"Loaded frontend config:\n{pprint_dcls(frontend)}")
    settings = load_settings(args.settings)
    logger.info(f"Loaded a total of {len(settings)} settings")
    chats = load_chats_from_cache(args.cache_dir)
    logger.info(f"Loaded a total of {len(chats)} chats")

    if len(chats) == 0:
        chat = empty_chat("Start")
        chats.append(chat)

    chat_id = frontend.chat_id
    if chat_id is None:
        chat_id = chats[0].id
    setting_id = frontend.setting_id
    print(f"{chat_id=}")

    with gr.Blocks() as demo:
        # Set the states
        chat_id_state = gr.State(chat_id)
        setting_id_state = gr.State(setting_id)

        # Init the layout
        with gr.Row():
            select_chat_radio = gr.Radio(
                choices=list_chat_ids(chats),
                value=chat_id,
                label="Select chat", 
                interactive=True
            )
            with gr.Row():
                add_chat_button = gr.Button(value="New chat")
                delete_chat_button = gr.Button(value="Delete chat")
        
        with gr.Column():
            chat = find_chat_by_id(chat_id, chats)
            chatbot = gr.Chatbot(
                value=chat.history, 
                interactive=True, 
                label="Chat history"
            )
            message_text_box = gr.Textbox(label="Submit a message")
            clear_chat_button = gr.Button(value="Clear chat")

            with gr.Accordion("Settings"):
                select_setting_radio = gr.Radio(
                    choices=list_setting_ids(settings),
                    value=setting_id,
                    label="Select a LLM setting", 
                    interactive=True
                )
                rename_text_box = gr.Textbox(
                    value=chat_id,
                    label="Rename the chat",
                    interactive=True
                )

        # Set the events
        add_chat_button.click(
            add_chat_event, 
            inputs=[
                chat_id_state,
                chatbot,
            ],
            outputs=[
                chat_id_state,
                chatbot,
                select_chat_radio
            ]
        )
        delete_chat_button.click(
            delete_chat_event, 
            inputs=[
                chat_id_state,
            ],
            outputs=[
                chat_id_state, 
                chatbot,
                select_chat_radio
            ]
        )
        clear_chat_button.click(
            clear_chat_event, 
            inputs=None, 
            outputs=chatbot, 
            queue=False
        )
        select_chat_radio.change(
            select_chat_event, 
            inputs=[
                select_chat_radio, 
                chat_id_state, 
                chatbot
            ], 
            outputs=[
                chat_id_state, 
                chatbot,
                rename_text_box
            ]
        )
        message_text_box.submit(
            message_fn, 
            inputs=[
                message_text_box, 
                chatbot,
                setting_id_state
            ], 
            outputs=[
                message_text_box, 
                chatbot
            ]
        )
        select_setting_radio.change(
            select_setting_event,
            inputs=setting_id_state,
            outputs=setting_id_state
        )
        rename_text_box.submit(
            rename_chat_event, 
            inputs=[
                rename_text_box, 
                chat_id_state
            ], 
            outputs=[
                chat_id_state, 
                select_chat_radio
            ]
        )

    demo.launch(
        share=args.share, 
        server_name=args.server_name,
        server_port=args.server_port
    )


def main() -> None:
    parser = argument_parser()
    args = parser.parse_args()

    # Set up the logging
    os.makedirs(args.log_dir, exist_ok=True)
    logs_filename = os.path.join(args.log_dir, f"{timestamp()}.log")
    logs_format = "%(asctime)s | %(levelname)s | %(message)s"
    logs_encoding = "utf-8"
    logging.basicConfig(
        format=logs_format,
        encoding=logs_encoding,
        level=logging.INFO,
        handlers=[
            logging.FileHandler(logs_filename),
            logging.StreamHandler()
        ],
    )

    logger = logging.getLogger(__name__)
    logger.info(f"Writing logs to file: {logs_filename}")

    # Logging config
    logger.info(f"Starting frontend with args:\n{pprint_dict(vars(args))}")

    if args.local:
        # Set up the local environment
        from dotenv import load_dotenv
        if load_dotenv(args.env_file, verbose=True):
            logger.info(
                f"Loaded local environment variables with dotenv from: {args.env_file}"
            )

    app(args)


if __name__ == '__main__':
    main()