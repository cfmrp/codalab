#!/usr/bin/env python3
import os.path
import sys
from io import StringIO

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

    with open(files[0], encoding="utf-8") as f:
        graphs, _ = read_graphs(f, format="mrp")
    if not graphs:
        sys.exit("unable to read input graphs")
    print("validating %d graphs" % len(graphs))

    log = StringIO
    n = sum(validate.core.test(graph, VALIDATIONS, stream=log)
            for graph in graphs)
    log = log.getvalue()
    print(log, file=sys.stderr)

    with open(os.path.join(output_dir, 'scores.txt'), 'w') as output_file, \
            open(os.path.join(output_dir, 'scores.html'), 'w') as output_html_file:
        print("<!DOCTYPE html>\n<html>\n<head>\n<style>\ntable {\n"
              "font-family: Tahoma, Geneva, sans-serif;\n"
              "border: 0px solid #000000;\n"
              "width: 100%;\nheight: 200px;\ntext-align: center;\n"
              "border-collapse: collapse;\n}\n"
              "td, th {\nborder: 1px solid #000000;\npadding: 3px 2px;\n}\n"
              "tbody td {\nfont-size: 13px;\n}\n"
              "thead {\nbackground: #0B6FA4;\n"
              "border-bottom: 5px solid #000000;\n}\n"
              "thead th {\nfont-size: 14px;\n"
              "font-weight: bold;\ncolor: #FFFFFF;\ntext-align: center;\n"
              "border-left: 2px solid #000000;\n}\n</style>\n"
              "<title>Validation Results</title>\n</head>\n"
              "<body>\n<h1>Validation Results</h1>\n"
              "<pre>" + log + "</pre>"
              "</tbody>\n</table>\n</body>\n</html>", file=output_html_file)

        if n:
            print("errors: %d" % n, file=output_file)
            sys.exit("%d validation errors occurred" % n)
        print("correct: 1", file=output_file)
    print("done")


if __name__ == "__main__":
    main()
