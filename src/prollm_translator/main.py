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
import json
import logging
from prollm.parser import argument_parser
from prollm.utils import timestamp


logger = logging.getLogger(__name__)


def main() -> None:
    """Implement a main starting point for a prollm application."""
    # Define arguments and parse
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

    # Print the current config
    config = json.dumps(vars(args), indent=2)
    logger.info(f"Starting prollm with config:\n{config}")

    if args.local:
        # Set up the local environment
        from dotenv import load_dotenv
        if load_dotenv(args.env_file, verbose=True):
            logger.info(
                f"Loaded local environment variables with dotenv from: {args.env_file}"
            )


if __name__ == "__main__":
    main()
