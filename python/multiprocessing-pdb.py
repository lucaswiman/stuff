import sys, os, pdb
from multiprocessing import *


class ForkedPdb(pdb.Pdb):
    def interaction(self, *args, **kwargs):
        _stdin = sys.stdin
        try:
            sys.stdin = open('/dev/stdin')
            pdb.Pdb.interaction(self, *args, **kwargs)
        finally:
            sys.stdin = _stdin


def run(stdin_fileno, stdout_fileno):
    sys.stdout = os.fdopen(stdin_fileno)
    sys.stdin = os.fdopen(stdout_fileno)
    breakpoint()
    # pdb.Pdb().set_trace()
    1 + 1


def run(*args):
    ForkedPdbFileNo().set_trace()

class ForkedPdbFileNo(pdb.Pdb):
    _parent_stdin_fileno = sys.stdin.fileno()
    _parent_stdin = None
    def __init__(self):
        pdb.Pdb.__init__(self, nosigint=True)

    def _cmdloop(self):
        prev_stdin = sys.stdin
        try:
            if not self._parent_stdin:
                self._parent_stdin = os.fdopen(self._parent_stdin_fileno)
            sys.stdin = self._parent_stdin
            self.cmdloop()
        finally:
            sys.stdin = prev_stdin


def test():
    from _pytest.debugging import pytestPDB
    capman = pytestPDB._pluginmanager.get_plugin('capturemanager')
    capman.suspend_global_capture(in_=True)
    stdin_fileno = sys.stdin.fileno()
    stdout_fileno = sys.stdout.fileno()
    capman.resume()
    
    
    # breakpoint()

    p = Process(target=run, args=(stdin_fileno, stdout_fileno))
    p.start()
    import time
    time.sleep(100)

if __name__ == "__main__":
    p = Process(target=run)
    p.start()






import datetime
import io
import logging
import multiprocessing
import pdb
import sys
import threading
import time
from multiprocessing.queues import Empty  # typing: ignore
from pathlib import Path
from test.test_queue_files_for_processing import yield_until
from unittest import mock

import pytest

from common.db.models import ActiveSplitXmlModel, Edi837Model, EdiFileModel, RemitMLModel
from src import settings
from src.client_config import CLIENT_TO_CONFIG
from src.parsers import xml_835, xml_837
from src.pipeline import process_files
from src.pipeline.process_files import QUEUES, extract, poison, start, unpoison
from src.pipeline.queue_files_for_processing import Counter, count_files_to_process, enqueue_once
from src.utils import get_s3_client

ALL_QUEUES = (
    QUEUES["EXTRACT_QUEUE"],
    QUEUES["PARSE_AND_SPLIT_QUEUE"],
    *QUEUES["CLIENT_TO_DB_WRITE_QUEUE"].values(),
)


TESTS_DIRECTORY = Path(__file__).parents[0]



try:
    class MultiprocessingPdb(pdb.Pdb):
        _parent_stdin_fileno = sys.stdin.fileno()
        _parent_stdin = None
        def __init__(self):
            pdb.Pdb.__init__(self, nosigint=True)

        def _cmdloop(self):
            prev_stdin = sys.stdin
            try:
                if not self._parent_stdin:
                    self._parent_stdin = os.fdopen(self._parent_stdin_fileno)
                sys.stdin = self._parent_stdin
                self.cmdloop()
            finally:
                sys.stdin = prev_stdin

        @classmethod
        def breakpointhook(cls, *, header=None):
            pdb = cls()
            if header is not None:
                pdb.message(header)
            pdb.set_trace(sys._getframe().f_back)
except io.UnsupportedOperation:
    MultiprocessingPdb = None


@pytest.fixture
def cleanup_concurrency(monkeypatch, methodist_db_session, mock_env_s3):
    """
    Monkey-patch the concurrency class to make it easier to clean up

    Also ensure cleanup of threads after test execution.
    """
    # Constantly check for new work rather then sleeping for extended periods when no work is found.
    monkeypatch.setattr(process_files, "SLEEP_TIME_WHEN_NOTHING_TO_DO", 0)
    if MultiprocessingPdb is None:
        logging.getLogger('test').warning(
            "Unable to use breakpoints. Use with `make test PYTEST_ARG=-s` to use breakpoints in subprocesses.")
    else:
        monkeypatch.setattr(sys, 'breakpointhook', MultiprocessingPdb.breakpointhook)

    processes = []

    class MyProcess(multiprocessing.Process):
        def __init__(self, *args, **kwargs):
            kwargs["daemon"] = True
            self.debug_args = args, kwargs
            super().__init__(*args, **kwargs)
            processes.append(self)

        def __repr__(self):
            return f"MyProcess(args={self.debug_args[0]}, kwargs={self.debug_args[1]}, orig_repr={super().__repr__()})"

    try:
        with mock.patch("src.pipeline.process_files.ConcurrencyClass", MyProcess):
            yield methodist_db_session
    finally:
        breakpoint()
        for process in processes:
            process.terminate()
        for process in processes:
            process.join()
        for process in processes:
            assert not process.is_alive()
        # Clear all queues so test runs do not process previous tests entries.
        for queue in ALL_QUEUES:
            while True:
                try:
                    queue.get_nowait()
                except Empty:
                    break


