class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class CircularLinkedList:
    def __init__(self):
        self.head = None

    def append(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            self.head.next = self.head  # Kreisförmige Verbindung
            return
        
        temp = self.head
        while temp.next != self.head:
            temp = temp.next
        temp.next = new_node
        new_node.next = self.head

    def print_list(self, count=10):  # Begrenzte Ausgabe zur Vermeidung einer Endlosschleife
        if not self.head:
            print("Liste ist leer")
            return
        
        temp = self.head
        printed = 0
        while printed < count:
            print(temp.data, end=" -> ")
            temp = temp.next
            printed += 1
        print("... (kreisläufig)")

# Beispielnutzung
cll = CircularLinkedList()
cll.append(1)
cll.append(2)
cll.append(3)
cll.print_list()
