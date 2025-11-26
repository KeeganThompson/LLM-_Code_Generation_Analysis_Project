import sys

class SplayTree:
    """
    A self-contained Python class that implements a Splay Tree.
    This tree acts as a dictionary-like set for storing unique integer keys.
    """

    class _Node:
        """
        A node in the Splay Tree.
        """
        def __init__(self, key):
            self.key = key
            self.parent = None
            self.left = None
            self.right = None

    def __init__(self):
        """
        Initializes an empty Splay Tree.
        """
        self.root = None

    def _left_rotate(self, x):
        """
        Performs a left rotation on node x.
        """
        y = x.right
        if y:
            x.right = y.left
            if y.left:
                y.left.parent = x
            y.parent = x.parent
        
        if not x.parent:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        
        if y:
            y.left = x
        x.parent = y

    def _right_rotate(self, x):
        """
        Performs a right rotation on node x.
        """
        y = x.left
        if y:
            x.left = y.right
            if y.right:
                y.right.parent = x
            y.parent = x.parent

        if not x.parent:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
            
        if y:
            y.right = x
        x.parent = y

    def _splay(self, x):
        """
        Performs the splaying operation on node x, moving it to the root.
        """
        while x.parent:
            parent = x.parent
            grandparent = parent.parent
            if not grandparent:
                # Zig case
                if x == parent.left:
                    self._right_rotate(parent)
                else:
                    self._left_rotate(parent)
            elif x == parent.left and parent == grandparent.left:
                # Zig-Zig case (left-left)
                self._right_rotate(grandparent)
                self._right_rotate(parent)
            elif x == parent.right and parent == grandparent.right:
                # Zig-Zig case (right-right)
                self._left_rotate(grandparent)
                self._left_rotate(parent)
            elif x == parent.right and parent == grandparent.left:
                # Zig-Zag case (left-right)
                self._left_rotate(parent)
                self._right_rotate(grandparent)
            else:
                # Zig-Zag case (right-left)
                self._right_rotate(parent)
                self._left_rotate(grandparent)

    def search(self, key):
        """
        Searches for a key in the tree.
        
        If the key is found, the corresponding node is splayed to the root and
        True is returned.
        
        If the key is not found, the last accessed node (the parent of where
        the key would be) is splayed to the root and False is returned.
        
        Args:
            key: The integer key to search for.
            
        Returns:
            True if the key is found, False otherwise.
        """
        if not self.root:
            return False

        last_node = None
        current = self.root
        while current:
            last_node = current
            if key == current.key:
                self._splay(current)
                return True
            elif key < current.key:
                current = current.left
            else:
                current = current.right
        
        # Key not found, splay the last visited node if it exists
        if last_node:
            self._splay(last_node)
        return False

    def insert(self, key):
        """
        Inserts a key into the tree.
        
        If the key already exists, the existing node is splayed to the root.
        If the key is new, it is inserted and the new node is splayed to the root.
        
        Args:
            key: The integer key to insert.
        """
        # Find the parent for the new node, similar to BST insertion
        parent = None
        current = self.root
        while current:
            parent = current
            if key < current.key:
                current = current.left
            elif key > current.key:
                current = current.right
            else:
                # Key already exists, splay the node and return
                self._splay(current)
                return

        # Create and link the new node
        new_node = self._Node(key)
        new_node.parent = parent
        
        if not parent:
            self.root = new_node
        elif new_node.key < parent.key:
            parent.left = new_node
        else:
            parent.right = new_node
            
        # Splay the newly inserted node to the root
        self._splay(new_node)

    def delete(self, key):
        """
        Deletes a key from the tree.
        
        The tree is first searched for the key, which brings the node (or its
        closest neighbor) to the root. If the key is found at the root, it is
        deleted and the remaining subtrees are joined.
        
        Args:
            key: The integer key to delete.
        """
        if not self.root:
            return

        # Search for the key. This will splay the node or its parent to the root.
        self.search(key)

        # If the key is not at the root after searching, it was not in the tree.
        if self.root.key != key:
            return

        # The node to delete is now at the root.
        left_subtree = self.root.left
        right_subtree = self.root.right

        if not left_subtree:
            # If there's no left subtree, the right subtree becomes the new tree.
            self.root = right_subtree
            if self.root:
                self.root.parent = None
        else:
            # If there is a left subtree, we need to join it with the right one.
            # 1. Disconnect the left subtree.
            left_subtree.parent = None
            
            # 2. Find the maximum element in the left subtree.
            max_in_left = left_subtree
            while max_in_left.right:
                max_in_left = max_in_left.right
            
            # 3. Splay this maximum element to the root of the left subtree.
            #    After this, it will have no right child.
            #    We temporarily treat the left subtree as the main tree for splaying.
            self.root = left_subtree
            self._splay(max_in_left)
            
            # 4. Attach the original right subtree as the right child of the new root.
            self.root.right = right_subtree
            if right_subtree:
                right_subtree.parent = self.root