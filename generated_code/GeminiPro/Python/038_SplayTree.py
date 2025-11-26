import sys

class SplayTree:
    """
    A self-contained Splay Tree class that implements a dictionary-like set for integers.
    
    This implementation includes insert, delete, and search operations. The key
    feature of a splay tree is that after any operation (insert, delete, search),
    the accessed node (or its parent/successor) is moved to the root of the tree
    through a series of rotations. This "splaying" operation makes recently
    accessed elements faster to access again.
    """

    class _Node:
        """A node in the splay tree."""
        def __init__(self, key, parent=None, left=None, right=None):
            self.key = key
            self.parent = parent
            self.left = left
            self.right = right

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
            else:  # Zig-Zag case
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
        if not self.root:
            return False

        current = self.root
        last_visited = None
        while current:
            last_visited = current
            if key < current.key:
                current = current.left
            elif key > current.key:
                current = current.right
            else:
                # Key found, splay the node
                self._splay(current)
                return True
        
        # Key not found, splay the last visited node (parent)
        if last_visited:
            self._splay(last_visited)
        return False

    def insert(self, key):
        """
        Inserts a key into the tree.
        
        If the key is not already in the tree, it is inserted and the new node
        is splayed to the root. If the key already exists, the existing node
        is splayed to the root.

        Args:
            key (int): The integer key to insert.
        """
        # Case 1: Tree is empty
        if not self.root:
            self.root = self._Node(key)
            return

        # Case 2: Tree is not empty, find insertion point
        current = self.root
        parent = None
        while current:
            parent = current
            if key < current.key:
                current = current.left
            elif key > current.key:
                current = current.right
            else:
                # Key already exists, splay it and return
                self._splay(current)
                return
        
        # Key does not exist, insert new node
        new_node = self._Node(key, parent=parent)
        if key < parent.key:
            parent.left = new_node
        else:
            parent.right = new_node
        
        # Splay the new node to the root
        self._splay(new_node)

    def delete(self, key):
        """
        Deletes a key from the tree.
        
        If the key is found, it is deleted. The parent of the deleted node (or its
        in-order successor if it had two children) is splayed to the root. If the
        key is not found, the last accessed node during the search is splayed.

        Args:
            key (int): The integer key to delete.
        """
        if not self.root:
            return

        # Splay the node with the key (or its parent if not found) to the root
        self.search(key)
        
        # If the key is not at the root after splaying, it wasn't in the tree
        if self.root.key != key:
            return

        # Now the node to delete is at the root.
        # Split the tree into two: L (left subtree) and R (right subtree)
        left_subtree = self.root.left
        right_subtree = self.root.right

        if not left_subtree:
            # If no left subtree, the right subtree becomes the new tree
            self.root = right_subtree
            if self.root:
                self.root.parent = None
        elif not right_subtree:
            # If no right subtree, the left subtree becomes the new tree
            self.root = left_subtree
            if self.root:
                self.root.parent = None
        else:
            # Both subtrees exist. Join them.
            # 1. Make the left subtree the current tree.
            self.root = left_subtree
            self.root.parent = None
            
            # 2. Find the maximum element in the left subtree.
            max_node = self.root
            while max_node.right:
                max_node = max_node.right
            
            # 3. Splay this max element. It becomes the new root of the merged tree
            #    and will have no right child.
            self._splay(max_node)
            
            # 4. Attach the original right subtree as the right child of the new root.
            self.root.right = right_subtree
            right_subtree.parent = self.root

    def inorder_traversal(self):
        """Helper method to return keys in-order for verification."""
        result = []
        self._inorder_recursive(self.root, result)
        return result

    def _inorder_recursive(self, node, result):
        if node:
            self._inorder_recursive(node.left, result)
            result.append(node.key)
            self._inorder_recursive(node.right, result)

    def __str__(self):
        """String representation of the tree (in-order)."""
        return str(self.inorder_traversal())

if __name__ == '__main__':
    # Example Usage
    st = SplayTree()
    
    # Insert operations
    print("--- Inserting keys ---")
    keys_to_insert = [10, 20, 30, 40, 50, 25]
    for k in keys_to_insert:
        st.insert(k)
        print(f"Inserted {k}. Root is now: {st.root.key}. Tree: {st}")

    # Search operations
    print("\n--- Searching for keys ---")
    print(f"Search for 25: {st.search(25)}")
    print(f"Root after searching 25: {st.root.key}. Tree: {st}")
    
    print(f"Search for 10: {st.search(10)}")
    print(f"Root after searching 10: {st.root.key}. Tree: {st}")
    
    print(f"Search for 99 (not present): {st.search(99)}")
    print(f"Root after searching 99: {st.root.key}. Tree: {st}") # Parent (50) is splayed

    # Delete operations
    print("\n--- Deleting keys ---")
    print(f"Deleting 30. Current tree: {st}")
    st.delete(30)
    print(f"Root after deleting 30: {st.root.key}. Tree: {st}") # 25 (successor) becomes root
    
    print(f"Deleting 50. Current tree: {st}")
    st.delete(50)
    print(f"Root after deleting 50: {st.root.key}. Tree: {st}") # 40 becomes root
    
    print(f"Deleting 99 (not present). Current tree: {st}")
    st.delete(99)
    print(f"Root after trying to delete 99: {st.root.key}. Tree: {st}") # No change