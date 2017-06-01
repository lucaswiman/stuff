import sys
import os

VERSIONS = {'_compiled_2_7': (2, 7),
            '_compiled_3_0': (3, 0),
            '_compiled_3_1': (3, 1),
            '_compiled_3_2': (3, 2),
            '_compiled_3_3': (3, 3),
            '_compiled_3_4': (3, 4),
            '_compiled_3_5': (3, 5),
            '_compiled_3_6': (3, 6)}
root = os.path.abspath(os.path.dirname(__file__))


def _get_available_versions():
    for version in os.listdir(root):
        if version in VERSIONS:
            yield version


def _get_version():
    available_versions = sorted(_get_available_versions())[::-1]
    for version in available_versions:
        if VERSIONS[version] <= sys.version_info:
            return version


# We should pass `__name__` as an argument, because
# we can't access `__name__` after module deletion
def _import_module(name):
    version = _get_version()
    version_path = os.path.join(root, version)
    sys.path.insert(0, version_path)
    del sys.modules[name]
    __import__(name)


_import_module(__name__)
