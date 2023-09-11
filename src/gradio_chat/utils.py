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

from typing import (
    Any,
    Type,
    Optional
)

import os
import json
import glob
import logging
from dataclasses import dataclass, asdict

from haikunator import Haikunator

from gradio_chat.models import (
    Setting, 
    Frontend,
    Chat,
    ChatHistory
)


logger = logging.getLogger(__name__)


def haikunate() -> str:
    return Haikunator().haikunate()


def load_json(path: str) -> dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_setting(path: str) -> Setting:
    data = load_json(path)
    data['file'] = path
    return Setting(**data)
    

def load_settings(path: str) -> list[Setting]:
    pattern = os.path.join(path, "**", "*.json")
    paths = glob.glob(pattern, recursive=True)
    settings = []
    for path in paths:
        setting = load_setting(path)
        settings.append(setting)
    return settings


def load_frontend(path: str) -> Frontend:
    data = load_json(path)
    return Frontend(**data)


def load_frontend_from_cache(path: str, cache: str) -> Frontend:
    cache_path = os.path.join(cache, "frontend.json")
    if os.path.exists(cache_path):
        logger.info(f"Loading frontend from cache at: {path}")
        return load_frontend(cache_path)
    logger.info(f"Loading frontend from: {path}")
    return load_frontend(path)


def load_chat(path: str) -> Chat:
    data = load_json(path)
    return Chat(**data)


def load_chats(path: str) -> list[Chat]:
    pattern = os.path.join(path, "**", "*.json")
    paths = glob.glob(pattern, recursive=True)
    chats = []
    for path in paths:
        chat = load_chat(path)
        chats.append(chat)
    return chats


def load_chats_from_cache(path: str) -> list[Chat]:
    path = os.path.join(path, "chats")
    os.makedirs(path, exist_ok=True)
    logger.info(f"Loading chats from cache at: {path}")
    return load_chats(path)


def list_chat_ids(chats: list[Chat]) -> list[str]:
    return list(map(lambda x: x.id, chats))


def find_chat_by_id(id: str, chats: list[Chat]) -> Optional[Chat]:
    filtered = list(filter(lambda x: x.id == id, chats))
    if len(filtered) > 0:
        return filtered[0]
    return None


def find_chat_index_by_id(id: str, chats: list[Chat]) -> int:
    for index, chat in enumerate(chats):
        if chat.id == id:
            return index
    return -1


def set_chat_by_id(id: str, history: ChatHistory, chats: list[Chat]) -> None:
    index = find_chat_index_by_id(id, chats)
    if index < 0:
        return
    logger.info(f"Setting existing chat with id: {id}")
    chat = Chat(id=id, history=history)
    chats[index] = chat


def update_chat_by_id(id: str, chat: Chat, chats: list[Chat]) -> None:
    index = find_chat_index_by_id(id, chats)
    if index < 0:
        return
    logger.info(f"Updating existing chat with id: {id}")
    chats[index] = chat


def del_chat_by_id(id: str, chats: list[Chat]) -> None:
    index = find_chat_index_by_id(id, chats)
    if index < 0:
        return
    logger.info(f"Deleting chat with id: {id}")
    del chats[index]


def pprint_dict(dictionary: dict) -> str:
    return json.dumps(
        dictionary, 
        ensure_ascii=False, 
        indent=2
    )


def pprint_dcls(dcls: Type[dataclass]) -> str:
    return pprint_dict(asdict(dcls))


def empty_chat(id: Optional[str] = None, history: ChatHistory = []) -> Chat:
    if id is None:
        id = haikunate()
    return Chat(id=id, history=history)


def list_setting_ids(settings: list[Setting]) -> list[str]:
    return list(map(lambda x: x.id, settings))


def find_setting_by_id(id: str, settings: list[Setting]) -> Optional[Setting]:
    filtered = list(filter(lambda x: x.id == id, settings))
    if len(filtered) > 0:
        return filtered[0]
    return None