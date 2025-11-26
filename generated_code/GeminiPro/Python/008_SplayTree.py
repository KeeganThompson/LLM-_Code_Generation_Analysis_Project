import sys

# To prevent deep recursion errors on large trees
sys.setrecursionlimit(2000)

class SplayTree:
    """
    An implementation of a Splay Tree that acts as a dictionary-like set for integers.

    A splay tree is a self-adjusting binary search tree with the additional
    property that recently accessed elements are quick to access again.
    It performs basic operations such as insertion, look-up and removal
    in O(log n) amortized time.
    """

    class _Node:
        """A node in the Splay Tree."""
        def __init__(self, key):
            self.key = key
            self.parent = None
            self.left = None
            self.right = None

    def __init__(self):
        """Initializes an empty Splay Tree."""
        self.root = None

    def _left_rotate(self, x: _Node):
        """Performs a left rotation on the given node x."""
        y = x.right
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
        y.left = x
        x.parent = y

    def _right_rotate(self, x: _Node):
        """Performs a right rotation on the given node x."""
        y = x.left
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
        y.right = x
        x.parent = y

    def _splay(self, x: _Node):
        """
        Performs the splaying operation on node x, moving it to the root.
        """
        while x.parent:
            parent = x.parent
            grandparent = parent.parent
            if not grandparent:  # Zig case
                if x == parent.left:
                    self._right_rotate(parent)
                else:
                    self._left_rotate(parent)
            elif x == parent.left and parent == grandparent.left:  # Zig-Zig case (left-left)
                self._right_rotate(grandparent)
                self._right_rotate(parent)
            elif x == parent.right and parent == grandparent.right:  # Zig-Zig case (right-right)
                self._left_rotate(grandparent)
                self._left_rotate(parent)
            elif x == parent.right and parent == grandparent.left:  # Zig-Zag case (left-right)
                self._left_rotate(parent)
                self._right_rotate(grandparent)
            else:  # Zig-Zag case (right-left)
                self._right_rotate(parent)
                self._left_rotate(grandparent)

    def search(self, key: int) -> bool:
        """
        Searches for a key in the tree.

        If the key is found, the corresponding node is splayed to the root.
        If the key is not found, the last accessed node (the parent of the
        would-be key) is splayed to the root.

        Args:
            key: The integer key to search for.

        Returns:
            True if the key is found, False otherwise.
        """
        if not self.root:
            return False

        current = self.root
        last_visited = None
        while current:
            last_visited = current
            if key == current.key:
                self._splay(current)
                return True
            elif key < current.key:
                current = current.left
            else:
                current = current.right
        
        # If key not found, splay the last visited node
        if last_visited:
            self._splay(last_visited)
            
        return False

    def insert(self, key: int):
        """
        Inserts a key into the Splay Tree.

        If the key already exists, the existing node is splayed to the root.
        If the key is new, it is inserted and the new node is splayed to the root.

        Args:
            key: The integer key to insert.
        """
        if not self.root:
            self.root = self._Node(key)
            return

        current = self.root
        parent = None
        while current:
            parent = current
            if key == current.key:
                # Key already exists, splay it and return
                self._splay(current)
                return
            elif key < current.key:
                current = current.left
            else:
                current = current.right

        new_node = self._Node(key)
        new_node.parent = parent
        if key < parent.key:
            parent.left = new_node
        else:
            parent.right = new_node
        
        self._splay(new_node)

    def delete(self, key: int):
        """
        Deletes a key from the Splay Tree.

        The tree is re-structured after deletion to maintain the splay tree properties.
        Specifically, the parent of the deleted node is splayed to the root.

        Args:
            key: The integer key to delete.
        """
        # Search for the key, which will splay it (or a nearby node) to the root
        if not self.search(key):
            # Key not in tree, nothing to do
            return

        # After search(key), if the key was found, it's now the root
        # If self.root.key is not key, it means the key was not found.
        if self.root.key != key:
            return

        node_to_delete = self.root
        left_subtree = node_to_delete.left
        right_subtree = node_to_delete.right

        if not left_subtree:
            self.root = right_subtree
            if right_subtree:
                right_subtree.parent = None
        elif not right_subtree:
            self.root = left_subtree
            if left_subtree:
                left_subtree.parent = None
        else:
            # Disconnect left subtree from the node to be deleted
            left_subtree.parent = None
            
            # Find the maximum element in the left subtree
            max_node = left_subtree
            while max_node.right:
                max_node = max_node.right
            
            # Splay this maximum element to the top of the left subtree
            # This is a splay operation on a detached tree, so we temporarily
            # set self.root to the root of the left subtree.
            temp_root = self.root
            self.root = left_subtree
            self._splay(max_node) # Now self.root is max_node
            
            # Attach the original right subtree to the new root
            self.root.right = right_subtree
            right_subtree.parent = self.root
            
            # Restore the original root if it was changed for the splay
            # (although in this logic, self.root is correctly set now)

        # Clean up the deleted node's references to be safe
        del node_to_delete

    def __str__(self):
        """Returns an in-order traversal string representation of the tree."""
        if not self.root:
            return "[]"
        
        result = []
        def inorder_traverse(node):
            if node:
                inorder_traverse(node.left)
                result.append(str(node.key))
                inorder_traverse(node.right)
        
        inorder_traverse(self.root)
        return "[" + ", ".join(result) + "]"