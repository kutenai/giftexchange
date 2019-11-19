import argparse
from collections import defaultdict
from os.path import exists
import random
import re

def get_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument('--history_files',
        nargs='*',
        help="Input file with previous years draws")

    return parser.parse_args()


def read_history(files):
    """
    Accepts a list of files
    For each file, read in the name:name pairs, and add to the history
    """

    history = defaultdict(set)
    for filename in files:
        if exists(filename):
            with open(filename, 'r') as fp:
                for line in fp:
                    line = line.strip()
                    m = re.match("(\w+)\s*:\s*(\w+)", line)
                    if m:
                        history[m.group(1)].add(m.group(2))
    return history


def get_history(person, history):
    """ Get a list of people this person has drawn in previous years """
    drawn = set()
    for year in history:
        drawee = year.get('Draws').get(person)
        if drawee:
            drawn.add(drawee)

    return drawn


def draw(peeps, couples, history):
    """ Draw the pairs, considering the history if provided """

    random.seed()
    draws = {} # Output set. Key is drawer, value is drawee
    drawn = set() # List of those already drawn this year.

    couplemap = defaultdict(str)
    for couple in couples:
        a, b = couple
        couplemap[a] = b
        couplemap[b] = a

    for drawer in peeps:
        # List of available people.
        # Remove the drawer
        # Remove anyone already drawn
        # Remove anyone in the history for this drawer
        available = [p for p in peeps
            if p != drawer
            and p != couplemap[p]
            and p not in drawn
            and p not in get_history(drawer, history)]

        draw = random.choice(available)
        draws[drawer] = draw
        drawn.add(draw)
    return draws


def main():
    args = get_arguments()
    history = []
    if args.history_files:
        history = get_history(args.history_files)
    else:
        # Just an example..
        history = [
            {
                'Year': '2018',
                'Draws': {
                    'Ed': 'Dale',
                    'Anne': 'Dave',
                }
            },
            {
                'Year': '2019',
                'Draws': {
                }
            }
        ]

    peeps = ['Eddie', 'Beverly', 'Ed', 'Vicki', 'Dale', 'Adrianna', 'Dan', 'Deb', 'Dave', 'Michelle', 'Anne']
    couples = [['Eddie', 'Beverly'], ['Ed', 'Vicki'], ['Dale', 'Adrianna'], ['Dan', 'Deb'], ['Dave', 'Michelle']]

    result = draw(peeps, couples, history)

    for k in sorted(result.keys()):
        v = result[k]
        print(f"{k}: {v}")


if __name__ == "__main__":
    main()


