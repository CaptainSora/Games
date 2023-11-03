from itertools import combinations, product


def find_collectors():
    with open("APGP.txt") as f:
        # Name, Body, Year, RQ
        cars = [car.strip().split(", ") for car in f.readlines()]
    # [Name, Hyundai, SUV, Saloon, Conv/Roadster, 20s, 10s, 1900s]
    goal = [1, 1, 3, 1, 1, 1, 1]
    top = []  # rq 44-45, need 1
    mid = []  # rq 42-43, need 2
    bot = []  # rq 40-41, need 2
    cardict = {}
    for car in cars:
        cardict[car[0]] = f"rq{car[3]} {car[0]} ({car[2]})"
        spec = [
            car[0],
            car[0].split(" ")[0] == "Hyundai",
            car[1] == "SUV",
            car[1] == "Saloon",
            car[1] == "Convertible" or car[1] == "Roadster",
            int(car[2]) >= 2020,
            2010 <= int(car[2]) < 2020,
            int(car[2]) < 2000,
            int(car[4])
        ]
        if int(car[3]) >= 44:
            top.append(spec)
        elif int(car[3]) >= 42:
            mid.append(spec)
        else:
            bot.append(spec)
    # Track possibilities
    possible = []
    for tup in product(top, combinations(mid, 2), combinations(bot, 2)):
        flat = [tup[0]] + [car for cars in tup[1:] for car in cars]
        flat_t = [list(col) for col in zip(*flat)]
        score = [sum(col) for col in flat_t[1:-1]]
        points = (max(flat_t[-1]), sum(flat_t[-1]))
        if all([score[i] >= goal[i] for i in range(len(score))]):
            possible.append([
                points,
                "\n".join([cardict[car] for car in flat_t[0]])
            ])
    possible.sort(key=lambda x: x[0], reverse=True)
    for tup in possible:
        print(f"Score: {tup[0]}\n{tup[1]}\n\n")


find_collectors()