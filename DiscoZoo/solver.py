from random import choice


PATTERNS = [
    [ # Farm
        [(0, 0), (1, 0), (2, 0), (3, 0)],
        [(0, 0), (1, 0), (0, 1), (1, 1)],
        [(0, 0), (0, 1), (0, 2), (0, 3)],
        [(0, 0), (0, 1), (0, 2)],
        [(0, 0), (1, 0), (2, 0)],
        [(0, 0), (1, 1), (2, 1)]
    ],
    [ # Outback
        [(0, 0), (1, 1), (2, 2), (3, 3)],
        [(0, 0), (1, 0), (1, 1), (2, 1)],
        [(0, 0), (1, 0), (2, 0), (3, 0)],
        [(0, 0), (1, 0), (1, 1)],
        [(0, 0), (1, 1), (1, 2)],
        [(1, 0), (0, 1), (2, 1)]
    ],
    [ # Savannah
        [(1, 0), (0, 1), (2, 1), (1, 2)],
        [(0, 0), (2, 0), (0, 2), (2, 2)],
        [(0, 0), (0, 1), (0, 2), (0, 3)],
        [(0, 0), (1, 0), (2, 0)],
        [(0, 0), (1, 0), (0, 1)],
        [(0, 0), (1, 1), (2, 0)]
    ],
    [ # Northern
        [(0, 0), (1, 0), (1, 1), (1, 2)],
        [(1, 0), (2, 0), (0, 1), (1, 1)],
        [(2, 0), (0, 1), (1, 1), (2, 2)],
        [(0, 0), (1, 1), (2, 0)],
        [(0, 0), (1, 0), (2, 1)],
        [(0, 0), (0, 1)]
    ],
    [ # Polar
        [(1, 0), (1, 1), (0, 2), (2, 2)],
        [(0, 0), (1, 1), (2, 2), (3, 1)],
        [(0, 0), (1, 0), (0, 1), (2, 1)],
        [(0, 0), (2, 0), (2, 1)],
        [(0, 0), (1, 1), (2, 1)],
        [(0, 0), (0, 2)]
    ],
    [ # Jungle
        [(0, 0), (1, 1), (2, 0), (3, 1)],
        [(1, 0), (0, 1), (1, 2), (1, 3)],
        [(0, 0), (0, 1), (2, 0), (2, 1)],
        [(2, 0), (0, 1), (2, 2)],
        [(0, 0), (2, 0), (3, 0)],
        [(0, 0), (2, 2)]
    ],
    [ # Jurassic
        [(0, 0), (1, 1), (2, 1), (1, 2)],
        [(1, 0), (2, 0), (0, 1), (3, 1)],
        [(0, 0), (1, 0), (1, 1), (2, 2)],
        [(0, 0), (0, 2), (1, 2)],
        [(0, 0), (2, 1), (0, 2)],
        [(0, 0), (2, 1)]
    ],
    [ # Ice Age
        [(2, 0), (0, 1), (3, 1), (1, 2)],
        [(0, 0), (2, 1), (0, 2), (2, 2)],
        [(1, 0), (0, 1), (3, 1), (1, 2)],
        [(0, 0), (2, 1), (1, 2)],
        [(1, 0), (0, 1), (2, 2)],
        [(2, 0), (0, 1), (2, 2)]
    ],
    [ # City
        [(0, 0), (2, 0), (0, 1), (3, 1)],
        [(0, 0), (1, 1), (1, 2), (2, 2)],
        [(0, 0), (1, 0), (1, 1), (3, 1)],
        [(2, 0), (0, 1), (1, 2)],
        [(0, 0), (0, 1), (2, 1)],
        [(0, 0), (1, 0)]
    ],
    [ # Mountain
        [(0, 0), (0, 1), (1, 1), (2, 1)],
        [(0, 0), (1, 1), (0, 2), (2, 2)],
        [(0, 0), (2, 0), (1, 1), (2, 1)],
        [(0, 0), (0, 1), (1, 2)],
        [(0, 0), (1, 0), (2, 1)],
        [(2, 0), (0, 1)]
    ],
    [ # Moon
        [(0, 0), (0, 1), (2, 1), (2, 2)],
        [(1, 0), (1, 2), (0, 3), (2, 3)],
        [(1, 0), (0, 1), (1, 1), (2, 1)],
        [(0, 0), (0, 1), (1, 1)],
        [(0, 0), (2, 0), (1, 2)],
        [(0, 0), (1, 2)]
    ],
    [ # Mars
        [(0, 0), (1, 0), (0, 1), (1, 1)],
        [(1, 0), (1, 1), (0, 2), (1, 2)],
        [(0, 0), (2, 0), (2, 1), (1, 2)],
        [(1, 0), (0, 1), (2, 1)],
        [(0, 0), (2, 0), (1, 1)],
        [(0, 0), (0, 2)]
    ]
]
DEST_DICT = {
    1: "Farm", 2: "Outback", 3: "Savanna", 4:"Northern", 5: "Polar",
    6: "Jungle", 7: "Jurassic", 8: "Ice Age", 9: "City", 10: "Mountain",
    11: "Moon", 12: "Mars"
}
ANIM_DICTS = [
    {},
    { # Farm
        1: "Sheep", 2: "Pig", 3: "Rabbit", 4: "Horse", 5: "Cow",
        6: "Unicorn"
    },
    { # Outback
        1: "Kangaroo", 2: "Platypus", 3: "Crocodile", 4: "Koala",
        5: "Cockatoo", 6: "Tiddalik"
    },
    { # Savannah
        1: "Zebra", 2: "Hippo", 3: "Giraffe", 4: "Lion", 5: "Elephant",
        6: "Gryphon"
    },
    { # Northern
        1: "Bear", 2: "Skunk", 3: "Beaver", 4: "Moose", 5: "Fox", 6: "Sasquatch"
    },
    { # Polar
        1: "Penguin", 2: "Seal", 3: "Muskox", 4: "Polar Bear", 5: "Walrus",
        6: "Yeti"
    },
    { # Jungle
        1: "Monkey", 2: "Toucan", 3: "Gorilla", 4: "Panda", 5: "Tiger",
        6: "Phoenix"
    },
    { # Jurassic
        1: "Diplodicus", 2: "Stegosaurus", 3: "Raptor", 4: "T-Rex",
        5: "Triceratops", 6: "Dragon"
    },
    { # Ice Age
        1: "Wooly Rhino", 2: "Giant Sloth", 3: "Dire Wolf", 4: "Saber Tooth",
        5: "Mammoth", 6: "Akhlut"
    },
    { # City
        1: "Raccoon", 2: "Pigeon", 3: "Rat", 4: "Squirrel", 5: "Opossum",
        6: "Sewer Turtle"
    },
    { # Mountain
        1: "Goat", 2: "Cougar", 3: "Elk", 4: "Eagle", 5: "Coyote", 6: "Aatxe"
    },
    { # Moon
        1: "Moonkey", 2: "Lunar Tick", 3: "Tribble", 4: "Moonicorn",
        5: "Luna Moth", 6: "Jade Rabbit"
    },
    { # Mars
        1: "Rock", 2: "Marsmot", 3: "Marsmoset", 4: "Rover", 5: "Martian",
        6: "Marsmallow"
    }   
]

