import unittest
from RBTree import RBTree, Car
import sys
from io import StringIO


class MyTestCase(unittest.TestCase):
    def test_is_empty(self):
        tree: RBTree = RBTree()
        self.assertEqual(tree.is_empty(), True)

    def test_insert_and_print(self):
        tree: RBTree = RBTree()
        cars: list[Car] = [
            Car("W0999876532YYY234", "BMW", 1673, 5000000, 123.33),
            Car("W1234567890ABCDEF", "Audi", 1900, 6030000, 145.75),
            Car("W9876543210ABCXYZ", "Mercedes", 1750, 5500000, 135.50),
            Car("W7777777777XYZ123", "Lamborghini", 1800, 8000000, 200.25),
            Car("W5555555555LMN456", "Ferrari", 1650, 7500000, 175.60),
            Car("W4444444444PQR789", "Porsche", 1600, 7000000, 155.25),
            Car("W8888888888JKL321", "Jaguar", 1700, 6503000, 130.75),
            Car("W6666666666QWE987", "Tesla", 1550, 6500000, 190.30),
            Car("W2222222222MNO654", "Ford", 1500, 6000000, 125.40)
        ]

        original_stdout = sys.stdout
        output_buffer = StringIO()
        sys.stdout = output_buffer
        for it in cars:
            tree.insert(it)
        print()
        tree.print_tree()
        sys.stdout = original_stdout
        output_text = output_buffer.getvalue()
        output_buffer.close()
        with open('../lab3_algorithms_and_data_structures/test.txt', "r", encoding="utf-8") as f:
            self.assertEqual(output_text, f.read())
            f.close()

    def test_remove(self):
        tree: RBTree = RBTree()
        cars: list[Car] = [
            Car("W0999876532YYY234", "BMW", 1673, 5000000, 123.33),
            Car("W1234567890ABCDEF", "Audi", 1900, 6030000, 145.75),
            Car("W9876543210ABCXYZ", "Mercedes", 1750, 5500000, 135.50),
            Car("W7777777777XYZ123", "Lamborghini", 1800, 8000000, 200.25),
            Car("W5555555555LMN456", "Ferrari", 1650, 7500000, 175.60),
            Car("W4444444444PQR789", "Porsche", 1600, 7000000, 155.25),
            Car("W8888888888JKL321", "Jaguar", 1700, 6503000, 130.75),
            Car("W6666666666QWE987", "Tesla", 1550, 6500000, 190.30),
            Car("W2222222222MNO654", "Ford", 1500, 6000000, 125.40)
        ]

        original_stdout = sys.stdout
        output_buffer = StringIO()
        sys.stdout = output_buffer
        for it in cars:
            tree.insert(it)
        tree.remove(6503000)
        print()
        tree.print_tree()
        sys.stdout = original_stdout
        output_text = output_buffer.getvalue()
        output_buffer.close()

        with open('../lab3_algorithms_and_data_structures/test2.txt', "r", encoding="utf-8") as f:
            self.assertEqual(output_text, f.read())
            f.close()

    def test_find(self):
        cars: list[Car] = [
            Car("W0999876532YYY234", "BMW", 1673, 5000000, 123.33),
            Car("W1234567890ABCDEF", "Audi", 1900, 6030000, 145.75),
            Car("W9876543210ABCXYZ", "Mercedes", 1750, 5500000, 135.50),
            Car("W7777777777XYZ123", "Lamborghini", 1800, 8000000, 200.25),
            Car("W5555555555LMN456", "Ferrari", 1650, 7500000, 175.60),
            Car("W4444444444PQR789", "Porsche", 1600, 7000000, 155.25),
            Car("W8888888888JKL321", "Jaguar", 1700, 6503000, 130.75),
            Car("W6666666666QWE987", "Tesla", 1550, 6500000, 190.30),
            Car("W2222222222MNO654", "Ford", 1500, 6000000, 125.40)
        ]
        tree: RBTree = RBTree()

        for it in cars:
            tree.insert(it)

        self.assertEqual(tree.find(6000000), (Car(mark='W2222222222MNO654', VIN='Ford', capacity=1500, id=6000000, avg_speed=125.40), True))

    def test_contains(self):
        cars: list[Car] = [
            Car("W0999876532YYY234", "BMW", 1673, 5000000, 123.33),
            Car("W1234567890ABCDEF", "Audi", 1900, 6030000, 145.75),
            Car("W9876543210ABCXYZ", "Mercedes", 1750, 5500000, 135.50),
            Car("W7777777777XYZ123", "Lamborghini", 1800, 8000000, 200.25),
            Car("W5555555555LMN456", "Ferrari", 1650, 7500000, 175.60),
            Car("W4444444444PQR789", "Porsche", 1600, 7000000, 155.25),
            Car("W8888888888JKL321", "Jaguar", 1700, 6503000, 130.75),
            Car("W6666666666QWE987", "Tesla", 1550, 6500000, 190.30),
            Car("W2222222222MNO654", "Ford", 1500, 6000000, 125.40)
        ]
        tree: RBTree = RBTree()

        for it in cars:
            tree.insert(it)

        self.assertEqual(6500000 in tree, True)

    def test_balanced(self):
        cars: list[Car] = [
            Car("W0999876532YYY234", "BMW", 1673, 5000000, 123.33),
            Car("W1234567890ABCDEF", "Audi", 1900, 6030000, 145.75),
            Car("W9876543210ABCXYZ", "Mercedes", 1750, 5500000, 135.50),
            Car("W7777777777XYZ123", "Lamborghini", 1800, 8000000, 200.25),
            Car("W5555555555LMN456", "Ferrari", 1650, 7500000, 175.60),
            Car("W4444444444PQR789", "Porsche", 1600, 7000000, 155.25),
            Car("W8888888888JKL321", "Jaguar", 1700, 6503000, 130.75),
            Car("W6666666666QWE987", "Tesla", 1550, 6500000, 190.30),
            Car("W2222222222MNO654", "Ford", 1500, 6000000, 125.40)
        ]

        tree = RBTree()
        for it in cars:
            tree.insert(it)
        tree.remove(6500000)
        self.assertEqual(tree.is_balanced(), True)


if __name__ == '__main__':
    unittest.main()
