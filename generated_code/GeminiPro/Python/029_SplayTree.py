import sys

class SplayTree:
    """
    A self-contained Python class implementing a Splay Tree.
    This tree acts as a dictionary-like set for storing unique integer keys.
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

    def _left_rotate(self, x):
        """Performs a left rotation on node x."""
        y = x.right
        x.right = y.left
        if y.left:
            y.left.parent = x
        
        y.parent = x.parent
        if x.parent is None:
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
        if x.parent is None:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
            
        y.right = x
        x.parent = y

    def _splay(self, node):
        """
        Performs the splaying operation on a node, moving it to the root.
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
        
        If the key is found, the corresponding node is splayed to the root.
        If the key is not found, the last accessed node (the would-be parent)
        is splayed to the root.

        Args:
            key: The integer key to search for.

        Returns:
            True if the key is found, False otherwise.
        """
        last_visited = None
        node = self.root
        while node:
            last_visited = node
            if key == node.key:
                self._splay(node)
                return True
            elif key < node.key:
                node = node.left
            else:
                node = node.right
        
        # If key not found, splay the last visited node
        if last_visited:
            self._splay(last_visited)
        
        return False

    def insert(self, key):
        """
        Inserts a key into the tree.
        
        If the key is not present, it is added and splayed to the root.
        If the key already exists, the existing node is splayed to the root.

        Args:
            key: The integer key to insert.
        """
        parent = None
        current = self.root
        
        # Find position for new node or existing node
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
        
        # Insert new node
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
        
        The tree is first splayed on the key. If the key exists, it is
        removed, and its two subtrees are joined.

        Args:
            key: The integer key to delete.
        """
        # Splay the node to the root (or its parent if not found)
        if not self.search(key):
            # Key was not in the tree, search already splayed the parent
            return

        # At this point, the node to delete is the root, because search(key)
        # returned True, splaying the node with the given key to the root.
        z = self.root
        left_subtree = z.left
        right_subtree = z.right

        if not left_subtree:
            # No left child, promote the right subtree
            self.root = right_subtree
            if right_subtree:
                right_subtree.parent = None
        else:
            # Disconnect the left subtree to operate on it
            left_subtree.parent = None
            
            # Find the maximum node in the left subtree
            max_in_left = left_subtree
            while max_in_left.right:
                max_in_left = max_in_left.right
            
            # Splay this maximum node to the root of the left subtree
            # We can do this by temporarily setting self.root and using _splay
            temp_root_holder = self.root
            self.root = left_subtree
            self._splay(max_in_left)
            # After splaying, self.root is now max_in_left
            
            # The new root is the splayed max node from the left subtree
            new_root = self.root
            self.root = temp_root_holder # Restore original root context (not strictly needed)

            # Join the right subtree to the new root
            new_root.right = right_subtree
            if right_subtree:
                right_subtree.parent = new_root
            
            self.root = new_root
            self.root.parent = None
    
    # Helper for visualization
    def _print_helper(self, node, prefix="", is_left=True):
        if not node:
            return
        if node.right:
            self._print_helper(node.right, prefix + ("│   " if is_left else "    "), False)
        print(prefix + ("└── " if is_left else "┌── ") + str(node.key))
        if node.left:
            self._print_helper(node.left, prefix + ("    " if is_left else "│   "), True)

    def print_tree(self):
        """Prints a visual representation of the tree."""
        if self.root:
            self._print_helper(self.root)
        else:
            print("Tree is empty.")


if __name__ == '__main__':
    # Example Usage
    splay_tree = SplayTree()

    print("Inserting 10, 20, 30, 40, 50, 5, 15...")
    keys_to_insert = [10, 20, 30, 40, 50, 5, 15]
    for key in keys_to_insert:
        splay_tree.insert(key)
        print(f"\nAfter inserting {key}, root is {splay_tree.root.key}:")
        splay_tree.print_tree()

    print("\n" + "="*40)
    print("Searching for key 15...")
    found = splay_tree.search(15)
    print(f"Key 15 found: {found}")
    print(f"Tree after searching for 15 (root is {splay_tree.root.key}):")
    splay_tree.print_tree()

    print("\n" + "="*40)
    print("Searching for key 99 (not in tree)...")
    found = splay_tree.search(99)
    print(f"Key 99 found: {found}")
    print(f"Tree after searching for 99 (root is {splay_tree.root.key}, the last visited node):")
    splay_tree.print_tree()

    print("\n" + "="*40)
    print("Deleting key 30...")
    splay_tree.delete(30)
    print(f"Tree after deleting 30 (root is {splay_tree.root.key}):")
    splay_tree.print_tree()
    
    print("\n" + "="*40)
    print("Deleting key 50...")
    splay_tree.delete(50)
    print(f"Tree after deleting 50 (root is {splay_tree.root.key}):")
    splay_tree.print_tree()

    print("\n" + "="*40)
    print("Deleting key 99 (not in tree)...")
    splay_tree.delete(99)
    print(f"Tree after attempting to delete 99 (root is {splay_tree.root.key}):")
    splay_tree.print_tree()