class Square:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
    
    def __add__(self, other):
        return Square(self.x + other.x, self.y + other.y)

    # def __eq__(self, other):
    #     return self.x == other.x and self.y == other.y
    
    def to_int(self):
        return self.x + 5 * self.y

class Board:
    def __init__(self, board=[0]*25, blank=False):
        self.squares = [*board]  # Splat copy
        if blank:
            self.squares = [-1] * 25
    
    def has(self, square):
        return self.squares[square.to_int()] > 0
    
    def matches(self, otherboard):
        for i in range(25):
            if otherboard.squares[i] >= 0:
                if otherboard.squares[i] != self.squares[i]:
                    return False
        return True
    
    def add(self, animal_num, offset):
        """
        Tries to add the animal onto the board at offset.
        Animal_num is a tuple, offset is a Square.
        Returns True if successful, False otherwise.
        """
        animal = PATTERNS[animal_num[0]][animal_num[1]]
        animalpos = [Square(pos[0], pos[1]) + offset for pos in animal]
        if any(self.has(sq) for sq in animalpos):
            return False
        for sq in animalpos:
            self.squares[sq.to_int()] = animal_num[1] + 1
        return True
    
    def display(self, target_index=-1, blank=False):
        printstr = "\n"
        for i in range(25):
            if i == target_index:
                printstr += "#"
            elif self.squares[i] < 0:
                printstr += "-"
            elif blank and self.squares[i] == 0:
                printstr += "."
            else:
                printstr += str(self.squares[i])
            if i % 5 == 4:
                printstr += "\n"
            else:
                printstr += " "
        print(printstr)