@pytest.mark.config_env("prod")
def test_run_ends(cleanup_concurrency):
    # Test that concurrency cleanup actually occurs
    start()
    time.sleep(1)


@pytest.mark.parametrize(
    "filename,model_cls,expected_count",
    [
        ("Hipaa-5010-837I-InstitutionalClaim.txt", Edi837Model, 4),
        ("Hipaa-5010-837P-ClaimPayment.txt", Edi837Model, 2),
        ("scribd-837I.txt", Edi837Model, 1),
        ("X12.NET-837P-example.x12", Edi837Model, 1),
        ("fake-835.edi", RemitMLModel, 3),
        ("Hipaa-5010-835-Payment.txt", RemitMLModel, 1),
    ],
)
@pytest.mark.config_env("prod")
def test_end_to_end_initial_file(cleanup_concurrency, filename, model_cls, expected_count):
    db_session = cleanup_concurrency
    assert db_session.query(EdiFileModel).count() == 0
    s3 = get_s3_client()
    client_config = CLIENT_TO_CONFIG["methodist"]

    key = f"{client_config.s3_prefixes[0]}/valid.x12"
    with open(TESTS_DIRECTORY / f"fake_edi_files/{filename}", "rb") as f:
        s3.put_object(
            Bucket=settings.S3_BUCKET,
            Key=key,
            Body=f.read(),
        )
    file_count = Counter()
    enqueue_once(
        db_name="methodist",
        client_config=client_config,
        file_count=file_count,
        should_stop=lambda: False,
    )
    assert file_count.count == 1
    assert db_session.query(EdiFileModel).count() == 1
    db_session.execute("UPDATE edi_file SET updated_at = NOW() - INTERVAL '1 day'")
    db_session.commit()
    start()

    def check_count():
        return db_session.query(model_cls).count() == expected_count

    for _ in yield_until(seconds=10, condition=check_count):
        pass
    assert db_session.query(model_cls).count() == expected_count
    edi_file = db_session.query(EdiFileModel).one()
    assert edi_file.file_type == ("835" if model_cls == RemitMLModel else "837")
    # Files have been processed, so shouldn't find any to process:
    assert count_files_to_process(db_session) == 0

    # Now test backfilling. Note that the pipeline should still be running, querying for backfills.
    id_to_transmitted_date = dict(db_session.query(model_cls.id, model_cls.transmitted_date).all())
    # TODO: add updated_at to remit_ml
    # db_session.execute("UPDATE remit_ml SET updated_at = NOW() - INTERVAL '1 day'")
    wrong_date = datetime.date(1906, 4, 28)
    db_session.execute(
        model_cls.__table__.update().values(transmitted_date=wrong_date, schema_version=-1)
    )
    db_session.execute(
        "UPDATE edi_file SET updated_at = NOW() - INTERVAL '1 day', schema_version=-1"
    )
    # Changes are not visible to the other threads yet, so should find one file to process.
    assert count_files_to_process(db_session) == 1
    db_session.commit()

    schema_version = (
        xml_837.EDI_837_SCHEMA_VERSION
        if model_cls == Edi837Model
        else xml_835.EDI_835_SCHEMA_VERSION
    )

    def check_assertions(do_assertion=False):
        new_id_to_transmitted_date = dict(
            db_session.query(model_cls.id, model_cls.transmitted_date).all()
        )
        edi_file_schema_version = db_session.query(EdiFileModel.schema_version).one()[0]
        if do_assertion:
            assert new_id_to_transmitted_date == id_to_transmitted_date
            assert edi_file_schema_version == schema_version

        return (
            new_id_to_transmitted_date == id_to_transmitted_date
            and edi_file_schema_version == schema_version
        )

    for _ in yield_until(seconds=10, condition=check_assertions):
        pass
    check_assertions(do_assertion=True)
    # Files have been processed, so shouldn't find any to process:
    assert count_files_to_process(db_session) == 0
    assert set(db_session.query(model_cls.schema_version).all()) == {(schema_version,)}


