low = 1
high = 1000

print(f"please think of a num between {low} and {high}")
input("press enter to start")

guesses = 1
# // 나누고 정수만 사용
while True:
    print(f"\tGuessing in the range of {low} to {high}")
    guess = low + (high - low) // 2
    high_low = input(f"My guess is {guess} if high h or l, correct c ").casefold()

    if high_low == "h":
        low = guess + 1
    elif high_low == "l":
        high = guess - 1
    elif high_low == "c":
        print(f"I got it in {guesses} guesses!")
        break
    else:
        print("please enter h, l or c")

    guesses += 1
