#!/usr/bin/env python -i


from contextlib import contextmanager
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

@contextmanager
def retrying_requests_session(total=10, backoff_factor=0.2, status_forcelist=(500, 503, 504)):
    """
    Retries on connection errors and (possibly) temporary status codes.

    See https://urllib3.readthedocs.io/en/latest/reference/urllib3.util.html
    for the full list of options to Retry.
    """
    with requests.Session() as session:
        retry = Retry(total=total, backoff_factor=backoff_factor, status_forcelist=status_forcelist)
        adapter = HTTPAdapter(max_retries=retry)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        yield session


import logging
log = logging.getLogger('urllib3')
if not any(isinstance(h, logging.StreamHandler) for h in log.handlers):
    print("adding urllib3 debug logging")
    log.setLevel(logging.DEBUG)
    stream = logging.StreamHandler()
    stream.setLevel(logging.DEBUG)
    log.addHandler(stream)


with retrying_requests_session(total=4) as session:
    for i in range(100):
        print(i)
        resp = session.get("https://staging-api.a10ai.com/perception/model/perception-staging-nearest-neighbor:hello_world-james-onboarding-100")
        print(resp.status_code)
