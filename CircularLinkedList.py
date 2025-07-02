from Node import Node

class CircularLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.current = None

    def append(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = self.tail = new_node
            self.tail.next = self.head
        else:
            self.tail.next = new_node
            self.tail = new_node
            self.tail.next = self.head

    def reset(self):
        self.current = self.head

    def next(self):
        if not self.current:
            self.reset()
        data = self.current.data
        self.current = self.current.next
        return data

    def clear(self):
        self.head = self.tail = self.current = None

    def is_empty(self):
        return self.head is None