@pytest.mark.config_env("prod")
def test_end_to_end_invalid_file(cleanup_concurrency):
    db_session = cleanup_concurrency
    assert db_session.query(EdiFileModel).count() == 0
    s3 = get_s3_client()
    client_config = CLIENT_TO_CONFIG["methodist"]

    key = f"{client_config.s3_prefixes[0]}/invalid.x12"
    s3.put_object(
        Bucket=settings.S3_BUCKET,
        Key=key,
        Body=b"This is not a valid x12 file. Nothing to be done but mark it as a failure.",
    )
    file_count = Counter()
    enqueue_once(
        db_name="methodist",
        client_config=client_config,
        file_count=file_count,
        should_stop=lambda: False,
    )
    assert file_count.count == 1
    assert db_session.query(EdiFileModel).filter_by(is_failed=False).count() == 1
    db_session.execute("UPDATE edi_file SET updated_at = NOW() - INTERVAL '1 day'")
    db_session.commit()
    start()

    def check_failure():
        return db_session.query(EdiFileModel).filter_by(is_failed=True).count() == 1

    for _ in yield_until(seconds=10, condition=check_failure):
        pass
    assert db_session.query(EdiFileModel).filter_by(is_failed=True).count() == 1


@pytest.mark.config_env("prod")
def test_failed_file_is_marked_then_retried(monkeypatch, cleanup_concurrency):
    def buggy_extract(split_xml_location, *args, **kwargs):
        if split_xml_location.endswith("_0.xml.gz"):
            raise Exception()
        else:
            return extract(split_xml_location, *args, **kwargs)

    monkeypatch.setattr(process_files, "extract", buggy_extract)
    filename = "Hipaa-5010-837P-ClaimPayment.txt"
    db_session = cleanup_concurrency
    assert db_session.query(EdiFileModel).count() == 0
    s3 = get_s3_client()
    client_config = CLIENT_TO_CONFIG["methodist"]

    key = f"{client_config.s3_prefixes[0]}/valid.x12"
    with open(TESTS_DIRECTORY / f"fake_edi_files/{filename}", "rb") as f:
        s3.put_object(
            Bucket=settings.S3_BUCKET,
            Key=key,
            Body=f.read(),
        )
    file_count = Counter()
    enqueue_once(
        db_name="methodist",
        client_config=client_config,
        file_count=file_count,
        should_stop=lambda: False,
    )
    assert file_count.count == 1
    assert db_session.query(EdiFileModel).count() == 1
    db_session.execute("UPDATE edi_file SET updated_at = NOW() - INTERVAL '1 day'")
    db_session.commit()
    start()

    def check_count():
        return (
            db_session.query(Edi837Model).count() == 1
            and db_session.query(ActiveSplitXmlModel).filter_by(number_of_attempts=1).count() == 1
        )

    for _ in yield_until(seconds=10, condition=check_count):
        pass
    assert db_session.query(Edi837Model).count() == 1
    edi_file = db_session.query(EdiFileModel).one()
    assert edi_file.file_type == "837"
    for active_split_file in db_session.query(ActiveSplitXmlModel).all():
        assert active_split_file.number_of_attempts == 1
        assert active_split_file.location.endswith("_0.xml.gz")
    edi_837 = db_session.query(Edi837Model).one()
    assert edi_837.xml_file.endswith("_1.xml.gz")

    # Now retry with the buggy version. It should increment the number of attempts.
    db_session.execute(
        """
        UPDATE active_split_xml SET updated_at = NOW() - INTERVAL '1 day'
    """
    )
    db_session.commit()

    def check_incremented():
        return db_session.query(ActiveSplitXmlModel).filter_by(number_of_attempts=2).count() == 1

    for _ in yield_until(seconds=10, condition=check_incremented):
        pass
    assert db_session.query(ActiveSplitXmlModel).filter_by(number_of_attempts=2).count() == 1

    # Now retry with the original version. It should succeed in processing an insert an edi_837.
    monkeypatch.setattr(process_files, "extract", extract)
    db_session.execute(
        """
        UPDATE active_split_xml SET updated_at = NOW() - INTERVAL '1 day'
    """
    )
    db_session.commit()

    def check_successfully_processed():
        return (
            db_session.query(Edi837Model).count() == 2
            and db_session.query(ActiveSplitXmlModel).count() == 0
        )

    for _ in yield_until(seconds=10, condition=check_successfully_processed):
        pass
    assert db_session.query(Edi837Model).count() == 2
    assert db_session.query(ActiveSplitXmlModel).count() == 0
