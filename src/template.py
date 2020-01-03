#!/usr/bin/env python

class Template:
    def __init__(self, template_dict):
        self.template_dict: dict = template_dict

    @property
    def rules(self):
        return self.template_dict['rules']

    @property
    def known_files(self):
        return self.template_dict['known_files']
