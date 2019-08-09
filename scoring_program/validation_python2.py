#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from __future__ import print_function

import json
import os.path
import sys

import yaml

sys.path.append(os.path.dirname(__file__))
from targets import TARGETS


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
        lines = list(f)
    if not lines:
        sys.exit("unable to read input graphs")
    print("found %d graphs" % len(lines))

    # Check for mismatches between expected and found ids and targets
    expected_ids = {i for i, _ in TARGETS}
    found_targets = {}
    log = ""
    for line in lines:
        graph = json.loads(line.rstrip())
        found_targets.setdefault(graph.get("id"), set()).add(graph.get("framework"))
        if graph.get("id") not in expected_ids:
            log += "\nunexpected id: '%s'" % graph.get("id")
    for i, targets in TARGETS:
        found = found_targets.get(i)
        if found:
            log += "".join("\nmissing target '%s' for id: '%s'" % (t, i) for t in targets - found)
            # log += "".join("\nunexpected target '%s' for id: '%s'" % (t, i) for t in found - targets)
        else:
            log += "\nmissing id: '%s'" % i

    # Report
    print(log, file=sys.stderr)
    with open(os.path.join(output_dir, 'scores.txt'), 'w', encoding="utf-8") as output_file, \
            open(os.path.join(output_dir, 'scores.html'), 'w', encoding="utf-8") as output_html_file:
        print("<!DOCTYPE html>\n<html>\n<head>\n<meta charset=\"UTF-8\">\n<style>\ntable {\n"
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
        print("correct: 1", file=output_file)
    print("done")


if __name__ == "__main__":
    main()