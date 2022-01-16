from zoneinfo import available_timezones


available_exits = ["north", "south", "east", "west"]

chosen_exit = ""

while chosen_exit not in available_exits:
    chosen_exit = input("please choose a direction : ")
    # casefold 소문자처리
    if chosen_exit.casefold() == "quit":
        print("Game over")
        break

print("got out of there")

