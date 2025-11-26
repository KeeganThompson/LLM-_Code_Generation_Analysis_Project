import sys

class SplayTree:
    """
    Implements a Splay Tree, a self-balancing binary search tree.

    This class provides a dictionary-like set for storing unique integers.
    The key feature is the splaying operation, which moves a recently accessed
    element to the root of the tree, optimizing for future accesses of the
    same element. The tree does not store duplicate keys.
    """

    class _Node:
        """A private class representing a node in the Splay Tree."""
        def __init__(self, key):
            self.key = key
            self.left = None
            self.right = None

    def __init__(self):
        """Initializes an empty Splay Tree."""
        self.root = None

    def _splay(self, key):
        """
        Performs the splaying operation on the given key.

        This method rearranges the tree so that the node with the given key,
        or the node that would be its parent if the key is not present, is
        moved to the root of the tree. This is a top-down splaying implementation.
        """
        if not self.root:
            return

        # Use a dummy node to simplify linking of left and right subtrees
        header = self._Node(None)
        left_tree_max, right_tree_min = header, header
        current = self.root

        while True:
            if key < current.key:
                if not current.left:
                    break
                # Zig-Zig case (left-left): Rotate right
                if key < current.left.key:
                    y = current.left
                    current.left = y.right
                    y.right = current
                    current = y
                    if not current.left:
                        break
                # Link current node to the right tree of the new assembly
                right_tree_min.left = current
                right_tree_min = current
                current = current.left
            elif key > current.key:
                if not current.right:
                    break
                # Zig-Zig case (right-right): Rotate left
                if key > current.right.key:
                    y = current.right
                    current.right = y.left
                    y.left = current
                    current = y
                    if not current.right:
                        break
                # Link current node to the left tree of the new assembly
                left_tree_max.right = current
                left_tree_max = current
                current = current.right
            else:  # key is found
                break

        # Reassemble the tree
        left_tree_max.right = current.left
        right_tree_min.left = current.right
        current.left = header.right
        current.right = header.left
        self.root = current

    def search(self, key):
        """
        Searches for a key in the tree and performs the splaying operation.

        After this operation, if the key is found, the node containing it
        becomes the new root. If not found, the last accessed node (the
        would-be parent) becomes the new root.

        Args:
            key (int): The key to search for.

        Returns:
            bool: True if the key is found, False otherwise.
        """
        if not self.root:
            return False
        
        self._splay(key)
        
        return self.root.key == key

    def insert(self, key):
        """
        Inserts a key into the tree.

        If the key already exists, the node is splayed to the root.
        If the key does not exist, it is inserted and becomes the new root.

        Args:
            key (int): The key to insert.
        """
        if not self.root:
            self.root = self._Node(key)
            return

        # Splay the tree to bring the closest node to the root
        self._splay(key)

        # If key is already at the root, we're done
        if self.root.key == key:
            return

        # Otherwise, insert the new node at the root and split the tree
        new_node = self._Node(key)
        if key < self.root.key:
            new_node.right = self.root
            new_node.left = self.root.left
            self.root.left = None
        else:  # key > self.root.key
            new_node.left = self.root
            new_node.right = self.root.right
            self.root.right = None
        
        self.root = new_node

    def delete(self, key):
        """
        Deletes a key from the tree.

        If the key is found, it is deleted. The tree is rebalanced by
        joining the two resulting subtrees. If the key is not found,
        the tree is splayed based on the search for the key, but no
        node is removed.

        Args:
            key (int): The key to delete.
        """
        if not self.root:
            return

        # Splay the key to the root
        self._splay(key)

        # If key is not at the root, it's not in the tree, so do nothing
        if self.root.key != key:
            return

        # The node to delete is now the root.
        # We join its left and right subtrees.
        left_subtree = self.root.left
        right_subtree = self.root.right

        if not left_subtree:
            # If there's no left child, the right subtree becomes the new tree
            self.root = right_subtree
        else:
            # Make the left subtree the main tree
            self.root = left_subtree
            # Splay for the largest element in this new tree.
            # Since `key` is larger than any element in the left subtree,
            # splaying for it will bring the max element to the root.
            self._splay(key)
            # Attach the original right subtree
            self.root.right = right_subtree