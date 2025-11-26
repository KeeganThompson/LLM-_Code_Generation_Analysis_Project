import sys

# It's good practice to increase recursion limit for deep trees, though splaying keeps the tree balanced.
sys.setrecursionlimit(2000)

class SplayTree:
    """
    An implementation of a Splay Tree.
    
    A splay tree is a self-adjusting binary search tree with the additional
    property that recently accessed elements are quick to access again.
    It performs basic operations such as insertion, look-up and removal
    in O(log n) amortized time.
    
    This class implements a dictionary-like set for storing unique integer keys.
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
        
        Performs the splaying operation on the accessed node if found.
        If the node is not found, its would-be parent is splayed to the root.
        
        Args:
            key: The integer key to search for.
            
        Returns:
            True if the key is found, False otherwise.
        """
        node = self.root
        last_node = None
        while node:
            last_node = node
            if key < node.key:
                node = node.left
            elif key > node.key:
                node = node.right
            else:  # Key found
                self._splay(node)
                return True
        
        # Key not found, splay the last visited node (parent of the would-be key)
        if last_node:
            self._splay(last_node)
        return False

    def insert(self, key):
        """
        Inserts a new key into the tree.
        
        If the key already exists, the existing node is splayed to the root.
        If the key is new, it is inserted and then splayed to the root.
        
        Args:
            key: The integer key to insert.
        """
        node = self.root
        parent = None
        while node:
            parent = node
            if key < node.key:
                node = node.left
            elif key > node.key:
                node = node.right
            else:  # Key already exists
                self._splay(node)
                return

        new_node = self._Node(key, parent)
        if not parent:
            self.root = new_node
        elif key < parent.key:
            parent.left = new_node
        else:
            parent.right = new_node
        
        self._splay(new_node)

    def delete(self, key):
        """
        Deletes a key from the tree.
        
        The tree is first searched for the key, which splays the found node
        (or its parent if not found) to the root. If the key is found,
        the node is removed and the tree is restructured.
        
        Args:
            key: The integer key to delete.
        """
        # Search for the key. This splays the node or its parent to the root.
        if not self.search(key):
            # Key not in tree. search() already splayed the parent, so we are done.
            return
        
        # At this point, the node to delete is the root because search() found it.
        z = self.root
        left_subtree = z.left
        right_subtree = z.right

        if not left_subtree:
            # Promote the right subtree to be the new tree
            self.root = right_subtree
            if right_subtree:
                right_subtree.parent = None
        else:
            # Detach the left subtree to operate on it
            left_subtree.parent = None
            
            # Find the maximum node in the left subtree
            max_node = left_subtree
            while max_node.right:
                max_node = max_node.right
            
            # Splay this max_node. It becomes the root of the tree formed by
            # the left subtree. We do this by temporarily setting the root.
            self.root = left_subtree
            self._splay(max_node)
            
            # Now, self.root is max_node. Re-attach the original right subtree.
            # max_node is guaranteed to have no right child at this point.
            self.root.right = right_subtree
            if right_subtree:
                right_subtree.parent = self.root

    def _inorder_traversal(self, node, nodes_list):
        """Helper for in-order traversal."""
        if node:
            self._inorder_traversal(node.left, nodes_list)
            nodes_list.append(node.key)
            self._inorder_traversal(node.right, nodes_list)

    def __str__(self):
        """Returns an in-order string representation of the tree's keys."""
        if not self.root:
            return "SplayTree()"
        nodes = []
        self._inorder_traversal(self.root, nodes)
        return f"SplayTree({', '.join(map(str, nodes))})"

    def __repr__(self):
        """Returns the string representation of the tree."""
        return str(self)

if __name__ == '__main__':
    # Example Usage
    st = SplayTree()

    # Insertions
    keys_to_insert = [10, 20, 30, 40, 50, 25]
    print(f"Inserting keys: {keys_to_insert}")
    for key in keys_to_insert:
        st.insert(key)
        print(f"After inserting {key}: root is {st.root.key}, tree is {st}")

    print("\n" + "="*30 + "\n")

    # Searches
    keys_to_search = [30, 15, 50]
    print(f"Searching for keys: {keys_to_search}")
    for key in keys_to_search:
        found = st.search(key)
        status = "found" if found else "not found"
        print(f"Searched for {key} ({status}): root is now {st.root.key}, tree is {st}")

    print("\n" + "="*30 + "\n")
    
    # Deletions
    keys_to_delete = [10, 40, 60]
    print(f"Deleting keys: {keys_to_delete}")
    for key in keys_to_delete:
        print(f"Attempting to delete {key}...")
        st.delete(key)
        if st.root:
            print(f"After deleting {key}: root is {st.root.key}, tree is {st}")
        else:
            print(f"After deleting {key}: tree is empty.")