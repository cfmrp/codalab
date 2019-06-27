#!/usr/bin/env python3
import os.path
import sys

import yaml

sys.path.append(os.path.join(os.path.dirname(__file__), 'mtool'))
from main import read_graphs
import score

"""
The scoring program will have to follow the standard CodaLab directory structure for the reference data, the system
submission, and the output ``scores.txt`` file:
https://github.com/codalab/codalab-competitions/wiki/User_Building-a-Scoring-Program-for-a-Competition#directory-structure-for-submissions

Be sure that your evaluation script gives clear error messages when it fails.
For example, if there is a formatting error in someone's submission, your script should explain the problem and exit
with an error status (e.g., ``sys.exit("some error message")`` in Python).

Be sure that your evaluation script is writing the output in the right format; it should print lines of the format
``<metric name>:<score>`` in the  ``scores.txt`` file. For example:

        correct:1
        f-score:0.74
"""


def find_files(submission_dir):
    return [os.path.join(root, fn)
            for root, dirnames, fns in os.walk(submission_dir)
            for fn in fns if fn.lower().endswith(".mrp")]


def filter_by_framework(graphs, framework):
    if framework == "all":
        return graphs
    return [graph for graph in graphs if graph.framework == framework]


def main():
    # as per the metadata file, input and output directories are the arguments
    [_, input_dir, output_dir] = sys.argv
    submission_dir = os.path.join(input_dir, 'res')
    gold_dir = os.path.join(input_dir, 'ref')
    files = find_files(submission_dir)
    gold_files = find_files(gold_dir)
    metadata = yaml.load(open(os.path.join(input_dir, 'metadata'), 'r'),
                         Loader=yaml.FullLoader)
    for key, value in metadata.items():
        print(key + ': ' + str(value))
    with open(os.path.join(output_dir, 'scores.txt'), 'w') as output_file, \
            open(os.path.join(output_dir, 'scores.html'), 'w') as output_html_file:
        # html style
        output_html_file.write("<!DOCTYPE html>\n"
                               "<html>\n"
                               "<head>\n"
                               "<style>\n"
                               "table {\n"
                               "font-family: Tahoma, Geneva, sans-serif;\n"
                               "border: 0px solid #000000;\n"
                               "width: 100%;\n"
                               "height: 200px;\n"
                               "text-align: center;\n"
                               "border-collapse: collapse;\n"

                               # "padding-right: 150px;\n"
                               "}\n"
                               "td, th {\n"
                               "border: 1px solid #000000;\n"
                               "padding: 3px 2px;\n"
                               "}\n"
                               "tbody td {\n"
                               "font-size: 13px;\n"
                               "}\n"


                               "thead {\n"
                               "background: #0B6FA4;\n"
                               "border-bottom: 5px solid #000000;\n"
                               "}\n"
                               "thead th {\n"
                               "font-size: 14px;\n"
                               "font-weight: bold;\n"
                               "color: #FFFFFF;\n"
                               "text-align: center;\n"
                               "border-left: 2px solid #000000;\n"
                               "}\n"
                               "</style>\n"
                               "<title>Detailed Results</title>\n"
                               "</head>\n"
                               "<body>\n")
        # header
        output_html_file.write('<h1>Detailed Results</h1>\n')
        # table
        output_html_file.write('<table style="width:100%">\n'
                               '<thead>\n'
                               '<tr>\n'
                               '<th rowspan="3">Framework</th>\n'
                               '<th>P</th>\n'
                               '<th>R</th>\n'
                               '<th>F1</th>\n'
                               '</tr>\n'
                               '</thead>\n'
                               '<tbody>\n')

        with open(files[0], encoding="utf-8") as f:
            graphs, _ = read_graphs(f, format="mrp")
        if not graphs:
            sys.exit("unable to read input graphs")

        gold, _ = [graph for f in gold_files for graph in read_graphs(f, format="mrp")]
        if not gold:
            sys.exit("unable to read gold graphs")

        # results - P, R, F1
        for framework in ["all", "dm", "psd", "eds", "ucca", "amr"]:
            print("Running '%s' evaluation" % framework)

            # write results to html file and append to values
            output_html_file.write("<tr>\n"
                                   "<td>%s</td>" % framework)

            result = score.mces.evaluate(filter_by_framework(gold, framework),
                                         filter_by_framework(graphs, framework))

            if framework == "all":
                output_file.write("correct: %f\n" % result["all"]["f"])
            output_html_file.write("<td>%.3f</td>\n" % result["all"]["p"])
            output_html_file.write("<td>%.3f</td>\n" % result["all"]["r"])
            output_html_file.write("<td>%.3f</td>\n" % result["all"]["f"])
            output_html_file.write("</tr>\n")

        output_html_file.write("</tbody>\n"
                               "</table>\n"
                               "</body>\n"
                               "</html>")


if __name__ == "__main__":
    main()
