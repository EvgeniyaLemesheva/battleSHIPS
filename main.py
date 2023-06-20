import random

class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


class Ship:
    def __init__(self, dots):
        self.dots = dots
        self.lives = len(dots)

    def hit(self, dot):
        for i, d in enumerate(self.dots):
            if d == dot:
                self.dots.pop(i)
                self.lives -= 1
                return True
        return False


class Board:
    def __init__(self):
        self.board_user = [['O' for _ in range(6)] for _ in range(6)]
        self.board_computer = [['O' for _ in range(6)] for _ in range(6)]
        self.ships = [
            Ship([Dot(1, 1), Dot(1, 2), Dot(1, 3)]),
            Ship([Dot(2, 1), Dot(2, 2)]),
            Ship([Dot(3, 1), Dot(3, 2)]),
            Ship([Dot(4, 1)]),
            Ship([Dot(4, 3)]),
            Ship([Dot(5, 1)]),
            Ship([Dot(5, 3)]),
            Ship([Dot(6, 1)]),
            Ship([Dot(6, 3)]),
        ]
        self.shots_user = []
        self.shots_computer = []

    def is_out_of_bounds(self, x, y):
        return x < 0 or x >= 6 or y < 0 or y >= 6

    def shoot_user(self, dot):
        self.shots_user.append(dot)
        for ship in self.ships:
            if ship.hit(dot):
                self.board_user[dot.x][dot.y] = 'X'
                if ship.lives == 0:
                    for d in ship.dots:
                        self.board_user[d.x][d.y] = 'X'
                    print("Вы потопили корабль противника!")
                return True
        self.board_user[dot.x][dot.y] = 'T'
        return False

    def shoot_computer(self, dot):
        self.shots_computer.append(dot)
        for ship in self.ships:
            if ship.hit(dot):
                self.board_computer[dot.x][dot.y] = 'X'
                if ship.lives == 0:
                    for d in ship.dots:
                        self.board_computer[d.x][d.y] = 'X'
                    print("Компьютер потопил ваш корабль!")
                return True
        self.board_computer[dot.x][dot.y] = 'T'
        return False

    def display(self):
        print("--------------------")
        print(" Доска пользователя:")
        for row in self.board_user:
            print(' '.join(row))
        print("--------------------")
        print(" Доска компьютера:")
        for row in self.board_computer:
            print(' '.join(row))

    def is_game_over(self):
        return all(ship.lives == 0 for ship in self.ships)


class Player:
    def __init__(self, board):
        self.board = board

    def move(self):
        while True:
            try:
                x, y = input("Ваш ход (x y): ").split()
                x = int(x) - 1
                y = int(y) - 1
                if self.board.is_out_of_bounds(x, y):
                    print("Координаты выходят за границы доски. Попробуйте снова.")
                    continue
                dot = Dot(x, y)
                if dot in self.board.shots_user:
                    print("Вы уже стреляли в эту клетку. Попробуйте снова.")
                    continue
                if self.board.shoot_user(dot):
                    print("Попадание!")
                    if self.board.is_game_over():
                        print("--------------------")
                        print(" Вы победили!")
                    return
                else:
                    print("Мимо!")
                break
            except ValueError:
                print("Некорректный формат координат. Попробуйте снова.")


class Computer:
    def __init__(self, board):
        self.board = board

    def move(self):
        while True:
            x = random.randint(0, 5)
            y = random.randint(0, 5)
            dot = Dot(x, y)
            if dot in self.board.shots_computer:
                continue
            print("Ход компьютера:", x + 1, y + 1)
            if self.board.shoot_computer(dot):
                print("Попадание компьютера!")
                if self.board.is_game_over():
                    print("--------------------")
                    print(" Компьютер победил!")
                    return
            else:
                print("Мимо компьютера!")
            break


class Game:
    def __init__(self):
        self.board = Board()
        self.player = Player(self.board)
        self.computer = Computer(self.board)

    def start(self):
        print("-----------------------------------")
        print("        Игра Морской Бой           ")
        print("-----------------------------------")
        print("   Правила:")
        print("   Формат ввода: x y (например: 3 4)")
        print("   Координаты от 1 до 6")
        print("   Буквой X помечаются подбитые корабли")
        print("   Буквой T — промахи")
        print("--------------------")
        while True:
            self.player.move()
            self.computer.move()
            self.board.display()


game = Game()
game.start()
