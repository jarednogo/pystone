#!/usr/bin/python

import sgfparse

if __name__ == '__main__':
    f = open("Artem-Blankie.sgf")
    raw = f.read()
    print sgfparse.make_keys(raw)

