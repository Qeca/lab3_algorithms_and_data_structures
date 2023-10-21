import pickle
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TypeVar, Generic, Optional, Callable


class IKey(ABC):

    @abstractmethod
    def key(self) -> float:
        ...


T = TypeVar("T", bound=IKey)


class HeapOverFlowException(Exception):
    pass


class EmptyHeapException(Exception):
    pass


class IndexOutRangeException(Exception):
    pass


@dataclass
class Student(IKey):
    def __init__(self, surname=None, name=None, patronymic=None, group_number=None, course=None, id=None):
        self.surname = surname
        self.name = name
        self.patronymic = patronymic
        self.group_number = group_number
        self.course = course
        self.id = id

    def key(self) -> float:
        return self.id

    def __str__(self) -> str:
        return f"Student({self.surname} {self.name} {self.patronymic},{self.id})"


@dataclass
class DoublyNode(Generic[T]):
    data: T
    next_ptr: Optional['DoublyNode[T]'] = None
    prev_ptr: Optional['DoublyNode[T]'] = None


class DoublyLinkedList(Generic[T]):

    def __init__(self) -> None:
        self._length: int = 0
        self._head: Optional[DoublyNode[T]] = None
        self._tail: Optional[DoublyNode[T]] = None

    def get_size(self) -> int:
        return self._length

    def is_empy(self) -> bool:
        return self._length == 0

    def push_tail(self, data: T) -> None:
        node = DoublyNode[T](data, None)
        if self._length <= 0:
            self._head = node
            self._tail = node
            self._length += 1
            return

        self._tail.next_ptr = node
        node.prev_ptr = self._tail
        self._tail = node
        self._length += 1

    def push_head(self, data: T) -> None:
        node = DoublyNode[T](data)
        if self._length <= 0:
            self._head = node
            self._tail = node
            self._length += 1
            return

        node.next_ptr = self._head
        self._head.prev_ptr = node
        self._head = node
        self._length += 1

    def insert(self, index: int, data: T) -> None:
        if index == 0:
            self.push_head(data)
            return
        elif index == self._length - 1:
            self.push_tail(data)
            return

        node = self._head
        for i in range(0, index):
            node = node.next_ptr

        insert_node = DoublyNode[T](data)
        insert_node.next_ptr = node
        node.prev_ptr.next_ptr = insert_node
        insert_node.prev_ptr = node.prev_ptr
        node.prev_ptr = insert_node
        self._length += 1

    def __setitem__(self, index: int, data: T) -> None:
        if 0 <= index < self._length:
            # Если индекс находится в допустимых пределах
            node = self._head
            for i in range(index):
                node = node.next_ptr
            node.data = data

    def __getitem__(self, item):
        return self.get(item)

    def get(self, index: int) -> T:
        if index == 0:
            return self._head.data
        if index == self._length - 1:
            return self._tail.data

        node = self._head
        for i in range(0, index):
            node = node.next_ptr
        return node.data

    def remove(self, index: int) -> bool:
        if index == 0:
            node = self._head
            self._head = node.next_ptr
            self._head.prev_ptr = None
            del node
            self._length -= 1
            return True

        node = self._head
        for i in range(0, index - 1):
            node = node.next_ptr

        if index == self._length - 1:
            self._tail.prev_ptr = None
            self._tail = node
            self._tail.next_ptr = None
            self._length -= 1
            return True

        delete_node = node.next_ptr
        node.next_ptr = delete_node.next_ptr
        node.next_ptr.prev_ptr = delete_node.prev_ptr
        self._length -= 1
        return True

    def __str__(self) -> str:
        my_str: str = ""
        node = self._head
        while node is not None:
            my_str += str(node.data) + " "
            node = node.next_ptr
        return f"Current state: [{my_str}]"


class Heap(Generic[T]):

    def __init__(self,
                 fixed: bool = False,
                 comp: Callable[[T, T], bool] = lambda a, b: a.key() <= b.key()) -> None:
        self._llist: DoublyLinkedList[Optional[T]] = DoublyLinkedList()
        self._length: int = 0
        self._is_fixed: bool = fixed
        self._comp: Callable[[T, T], bool] = comp

    @staticmethod
    def create_heap_from_list(data: list[T],
                              fixed: bool = True,
                              comp: Callable[[T, T], bool] = lambda a, b: a.key() < b.key()) -> 'Heap[T]':
        heap: Heap[T] = Heap[T](fixed=fixed, comp=comp)
        for it in data:
            heap.append(it)
        return heap

    def is_empty(self) -> bool:
        return self._length == 0

    def get_size(self) -> int:
        return self._length

    def __trickle_up(self, index: int) -> None:
        parent: int = (index - 1) // 2
        bottom: T = self._llist[index]
        while index > 0 and self._comp(self._llist[parent], bottom):
            self._llist[index] = self._llist[parent]
            index = parent
            parent = (parent - 1) // 2

        self._llist[index] = bottom

    def __trickle_down(self, index: int) -> None:
        large_child: int = 0
        top: T = self._llist[index]
        while index < self._length // 2:
            left_child: int = 2 * index + 1
            right_child: int = left_child + 1
            if (right_child < self._length and
                    self._comp(self._llist[large_child], self._llist[right_child])):
                large_child = right_child
            else:
                large_child = left_child

            if not self._comp(top, self._llist[large_child]):
                break

            # Потомок сдвигается вверх
            self._llist[index] = self._llist[large_child]
            index = large_child

        self._llist[index] = top  # index <- корень

    def change(self, index: int, new_value: T) -> None:
        old_value: T = self._llist[index]
        self._llist[index] = new_value
        if self._comp(old_value, new_value):
            self.__trickle_up(index)
        else:
            self.__trickle_down(index)

    def append(self, value: T) -> None:
        self._llist.push_tail(value)
        self.__trickle_up(self._length)
        self._length += 1

    def print_heap(self) -> None:
        print("heapArray: ")
        for it in range(0, self._length):
            if self._llist[it] is not None:
                print(f"{self._llist[it].key()} ", end='')
            else:
                print("-- ", end='')

        print("")

        n_blanks, items_per_row, column, j = (32, 1, 0, 0)
        dots: str = 32 * "."
        print(dots * 2)
        while self._length > 0:
            if column == 0:
                for it in range(0, n_blanks):
                    print(" ", end='')

            print(f"{self._llist[j].key()} ", end='')
            j += 1
            if j >= self._length:
                break

            column += 1
            if column == items_per_row:
                # Конец строки
                n_blanks //= 2  # Половина пробелов
                items_per_row *= 2  # Вдвое больше элементов
                column = 0  # Начать заново
                print("")  # Переход на новую строку
            else:
                for it in range(0, n_blanks * 2 - 2):
                    print(" ", end='')
        print("\n" + dots * 2)

    def find(self, value: T) -> int:
        for i in range(self._length):
            if self._llist[i].key() == value:
                return i
        return False

    def __contains__(self, item):
        if self.find(item) != False:
            return True
        else:
            return False


if __name__ == '__main__':
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

    with open("data.pickle", "wb") as f:
        pickle.dump(Heap, f)

    with open("data.pickle", "rb") as f:
        data_new = pickle.load(f)

    heap = data_new()
    heap = heap.create_heap_from_list(students)
    heap.print_heap()
