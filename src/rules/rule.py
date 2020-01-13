#!/usr/bin/env python


class Rule():
    def __init__(self, expression):
        self.expression: bool = expression

    def __bool__(self):
        return self.expression

    def __str__(self):
        return "%s" % (self.expression)
