from datetime import datetime


class Node():
    def __init__(self, action_id, timestamp, username, action_type):
        self.action_id = action_id
        self.timestamp = timestamp
        self.username = username
        self.action_type = action_type
        self.prev = None
        self.next = None


    def __str__(self):
        return f"{self.action_id}, {self.timestamp}, {self.username}, {self.action_type}"


class History():
    def __init__(self):
        self.head = None
        self.tail = None
        self.current = self.tail
        self.actions_map = {}

    def add_action(self, username, action_type):
        action_id = len(self.actions_map)
        timestamp = datetime.now()
        new_node = Node(action_id, timestamp, username, action_type)
        self.actions_map[action_id] = new_node

        if self.current is None:
            self.head = self.tail = self.current = new_node

        else:
            new_node.prev = self.tail
            self.tail.next = new_node
            self.tail = new_node
            self.current = self.tail

    def undo(self):
        if self.current and self.current.prev:
            self.current = self.current.prev


    def redo(self):
        if self.current and self.current.next:
            self.current = self.current.next


    def find_action(self, action_id):
        return self.actions_map.get(action_id)

    def remove_action(self, action_id):
        new_node = self.find_action(action_id)
    
        if not new_node:
            return
       
        if new_node.prev:
            new_node.prev.next = new_node.next
        else:
            self.head = new_node.next
      
        if new_node.next:
            new_node.next.prev = new_node.prev

        else:
            self.tail = new_node.prev

        if self.current == new_node:
            if new_node.prev:
                self.current = new_node.prev
            elif new_node.next:
                self.current = new_node.next
            else:
                self.current = None

        del self.actions_map[action_id]

        current = self.head
        index = 0
        actions_map_copy = {}
        while current:
            current.action_id = index
            actions_map_copy[index] = current
            current = current.next
            index += 1

        self.actions_map = actions_map_copy
            
    def filter_and_remove(self, action_type):
        to_remove = []
        for new_node in self.actions_map.values():
            if new_node.action_type == action_type:
                to_remove.append(new_node)

        for new_node in to_remove:
            self.remove_action(new_node.action_id)

    def iter(self):
        current = self.head
        current_reached = False
        while current:
            if current_reached == False:
                color = "\033[92m"
            else:
                color = "\033[90m"

            if current == self.current:
                    current_reached = True
            yield f"{color}{current.action_id} {current.action_type} ({current.username})\033[0m"
            current = current.next
