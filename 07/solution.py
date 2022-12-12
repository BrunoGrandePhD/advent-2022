#!/usr/bin/env python3

import sys
from typing import Mapping


class Node:
    name: str
    is_file: bool
    size: int
    children: Mapping

    def __init__(self, parent, name, is_file, size=None) -> None:
        self.parent = parent
        self.name = name
        self.is_file = is_file
        self.size = size or 0
        self.children = {}

    def add_child(self, child_node):
        self.children[child_node.name] = child_node

    def has_child(self, child_name):
        return child_name in self.children

    def get_child(self, child_name):
        return self.children[child_name]


class FileTree:
    root: Node
    space: int

    def __init__(self) -> None:
        self.root = Node(None, "/", False)
        self.space = 70000000

    def add_node(cls, parent, name, is_file, size=None):
        if parent.has_child(name):
            return parent.get_child(name)
        node = Node(parent, name, is_file, size)
        if is_file:
            current_node = parent
            while current_node is not None:
                current_node.size += size
                current_node = current_node.parent
        else: # add dir
            parent.add_child(node)
        return node

    def calc_size(self, max_size=100000):
        return self._calc_size(self.root, max_size)

    @classmethod
    def _calc_size(cls, node, max_size):
        if node.is_file:
            return 0
        total_size = 0
        if node.size <= max_size:
            total_size = node.size
        for child in node.children.values():
            size = cls._calc_size(child, max_size)
            total_size += size
        return total_size

    @classmethod
    def _print_tree(cls, node, indent=0):
        current_node = node
        if indent == 0:
            print('Root: ', node.name)
        for child_name in current_node.children.keys():
            child_node = node.get_child(child_name)
            indent_str = ' ' * indent
            print(indent_str, '|--', child_node.name, ' ', child_node.size)
            cls._print_tree(child_node, indent + 2)

    def calc_remaining_space(self):
        return self.space - self.root.size

    def find_smallest_dir_for_update(self, update_size=30000000):
        needed_space = update_size - self.calc_remaining_space()
        return self._find_smallest_dir_for_update(self.root, self.root.size, needed_space)

    def _find_smallest_dir_for_update(self, node, smallest_size, needed_space):
        if node.is_file:
            return smallest_size
        if node.size < needed_space:
            return smallest_size
        smallest_size = min(smallest_size, node.size)
        for child in node.children.values():
            new_size = self._find_smallest_dir_for_update(child, smallest_size, needed_space)
            smallest_size = min(smallest_size, new_size)
        return smallest_size


class Parser:
    def __init__(self, path) -> None:
        self.path = path
        self.tree = FileTree()
        self.cwd  = None
        self.parse_input()

    def parse_input(self):
        with open(self.path, "r") as infile:
            for line in infile:
                line = line.strip()
                if line.startswith("$ cd"):
                    self.parse_cd(line)
                elif line.startswith("$ ls"):
                    pass
                else:
                    self.parse_ls_output(line)


    def parse_cd(self, line):
        _, _, folder = line.split(" ")
        if folder == "/":
            self.cwd = self.tree.root
        elif folder == "..":
            self.cwd = self.cwd.parent
        else:
            folder_node = self.tree.add_node(self.cwd, folder, False)
            self.cwd = folder_node

    def parse_ls_output(self, line):
        if not line.startswith("dir"):
            size, name = line.split(" ")
            size = int(size)
            self.tree.add_node(self.cwd, name, True, size)
        else:
            _, folder = line.split(" ")
            self.tree.add_node(self.cwd, folder, False, 0)

if __name__ == "__main__":
    parser = Parser(sys.argv[1])
    # parser.tree._print_tree(parser.tree.root)
    size = parser.tree.calc_size()
    print(size)
    smallest_dir_size = parser.tree.find_smallest_dir_for_update()
    print(smallest_dir_size)
