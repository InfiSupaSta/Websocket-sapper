
class FieldAlreadyFilledException(Exception):

    def __repr__(self):
        return "Can't add bombs to field - all bombs already at their places."


class FieldAlreadyExistsException(Exception):

    def __repr__(self):
        return "Can't create field - it already exists for current game."
