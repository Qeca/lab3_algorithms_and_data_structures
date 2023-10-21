from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import TypeVar, Generic, Optional, Callable
from random import choice
import pickle
import sys
from io import StringIO


class IKey(ABC):

    @abstractmethod
    def key(self) -> float:
        ...


T = TypeVar("T", bound=IKey)


class Color(Enum):
    RED = 0
    BLACK = 1


@dataclass
class Node(Generic[T]):
    data: T
    parent: Optional['Node[T]'] = None
    left: Optional['Node[T]'] = None
    right: Optional['Node[T]'] = None
    color: Color = Color.RED

    def key(self) -> float:
        return self.data.key()

    def grandfather(self) -> Optional['Node[T]']:
        if self.parent is not None:
            return self.parent.parent
        return None

    def uncle(self) -> Optional['Node[T]']:
        if self.parent is None or self.parent.parent is None:
            return None
        return self.parent.brother()

    def brother(self) -> Optional['Node[T]']:
        if self.parent is None:
            return None
        if self == self.parent.left:
            return self.parent.right
        return self.parent.left


def _get_color(node: Optional['Node[T]']) -> Color:
    if node is None:
        return Color.BLACK
    return node.color


class KeyNotFoundException(Exception):
    pass


class EmptyTreeException(Exception):
    pass


class EmptyNodeException(Exception):
    pass


@dataclass
class Car(IKey):
    mark: str
    VIN: str
    capacity: float
    id: float
    avg_speed: float

    def key(self) -> float:
        return self.id

    def __str__(self) -> str:
        return f"Student({self.VIN}, {self.id})"


