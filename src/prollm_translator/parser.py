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
import argparse


def local_path(path: str) -> str | None:
    """Typing for provided path arguments.

    Args:
        path: A local path of a file or directory.

    Returns:
        The path if it exists.

    Raises:
        ArgumentTypeError: The provided path doesn't exist.
    """
    if os.path.exists(path):
        return path
    else:
        raise argparse.ArgumentTypeError(f"The provided '{path=}' doesn't exist!")


def argument_parser() -> argparse.ArgumentParser:
    """Return an argument parser.

    Returns:
        An argument parser.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-l",
        "--local",
        action="store_true",
        default=False,
        help="Whether this is a local dev environment or not.",
    )
    parser.add_argument(
        "-e",
        "--env_file",
        default=".env",
        type=local_path,
        help="The path if an environment variables file.",
    )
    parser.add_argument(
        "--log_dir",
        default="logs",
        type=str,
        help="The path to the logging directory.",
    )
    return parser
