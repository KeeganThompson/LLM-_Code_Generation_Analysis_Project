import sys

class SplayTree:
    """
    A complete, self-contained Python class that implements a splay tree.

    This class provides a dictionary-like set for integers, supporting
    insert, delete, and search operations. Each operation is followed by
    a 'splaying' step, which moves the accessed node (or a related one)
    to the root of the tree. This restructuring heuristic helps to keep
    frequently accessed elements near the top, providing amortized
    O(log n) time complexity for all operations.
    """

    class _Node:
        """A private node class for the splay tree."""
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

    def _splay(self, p):
        """
        Performs the splaying operation on node p, moving it to the root.
        """
        while p.parent:
            parent = p.parent
            grandparent = parent.parent
            if not grandparent:
                # Zig case: parent is root
                if p == parent.left:
                    self._right_rotate(parent)
                else:
                    self._left_rotate(parent)
            else:
                if p == parent.left:
                    if parent == grandparent.left:
                        # Zig-Zig case (left-left)
                        self._right_rotate(grandparent)
                        self._right_rotate(parent)
                    else:
                        # Zig-Zag case (left-right)
                        self._right_rotate(parent)
                        self._left_rotate(grandparent)
                else: # p is right child
                    if parent == grandparent.right:
                        # Zig-Zig case (right-right)
                        self._left_rotate(grandparent)
                        self._left_rotate(parent)
                    else:
                        # Zig-Zag case (right-left)
                        self._left_rotate(parent)
                        self._right_rotate(grandparent)
        self.root = p

    def search(self, key):
        """
        Searches for a key in the tree and splays the accessed node.

        If the key is found, the corresponding node is splayed to the root
        and the method returns True. If the key is not found, the last
        accessed node (the parent of the would-be position) is splayed
        to the root, and the method returns False.

        Args:
            key: The integer key to search for.

        Returns:
            True if the key is found, False otherwise.
        """
        node = self.root
        last_node = None
        while node:
            last_node = node
            if key == node.key:
                self._splay(node)
                return True
            elif key < node.key:
                node = node.left
            else:
                node = node.right
        
        # Key not found, splay the last visited node if the tree is not empty
        if last_node:
            self._splay(last_node)
        return False

    def insert(self, key):
        """
        Inserts a key into the tree.

        If the key does not exist, it is inserted and the new node is
        splayed to the root. If the key already exists, the existing node
        is splayed to the root.

        Args:
            key: The integer key to insert.
        """
        if not self.root:
            self.root = self._Node(key)
            return

        node = self.root
        parent = None
        while node:
            parent = node
            if key == node.key:
                # Key already exists, splay it and return
                self._splay(node)
                return
            elif key < node.key:
                node = node.left
            else:
                node = node.right

        # Insert the new node
        new_node = self._Node(key)
        new_node.parent = parent
        if key < parent.key:
            parent.left = new_node
        else:
            parent.right = new_node
        
        # Splay the new node to the root
        self._splay(new_node)

    def delete(self, key):
        """
        Deletes a key from the tree.

        The tree is first searched for the key, which brings the node (or its
        parent if not found) to the root. If the key is at the root, it is
        deleted by splitting the tree into two subtrees (L and R) and then
        joining them. The join operation involves finding the maximum element
        in L, splaying it to the root of L, and then attaching R as its
        right child.

        Args:
            key: The integer key to delete.
        """
        if not self.root:
            return

        # Search for the key, which splays the node (or its parent) to the root.
        if not self.search(key):
            # Key was not found, search() already splayed the last accessed node.
            return

        # After search, if the key was found, it is now at the root.
        # We can proceed with the deletion.
        left_subtree = self.root.left
        right_subtree = self.root.right

        if not left_subtree:
            # No left subtree, the right subtree becomes the new tree.
            self.root = right_subtree
            if self.root:
                self.root.parent = None
            return

        # The left subtree exists.
        left_subtree.parent = None  # Disconnect left subtree from the old root.

        # Find the maximum node in the left subtree.
        max_node = left_subtree
        while max_node.right:
            max_node = max_node.right
        
        # Splay this max_node to be the root of the left subtree.
        # We can do this by temporarily setting self.root and calling _splay.
        # The _splay method will update self.root to be max_node.
        self.root = left_subtree
        self._splay(max_node)

        # The splayed max_node is now the new root. Attach the original right subtree.
        # Since it was the max element, its right child is guaranteed to be None.
        self.root.right = right_subtree
        if right_subtree:
            right_subtree.parent = self.root
    
    def get_inorder_keys(self):
        """
        Utility method to get a list of keys via inorder traversal.
        
        Returns:
            A sorted list of integers present in the tree.
        """
        result = []
        self._inorder_helper(self.root, result)
        return result

    def _inorder_helper(self, node, result):
        if node:
            self._inorder_helper(node.left, result)
            result.append(node.key)
            self._inorder_helper(node.right, result)

    def __str__(self):
        """String representation of the tree (inorder traversal)."""
        return str(self.get_inorder_keys())

# Example Usage:
if __name__ == '__main__':
    st = SplayTree()

    # Insert elements
    keys_to_insert = [10, 20, 30, 40, 50, 25]
    for key in keys_to_insert:
        st.insert(key)
        print(f"Inserted {key}. Root is now: {st.root.key}. Inorder: {st}")

    # Search for an element
    print("\nSearching for 30...")
    found = st.search(30)
    print(f"Found 30: {found}. Root is now: {st.root.key}. Inorder: {st}")
    
    # Search for a non-existent element
    print("\nSearching for 99 (not present)...")
    found = st.search(99)
    # The last accessed node (50) should be splayed to the root
    print(f"Found 99: {found}. Root is now: {st.root.key}. Inorder: {st}")

    # Delete an element
    print("\nDeleting 30...")
    st.delete(30)
    # Deletion involves a search (splaying 30), then a join (splaying 25).
    # The new root should be the max of the left subtree (25).
    print(f"Root after deleting 30 is: {st.root.key}. Inorder: {st}")

    # Delete another element
    print("\nDeleting 40...")
    st.delete(40)
    # Search splays 40, join splays 25 (max of left subtree of 40)
    print(f"Root after deleting 40 is: {st.root.key}. Inorder: {st}")

    # Delete root
    print(f"\nDeleting root ({st.root.key})...")
    st.delete(st.root.key)
    print(f"New root is: {st.root.key}. Inorder: {st}")