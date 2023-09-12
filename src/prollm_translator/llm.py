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

from typing import Any, Generator

import os
from dataclasses import dataclass

import openai


@dataclass
class OpenAiChatCompletionChunkChoiceDelta:
    """A OpenAI chat completion chunk choice delta object.

    Attrs:
        content: The content of the delta object.
        role: The role of the chunk content creator.
    """
    content: str | None = None
    role: str | None = None

@dataclass
class OpenAiChatCompletionChunkChoice:
    """A OpenAI chat completion chunk choice object.

    Attrs:
        index: The index of the choice.
        delta: The chunk object delta.
    """
    index: int
    delta: OpenAiChatCompletionChunkChoiceDelta
    finish_reason: str | None


    def __post_init__(self) -> None:
        # Cast the delta
        if not isinstance(self.delta, OpenAiChatCompletionChunkChoiceDelta):
            self.delta = OpenAiChatCompletionChunkChoiceDelta(**self.delta)


@dataclass
class OpenAiChatCompletionChunk:
    """A OpenAI chat completion chunk object.

    Attrs:
        id: The ID of the chat completion chunk
        object: The type of the chat completion object.
        created: A timetamp (unix epoch time) of the chat completion object creation.
        model: The OpenAI chat completion model ID.
        choices: A list of chat completion choices of this chunk.
        finish_reason: The finish reason of the chat completion endpoint.
    """
    id: str
    object: str
    created: int
    model: str
    choices: list[OpenAiChatCompletionChunkChoice]

    def __post_init__(self) -> None:
        # Cast the choices
        for i, choice in enumerate(self.choices):
            if not isinstance(choice, OpenAiChatCompletionChunkChoice):
                self.choices[i] = OpenAiChatCompletionChunkChoice(**choice)

    def get_output(self) -> str:
        return self.choices[0].delta.content



def openai_chat_completion(
    messages: list[dict],
    model: str = "gpt-3.5-turbo-0613",
    functions: list[dict] | None = None,
    function_call: str | None = None,
    user: str | None = None,
    return_chat_completion: bool = False, 
    openai_api_key: str | None = None, 
    **kwargs
) -> Generator[str | tuple[str, OpenAiChatCompletionChunk], None, None]:
    """Generate a OpenAI chat completion.

    Note:
        Further details on how to use the OpenAI chat completion can be found at:
            https://platform.openai.com/docs/api-reference/chat/create?lang=python

    Args:
        messages: A list of message dictionaries. A message has the keys 'role' and 'content'.
        model: A unique string identifier of an OpenAI chat completion model.
        functions: A list of function dictionaries.
        function_call: Controll how the chat completion model should call functions.
        user: Provide a user ID to monitore and detect abuse.
        return_chat_completion: Whether to also return the `OpenAIObject` 
            from the OpenAI chat completion API.
        openai_api_key: An optional OpenAI API-Key.
            This can also be provided through the 'OPENAI_API_KEY' environment variable.

    Returns:
        A generator that returns the output chunks or tuples of output chunks and chunk objects.

    Raises:
        ValueError: No OpenAI API-Key was provided.
    """
    openai_api_key = openai_api_key or os.getenv("OPENAI_API_KEY")
    if openai_api_key is None:
        raise ValueError(
            "An OpenAI API-Key has to be provided in order to use the OpenAI chat completion endpoint!"
        )
    else:
        # Set the OpenAI API-Key manually
        openai.api_key = openai_api_key

    kwargs = dict(
        **kwargs,
        model=model,
        messages=messages,
        functions=functions,
        function_call=function_call,
        user=user,
        stream=True
    )
    # Filter out `None` key-value-pairs - We don't send them to the chat completion endpoint
    kwargs = {k: v for k, v in kwargs.items() if v is not None}

    completion = openai.ChatCompletion.create(**kwargs)

    for chunk in completion:
        chunk = OpenAiChatCompletionChunk(**chunk)
        output = chunk.get_output()
        if return_chat_completion:
            yield output, chunk
        else:
            yield output