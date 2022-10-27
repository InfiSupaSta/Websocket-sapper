from unittest import TestCase, main
from typing import List

from backend.sapper.field.core import Field
from backend.sapper.field.exceptions import FieldAlreadyExistsException

EXPECTED_FIELD = [
    ['[ ]', '[ ]', '[ ]'],
    ['[ ]', '[ ]', '[ ]'],
    ['[ ]', '[ ]', '[ ]'],
    ['[ ]', '[ ]', '[ ]'],
    ['[ ]', '[ ]', '[ ]'],
]


class FieldTest(TestCase):

    def setUp(self):
        self.field_x_size = 3
        self.field_y_size = 5
        self.amount_of_bombs_on_field = int(self.field_x_size * self.field_y_size * 0.3)

        self.field = Field(size_x=self.field_x_size,
                           size_y=self.field_y_size,
                           amount_of_bombs=self.amount_of_bombs_on_field)

    def test_field_creates_properly(self):
        self.assertEqual(self.field.get_field(), None)
        self.field.create_field()
        self.assertEqual(isinstance(self.field.get_field(), List), True)

    def test_field_cant_be_created_if_it_exists(self):
        self.test_field_creates_properly()
        with self.assertRaises(FieldAlreadyExistsException):
            self.field.create_field()

    def test_created_field_equal_to_expected(self):
        self.test_field_creates_properly()
        self.assertEqual(self.field.get_field(), EXPECTED_FIELD)


if __name__ == '__main__':
    main()
