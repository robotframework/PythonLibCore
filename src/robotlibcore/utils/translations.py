# Copyright 2017- Robot Framework Foundation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import json
from pathlib import Path
from typing import Optional

from robot.api import logger


def _translation(translation: Optional[Path] = None):
    if translation and isinstance(translation, Path) and translation.is_file():
        with translation.open("r") as file:
            try:
                return json.load(file)
            except json.decoder.JSONDecodeError:
                logger.warn(f"Could not convert json file {translation} to dictionary.")
                return {}
    else:
        return {}


def _translated_keywords(translation_data: dict) -> list:
    return [item.get("name") for item in translation_data.values() if item.get("name")]
