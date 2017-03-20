# -*- coding:utf-8 -*-
import yaml as pyyaml

class YAML_Parser:
    def __init__(self, file):
        self.file = file

    def parse(self):
        with open(self.file, 'r') as stream:
            try:
                return pyyaml.load(stream)
            except pyyaml.YAMLError as exc:
                print(exc)
