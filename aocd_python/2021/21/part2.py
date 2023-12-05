from collections import Counter

POSSIBLE_UNIVERSES = [
    (3, 1),
    (4, 3),
    (5, 6),
    (6, 7),
    (7, 6),
    (8, 3),
    (9, 1),
]
WINNING_SCORE = 21

with open('input.txt') as file:
    p1_pos = int(file.readline().strip()[-1])
    p2_pos = int(file.readline().strip()[-1])

p1_score = 0
p2_score = 0

start_universe = (p1_pos, p1_score, p2_pos, p2_score)
universes = Counter({start_universe: 1})
current_player = True  # True: 1, False: 2

while True:
    is_it_over = [max(universe[1], universe[3]) >= WINNING_SCORE for universe in universes.keys()]
    if all(is_it_over):
        break

    current_counter = Counter()
    for u_state, u_count in universes.items():
        p1_pos, p1_score, p2_pos, p2_score = u_state
        if p1_score >= WINNING_SCORE or p2_score >= WINNING_SCORE:
            # Re-add these universes, they need no changes
            current_counter.update({u_state: u_count})
            continue

        for roll, n_universes in POSSIBLE_UNIVERSES:
            if current_player:
                new_p1_pos = (p1_pos + roll) % 10
                new_p1_score = p1_score + (10 if new_p1_pos == 0 else new_p1_pos)
                new_state = (new_p1_pos, new_p1_score, p2_pos, p2_score)
            else:
                new_p2_pos = (p2_pos + roll) % 10
                new_p2_score = p2_score + (10 if new_p2_pos == 0 else new_p2_pos)
                new_state = (p1_pos, p1_score, new_p2_pos, new_p2_score)
            current_counter.update({new_state: u_count*n_universes})
    universes = current_counter
    current_player = not current_player

n_p1_wins = 0
n_p2_wins = 0
for u_state, u_count in universes.items():
    _, p1_score, _, p2_score = u_state
    if p1_score > p2_score:
        n_p1_wins += u_count
    else:
        n_p2_wins += u_count
print(f'{n_p1_wins=}')
print(f'{n_p2_wins=}')