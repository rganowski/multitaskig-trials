import argparse
from multiprocessing import cpu_count, current_process, Process, Queue

parser = argparse.ArgumentParser(
    description="""Calculates sum of array elements. 
    Can do that using more then one of your cpu cores."""
)
parser.add_argument(
    "--cores", "-c",
    dest="NUM_CORES",
    type=int, default=(available_cores := cpu_count()),
    help=f"number of cores you want to utilize (default: {available_cores})"
)

args = parser.parse_args()

NUM_CORES = args.NUM_CORES


DATA = [10, 9, 4, 15, 2, 9, 13, 10, 8, 8, 22, 6, 3, 8, 4, 12, 5, 9, 12]
NUM_ELEMS = len(DATA)

fair_core_worload = NUM_ELEMS // NUM_CORES
cores_with_1_more = NUM_ELEMS % NUM_CORES

print("index: | " + "| ".join([f"{x:>3} " for x in range(NUM_ELEMS)]) + "|")
print("value: | " + "| ".join([f"{x:>3} " for x in DATA]) + "|")
print()

EXTENTS_OF_SUBRANGES = []
bound = 0
for i, extent_size in enumerate(
    [fair_core_worload + 1 for _ in range(cores_with_1_more)]
    + [fair_core_worload for _ in range(NUM_CORES - cores_with_1_more)]
):
    EXTENTS_OF_SUBRANGES.append((bound, bound := bound + extent_size))


def calc_subtotal(lower_bound: int, upper_bound: int, subtotals: Queue) -> None:
    p = current_process().name.split("-")[-1]
    subtotal = 0
    for i in range(lower_bound, upper_bound):
        new_subtotal = subtotal + DATA[i]
        print(f"| {p:>3} | {i:>12} | {subtotal:>12} | {new_subtotal:>12} |")
        subtotal = new_subtotal
    subtotals.put(subtotal)


print("|   p |  counter (i) |  in subtotal | out subtotal |")
print("| --- | ------------ | ------------ | ------------ |")

PROCESSES = []
subtotals = Queue()

for extent in EXTENTS_OF_SUBRANGES:
    p = Process(target=calc_subtotal, args=(extent[0], extent[1], subtotals))
    p.start()
    PROCESSES.append(p)

for p in PROCESSES:
    p.join()

total = 0
for i in range(subtotals.qsize()):
    total += subtotals.get()

print("| --- | ------------ | ------------ | ------------ |")
print(f"                             TOTAL: | {total:>12} |")
