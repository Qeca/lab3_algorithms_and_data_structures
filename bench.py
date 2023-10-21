from RBTree import RBTree, Student
import timeit

students: list[Student] = [
    Student("Шаронов", "Дмитрий", "Вадимович", "4219", 2, 4.33),
    Student("Иванов", "Иван", "Иванович", "4219", 2, 4.33),
    Student("Петров", "Петр", "Петрович", "4219", 3, 4.11),
    Student("Сидоров", "Андрей", "Васильевич", "4220", 2, 4.85),
    Student("Козлова", "Мария", "Викторовна", "4221", 1, 4.75),
    Student("Григорьева", "Екатерина", "Александровна", "4220", 3, 4.21),
    Student("Смирнов", "Алексей", "Николаевич", "4218", 4, 4.02),
    Student("Михайлов", "Денис", "Сергеевич", "4218", 3, 4.56),
    Student("Зайцев", "Олег", "Валентинович", "4221", 2, 4.01),
    Student("Лебедева", "Анна", "Андреевна", "4222", 1, 4.89),
]
tree: RBTree = RBTree()

for it in students:
    tree.insert(it)
start_time = timeit.default_timer()
tree.print_tree()
print(timeit.default_timer() - start_time)

start_time = timeit.default_timer()
tree.remove(4.33)
print(timeit.default_timer() - start_time)
tree.print_tree()
