#!/usr/bin/env python
import sys
import difflib
from ast import *

from redbaron import *
from redbaron.nodes import *
from flake8_import_order import ImportVisitor
from flake8_import_order.styles import Smarkets

fun = RedBaron('''\
def foo():
    from foo import bar
    from baz import quux
    return bar(quuz)
''')


def process(filetext):
    fst = RedBaron(filetext)
    _process_fst(fst)
    postprocessed = fst.dumps().replace('\n  # nopep8\n', '  # nopep8\n')
    print '\n'.join(difflib.unified_diff(filetext.split('\n'), postprocessed.split('\n')))


def process_lines(lines):
    orig_lines = list(lines)
    import_lines = [(i, line) for i, line in enumerate(lines) if get_import_object_from_line(line) is not None]
    if not import_lines:
        return
    first, last = import_lines[0][0], import_lines[-1][0]
    for i, line in import_lines[first:last+1]:
        if not get_import_object_from_line(line) and not line.startswith('#') and not re.match(r'\s+', line):
            raise ValueError('Import blocks not contiguous')
    new_lines = bubblesort_lines(lines[first:last+1])
    lines[first:last + 1] = new_lines
    print ''.join(difflib.unified_diff(orig_lines, lines))
    
    

def _process_fst(fst):
    import_lines = [(i, node) for i, node in enumerate(fst) if isinstance(node, (FromImportNode, ImportNode))]
    if not import_lines:
        return
    first, last = import_lines[0], import_lines[-1]
    nodes = [fst[i] for i in range(first[0], last[0] + 1)]
    if not (set(map(type, nodes)) <= {FromImportNode, ImportNode, EndlNode, CommentNode}):
        raise ValueError('Import blocks not contiguous')
    new_lines = bubblesort(nodes)
    fst[first[0]:last[0] + 1] = new_lines


def get_sort_key_for_import(import_):
    return Smarkets.import_key(import_)


def is_same_section(import1, import2):
    return Smarkets.same_section(import1, import2)


def newline():
    return RedBaron('\n')[0]

def bubblesort_lines(lst):
    bubble = True
    imports = list(map(get_import_object_from_line, lst))
    lines = [((get_sort_key_for_import(import_) if import_ is not None else None), import_, line) for import_, line in zip(imports, lst)]
    while bubble:
        bubble = False
        for i in range(len(lst)):
            key, import_, line = lines[i]
            if key is None:
                continue
            j = next((j for j in range(i+1, len(lst)) if lines[j][0] is not None), None)
            if j is not None:
                if lines[i][0] > lines[j][0]:
                    bubble = True
                    lines[i], lines[j] = lines[j], lines[i]
                elif j == i + 1 and not is_same_section(lines[i][1], lines[j][1]):
                    lines.insert(j, (None, None, '\n'))
                    bubble = True
    return [l for (k, imp, l) in lines]


def bubblesort(lst):
    bubble = True
    imports = list(map(get_import_object, lst))
    lines = [((get_sort_key_for_import(import_) if import_ is not None else None), import_, line) for import_, line in zip(imports, lst)]
    while bubble:
        bubble = False
        for i in range(len(lst)):
            key, import_, line = lines[i]
            if key is None:
                continue
            j = next((j for j in range(i+1, len(lst)) if lines[j][0] is not None), None)
            if j is not None:
                if lines[i][0] > lines[j][0]:
                    bubble = True
                    lines[i], lines[j] = lines[j], lines[i]
                elif j == i + 1 and not is_same_section(lines[i][1], lines[j][1]):
                    lines.insert(j, (None, None, newline()))
                    bubble = True
    return [l for (k, imp, l) in lines]


def get_import_object(node):
    text = node.dumps()
    visitor = ImportVisitor(['counsyl', 'counsyl_fabric'], [])
    visitor.visit(ast.parse(text))
    try:
        [import_] = visitor.imports
    except ValueError:
        return None
    else:
        return import_


def get_import_object_from_line(line):
    try:
        node = ast.parse(line)
    except SyntaxError:
        # if single lines aren't parsable, ignore them, we only care about single line imports.
        return None
    except TypeError as e:
        from nose.tools import set_trace; set_trace()
    except Exception as e:
        raise
    visitor = ImportVisitor(['counsyl', 'counsyl_fabric'], [])
    visitor.visit(node)
    try:
        [import_] = visitor.imports
    except ValueError:
        return None
    else:
        return import_


if __name__ == '__main__':
    with open(sys.argv[1]) as f:
        print sys.argv
        try:
            process_lines(list(f))
        except ValueError as e:
            print 'Cannot process %s: %s' % (sys.argv[1], e)