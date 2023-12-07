EXAMPLE_DATA = """$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k"""

class File:
    def __init__(self, size):
        self.size = int(size)

    def __repr__(self):
        return f"File <{self.size}>"

class Directory:
    def __init__(self, parent, name):
        self._name = name
        self._parent = parent
        self._items = []

    def __repr__(self):
        return f"Directory <{self._name}>"

    @property
    def parent(self):
        return self._parent

    @property
    def size(self):
        return sum(item.size for item in self._items)

    def add_directory(self, directory):
        self._items.append(directory)

    def add_file(self, size):
        self._items.append(File(size))

    def show_items(self):
        print([item for item in self._items])


def create_file_tree(data):
    current_dir = None
    top_level_dir = None
    all_dirs = []
    for line in data.splitlines():
        commands = line.split(" ")

        if commands[0] == "$" and commands[1] == "cd":
            target_dir = commands[2]
            if target_dir == "..":
                current_dir = current_dir.parent
            else:
                next_dir = Directory(parent=current_dir, name=target_dir)
                if current_dir is not None:
                    current_dir.add_directory(next_dir)
                else:
                    top_level_dir = next_dir
                current_dir = next_dir
                all_dirs.append(next_dir)
            continue

        try:
            size = int(commands[0])
        except ValueError:
            pass
        else:
            current_dir.add_file(size)

    return all_dirs, top_level_dir
        

def part1(data):
    # data = EXAMPLE_DATA

    file_tree, _ = create_file_tree(data)

    return sum(directory.size for directory in file_tree if directory.size < 100_000)


def part2(data):
    # data = EXAMPLE_DATA

    file_tree, top_level_dir = create_file_tree(data)

    available_space = 70_000_000 - top_level_dir.size
    space_required = 30_000_000 - available_space
    return min(directory.size for directory in file_tree if directory.size >= space_required)
