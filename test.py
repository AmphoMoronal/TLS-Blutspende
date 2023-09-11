time = 1000
while time < 1500:
    if time % 100 == 45:
        time -= 45
        time += 100
    else:
        time += 15
    print(time)
