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


class KeywordSpecification:
    def __init__(
        self,
        argument_specification=None,
        documentation=None,
        argument_types=None,
    ) -> None:
        self.argument_specification = argument_specification
        self.documentation = documentation
        self.argument_types = argument_types
