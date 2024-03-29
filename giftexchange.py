import argparse
from collections import defaultdict
from os.path import exists
import random
import re
import sys
import json


def get_arguments():
    """
    Get arguments from the command line
    :return:
    """
    parser = argparse.ArgumentParser()

    parser.add_argument('peeps', help="List of people and their spouses")

    parser.add_argument('--history_files',
        nargs='*',
        help="Input file with previous years draws")

    parser.add_argument('--output_file', '-o', help="Specify the output file to write to")

    return parser.parse_args()


def read_history(files):
    """
    Accepts a list of files
    For each file, read in the name:name pairs, and add to the history
    """
    print(sys.stderr, f"History files are {files}")

    history = defaultdict(list)
    for filename in files:
        if exists(filename):
            with open(filename, 'r') as fp:
                for line in fp:
                    line = line.strip()
                    if m := re.match(r"(\w+)\s*:\s*(\w+)", line):
                        history[m.group(1)].append(m.group(2))
    return history


def draw(peeps, couples, history):
    """ Draw the pairs, considering the history if provided """

    random.seed()
    draws = {}  # Output set. Key is drawer, value is drawee
    drawn = set()  # List of those already drawn this year.

    for drawer in peeps:
        # List of available people.
        # Remove the drawer
        # Remove anyone already drawn
        # Remove anyone in the history for this drawer
        available = [p for p in peeps
            if p != drawer
            and p != couples[drawer]
            and p not in drawn
            and p not in history[drawer]]

        draw = random.choice(available)
        draws[drawer] = draw
        drawn.add(draw)

    return draws


def draw_with_retries(peeps, couples, history, retries=3):

    while retries:
        try:
            draws = draw(peeps, couples, history)
            return draws
        except IndexError as e:
            retries -= 1
            print(f"Failed iteration. Will try again {retries} times")

    return None


def read_peeps(file):
    """
    Read in the list of people.
    Can be a single person, OR a couple
    Couples are defined as:
        Name and Name

    Sinles are just
        Name
    :param file:
    :return:
    """
    peeps = []

    couples = defaultdict(str)

    with open(file, 'r') as fp:
        for line in fp:
            line = line.strip()
            if m:= re.match(r'(\w+)\s+and\s+(\w+)', line):
                a, b = m.group(1), m.group(2)
                peeps.append(a)
                peeps.append(b)
                couples[a] = b
                couples[b] = a
            else:
                peeps.append(line)

    return peeps, couples


def main():
    args = get_arguments()
    history = []

    peeps, couples = read_peeps(args.peeps)
    if args.history_files:
        history = read_history(args.history_files)
    result = draw_with_retries(peeps, couples, history, retries=10)

    jhist = json.dumps(dict(history))

    if result:
        for k in sorted(result.keys()):
            v = result[k]
            print(f"{k}: {v}")

        if args.output_file:
            with open(args.output_file, 'w') as fp:
                for k in sorted(result.keys()):
                    v = result[k]
                    fp.write(f"{k}: {v}\n")

    else:
        print("Sorry, could not generate a sequence. Too much history??")


if __name__ == "__main__":
    main()


