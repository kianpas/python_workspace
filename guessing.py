import random

highest = 1000
answer = random.randint(1, highest)
print(answer)

print(f'1 ~ {highest} : ')

guess = 0
while guess != answer:
    guess = int(input())
    if guess == answer:
        print("you got it")
        break
    else:
        if guess < answer:
            print("higher")
        else:
            print("lower")
        continue