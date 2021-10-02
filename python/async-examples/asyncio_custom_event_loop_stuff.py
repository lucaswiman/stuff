# https://stackoverflow.com/a/54234839/303931
import asyncio

class MeasuredEventLoop(asyncio.SelectorEventLoop):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._total_time = 0
        self._select_time = 0

        self._before_select = None

    # TOTAL TIME:
    def run_forever(self):
        started = self.time()
        try:
            super().run_forever()
        finally:
            finished = self.time()
            self._total_time = finished - started

    # SELECT TIME:
    def _run_once(self):
        self._before_select = self.time()
        super()._run_once()

    def _process_events(self, *args, **kwargs):
        after_select = self.time()
        self._select_time += after_select - self._before_select
        super()._process_events(*args, **kwargs)

    # REPORT:
    def close(self, *args, **kwargs):
        super().close(*args, **kwargs)

        select = self._select_time
        cpu = self._total_time - self._select_time
        total = self._total_time

        print(f'Waited for select: {select:.{3}f}')
        print(f'Did other stuff: {cpu:.{3}f}')
        print(f'Total time: {total:.{3}f}')


import time


async def main():
    print("foo")
    await asyncio.sleep(1)  # simulate I/O, will be handled by selectors
    time.sleep(0.01)        # CPU job, executed here, outside event loop
    print("bar")
    await asyncio.sleep(1)
    time.sleep(0.01)
    print("baz")


# loop = MeasuredEventLoop()
# asyncio.set_event_loop(loop)

# https://docs.python.org/3/library/asyncio-policy.html#custom-policies
class MyEventLoopPolicy(asyncio.DefaultEventLoopPolicy):
    _loop_factory = MeasuredEventLoop

asyncio.set_event_loop_policy(MyEventLoopPolicy())

try:
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
finally:
    loop.close()
# asyncio.run(main())