# see https://medium.com/@steveYeah/using-generics-in-python-99010e5056eb
from typing import Generic, TypeVar
T = TypeVar("T")  # allows variable T to be used to represent a generic type

class Node(Generic[T]):
    def __init__(self, data: T):
        self.data: T      = data
        self.prev: Optional('Node') = None
        self.next: Optional('Node') = None  # eventually another Node

class LinkedList(Generic[T]):

    def __init__(self) -> None:
        self._head: Optional(Node[T]) = None   # the head pointer in the linked list
        self._tail: Optional(Node[T]) = None   # the tail pointer in the linked list
        self._num_entries: int = 0
    def __len__(self)-> int:
        return self._num_entries
    def add_left(self, item: T) -> None:
        ''' adds the given T-type data item as part of a new Node to the left
            of the linked list... remember to reset the head pointer, and, when
            appropriate, the tail pointer
        Parameters:
            item: a type T data item to be included as the data in the inserted Node
        Returns:
            nothing
        '''
        new_node = Node(item)
        if self._head is None:
            self._head = new_node
            self._tail = new_node
        else:
            new_node.next = self._head
            self._head.prev = new_node
            self._head = new_node
        self._num_entries +=1 

    def add_right(self, item: T) -> None:
        ''' adds the given T-type data item as part of a new Node to the right 
            of the linked list... remember to reset the tail pointer, and, when
            appropriate, the head pointer
        Parameters:
            item: a type T data item to be included as the data in the inserted Node
        Returns:
            nothing
        '''
        new_node = Node(item)
        if self._tail is None:
            self._head = new_node
            self._tail = new_node
        else:
            self._tail.next = new_node
            g = self._tail
            self._tail = new_node
            self._tail.prev = g
        self._num_entries +=1
        
    def remove_left(self) -> T:
        ''' removes the first Node in the linked list, returning the data item
            inside that Node...  Remember to handle the special case of an 
            empty list (what should the head and tail pointers be in that case?)
            and remember to update the head & tail pointer(s) when appropriate.
        Returns:
            a T type data item extracted from the removed Node
        '''
        new_node = self._head
        if new_node is None:
            print("Empty List, can't remove")
        elif self._num_entries == 1:
            self._head = None
            self._tail = None
            self._num_entries -= 1
        else:
            self._head = new_node.next
            self._head.prev = None
            self._num_entries -=1
        return new_node.data

    def remove_right(self) -> T:
        ''' removes the last Node in the linked list, returning the data item
            inside that Node...  Remember to handle the special case of an 
            empty list (what should the head and tail pointers be in that case?)

            Note: This one is trickier because you always have to walk (almost)
            all the way through the list in order to know what the new tail
            should be.

            Remember to update the head & tail pointer(s) when appropriate.

        Returns:
            a T type data item extracted from the removed Node
        '''
        old_node = self._tail
        g = self._head.next
        data_list = [g]
        while g != old_node:
            data_list.append(g)
            if g == old_node:
                break
            if g != None:
                g = g.next
        new_node = data_list[-1]
        new_node.next = None
        self._tail = new_node
        if new_node is None:
            print("List is empty can't remove")
        self._num_entries -=1
        return old_node.data
    def __str__(self):
        ''' returns a str representation of the linked list data
        Returns:
            an str representation of the linked list, showing head pointer
                and data tiems
        '''
        str_ = "head->"

        # start out at the head Node, and walk through Node by Node until we
        # reach the end of the linked list (i.e., the ._next entry is None)
        ptr_ = self._head
        while ptr_ is not None:
            str_ += "[" + str(ptr_.data) + "]->" 
            ptr_ = ptr_.next  # move ptr_ to the next Node in the linked list

        if self._head != None: str_ = str_[:-2]
        str_ += "<-tail"
        return str_
        
if __name__ == "__main__":
    ll = LinkedList()
    print(ll)
    ll.add_left(7)
    ll.add_left(8)
    ll.add_left(7)
    ll.add_right(6)
    ll.add_right(1)
    ll.add_right(6)
    ll.add_left(4)
    ll.add_right(5)
    print(ll)

    print(f"Removing from right: {ll.remove_right()}")
    
    print(ll)

    for i in range(3):
        print(f"Removing from left: {ll.remove_left()}")
        print(ll)
