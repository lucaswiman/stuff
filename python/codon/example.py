import re, random, time, sys

random.seed(0)
s = ''.join(random.choice('abcdefghjiklmnopqrstuvwxyz') for _ in range(10_000_000))

t0 = time.time()
counts = []
for _ in range(int(sys.argv[1])):
    counts.append(re.findall(r"(abc)", s))
t1 = time.time()
print(f"Ran in {t1-t0}s, {len(counts)}")