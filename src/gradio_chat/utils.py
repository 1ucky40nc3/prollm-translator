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
import datetime
from dataclasses import dataclass, asdict

from haikunator import Haikunator

from gradio_chat.models import (
    Setting, 
    Frontend,
    Chat,
    ChatHistory
)


logger = logging.getLogger(__name__)


def timestamp() -> str:
    """Return a current timestamp."""
    return datetime.datetime.now().strftime("%Y%m%d%H%M%S")


def haikunate() -> str:
    """Return a random name."""
    return Haikunator().haikunate()


def load_json(path: str) -> dict[str, Any]:
    """Load JSON file content."""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_setting(path: str) -> Setting:
    """Load settings from a JSON file."""
    data = load_json(path)
    data['file'] = path
    return Setting(**data)
    

def load_settings(path: str) -> list[Setting]:
    """Load multiple settings in a directory."""
    pattern = os.path.join(path, "**", "*.json")
    paths = glob.glob(pattern, recursive=True)
    settings = []
    for path in paths:
        setting = load_setting(path)
        settings.append(setting)
    return settings


def load_frontend(path: str) -> Frontend:
    """Initialize a frontend from JSON file settings."""
    data = load_json(path)
    return Frontend(**data)


def load_frontend_from_cache(path: str, cache: str) -> Frontend:
    """Initialize a cached frontend.
    
    Args:
        path: The fallback path for a JSON frontend settings file.
        cache: The cache directory with a 'frontend.json' JSON 
            frontend settings file w/ cached data.
    
    Returns:
        The initialized frontend.
    """
    cache_path = os.path.join(cache, "frontend.json")
    if os.path.exists(cache_path):
        logger.info(f"Loading frontend from cache at: {cache_path}")
        return load_frontend(cache_path)
    logger.info(f"Loading frontend from: {path}")
    return load_frontend(path)


def load_chat(path: str) -> Chat:
    """Initialize a chat from a JSON file."""
    data = load_json(path)
    return Chat(**data)


def load_chats(path: str) -> list[Chat]:
    """Initialize multiple chats from JSON files in a directory."""
    pattern = os.path.join(path, "**", "*.json")
    paths = glob.glob(pattern, recursive=True)
    chats = []
    for path in paths:
        chat = load_chat(path)
        chats.append(chat)
    return chats


def load_chats_from_cache(path: str) -> list[Chat]:
    """Initialize cached chats from JSON files."""
    path = os.path.join(path, "chats")
    os.makedirs(path, exist_ok=True)
    logger.info(f"Loading chats from cache at: {path}")
    return load_chats(path)


def list_chat_ids(chats: list[Chat]) -> list[str]:
    """Return the chat IDs.
    
    Args:
        chats: A list of chats.

    Returns:
        The IDs of the chats (in the same order).
    """
    return list(map(lambda x: x.id, chats))


def find_chat_by_id(id: str, chats: list[Chat]) -> Optional[Chat]:
    """Find a single chat by it's ID.
    
    Args:
        id: A chat ID.
        chats: A list of chats.
    
    Returns:
        A matched chat or `None`.
    """
    filtered = list(filter(lambda x: x.id == id, chats))
    if len(filtered) > 0:
        return filtered[0]
    return None


def find_chat_index_by_id(id: str, chats: list[Chat]) -> int:
    """Find the index of a chat by the chat ID.
    
    Args:
        id: A chat ID.
        chats: A list of chats.
    
    Returns:
        The value `-1` if we couldn't find a chat with the ID
        else the index of the matched chat (in the list of chats).
    """
    for index, chat in enumerate(chats):
        if chat.id == id:
            return index
    return -1


def set_chat_by_id(id: str, history: ChatHistory, chats: list[Chat]) -> None:
    """Set an update the a chat's history.
    
    Args:
        id: The ID of the chat we want to update.
        history: The chat history we want to set.
        chats: A list of chats, including the chat we want to update.
    """
    index = find_chat_index_by_id(id, chats)
    if index < 0:
        return
    logger.info(f"Setting existing chat with id: {id}")
    chat = Chat(id=id, history=history)
    chats[index] = chat


def update_chat_by_id(id: str, chat: Chat, chats: list[Chat]) -> None:
    """Update a chat.
    
    Args:
        id: The ID of the chat we want to update.
        chat: The updated chat we want to set.
        chats: A list of chats, including the chat we want to update.
    """
    index = find_chat_index_by_id(id, chats)
    if index < 0:
        return
    logger.info(f"Updating existing chat with id: {id}")
    chats[index] = chat


def del_chat_by_id(id: str, chats: list[Chat]) -> None:
    """Delete a chat.
    
    Args:
        id: The ID of the chat we want to delete.
        chats: A list of chats, including the chat we want to delete.
    """
    index = find_chat_index_by_id(id, chats)
    if index < 0:
        return
    logger.info(f"Deleting chat with id: {id}")
    del chats[index]


def pprint_dict(dictionary: dict) -> str:
    """Return a pretty string of a dictionary."""
    return json.dumps(
        dictionary, 
        ensure_ascii=False, 
        indent=2
    )


def pprint_dcls(dcls: Type[dataclass]) -> str:
    """Return a pretty string representation of a dictionary."""
    return pprint_dict(asdict(dcls))


def empty_chat(id: Optional[str] = None, history: ChatHistory = []) -> Chat:
    """Return an empty chat.
    
    Args:
        id: An optional ID for the empty chat.
        history: The history of the chat.
    
    Returns:
        The initialized chat.
    """
    if id is None:
        id = haikunate()
    return Chat(id=id, history=history)


def list_setting_ids(settings: list[Setting]) -> list[str]:
    """Return the settings' IDs.
    
    Args:
        settings: A list of settings.

    Returns:
        The IDs of the settings (in the same order).
    """
    return list(map(lambda x: x.id, settings))


def find_setting_by_id(id: str, settings: list[Setting]) -> Optional[Setting]:
    """Find a single setting by it's ID.
    
    Args:
        id: A setting ID.
        chats: A list of settings.
    
    Returns:
        A matched setting or `None`.
    """
    filtered = list(filter(lambda x: x.id == id, settings))
    if len(filtered) > 0:
        return filtered[0]
    return None