def place(animal_list, board_state):
    validboards = []
    if animal_list:
        animal = PATTERNS[animal_list[0][0]][animal_list[0][1]]
        width, height = (5 - max(x) for x in zip(*animal))
        for x in range(width):
            for y in range(height):
                b = Board(board_state.squares)
                valid = b.add(animal_list[0], Square(x, y))
                if not valid:
                    continue
                if len(animal_list) > 1:
                    validboards.extend(place(animal_list[1:], b))
                else:
                    validboards.append(b)
    return validboards


def find_probability_grid(animal_list, validboards):
    return [
        len([b.squares[i] for b in validboards if b.squares[i] > 0])
        for i in range(25)
    ]


def find_variance_grid(animal_list, validboards):
    return [len(set([b.squares[i] for b in validboards])) for i in range(25)]


def guess(animal_list, valid_anims):
    guess_board = Board(blank=True)
    valid_boards = place(animal_list, Board())
    guesses = 0
    attempts = 0
    while True:
        prob_grid = find_probability_grid(animal_list, valid_boards)
        var_grid = find_variance_grid(animal_list, valid_boards)
        for i in range(25):
            if guess_board.squares[i] >= 0:
                prob_grid[i] = -1
                var_grid[i] = 99
        maxval = max(prob_grid)
        minvar = min(var_grid)
        if maxval <= 0:
            # Only one solution
            valid_boards[0].display(blank=True)
            print(f"Board search complete. Took {guesses} guesses.")
            print(f"Requires {attempts} attempts.")
            if 25 - valid_boards[0].squares.count(0) == attempts:
                print("PERFECT SEARCH!")
            return
        elif minvar == 1:
            # All boards have this in common
            maxpos = choice([i for i in range(25) if var_grid[i] == minvar])
            i = valid_boards[0].squares[maxpos]
            if i == 0:
                attempts -= 1
        else:
            # Pick a square to guess
            maxpos = choice([i for i in range(25) if prob_grid[i] == maxval])
            guess_board.display(maxpos)
            response = input(f"What is at this square? {valid_anims}: ")
            if not response:
                response = 0
            try:
                i = int(response)
            except ValueError:
                if response == "done":
                    return None
                elif response == "print":
                    for b in valid_boards:
                        b.display()
                    continue
                else:
                    continue
            else:
                guesses += 1
        guess_board.squares[maxpos] = i
        valid_boards = [b for b in valid_boards if b.matches(guess_board)]
        attempts += 1


def select():
    loc_num = 1
    while True:
        # Initialize variables
        animal_list = []
        # Select location
        while True:
            for i in DEST_DICT:
                print(f"{i}: {DEST_DICT[i]}")
            response = input("What is your destination? ")
            if not response:  # Default to previous
                response = loc_num
            try:
                loc_num = int(response)
            except ValueError:
                print("Please enter a valid number.")
                continue
            except:
                print("Unknown error")
                continue
            if loc_num not in DEST_DICT:
                print("Please enter a destination number.")
                continue
            else:
                break
        # Select animals
        while True:
            for i in ANIM_DICTS[loc_num]:
                print(f"{i}: {ANIM_DICTS[loc_num][i]}")
            response = input("Select animals, space-separated: ")
            try:
                anim_nums = [int(i) for i in response.split(' ')]
            except:
                print("Invalid input")
                continue
            if any(i not in ANIM_DICTS[loc_num] for i in anim_nums):
                print("Please enter valid numbers")
                continue
            for i in anim_nums:
                animal_list.append((loc_num - 1, i - 1))
            break
        # Run location guesser
        guess(animal_list, [0] + anim_nums)
        # Check for repetition
        response = input("Input q to quit, all else continues: ")
        if response == "q":
            break
            

select()
