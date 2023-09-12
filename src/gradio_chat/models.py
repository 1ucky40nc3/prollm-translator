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
    Optional
)

from dataclasses import dataclass

Update = dict
UserMessage = str
BotMessage = str | None
ChatHistory = list[tuple[UserMessage, BotMessage]]


@dataclass
class Setting:
    """A settings object.
    
    Attrs:
        id: The ID (name) of the setting.
        file: A JSON file with the setting data.
        data: The setting data.
    """
    id: str
    file: str
    data: dict[str, Any]


@dataclass
class Frontend:
    """A frontend object.

    Attrs:
        setting_id: The ID of the current setting.
        chat_id: The ID of the current chat.
    """
    setting_id: str
    chat_id: Optional[str]


@dataclass
class Chat:
    """A chat object.
    
    Attrs:
        id: A chat's ID (name).
        history: The chat history.
    """
    id: str
    history: ChatHistory
