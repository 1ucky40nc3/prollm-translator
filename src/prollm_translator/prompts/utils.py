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

import iso639


def parse_iso639(lang: str) -> iso639.Language:
    """Parse a ISO 639-1 string.
    
    Args:
        lang: The language string.
    
    Returns:
        A `iso639.Language` language object.

    Raises:
        iso639.LanguageNotFoundError: The string is not compliant with ISO 639-1.
    """
    return iso639.Language.match(lang)