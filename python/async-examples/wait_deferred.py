import asyncio
import time


async def foo(n):
    if n == 10:
        time.sleep(n)
        print(f"Ran {n} sync.")
    else:
        await asyncio.sleep(n)
        print(f"Ran {n}.")
    return n


async def main():
    pending = {asyncio.create_task(foo(i)) for i in range(20)}
    completions = []
    t0 = time.time()
    while True:
        print("running a loop")
        tick = asyncio.Task(asyncio.sleep(0.1))
        done, pending = await asyncio.wait({tick} | pending, return_when=asyncio.FIRST_COMPLETED)
        for t in done:
            print(t.result())
        if not pending:
            break
        print(completions)
        if time.time() - t0 > 11:
            for t in pending:
                print(f"Cancelling {t}")
                t.cancel()
                try:
                    await t  # Do not leave tasks hanging.
                except asyncio.exceptions.CancelledError:
                    print("caught")
            break


asyncio.run(main())
