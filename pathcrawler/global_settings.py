from multiprocessing import cpu_count

# Verbosity Levels:
#   0 -> non-verbose
#   1 -> verbose
#   2 -> very verbose
VERBOSITY_LEVEL = 0

NUM_THREADS = 1
def setThreads(n: int):
    global NUM_THREADS
    NUM_THREADS = min(n, cpu_count())

DEBUG = False