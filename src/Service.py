#!/usr/bin/env python
# Copyright (c) 2015 Vedams Software Solutions PVT LTD
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

class Service(object):

    def __init__(self):
        self.ALL_NODE = ["swift-proxy:True", "swift-object:True",
                         "swift-object-replicator:True",
                         "swift-object-updater:True",
                         "swift-object-auditor:True",
                         "swift-container:True",
                         "swift-container-replicator:True",
                         "swift-container-updater:True",
                         "swift-container-auditor:True",
                         "swift-account:True",
                         "swift-account-replicator:True",
                         "swift-account-reaper:True",
                         "swift-account-auditor:True"]

        self.STORAGE_NODE = ["swift-proxy:False", "swift-object:True",
                             "swift-object-replicator:True",
                             "swift-object-updater:True",
                             "swift-object-auditor:True",
                             "swift-container:True",
                             "swift-container-replicator:True",
                             "swift-container-updater:True",
                             "swift-container-auditor:True",
                             "swift-account:True",
                             "swift-account-replicator:True",
                             "swift-account-reaper:True",
                             "swift-account-auditor:True"]

        self.PROXY_NODE = ["swift-proxy:True", "swift-object:False",
                           "swift-object-replicator:False",
                           "swift-object-updater:False",
                           "swift-object-auditor:False",
                           "swift-container:False",
                           "swift-container-replicator:False",
                           "swift-container-updater:False",
                           "swift-container-auditor:False",
                           "swift-account:False",
                           "swift-account-replicator:False",
                           "swift-account-reaper:False",
                           "swift-account-auditor:False"]
