from RBTree import RBTree, Car
import timeit

cars: list[Car] = [
        Car("W0999876532YYY234", "BMW", 1673, 123.33, 5000000),
        Car("W1234567890ABCDEF", "Audi", 1900, 145.75, 6000000),
        Car("W9876543210ABCXYZ", "Mercedes", 1750, 135.50, 5500000),
        Car("W7777777777XYZ123", "Lamborghini", 1800, 200.25, 8000000),
        Car("W5555555555LMN456", "Ferrari", 1650, 175.60, 7500000),
        Car("W4444444444PQR789", "Porsche", 1600, 155.25, 7000000),
        Car("W8888888888JKL321", "Jaguar", 1700, 130.75, 6500000),
        Car("W6666666666QWE987", "Tesla", 1550, 190.30, 6500000),
        Car("W2222222222MNO654", "Ford", 1500, 125.40, 6000000)
    ]
tree: RBTree = RBTree()

for it in cars:
    tree.insert(it)
start_time = timeit.default_timer()
tree.print_tree()
print(timeit.default_timer() - start_time)

start_time = timeit.default_timer()
tree.is_balanced()
print(timeit.default_timer() - start_time)
tree.print_tree()
