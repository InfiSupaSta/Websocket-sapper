from typing import List
import random

from exceptions import FieldAlreadyFilledException, FieldAlreadyExistsException


class Coordinates:
    def __init__(self, *, x: int, y: int):
        self.x = x
        self.y = y

    def __eq__(self, other_pair_of_coordinated):
        if isinstance(self, Coordinates):
            return self.x == other_pair_of_coordinated.x and self.y == other_pair_of_coordinated.y
        raise TypeError

    def __repr__(self):
        human_readable_representation = f"Coordinates(x={self.x}, y={self.y})"
        return human_readable_representation


class Field:

    def __init__(self, *, size_x: int, size_y: int, amount_of_bombs: int):
        self.size_x = size_x
        self.size_y = size_y
        self.amount_of_bombs = amount_of_bombs
        self.field = None
        self.bomb_coordinates = []

    def create_field(self):
        if self.field is None:
            self.field = [["[ ]"] * self.size_x for _ in range(self.size_y)]
            return self.field
        raise FieldAlreadyExistsException

    def fill_field_with_bombs(self):

        for _ in range(self.amount_of_bombs):
            bomb_coordinates = self._generate_coordinates_for_bomb()

            self.field[bomb_coordinates.x][bomb_coordinates.y] = "X"
            self.bomb_coordinates.append(bomb_coordinates)

        return self.field

    def _generate_coordinates_for_bomb(self):

        if len(self.bomb_coordinates) == self.amount_of_bombs:
            raise FieldAlreadyFilledException

        while True:
            random_x_position_coordinate = random.randint(0, self.size_x - 1)
            random_y_position_coordinate = random.randint(0, self.size_y - 1)

            bomb_coordinates = Coordinates(x=random_x_position_coordinate, y=random_y_position_coordinate)
            if bomb_coordinates in self.bomb_coordinates:
                continue

            break

        return bomb_coordinates

    def fill_field_with_numbers(self):
        for x_position in range(self.size_x):
            for y_position in range(self.size_y):

                if self.field[x_position][y_position] == "X":
                    continue

                current_position = Coordinates(x=x_position, y=y_position)
                bombs_around = self._check_cells_around_current_coordinates(current_position)
                # self.field[x_position][y_position] = bombs_around
                self.field[x_position][y_position] = str(bombs_around)

    def _check_cells_around_current_coordinates(self, coordinates: Coordinates) -> int:

        top_left = Coordinates(x=coordinates.x - 1, y=coordinates.y + 1)
        top = Coordinates(x=coordinates.x, y=coordinates.y + 1)
        top_right = Coordinates(x=coordinates.x + 1, y=coordinates.y + 1)
        right = Coordinates(x=coordinates.x + 1, y=coordinates.y)
        bottom_right = Coordinates(x=coordinates.x + 1, y=coordinates.y - 1)
        bottom = Coordinates(x=coordinates.x, y=coordinates.y - 1)
        bottom_left = Coordinates(x=coordinates.x - 1, y=coordinates.y - 1)
        left = Coordinates(x=coordinates.x - 1, y=coordinates.y)

        cells_around = [top_left, top, top_right, right, bottom_right, bottom, bottom_left, left]
        bombs_around = 0

        for cell in cells_around:
            if cell.x < 0 or cell.y < 0 or cell.x > self.size_x or cell.y > self.size_y:
                continue
            if cell in self.bomb_coordinates:
                bombs_around += 1

        return bombs_around

    def get_field(self) -> List[List[str]]:
        return self.field

    def __repr__(self):
        human_readable_representation = f"Field(size_x={self.size_x}, size_y={self.size_y})"
        return human_readable_representation
