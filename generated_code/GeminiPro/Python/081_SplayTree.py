import sys

# It is recommended to increase recursion limit for deep trees,
# although the splaying operation keeps the tree relatively balanced.
# sys.setrecursionlimit(2000)

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
        def __init__(self, key, parent=None):
            self.key = key
            self.parent = parent
            self.left = None
            self.right = None

    def __init__(self):
        """Initializes an empty Splay Tree."""
        self.root = None

    def _left_rotate(self, x):
        """Performs a left rotation on node x."""
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
        """Performs a right rotation on node x."""
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

    def _splay(self, node):
        """
        Splays the given node to the root of the tree.
        This operation moves the node to the root through a series of rotations.
        """
        while node.parent:
            parent = node.parent
            grandparent = parent.parent
            if not grandparent:
                # Zig case
                if node == parent.left:
                    self._right_rotate(parent)
                else:
                    self._left_rotate(parent)
            elif node == parent.left and parent == grandparent.left:
                # Zig-Zig case (left-left)
                self._right_rotate(grandparent)
                self._right_rotate(parent)
            elif node == parent.right and parent == grandparent.right:
                # Zig-Zig case (right-right)
                self._left_rotate(grandparent)
                self._left_rotate(parent)
            elif node == parent.right and parent == grandparent.left:
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

        If the key is found, the node containing the key is splayed to the root.
        If the key is not found, the last accessed node (the parent of the
        hypothetical key) is splayed to the root.

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

    def insert(self, key):
        """
        Inserts a key into the tree.

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
                # Key already exists, splay it and we are done
                self._splay(current)
                return
            elif key < current.key:
                current = current.left
            else:
                current = current.right

        new_node = self._Node(key, parent)
        if key < parent.key:
            parent.left = new_node
        else:
            parent.right = new_node
        
        self._splay(new_node)

    def delete(self, key):
        """
        Deletes a key from the tree.

        The node to be deleted (or its parent if not found) is first splayed
        to the root. If the key is found at the root, it is removed, and the
        two resulting subtrees are merged.

        Args:
            key: The integer key to delete.
        """
        if not self.root:
            return

        # Splay the node (or its would-be parent) to the root
        self.search(key)

        # If the key is not at the root after splaying, it doesn't exist
        if self.root.key != key:
            return

        # Now the node to delete is the root
        left_subtree = self.root.left
        right_subtree = self.root.right

        if not left_subtree:
            # No left child, the right subtree becomes the new tree
            self.root = right_subtree
            if right_subtree:
                right_subtree.parent = None
        else:
            # Disconnect left subtree from the old root
            left_subtree.parent = None
            
            # Find the maximum element in the left subtree
            max_node = left_subtree
            while max_node.right:
                max_node = max_node.right
            
            # Splay this maximum element to the root of the left subtree
            # After this splay, the new root of the left subtree has no right child
            self._splay(max_node)
            
            # Attach the original right subtree as the right child of the new root
            max_node.right = right_subtree
            if right_subtree:
                right_subtree.parent = max_node
            
            self.root = max_node

    def get_inorder_keys(self):
        """Helper method to get keys in-order for testing/visualization."""
        if not self.root:
            return []
        keys = []
        def _inorder_traverse(node):
            if node:
                _inorder_traverse(node.left)
                keys.append(node.key)
                _inorder_traverse(node.right)
        _inorder_traverse(self.root)
        return keys

# Example Usage (optional, for demonstration)
if __name__ == '__main__':
    st = SplayTree()
    
    # Insert elements
    keys_to_insert = [10, 20, 30, 40, 50, 25]
    print(f"Inserting keys: {keys_to_insert}")
    for k in keys_to_insert:
        st.insert(k)
        print(f"After inserting {k}, root is: {st.root.key}")
        print(f"  In-order traversal: {st.get_inorder_keys()}")
    
    print("\n" + "="*30 + "\n")
    
    # Search for an element
    key_to_search = 30
    print(f"Searching for {key_to_search}...")
    found = st.search(key_to_search)
    print(f"Found {key_to_search}: {found}")
    if st.root:
        print(f"After searching for {key_to_search}, root is: {st.root.key}")
    
    print("\n" + "="*30 + "\n")

    # Search for another element
    key_to_search = 10
    print(f"Searching for {key_to_search}...")
    found = st.search(key_to_search)
    print(f"Found {key_to_search}: {found}")
    if st.root:
        print(f"After searching for {key_to_search}, root is: {st.root.key}")

    print("\n" + "="*30 + "\n")

    # Search for a non-existent element
    key_to_search = 99
    print(f"Searching for non-existent key {key_to_search}...")
    found = st.search(key_to_search)
    print(f"Found {key_to_search}: {found}")
    if st.root:
        print(f"After searching for {key_to_search}, root is: {st.root.key} (last accessed node)")

    print("\n" + "="*30 + "\n")

    # Delete an element
    key_to_delete = 30
    print(f"Deleting {key_to_delete}...")
    st.delete(key_to_delete)
    if st.root:
        print(f"After deleting {key_to_delete}, root is: {st.root.key}")
        print(f"  In-order traversal: {st.get_inorder_keys()}")
    
    print("\n" + "="*30 + "\n")

    # Delete another element
    key_to_delete = 50
    print(f"Deleting {key_to_delete}...")
    st.delete(key_to_delete)
    if st.root:
        print(f"After deleting {key_to_delete}, root is: {st.root.key}")
        print(f"  In-order traversal: {st.get_inorder_keys()}")