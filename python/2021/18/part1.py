
from collections import deque
from typing import Tuple
from uuid import uuid4

class Node:
    def __init__(self):
        self.id = uuid4()
        self.left = None
        self.right = None
        self.parent = None

    def set_child(self, other, target: str):
        setattr(self, target, other)
        if type(other) == Node:
            other.parent = self

    def __eq__(self, other):
        try:
            return self.id == other.id
        except AttributeError:
            return False

    def __gt__(self, other):
        return False

    def __str__(self):
        return f'[{str(self.left)},{str(self.right)}]'

    def __repr__(self):
        return self.__str__()


def explode_node(sf_node: Node) -> None:
    current_node = sf_node
    while True:
        if current_node.parent is None:
            break
        prev_node = current_node
        current_node = prev_node.parent

        if current_node.left == prev_node:
            continue

        if type(current_node.left) != Node:
            current_node.left += sf_node.left
            break
        else:
            current_node = current_node.left
            while type(current_node.right) == Node:
                current_node = current_node.right

            current_node.right += sf_node.left
            break

    current_node = sf_node
    while True:
        if current_node.parent is None:
            break
        prev_node = current_node
        current_node = prev_node.parent

        if current_node.right == prev_node:
            continue

        if type(current_node.right) != Node:
            current_node.right += sf_node.right
            break
        else:
            current_node = current_node.right
            while type(current_node.left) == Node:
                current_node = current_node.left

            current_node.left += sf_node.right
            break
    parent = sf_node.parent
    target = 'left' if parent.left == sf_node else 'right'
    parent.set_child(0, target)


def check_for_explode(sf_node: Node, depth=0):
    found = None
    is_node = type(sf_node) == Node
    if depth == 4 and is_node:
        return sf_node
    if is_node:
        found = check_for_explode(sf_node.left, depth=depth+1)
        if found is None:
            found = check_for_explode(sf_node.right, depth=depth+1)
    return found


def check_for_split(sf_node: Node) -> Tuple[Node, str]:
    found = None

    if type(sf_node.left) == Node:
        found = check_for_split(sf_node.left)
    elif sf_node.left > 9:
        return sf_node, 'left'
    
    if found is None:
        if type(sf_node.right) == Node:
            found = check_for_split(sf_node.right)
        elif sf_node.right > 9:
            return sf_node, 'right'
    return found


def split_child_value(sf_node: Node, target: str):
    old_val = getattr(sf_node, target)
    new_val = old_val // 2
    rem = old_val % 2

    new_node = Node()
    new_node.set_child(new_val, 'left')
    new_node.set_child(new_val + rem, 'right')

    sf_node.set_child(new_node, target)


def sf_add(left: Node, right: Node) -> Node:
    node = Node()
    node.set_child(left, 'left')
    node.set_child(right, 'right')

    while True:
        exploder = check_for_explode(node)
        if exploder is not None:
            explode_node(exploder)
            continue
        splitter = check_for_split(node)
        if splitter is not None:
            split_child_value(*splitter)
            continue

        return node


def create_sf_node(queue: deque):
    next_op = queue.popleft()
    node = Node()
    target = 'left'

    while next_op != ']':
        if next_op == '[':
            # New node
            child = create_sf_node(queue)
            node.set_child(child, target)
        elif next_op == ',':
            target = 'right'
        else:
            node.set_child(int(next_op), target)
        next_op = queue.popleft()
    return node


def get_sf_magnitude(sf_node: Node) -> int:
    if type(sf_node.left) == Node:
        left_val = get_sf_magnitude(sf_node.left)
    else:
        left_val = sf_node.left

    if type(sf_node.right) == Node:
        right_val = get_sf_magnitude(sf_node.right)
    else:
        right_val = sf_node.right

    return 3 * left_val + 2 * right_val


prev_sf_num = None
with open('input.txt') as file:
    for line in file.readlines():
        queue = deque(line.strip())
        if queue.popleft() == '[':
            sf_num = create_sf_node(queue)
        if prev_sf_num is None:
            prev_sf_num = sf_num
        else:
            prev_sf_num = sf_add(prev_sf_num, sf_num)

print(prev_sf_num)
magnitude = get_sf_magnitude(prev_sf_num)
print(magnitude)