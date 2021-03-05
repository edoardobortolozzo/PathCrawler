import argparse

# Parse cmd line args
parser = argparse.ArgumentParser(description="Find duplicate files.")
parser.add_argument( #TODO mandatory
        "path",
        default="",
        nargs="?",
        type=str,
        help="path"
)
parser.add_argument(
        "-v", "--verbose",
        default=0,
        action="count",
        help="increases verbosity level by 1 (default is 0)"
)
parser.add_argument(
        "-r", "--recursive",
        default=False,
        action="store_true",
        help="use recorsion on the directories instead"
)
parser.add_argument(
        "-x", "--exclude",
        action="extend",
        nargs="+",
        type=str,
        default=[],
        help="exclude file extension"
)
parser.add_argument(
        "-t", "--threads",
        default=1,
        type=int,
        action="store",
        help="set number of processes - if more than cpu core, is set to cpu_count()"
)
parser.add_argument(
        "-d", "--debug",
        default=False,
        action="store_true",
        help="set debug to true"
)