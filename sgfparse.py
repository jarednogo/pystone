#!/usr/bin/python

"""
regex to search sgfs by metadata
"""

import re

from sys import argv,exit, stdout, stderr

def process(filename):

    # open file
    with open(filename) as f:
        raw = f.read()

    keys = make_keys(raw)
    moves = pull_moves(raw)

    return keys, moves

def make_keys(raw):
    # make dictionary
    KEYS = {}

    # Look for keys
    L_ = re.findall('[A-Z]{1,2}\[[^\]]+\]', raw)
    L = [item for item in L_ if not item.startswith('B[') \
            and not item.startswith('W[') and not item.startswith('BL[')
            and not item.startswith('WL[') and not item.startswith('C[')]

    for item in L:
        i = item.index('[') 
        j = item.index(']') 
        KEYS[item[:i]] = item[i+1:j]
    return KEYS

def pull_moves(raw):
    moves = []
    lines = raw.split('\n')
    for line in lines:
        if line.startswith(';'):
            # Player
            assert line[1] == "B" or line[1] == "W"

            # Regular expression to find two characters following '['
            m = re.search('(?<=\[)[a-s]{2}', line)
            if m:
                pair = m.group(0)
                col = translate(pair[0])
                row = translate(pair[1])
                move = (col,row)
                moves.append(move)
    return moves

def translate(let):
    alphabet = 'abcdefghijklmnopqrs'
    assert let in alphabet
    return alphabet.index(let)

def untranslate(num):
    alphabet = 'abcdefghijklmnopqrs'
    assert num >=0 and num < 19
    return alphabet[num]


def write(filename, moves, keys={}):
    colors = ["W", "B"]
    move_num = 1
    with open(filename, 'w') as f:
        f.write('(;\n')
        for move in moves:
            c0,c1 = untranslate(move[0]), untranslate(move[1])
            string = ';' + colors[move_num % 2] + '[' + c0 + c1 + ']\n'
            f.write(string)
            move_num += 1
        f.write(')')

if __name__ == '__main__':
    if not argv[1:]:
        print("Need sgf filename")
        print("Usage: {} [sgf] [key]".format(argv[0]))
        print("Usage: {} [sgf]".format(argv[0]))
        exit(1)

    keys,moves = process(argv[1])

    if not argv[2:]:
        for key in keys:
            print(key + ':', keys[key])
        print(moves)
        exit(2)

    try:
        print(keys[argv[2]])
    except KeyError:
        stderr.write("Key not found: " + argv[2] + '\n')
