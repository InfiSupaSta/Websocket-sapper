class FieldAlreadyFilledException(Exception):

    def __repr__(self):
        return "Can't add bombs to field - all bombs already at their places."


class FieldAlreadyExistsException(Exception):

    def __repr__(self):
        return "Can't create field - it already exists."


class GameOverException(Exception):

    def __repr__(self):
        return "Game over."


class WrongCoordinatesException(Exception):
    def __repr__(self):
        return "Wrong x or y coordinates."


class CellAlreadyRevealedException(Exception):

    def __repr__(self):
        return "Cell is already revealed."
