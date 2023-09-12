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
import openai


def openai_chat_completion(
    messages: list[dict],
    model: str = "gpt-3.5-turbo-0613",
    functions: list[dict] | None = None,
    function_call: str | None = None,
    user: str | None = None,
    return_chat_completion: bool = False, 
    openai_api_key: str | None = None, 
    **kwargs
) -> str | tuple[str, openai.openai_object.OpenAIObject]:
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
        The generated output message and optionally the `OpenAIObject`.

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
        user=user
    )
    # Filter out `None` key-value-pairs - We don't send them to the chat completion endpoint
    kwargs = {k: v for k, v in kwargs.items() if v is not None}

    completion = openai.ChatCompletion.create(**kwargs)
    output = completion.choices[0].message.content

    if return_chat_completion:
        return output, completion
    return output