import sys

class SplayTree:
    """
    A self-contained Splay Tree class that implements a dictionary-like set for integers.

    This implementation includes insert, delete, and search operations. The key
    feature of a splay tree is that any accessed node is moved to the root of
    the tree through a series of rotations, which provides good amortized
    performance.

    Methods:
    - insert(key): Adds a key to the tree.
    - delete(key): Removes a key from the tree.
    - search(key): Returns True if the key is in the tree, False otherwise.
                   Performs the splaying operation on the accessed node
                   or its parent.
    """

    class _Node:
        """A private node class for the Splay Tree."""
        def __init__(self, key):
            self.key = key
            self.parent = None
            self.left = None
            self.right = None

    def __init__(self):
        """Initializes an empty Splay Tree."""
        self.root = None

    def _left_rotate(self, x):
        """Performs a left rotation on node x."""
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

    def _right_rotate(self, x):
        """Performs a right rotation on node x."""
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

    def _splay(self, x):
        """
        Performs the splay operation on node x, moving it to the root.
        """
        while x.parent:
            p = x.parent
            g = p.parent
            if not g:  # Zig case
                if x == p.left:
                    self._right_rotate(p)
                else:
                    self._left_rotate(p)
            elif x == p.left and p == g.left:  # Zig-Zig case
                self._right_rotate(g)
                self._right_rotate(p)
            elif x == p.right and p == g.right:  # Zig-Zig case
                self._left_rotate(g)
                self._left_rotate(p)
            elif x == p.right and p == g.left:  # Zig-Zag case
                self._left_rotate(p)
                self._right_rotate(g)
            else:  # Zig-Zag case (x == p.left and p == g.right)
                self._right_rotate(p)
                self._left_rotate(g)

    def search(self, key):
        """
        Searches for a key in the tree.

        If the key is found, the corresponding node is splayed to the root and
        True is returned. If the key is not found, the last accessed node (the
        would-be parent) is splayed to the root and False is returned.

        Args:
            key (int): The integer key to search for.

        Returns:
            bool: True if the key is found, False otherwise.
        """
        node = self.root
        last_node = None
        while node:
            last_node = node
            if key < node.key:
                node = node.left
            elif key > node.key:
                node = node.right
            else:
                self._splay(node)
                return True
        
        # Key not found, splay the last visited node if it exists
        if last_node:
            self._splay(last_node)
        return False

    def insert(self, key):
        """
        Inserts a key into the tree.

        If the key already exists, the existing node is splayed to the root.
        If the key is new, it is inserted and then the new node is splayed
        to the root.

        Args:
            key (int): The integer key to insert.
        """
        node = self.root
        parent = None
        while node:
            parent = node
            if key < node.key:
                node = node.left
            elif key > node.key:
                node = node.right
            else:
                # Key already exists, splay the node and return
                self._splay(node)
                return

        # Insert the new node
        new_node = self._Node(key)
        new_node.parent = parent
        
        if not parent:
            self.root = new_node
        elif key < parent.key:
            parent.left = new_node
        else:
            parent.right = new_node
        
        # Splay the new node to the root
        self._splay(new_node)

    def delete(self, key):
        """
        Deletes a key from the tree.

        The node with the given key is first splayed to the root. Then it is
        removed, and the remaining left and right subtrees are joined.

        Args:
            key (int): The integer key to delete.
        """
        # Splay the node to the root. If not found, splay its would-be parent.
        if not self.search(key):
            # Key was not in the tree, nothing to delete.
            # search() already splayed the appropriate node.
            return

        # After search, the node to delete is at the root
        left_subtree = self.root.left
        right_subtree = self.root.right

        if not left_subtree:
            # No left child, the right subtree becomes the new tree
            self.root = right_subtree
            if self.root:
                self.root.parent = None
        elif not right_subtree:
            # No right child, the left subtree becomes the new tree
            self.root = left_subtree
            if self.root:
                self.root.parent = None
        else:
            # Both subtrees exist. Join them.
            # Detach the left subtree from the old root
            left_subtree.parent = None
            
            # Find the maximum node in the left subtree
            max_node = left_subtree
            while max_node.right:
                max_node = max_node.right
            
            # Splay this max node to the root of the left subtree.
            # We can do this by temporarily setting self.root to the
            # left subtree's root.
            self.root = left_subtree
            self._splay(max_node)
            
            # After splaying, max_node is the new root.
            # It has no right child (because it was the maximum).
            # Attach the original right subtree as its right child.
            self.root.right = right_subtree
            right_subtree.parent = self.root

    def inorder(self):
        """
        Returns a list of keys in the tree in ascending order.
        Useful for verification and debugging.
        """
        result = []
        self._inorder_recursive(self.root, result)
        return result

    def _inorder_recursive(self, node, result):
        if node:
            self._inorder_recursive(node.left, result)
            result.append(node.key)
            self._inorder_recursive(node.right, result)

if __name__ == '__main__':
    # Example Usage
    st = SplayTree()

    print("Inserting keys: 10, 20, 30, 40, 50, 25")
    keys_to_insert = [10, 20, 30, 40, 50, 25]
    for key in keys_to_insert:
        st.insert(key)
        print(f"After inserting {key}, root is: {st.root.key}, inorder: {st.inorder()}")

    print("\n--- Searching ---")
    print("Searching for 20...")
    found = st.search(20)
    print(f"Found 20: {found}. Root is now: {st.root.key}, inorder: {st.inorder()}")

    print("\nSearching for 35 (not present)...")
    found = st.search(35)
    print(f"Found 35: {found}. Root is now: {st.root.key} (last accessed), inorder: {st.inorder()}")

    print("\n--- Deleting ---")
    print("Deleting 30...")
    st.delete(30)
    print(f"After deleting 30, root is: {st.root.key}, inorder: {st.inorder()}")

    print("\nDeleting 50...")
    st.delete(50)
    print(f"After deleting 50, root is: {st.root.key}, inorder: {st.inorder()}")
    
    print("\nDeleting 99 (not present)...")
    st.delete(99)
    print(f"After trying to delete 99, root is: {st.root.key}, inorder: {st.inorder()}")