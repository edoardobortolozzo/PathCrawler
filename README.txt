Given a path, the crawler explores every subdirectory and hashes the files.
The Hashes and realtives path are saved in a dictionary in the form of
(hash, list of path with same data).
If runned as __main__, the script returns a list of paths where are stored
duplicate data.

addFileHashes(path: Path) -> dict