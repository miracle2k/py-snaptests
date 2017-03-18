from __future__ import absolute_import
import os
from os import path
import hashlib
import pickle
import pytest


def pytest_addoption(parser):
    parser.addoption("--no-sni", action="store_true",
        help="skip tests that require sni")

    parser.addoption("--write", action="store", default='',
        help="specify which snapshot tests to write/update")
    parser.addoption("--write-all", action="store_true",
        help="update all snapshots")


class SnapshotOperations(object):

    def __init__(self, directory):
        self.directory = directory

    def get_snapshot(self, id):
        filename = path.join(self.directory, id)
        if not path.exists(filename):
            raise ValueError()
        with open(filename, 'rb') as f:
            return self.read_from_file(f)

    def write_snapshot(self, id, data):
        if not path.exists(self.directory):
            os.makedirs(self.directory)
        filename = path.join(self.directory, id)
        with open(filename, 'wb') as f:
            self.write_to_file(f, data)

    def read_from_file(self, f):
        return r.read()

    def write_to_file(self, f, data):
        f.write(data)


class PickleOperations(SnapshotOperations):

    def read_from_file(self, f):
        return pickle.load(f)

    def write_to_file(self, f, data):
        pickle.dump(data, f)


class TextOperations(SnapshotOperations):

    def read_from_file(self, f):
        return f.read().decode('utf-8')

    def write_to_file(self, f, data):
        f.write(data.encode('utf-8'))


@pytest.fixture
def snapshot(request):
    snapshot_dir = path.join(path.dirname(request.module.__file__), '__snapshots__')
    test_file_name = path.basename(request.module.__file__)
    test_name = request.node.name

    ops = TextOperations(snapshot_dir)

    test_name = '{}-{}'.format(
        test_file_name,
        test_name
    )
    snapshot_id = \
        hashlib.sha256().hexdigest()
    snapshot_name = test_name

    def test_func(result):
        write_id = request.config.option.write
        write_all = request.config.option.write_all
        if write_all or (write_id and snapshot_id.startswith(write_id)):
            ops.write_snapshot(snapshot_name, result)
        else:
            try:
                content = ops.get_snapshot(snapshot_name)
                print "Update the snapshot with --write %s" % snapshot_id[:5]
                assert content == result
            except ValueError:
                raise ValueError("Snapshot for this test does not exist. Generate it with --write %s" % snapshot_id[:5])

    return test_func