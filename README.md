# pathcrawler

Given a path, the crawler explores every subdirectory and calculate the files'
hashes.
The hashes with the relative paths are saved in a dictionary in the form of
`[hash, list of paths with same data]`.
When ran as `__main__`, the script returns a list of paths where the duplicate
data is stored.

addFileHashes(path: Path) -> Union[dict,bool]