class RBTree(Generic[T]):

    def __init__(self) -> None:
        self._length: int = 0
        self._root: Optional[Node[T]] = None

    def is_empty(self) -> bool:
        return self._length == 0

    def __replace_node(self, a: Optional[Node[T]], b: Optional[Node[T]]) -> None:
        if a.parent is None:
            self._root = b
        else:
            if a == a.parent.left:
                a.parent.left = b
            else:
                a.parent.right = b

        if b is not None:
            b.parent = a.parent

    def __rotate_left(self, node: Node[T]) -> None:
        right = node.right
        self.__replace_node(node, right)
        node.right = right.left
        if right.left is not None:
            right.left.parent = node
        right.left = node
        node.parent = right

    def __rotate_right(self, node: Node[T]) -> None:
        left = node.left
        self.__replace_node(node, left)
        node.left = left.right
        if left.right is not None:
            left.right.parent = node
        left.right = node
        node.parent = left

    def insert(self, value: T) -> None:
        new_node: Node[T] = Node(data=value, color=Color.RED)
        if self._root is None:
            self._root = new_node
            new_node = self._root
        else:
            current_node = self._root
            while True:
                if new_node.key() == current_node.key():
                    current_node.data = value
                    return
                if new_node.key() < current_node.key():
                    if current_node.left is None:
                        current_node.left = new_node
                        new_node = current_node.left
                        break
                    else:
                        current_node = current_node.left
                if new_node.key() > current_node.key():
                    if current_node.right is None:
                        current_node.right = new_node
                        new_node = current_node.right
                        break
                    else:
                        current_node = current_node.right
            new_node.parent = current_node
        self.__insert_case1(new_node)
        self._length += 1

    def __insert_case1(self, node: Node[T]) -> None:
        if node.parent is None:
            node.color = Color.BLACK
        else:
            self.__insert_case2(node)

    def __insert_case2(self, node: Node[T]) -> None:
        if _get_color(node.parent) == Color.BLACK:
            return
        self.__insert_case3(node)

    def __insert_case3(self, node: Node[T]) -> None:
        uncle = node.uncle()
        if _get_color(uncle) == Color.RED:
            node.parent.color = Color.BLACK
            uncle.color = Color.BLACK
            node.grandfather().color = Color.RED
            self.__insert_case1(node.grandfather())
        else:
            self.__insert_case4(node)

    def __insert_case4(self, node: Node[T]) -> None:
        grandfather = node.grandfather()
        if (node == node.parent.right and
                node.parent == grandfather.left):
            self.__rotate_left(node.parent)
            node = node.left
        elif (node == node.parent.left and
              node.parent == grandfather.right):
            self.__rotate_right(node.parent)
            node = node.right
        self.__insert_case5(node)

    def __insert_case5(self, node: Node[T]) -> None:
        node.parent.color = Color.BLACK
        grandfather = node.grandfather()
        grandfather.color = Color.RED
        if (node == node.parent.left and
                node.parent == grandfather.left):
            self.__rotate_right(grandfather)
        elif (node == node.parent.right and
              node.parent == grandfather.right):
            self.__rotate_left(grandfather)

    def __find_node(self, key: float) -> tuple[Optional[Node[T]], bool]:
        current_node = self._root
        while current_node.key() != key:
            if key < current_node.key():
                current_node = current_node.left
            else:
                current_node = current_node.right
            if current_node is None:
                return None, False
        return current_node, True

    def __find_left_maximum_node(self, node: Node[T]) -> tuple[Optional[Node[T]], bool]:
        current_node = node.left
        if current_node is None:
            return None, False
        while current_node.right is not None:
            current_node = current_node.right
        return current_node, True

    def remove(self, key: float) -> None:
        if self.is_empty():
            raise EmptyTreeException("EmptyTreeException")

        child_node: Optional[Node[T]] = None
        removing_node, ok = self.__find_node(key)
        if not ok:
            raise KeyNotFoundException("KeyNotFoundException")

        if removing_node.left is not None and removing_node.right is not None:
            successor, ok = self.__find_left_maximum_node(removing_node)
            if not ok:
                raise EmptyNodeException("EmptyNodeException")

            removing_node.data = successor.data
            removing_node = successor

        if removing_node.left is None or removing_node.right is None:
            if removing_node.right is None:
                child_node = removing_node.left
            else:
                child_node = removing_node.right

            if removing_node.color == Color.BLACK:
                removing_node.color = _get_color(child_node)
                self.__remove_case1(removing_node)
            self.__replace_node(removing_node, child_node)

            if removing_node.parent is None and child_node is not None:
                child_node.color = Color.BLACK
        self._length -= 1

    def __remove_case1(self, node: Node[T]) -> None:
        if node.parent is None:
            return
        self.__remove_case2(node)

    def __remove_case2(self, node: Node[T]) -> None:
        brother = node.brother()
        if _get_color(brother) == Color.RED:
            node.parent.color = Color.RED
            brother.color = Color.BLACK
            if node == node.parent.left:
                self.__rotate_left(node.parent)
            else:
                self.__rotate_right(node.parent)
        self.__remove_case3(node)

    def __remove_case3(self, node: Node[T]) -> None:
        brother = node.brother()
        if (_get_color(node.parent) == Color.BLACK and
                _get_color(brother) == Color.BLACK and
                _get_color(brother.left) == Color.BLACK and
                _get_color(brother.right) == Color.BLACK):
            brother.color = Color.RED
            self.__remove_case1(node.parent)
        else:
            self.__remove_case4(node)

    def __remove_case4(self, node: Node[T]) -> None:
        brother = node.brother()
        if (_get_color(node.parent) == Color.RED and
                _get_color(brother) == Color.BLACK and
                _get_color(brother.left) == Color.BLACK and
                _get_color(brother.right) == Color.BLACK):
            brother.color = Color.RED
            node.parent.color = Color.BLACK
        else:
            self.__remove_case5(node)

    def __remove_case5(self, node: Node[T]) -> None:
        brother = node.brother()
        if (node == node.parent.left and
                _get_color(brother) == Color.BLACK and
                _get_color(brother.left) == Color.RED and
                _get_color(brother.right) == Color.BLACK):
            brother.color = Color.RED
            brother.left.color = Color.BLACK
            self.__rotate_right(brother)
        elif (node == node.parent.right and
              _get_color(brother) == Color.BLACK and
              _get_color(brother.left) == Color.BLACK and
              _get_color(brother.right) == Color.RED):
            brother.color = Color.RED
            brother.right.color = Color.BLACK
            self.__rotate_left(brother)
        self.__remove_case6(node)

    def __remove_case6(self, node: Node[T]) -> None:
        brother = node.brother()
        brother.color = _get_color(node.parent)
        node.parent.color = Color.BLACK
        if (node == node.parent.left and
                _get_color(brother.right) == Color.RED):
            brother.right.color = Color.BLACK
            self.__rotate_left(node.parent)
        elif _get_color(brother.left) == Color.RED:
            brother.left.color = Color.BLACK
            self.__rotate_right(node.parent)

    def find(self, key: float) -> tuple[Optional[T], bool]:
        if self.is_empty():
            raise EmptyTreeException("EmptyTreeException")

        current_node = self._root
        while current_node.key() != key:
            if key < current_node.key():
                current_node = current_node.left
            else:
                current_node = current_node.right
            if current_node is None:
                return None, False
        return current_node.data, True

    def __contains__(self, item):
        if self.is_empty():
            return False
        current_node = self._root
        while current_node.key() != item:
            if item < current_node.key():
                current_node = current_node.left
            else:
                current_node = current_node.right
            if current_node is None:
                return False
        return True

    # -------------------------------------------------

    def print_tree(self) -> None:
        result: list[str] = []
        if not self.is_empty():
            self.__create_str_tree(result, "", self._root, True)
        print("".join(result))

    def __create_str_tree(self, result: list[str], prefix: str,
                          node: Optional[Node[T]], is_tail: bool):
        if node.right is not None:
            new_prefix = prefix
            if is_tail:
                new_prefix += "│   "
            else:
                new_prefix += "    "
            self.__create_str_tree(result, new_prefix, node.right, False)

        result.append(prefix)
        if is_tail:
            result.append("└── ")
        else:
            result.append("┌── ")
        result.append(str(node.key()) + "\n")

        if node.left is not None:
            new_prefix = prefix
            if is_tail:
                new_prefix += "    "
            else:
                new_prefix += "│   "
            self.__create_str_tree(result, new_prefix, node.left, True)

    def is_balanced(self) -> bool:
        def check_balance(node: Optional[Node[T]]) -> int:
            if node is None:
                # Для NIL-узлов (черных узлов) считаем, что высота равна 1
                return 1

            # Рекурсивно проверяем высоту левого и правого поддеревьев
            left_height = check_balance(node.left)
            right_height = check_balance(node.right)

            # Проверяем, что узел соответствует свойствам красно-черного дерева
            if left_height != right_height or _get_color(node) == Color.RED:
                return 0  # Несбалансированное поддерево

            # Возвращаем высоту поддерева, увеличенную на 1 (включая текущий узел)
            return left_height + 1

        # Проверяем баланс от корня
        return check_balance(self._root) > 0


if __name__ == '__main__':
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

    with open("../lab3_algorithms_and_data_structures/data.pickle", "wb") as f:
        pickle.dump(RBTree, f)

    with open("../lab3_algorithms_and_data_structures/data.pickle", "rb") as f:
        data_new = pickle.load(f)
    tree_1 = data_new()
    for it in cars:
        tree_1.insert(it)
    tree_1.print_tree()
