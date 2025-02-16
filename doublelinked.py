class Node:
    def __init__(self, value):
        self.value = value
        self.next = None
        self.previous = None


class DoublyLinkedList:
    def __init__(self, cycle=False):
        self.head = None
        self.tail = None
        self.length = 0
        self.cycle = cycle

    def print_doublelinkedlist(self):
        current = self.head
        count = 0
        while current:
            if current.next != None:
                print(f"{current.value} <->", end=" ")
            elif current.next == None:
                print(f"{current.value}")
            current = current.next
            count += 1
            if self.cycle and count >= self.length:
                break
            
    def add_first(self, value):
        new_node = Node(value)
        if self.length == 0:
            self.head = new_node
            self.tail = new_node
            if self.cycle:
                self.head.previous = self.tail
                self.tail.next = self.head
        else:
            new_node.next = self.head
            self.head.previous = new_node
            self.head = new_node
            if self.cycle:
                self.tail.next = self.head
                self.head.previous = self.tail
        self.length += 1

    def add_last(self, value):
        new_node = Node(value)
        if self.length == 0:
            self.head = new_node
            self.tail = new_node
            if self.cycle:
                self.head.previous = self.tail
                self.tail.next = self.head
        else:
            self.tail.next = new_node
            new_node.previous = self.tail
            self.tail = new_node
            if self.cycle:
                self.tail.next = self.head
                self.head.previous = self.tail
        self.length += 1

    def insert(self, index, value):
        if index == 0:
            self.add_first(value)
            return
        if index >= self.length:
            self.add_last(value)
            return

        new_node = Node(value)
        current = self.head
        for _ in range(index - 1):
            current = current.next

        new_node.next = current.next
        new_node.previous = current
        current.next.previous = new_node
        current.next = new_node
        self.length += 1

    def remove_first(self):
        if self.length > 0:
            self.head = self.head.next
            if self.head:
                self.head.previous = None
            else:
                self.tail = None
            if self.cycle:
                self.tail.next = self.head
                self.head.previous = self.tail
            self.length -= 1

    def remove_last(self):
        if self.length > 1:
            self.tail = self.tail.previous
            self.tail.next = None
            if self.cycle:
                self.tail.next = self.head
                self.head.previous = self.tail
        elif self.length == 1:
            self.head = None
            self.tail = None
        self.length -= 1

    def remove(self, index):
        if index == 0:
            self.remove_first()
            return
        if index >= self.length - 1:
            self.remove_last()
            return

        current = self.head
        for _ in range(index):
            current = current.next

        current.previous.next = current.next
        current.next.previous = current.previous
        self.length -= 1


    def remove_value(self, value):
        current = self.head
        while current:
            if current.value == value:
                if current == self.head:
                    self.remove_first()
                elif current == self.tail:
                    self.remove_last()
                else:
                    current.previous.next = current.next
                    current.next.previous = current.previous
                    self.length -= 1
            current = current.next
            if self.cycle and current == self.head:
                break

    def reverse(self):
        current = self.head
        previous = None
        while current:
            next_node = current.next
            current.next = previous
            current.previous = next_node
            previous = current
            current = next_node
            if self.cycle and current == self.head:
                break
        self.head = self.tail
        self.tail = self.head

class DoublyLinkedListIterator:
    def __init__(self, linked_list):
        self.current = linked_list.head
        self.start = linked_list.head
        self.cycle = linked_list.cycle

    def __iter__(self):
        return self

    def __next__(self):
        if self.current is None or (not self.cycle and self.current == self.start and self.start is not None):
            raise StopIteration
        value = self.current.value
        self.current = self.current.next
        if self.cycle and self.current == self.start:
            raise StopIteration
        return value
