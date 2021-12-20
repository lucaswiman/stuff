import asyncio
import time

def block(i):
    time.sleep(i)


async def foo():
    t0 = time.perf_counter()
    print("started")
    tasks = [asyncio.to_thread(block, 1) for _ in range(100)]
    async_tasks = [asyncio.sleep(1) for _ in range(100)]
    print(f"Done creating tasks in {time.perf_counter() - t0}s; now running.")
    await asyncio.gather(*tasks, *async_tasks)
    print(f"Done in {time.perf_counter() - t0}s.")

asyncio.run(foo())