is_good_mood: bool = True
answer: str = input("How are you today?")
if answer.lower() == "yes":
    print("Glad to hear that!")
elif answer.lower() == "no":
    print("Oh no!")
else:
    print("What did you say?")
