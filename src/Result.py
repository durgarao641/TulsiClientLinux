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
import time
import json
import math
import ConfigParser

class Result(object):

    def __init__(self):
        self.storage_drives_write = None
        self.storage_nodes = None
        self.proxy_nodes = None
        self.storage_node_status_storage_file = []
	self.ip_array_time = {}
	self.conf = ConfigParser.ConfigParser()
        self.conf.read('tulsiclient.conf')
	self.time_duration = int(self.conf.get('heartbeat','time_duration'))*60
    # Function to write the configuration file for User Interface
    def write_config_ui(self,proxy_node_list, storage_node_list,
                        storage_node_drives_file):
        self.storage_drives_write = None
        self.proxy_node_list = proxy_node_list
        self.storage_node_list = storage_node_list
        self.storage_node_drives_file = storage_node_drives_file
        self.proxy_servers = \
            "proxyServer,%s\n" % str(len(self.proxy_node_list))
        self.storage_servers = \
            "storageServer,%s\n" % str(len(self.storage_node_list))
        for i in self.storage_node_drives_file:
            if self.storage_drives_write is None:
                self.storage_drives_write = str(i)
            else:
                self.storage_drives_write = "%s\n%s" % (
                    str(self.storage_drives_write), str(i))
                self.storage_drives_write = str(self.storage_drives_write)
        fo = open("clusterConfig.txt", "w")
        if(self.proxy_servers is None and self.storage_servers is None):
            print "No proxy servers and storage servers are there "
        elif self.proxy_servers is not None and self.storage_drives_write is \
                None:
            fo.write(str(self.storage_drives_write))
        elif self.proxy_servers is not None and self.storage_drives_write is not\
                None:
            fo.write("%s%s%s" % (str(self.proxy_servers),
                                 str(self.storage_servers),
                                 str(self.storage_drives_write)))
        fo.close()
	
    # Function to write the status file of cluster for User Interface
    def write_status_ui(self,data,storage_node_storage_file,
                        proxy_node_status_file,
                        storage_node_status_storage_file):
        self.storage_nodes = None
        self.proxy_nodes = None
        self.storage_node_storage_file = storage_node_storage_file
        self.proxy_node_status_file = proxy_node_status_file
        self.storage_node_status_storage_file = storage_node_status_storage_file
        if(self.storage_node_storage_file is not None):
            for i in self.storage_node_storage_file:
                if self.storage_node_storage_file.index(i) == 0:
                    self.storage_nodes = "%s\n%s" % (
                        i,
                        self.storage_node_status_storage_file[
                            self.storage_node_storage_file.index(i)])
                else:
                    self.storage_nodes = "%s\n%s\n%s" % (
                        self.storage_nodes,
                        i,
                        self.storage_node_status_storage_file[
                            self.storage_node_storage_file.index(i)
                        ])
                    self.storage_nodes = str(self.storage_nodes)
        if(self.proxy_node_status_file is not None):
            for i in self.proxy_node_status_file:
                if self.proxy_node_status_file.index(i) == 0:
                    self.proxy_nodes = "\n%s" % i
                else:
                    self.proxy_nodes = "%s\n%s" % (self.proxy_nodes, i)
                    self.proxy_nodes = self.str(self.proxy_nodes)
	self.heartBeat(data)
        fo = open("clusterStatus.txt", "w")
        if(self.storage_nodes is None and self.proxy_nodes is None):
            print "no storage nodes and proxy nodes are coming"
        elif(self.storage_nodes is not None and self.proxy_nodes is None):
            fo.write(str(self.storage_nodes))
        elif(self.storage_nodes is None and self.proxy_nodes is not None):
            fo.write(str(self.proxy_nodes))
        elif(self.storage_nodes is not None and self.proxy_nodes is not None):
            fo.write("%s%s" % (str(self.storage_nodes), str(self.proxy_nodes)))
        
	fo.close()
	

    def heartBeat(self,data):
	data=json.loads(data)	
	host_name=data["hostname"]
	print "Heart Beat:",host_name
	self.ip_array_time[host_name]=math.ceil(time.time())
	present_time=math.ceil(time.time())
	for host in self.ip_array_time:
		if present_time-self.ip_array_time[host]>self.time_duration:
			if self.proxy_nodes.find(host) != -1:
				pos = self.proxy_nodes.find(',')
				self.proxy_nodes = self.proxy_nodes[:pos+1]+'w'
			else:
				first_pos=self.storage_nodes.find(host)
				sec_pos=self.storage_nodes.find(host,first_pos)
				first_brace=self.storage_nodes.find('[',sec_pos)
				sec_brace=self.storage_nodes.find(']',first_brace)
				if sec_brace - first_brace == 1:
					self.storage_nodes = self.storage_nodes[:first_brace+1] + "u'Tulsi:False'],w"+self.storage_nodes[sec_brace+3:]
				else:
					self.storage_nodes = self.storage_nodes[:first_brace+1]+"u'Tulsi:False',"+self.storage_nodes[first_brace+1:]
	print self.storage_nodes
	print self.proxy_nodes
	print "Heart Beat Ends"
									
						
	

