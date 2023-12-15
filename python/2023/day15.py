from collections import defaultdict

EXAMPLE_DATA = """rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7"""


def get_holiday_hash(data):
    total = 0

    for char in data:
        total += ord(char)
        total *= 17
        total %= 256

    return total


def find_label(box_contents, label):
    for i, (current_label, _) in enumerate(box_contents):
        if current_label == label:
            return i
    return None


def part1(data):
    # data = EXAMPLE_DATA

    return sum(get_holiday_hash(chunk) for chunk in data.split(","))


def part2(data):
    # data = EXAMPLE_DATA

    BOXES = defaultdict(list)

    for chunk in data.split(","):
        label, op = chunk[:-1], chunk[-1]
        try:
            int(op)
            label, op, value = chunk[:-2], chunk[-2], int(chunk[-1])
        except ValueError:
            pass

        box_no = get_holiday_hash(label)
        box_contents = BOXES[box_no]
        removal_index = find_label(box_contents, label)

        if op == "=":
            if removal_index is None:
                BOXES[box_no].append((label, value))
            else:
                BOXES[box_no][removal_index] = label, value
        else:
            if removal_index is not None:
                box_contents.pop(removal_index)


    focus_power = 0
    for box_no in range(256):
        box_contents = BOXES[box_no]

        for n in range(len(box_contents)):
            focus_power += (box_no + 1) * (n + 1) * box_contents[n][1]

    return focus_power
