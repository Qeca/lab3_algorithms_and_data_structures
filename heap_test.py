import sys
import unittest
from io import StringIO

from heap import Heap, Student


class MyTestCase(unittest.TestCase):
    def test_create_heap_from_list_and_print(self):
        students: list[Student] = [
            Student("Андреев", "Анатолий", "Денисович", "4219", 2, 4.33),
            Student("Иванов", "Иван", "Иванович", "4219", 2, 4.33),
            Student("Петров", "Петр", "Петрович", "4219", 3, 4.19),
            Student("Павлюченко", "Андрей", "Васильевич", "4220", 2, 4.85),
            Student("Козлова", "Мария", "Викторовна", "4221", 1, 4.75),
            Student("Григорьева", "Екатерина", "Александровна", "4220", 3, 4.23),
            Student("Смирнов", "Алексей", "Николаевич", "4218", 4, 4.02),
            Student("Исидова", "Денис", "Сергеевич", "4218", 3, 4.57),
            Student("Зайцев", "Олег", "Валентинович", "4221", 2, 4.11),
            Student("Лебедева", "Анна", "Андреевна", "4222", 1, 4.89),
        ]

        heap = Heap.create_heap_from_list(students)
        original_stdout = sys.stdout
        output_buffer = StringIO()
        sys.stdout = output_buffer
        print()
        heap.print_heap()
        sys.stdout = original_stdout
        output_text = output_buffer.getvalue()
        output_buffer.close()
        with open('test_heap_1.txt', "r", encoding="utf-8") as f:
            self.assertEqual(output_text, f.read())
            f.close()

    def test_is_empty(self):
        heap = Heap()
        self.assertEqual(heap.is_empty(), True)

    def test_size(self):
        students: list[Student] = [
            Student("Андреев", "Анатолий", "Денисович", "4219", 2, 4.33),
            Student("Иванов", "Иван", "Иванович", "4219", 2, 4.33),
            Student("Петров", "Петр", "Петрович", "4219", 3, 4.19),
            Student("Павлюченко", "Андрей", "Васильевич", "4220", 2, 4.85),
            Student("Козлова", "Мария", "Викторовна", "4221", 1, 4.75),
            Student("Григорьева", "Екатерина", "Александровна", "4220", 3, 4.23),
            Student("Смирнов", "Алексей", "Николаевич", "4218", 4, 4.02),
            Student("Исидова", "Денис", "Сергеевич", "4218", 3, 4.57),
            Student("Зайцев", "Олег", "Валентинович", "4221", 2, 4.11),
            Student("Лебедева", "Анна", "Андреевна", "4222", 1, 4.89),
        ]

        heap = Heap.create_heap_from_list(students)
        self.assertEqual(heap.get_size(), 10)

    def test_change(self):
        students: list[Student] = [
            Student("Андреев", "Анатолий", "Денисович", "4219", 2, 4.33),
            Student("Иванов", "Иван", "Иванович", "4219", 2, 4.35),
            Student("Петров", "Петр", "Петрович", "4219", 3, 4.19),
            Student("Павлюченко", "Андрей", "Васильевич", "4220", 2, 3.0),
            Student("Козлова", "Мария", "Викторовна", "4221", 1, 4.75),
            Student("Григорьева", "Екатерина", "Александровна", "4220", 3, 4.23),
            Student("Смирнов", "Алексей", "Николаевич", "4218", 4, 4.02),
            Student("Исидова", "Денис", "Сергеевич", "4218", 3, 4.57),
            Student("Зайцев", "Олег", "Валентинович", "4221", 2, 4.11),
            Student("Лебедева", "Анна", "Андреевна", "4222", 1, 4.89),
        ]

        heap = Heap.create_heap_from_list(students)
        heap.change(3, Student("Яблочков", "Анатолий", "Денисович", 2219, 3, 5))
        original_stdout = sys.stdout
        output_buffer = StringIO()
        sys.stdout = output_buffer
        print()
        heap.print_heap()
        sys.stdout = original_stdout
        output_text = output_buffer.getvalue()
        output_buffer.close()
        with open('test_heap_2.txt', "r", encoding="utf-8") as f:
            self.assertEqual(output_text, f.read())
            f.close()

    def test_change(self):
        students: list[Student] = [
            Student("Андреев", "Анатолий", "Денисович", "4219", 2, 4.33),
            Student("Иванов", "Иван", "Иванович", "4219", 2, 4.35),
            Student("Петров", "Петр", "Петрович", "4219", 3, 4.19),
            Student("Павлюченко", "Андрей", "Васильевич", "4220", 2, 3.0),
            Student("Козлова", "Мария", "Викторовна", "4221", 1, 4.75),
            Student("Григорьева", "Екатерина", "Александровна", "4220", 3, 4.23),
            Student("Смирнов", "Алексей", "Николаевич", "4218", 4, 4.02),
            Student("Исидова", "Денис", "Сергеевич", "4218", 3, 4.57),
            Student("Зайцев", "Олег", "Валентинович", "4221", 2, 4.11),
            Student("Лебедева", "Анна", "Андреевна", "4222", 1, 4.89),
        ]

        heap = Heap.create_heap_from_list(students)
        original_stdout = sys.stdout
        output_buffer = StringIO()
        sys.stdout = output_buffer
        print()
        heap.append(Student("Яблочков", "Анатолий", "Денисович", 2219, 3, 5))
        heap.print_heap()
        sys.stdout = original_stdout
        output_text = output_buffer.getvalue()
        output_buffer.close()
        with open('test_heap_3.txt', "r", encoding="utf-8") as f:
            self.assertEqual(output_text,f.read())
            f.close()

    def test_contains_and_find(self):
        students: list[Student] = [
            Student("Андреев", "Анатолий", "Денисович", "4219", 2, 4.33),
            Student("Иванов", "Иван", "Иванович", "4219", 2, 4.35),
            Student("Петров", "Петр", "Петрович", "4219", 3, 4.19),
            Student("Павлюченко", "Андрей", "Васильевич", "4220", 2, 3.0),
            Student("Козлова", "Мария", "Викторовна", "4221", 1, 4.75),
            Student("Григорьева", "Екатерина", "Александровна", "4220", 3, 4.23),
            Student("Смирнов", "Алексей", "Николаевич", "4218", 4, 4.02),
            Student("Исидова", "Денис", "Сергеевич", "4218", 3, 4.57),
            Student("Зайцев", "Олег", "Валентинович", "4221", 2, 4.11),
            Student("Лебедева", "Анна", "Андреевна", "4222", 1, 4.89),
        ]

        heap = Heap.create_heap_from_list(students)
        self.assertEqual(heap.find(4.57), 4)
        self.assertEqual(4.57 in heap, True)

if __name__ == '__main__':
    unittest.main()
