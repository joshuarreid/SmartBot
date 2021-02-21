
print("Text based Game!")

text = input("Left or Right: ")
if text == "left":
    print("You went left")
    text = input("up or down? ")
    if text == "up":
        print("you went up!")

elif text == 'right':
    print("you went right")
