def check_line_values(line):
    for value in line:
        if value != '*':
            return False
    return True


def check_bingo_win(card):
    return any([
        # Horizontal Lines
        check_line_values([card[0], card[1], card[2], card[3], card[4]]),
        check_line_values([card[5], card[6], card[7], card[8], card[9]]),
        check_line_values([card[10], card[11], card[12], card[13], card[14]]),
        check_line_values([card[15], card[16], card[17], card[18], card[19]]),
        check_line_values([card[20], card[21], card[22], card[23], card[24]]),
        # Vertical lines
        check_line_values([card[0], card[5], card[10], card[15], card[20]]),
        check_line_values([card[1], card[6], card[11], card[16], card[21]]),
        check_line_values([card[2], card[7], card[12], card[17], card[22]]),
        check_line_values([card[3], card[8], card[13], card[18], card[23]]),
        check_line_values([card[4], card[9], card[14], card[19], card[24]]),
    ])


def get_card_value(card, last_num):
    total = 0
    for item in card:
        try:
            total += item
        except TypeError:
            continue
    return total * last_num


def update_card(card, num):
    try:
        index = card.index(num)
    except ValueError:
        return None
    else:
        card[index] = '*'

with open('input.txt') as file:
    num_list = [int(num) for num in file.readline().split(',')]
    cards = []

    # Pretty hacky
    while True:
        more_cards = file.readline() != ''
        if not more_cards:
            break
        card = []
        for _ in range(5):
            row = [int(num) for num in file.readline().split()]
            card.extend(row)
        cards.append(card)

remove_list = []
final_value = None

for num in num_list:
    for idx, card in enumerate(cards):
        update_card(card, num)
        winner = check_bingo_win(card)
        if winner:
            remove_list.append(idx)
    last_removed = None
    while len(remove_list) > 1:
        index = remove_list.pop()
        last_removed = cards.pop(index)
    if len(cards) == 0:
        final_value = get_card_value(last_removed, num)
        break

print(final_value)