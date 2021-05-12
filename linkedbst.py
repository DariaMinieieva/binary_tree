"""
File: linkedbst.py
Author: Ken Lambert
"""

from time import time
from random import choice, shuffle
from abstractcollection import AbstractCollection
from bstnode import BSTNode
from linkedstack import LinkedStack
from math import log, floor


class LinkedBST(AbstractCollection):
    """An link-based binary search tree implementation."""

    def __init__(self, sourceCollection=None):
        """Sets the initial state of self, which includes the
        contents of sourceCollection, if it's present."""
        self._root = None
        AbstractCollection.__init__(self, sourceCollection)

    # Accessor methods
    def __str__(self):
        """Returns a string representation with the tree rotated
        90 degrees counterclockwise."""

        def recurse(node, level):
            s_v = ""
            if node != None:
                s_v += recurse(node.right, level + 1)
                s_v += "| " * level
                s_v += str(node.data) + "\n"
                s_v += recurse(node.left, level + 1)
            return s_v

        return recurse(self._root, 0)

    def __iter__(self):
        """Supports a preorder traversal on a view of self."""
        if not self.isEmpty():
            stack = LinkedStack()
            stack.push(self._root)
            while not stack.isEmpty():
                node = stack.pop()
                yield node.data
                if node.right != None:
                    stack.push(node.right)
                if node.left != None:
                    stack.push(node.left)

    def preorder(self):
        """Supports a preorder traversal on a view of self."""
        return None

    def inorder(self):
        """Supports an inorder traversal on a view of self."""
        lyst = list()

        def recurse(node):
            if node != None:
                recurse(node.left)
                lyst.append(node.data)
                recurse(node.right)

        recurse(self._root)
        return iter(lyst)

    def postorder(self):
        """Supports a postorder traversal on a view of self."""
        return None

    def levelorder(self):
        """Supports a levelorder traversal on a view of self."""
        return None

    def __contains__(self, item):
        """Returns True if target is found or False otherwise."""
        return self.find(item) != None

    def find(self, item):
        """If item matches an item in self, returns the
        matched item, or None otherwise."""

        node = self._root

        while node:
            if node is None:
                return None
            elif item == node.data:
                return node.data
            elif item < node.data:
                node = node.left
            else:
                node = node.right

    # Mutator methods
    def clear(self):
        """Makes self become empty."""
        self._root = None
        self._size = 0

    def add(self, item):
        """Adds item to the tree."""

        # Tree is empty, so new item goes at the root
        if self.isEmpty():
            self._root = BSTNode(item)
        # Otherwise, search for the item's spot
        else:
            node = self._root

        # Helper function to search for item's position
            while node:
                # New item is less, go left until spot is found
                if item < node.data:
                    if node.left == None:
                        node.left = BSTNode(item)
                        node = None
                    else:
                        node = node.left
                # New item is greater or equal,
                # go right until spot is found
                elif node.right == None:
                    node.right = BSTNode(item)
                    node = None
                else:
                    node = node.right
                    # End of recurse

        self._size += 1

    def remove(self, item):
        """Precondition: item is in self.
        Raises: KeyError if item is not in self.
        postcondition: item is removed from self."""
        if not item in self:
            raise KeyError("Item not in tree.""")

        # Helper function to adjust placement of an item
        def lift_max_in_left_subtree_to_top(top):
            # Replace top's datum with the maximum datum in the left subtree
            # Pre:  top has a left child
            # Post: the maximum node in top's left subtree
            #       has been removed
            # Post: top.data = maximum value in top's left subtree
            parent = top
            current_node = top.left
            while not current_node.right == None:
                parent = current_node
                current_node = current_node.right
            top.data = current_node.data
            if parent == top:
                top.left = current_node.left
            else:
                parent.right = current_node.left

        # Begin main part of the method
        if self.isEmpty():
            return None

        # Attempt to locate the node containing the item
        item_removed = None
        pre_root = BSTNode(None)
        pre_root.left = self._root
        parent = pre_root
        direction = 'L'
        current_node = self._root
        while not current_node == None:
            if current_node.data == item:
                item_removed = current_node.data
                break
            parent = current_node
            if current_node.data > item:
                direction = 'L'
                current_node = current_node.left
            else:
                direction = 'R'
                current_node = current_node.right

        # Return None if the item is absent
        if item_removed == None:
            return None

        # The item is present, so remove its node

        # Case 1: The node has a left and a right child
        #         Replace the node's value with the maximum value in the
        #         left subtree
        #         Delete the maximium node in the left subtree
        if not current_node.left == None \
                and not current_node.right == None:
            lift_max_in_left_subtree_to_top(current_node)
        else:

            # Case 2: The node has no left child
            if current_node.left == None:
                new_child = current_node.right

                # Case 3: The node has no right child
            else:
                new_child = current_node.left

                # Case 2 & 3: Tie the parent to the new child
            if direction == 'L':
                parent.left = new_child
            else:
                parent.right = new_child

        # All cases: Reset the root (if it hasn't changed no harm done)
        #            Decrement the collection's size counter
        #            Return the item
        self._size -= 1
        if self.isEmpty():
            self._root = None
        else:
            self._root = pre_root.left
        return item_removed

    def replace(self, item, new_item):
        """
        If item is in self, replaces it with new_item and
        returns the old item, or returns None otherwise."""
        probe = self._root
        while probe != None:
            if probe.data == item:
                old_data = probe.data
                probe.data = new_item
                return old_data
            elif probe.data > item:
                probe = probe.left
            else:
                probe = probe.right
        return None

    def height(self):
        '''
        Return the height of tree
        :return: int
        '''

        def height1(top):
            '''
            Helper function
            :param top:
            :return:
            '''
            if top is None:
                return -1

            return 1 + max(height1(top.left), height1(top.right))

        return height1(self._root)

    def is_balanced(self):
        '''
        Return True if tree is balanced
        :return:
        '''
        comp = 2 * log(self._size + 1) - 1

        if comp > self.height():
            return True

        return False

    def range_find(self, low, high):
        '''
        Returns a list of the items in the tree, where low <= item <= high."""
        :param low:
        :param high:
        :return:
        '''
        next_item = self.successor(low)
        res = [low, next_item]

        while next_item < high:
            next_item = self.successor(next_item)
            res.append(next_item)

        return res

    def rebalance(self):
        '''
        Rebalances the tree.
        :return:
        '''
        elems = list(self.inorder())
        self.clear()

        def helper(lst):
            if lst:
                mid_ind = floor(len(lst)/2)

                mid_value = lst[mid_ind]
                half_1 = lst[:mid_ind]
                half_2 = lst[mid_ind+1:]

                self.add(mid_value)

                helper(half_1)
                helper(half_2)

        return helper(elems)

    def successor(self, item):
        """
        Returns the smallest item that is larger than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        current = self._root
        success = None

        while current:

            if current.data <= item:
                current = current.right
            elif current.data > item:
                success = current.data
                current = current.left

        return success

    def predecessor(self, item):
        """
        Returns the largest item that is smaller than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        current = self._root
        predecess = None

        while current:

            if current.data >= item:
                current = current.left
            else:
                predecess = current.data
                current = current.right

        return predecess

    def demo_bst(self, path):
        """
        Demonstration of efficiency binary search tree for the search tasks.
        :param path:
        :type path:
        :return:
        :rtype:
        """
        words = self.create_list(path)
        rand = self.make_random(words)

        # search in python list
        start = time()
        for i in rand:
            words.index(i)
        print(f"Python list efficiency: {time() - start}")

        for word in words:
            self.add(word)

        # search in binary tree which got sorted dictionary
        start = time()
        for i in rand:
            self.find(i)
        print(f"Sorted dictionary, binary tree efficiency: {time() - start}")

        # search in binary tree which got unsorted dictionary
        shuffle(words)

        self.clear()

        for word in words:
            self.add(word)

        start = time()
        for i in rand:
            self.find(i)
        print(f"Unsorted dictionary, binary tree efficiency: {time() - start}")

        # search in a balanced binary tree
        self.rebalance()

        start = time()
        for i in rand:
            self.find(i)
        print(f"Balanced binary tree efficiency: {time() - start}")

    def make_random(self, lst):
        res = []

        for _ in range(10000):
            res.append(choice(lst))

        return res

    def create_list(self, path):
        res = []
        with open(path, "r", encoding="utf-8") as input_file:
            for line in input_file:
                res.append(line.strip())

        return res


if __name__ == "__main__":
    bst = LinkedBST()
    bst.demo_bst("words.txt")
