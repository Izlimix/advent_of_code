#!/usr/bin/env python3

# https://adventofcode.com/2022/day/7

from itertools import chain

def part1(root):
    sizes = dict()
    sizes[root] = root.get_size()
    for descendant in root._descendants():
        if isinstance(descendant, Directory):
            sizes[descendant] = descendant.get_size()
    
    total = sum(size for size in sizes.values() if size <= 100000)
    print("Part 1 result:")
    print(f"Sum of dir sizes of max 100000: {total}")
    
def part2(root):
    sizes = dict()
    sizes[root] = root.get_size()
    print(f"Current root directory size: {sizes[root]}")
    free_space = 70000000 - sizes[root]
    print(f"Free space: {free_space}")
    target_space = 30000000 - free_space
    print(f"We need to free up {target_space}")

    for descendant in root._descendants():
        if isinstance(descendant, Directory):
            sizes[descendant] = descendant.get_size()
    
    (out_d, out_size) = min(((d, size) for (d, size) in sizes.items() if size >= target_space), key = lambda e: e[1])
    print("Part 2 result:")
    print(f"Deleting the smallest appropriate directory {out_d.name} would save {out_size} space")
    
class Directory:
    def __init__(self, name, parent):
        self.name = name
        self.parent = parent
        self.child_directories = []
        self.child_files = []
        self.size = None
    
    def get_size(self):
        if self.size is None:
            self.size = sum(directory.get_size() for directory in self.child_directories) + sum(file.size for file in self.child_files)
        return self.size

    def ls(self):
        print(f"Directory {self.name}:")
        for directory in self.child_directories:
            print(f"dir {directory.name}")
        for file in self.child_files:
            print(f"{file.size} {file.name}")
    
    def _child_dir_names(self):
        return (d.name for d in self.child_directories)
    
    def _child_file_names(self):
        return (f.name for f in self.child_files)
    
    def _recursive_ls(self):
        self.ls()
        for d in self.child_directories:
            d._recursive_ls()
    
    def _descendants(self):
        return chain(self.child_files, self.child_directories, *(d._descendants() for d in self.child_directories))

class File:
    def __init__(self, name, size):
        self.name = name
        self.size = size

def parse_fs(lines):
    root = Directory("/", None)
    working_directory = root
    for l in lines:
        match l.split():
            case ["$", "cd", "/"]:
                working_directory = root
            case ["$", "cd", ".."]:
                working_directory = working_directory.parent
                if working_directory is None:
                    print("Warning: Just travelled to the parent of root?")
            case ["$", "cd", target]:
                for d in working_directory.child_directories:
                    if target == d.name:
                        working_directory = d
                        break
                else:
                    # Didn't find the target directory
                    print(f"Warning: trying to cd to {target} which we haven't seen yet!")
                    print("Current state:")
                    working_directory.ls()
                    print(f"Adding {target} and moving to it...")
                    d = Directory(target, working_directory)
                    working_directory.child_directories.append(d)
                    working_directory = d
            case ["$", "ls"]:
                # The next lines will be files and directories to add...
                pass
            case ["dir", d_name]:
                # Saw a directory, add it
                if d_name not in working_directory._child_dir_names():
                    d = Directory(d_name, working_directory)
                    working_directory.child_directories.append(d)
                else:
                    # We've seen this here before?
                    print(f"Warning: Tried to add {d_name} to {working_directory.name}, but it already exists.")
                    print("Current state:")
                    working_directory.ls()
            case [n, f_name]:
                # Saw a file, add it
                if f_name not in working_directory._child_file_names():
                    f = File(f_name, int(n))
                    working_directory.child_files.append(f)
                else:
                    # We've seen this here before?
                    print(f"Warning: Tried to add {f_name} to {working_directory.name}, but it already exists.")
                    print("Current state:")
                    working_directory.ls()
            case cmd:
                print(f"Couldn't parse unknown line:")
                print(cmd)

    return root

# Command-line execution:
if __name__ == "__main__":
    import sys
    filename = sys.argv[1]
    with open(filename, encoding="utf-8") as f:
        data = f.read()
    
    lines = data.strip().split("\n")
    root = parse_fs(lines)
    print("---- Done parsing ----")

    part1(root)
    print("--------")
    part2(root)
    