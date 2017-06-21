#!/usr/bin/env python
from __future__ import print_function

import argparse
import ast
import re
import sys
import difflib

from flake8_import_order import ImportVisitor
from flake8_import_order.styles import Smarkets
from six.moves import StringIO


class NonContiguousImportError(Exception):
    pass


def process_lines(lines):
    lines = list(lines)
    import_lines = [(i, line) for i, line in enumerate(lines) if get_import_object_from_line(line) is not None]
    if not import_lines:
        return lines
    first, last = import_lines[0][0], import_lines[-1][0]
    for line in lines[first:last+1]:
        if not get_import_object_from_line(line) and not line.startswith('#') and not re.match(r'\s+', line):
            raise NonContiguousImportError('Import blocks not contiguous')
    new_lines = bubblesort_lines(lines[first:last+1])
    lines[first:last + 1] = new_lines
    return lines


def get_sort_key_for_import(import_):
    return Smarkets.import_key(import_)


def is_same_section(import1, import2):
    return Smarkets.same_section(import1, import2)


def bubblesort_lines(lst):
    bubble = True
    imports = list(map(get_import_object_from_line, lst))
    lines = [((get_sort_key_for_import(import_) if import_ is not None else None), import_, line) for import_, line in zip(imports, lst)]
    while bubble:
        bubble = False
        for i in range(len(lines)):
            key, import_, line = lines[i]
            if key is None:
                continue
            try:
                j = next((j for j in range(i+1, len(lines)) if lines[j][0] is not None), None)
            except Exception as e:
                from nose.tools import set_trace; set_trace()
            if j is not None:
                if lines[i][0] > lines[j][0]:
                    bubble = True
                    lines[i], lines[j] = lines[j], lines[i]
                elif j == i + 1 and not is_same_section(lines[i][1], lines[j][1]):
                    lines.insert(j, (None, None, '\n'))
                    bubble = True
                elif j == i + 2 and is_same_section(lines[i][1], lines[j][1]) and lines[i + 1][2] == '\n':
                    # Extra newline between sections.
                    bubble = True
                    del lines[i + 1]
                    break
    return [l for (k, imp, l) in lines]


def get_import_object_from_line(line):
    try:
        node = ast.parse(line)
    except SyntaxError:
        # if single lines aren't parsable, ignore them, we only care about single line imports.
        return None
    visitor = ImportVisitor(['counsyl', 'counsyl_fabric'], [])
    visitor.visit(node)
    try:
        [import_] = visitor.imports
    except ValueError:
        return None
    else:
        return import_


def main():
    parser = argparse.ArgumentParser(description='Sort imports according to the `smarkets` style.')
    parser.add_argument(
        'input', nargs='?', default='-',
        help='File to process. Defaults to "-" (stdin)',
    )
    parser.add_argument(
        '-w', '--write', action='store_true', default=False,
        help='Write the changes to disk')
    parser.add_argument(
        '-q', '--quiet', action='store_true', default=False,
        help='Suppress display of diffs')
    args = parser.parse_args()
    if args.input == '-':
        input = sys.stdin
        if args.write:
            # We're outputting the file contents, so we should
            # suppress display of diffs
            args.quiet = True
    else:
        input = open(args.input)
    lines = list(input)
    input.close()
    output_lines = process_lines(lines)
    if not args.quiet:
        diff = ''.join(difflib.unified_diff(lines, output_lines, args.input, args.input))
        if diff:
            print(diff)
    if args.write:
        output = sys.stdout if args.input == '-' else open(args.input, 'w')
        output.write(''.join(output_lines))
        output.flush()


if __name__ == '__main__':
    try:
        main()
    except NonContiguousImportError as e:
        sys.stderr.write('Cannot process %s: %s\n' % (sys.argv[1], e))
        sys.exit(1)
