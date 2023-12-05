from itertools import count

def score_generator():
    dice = count()

    while True:
        values = [(next(dice) % 100) + 1 for _ in range(3)]
        yield sum(values)


with open('input.txt') as file:
    p1_pos = int(file.readline().strip()[-1])
    p2_pos = int(file.readline().strip()[-1])

p1_score = 0
p2_score = 0
roll_total = 0
dice = score_generator()
result_score = 0

while True:
    p1_move = next(dice)
    roll_total += 3
    p1_pos = ((p1_pos + p1_move) % 10)

    p1_score += 10 if p1_pos == 0 else p1_pos

    if p1_score >= 1000:
        p1_winner = True
        break

    p2_move = next(dice)
    roll_total += 3
    p2_pos = ((p2_pos + p2_move) % 10)

    p2_score += 10 if p2_pos == 0 else p2_pos

    if p2_score >= 1000:
        p1_winner = False
        break

result_score = p2_score if p1_winner else p1_score
result = result_score * roll_total
print(result)