#!/usr/bin/env python3
import os.path
import sys

import yaml

sys.path.append(os.path.join(os.path.dirname(__file__), 'mtool'))
from main import read_graphs, VALIDATIONS
import validate


def find_files(submission_dir):
    return [os.path.join(root, fn)
            for root, dirnames, fns in os.walk(submission_dir)
            for fn in fns if fn.lower().endswith(".mrp")]


def main():
    # as per the metadata file, input and output directories are the arguments
    [_, input_dir, output_dir] = sys.argv

    metadata = yaml.load(open(os.path.join(input_dir, 'metadata'), 'r'),
                         Loader=yaml.FullLoader)
    for key, value in metadata.items():
        print("%s: %s" % (key, value))

    submission_dir = os.path.join(input_dir, 'res')
    files = find_files(submission_dir)
    if len(files) != 1:
        sys.exit(("submission must include exactly one *.mrp file, but found %d:\n"
                  % len(files)) + "\n".join(files))
    print("validating %s" % files[0])

    graphs, _ = [graph for f in files for graph in read_graphs(f, format="mrp")]
    if not graphs:
        sys.exit("unable to read input graphs")
    print("validating %d graphs" % len(graphs))

    n = sum(validate.core.test(graph, VALIDATIONS, stream=sys.stderr)
            for graph in graphs)

    with open(os.path.join(output_dir, 'scores.txt'), 'w') as output_file:
        if n:
            print("errors: %d" % n, file=output_file)
            sys.exit("%d validation errors occurred" % n)
        print("correct: 1", file=output_file)
    print("wrote %s" % output_file)


if __name__ == "__main__":
    main()
