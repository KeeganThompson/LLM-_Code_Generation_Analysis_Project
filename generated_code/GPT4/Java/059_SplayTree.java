public class SplayTree {
    private class Node {
        int key;
        Node left, right, parent;

        Node(int key) {
            this.key = key;
        }
    }

    private Node root;

    /**
     * Insert a key into the Splay Tree.
     */
    public void insert(int key) {
        if (root == null) {
            root = new Node(key);
            return;
        }
        Node curr = root;
        Node parent = null;
        while (curr != null) {
            parent = curr;
            if (key < curr.key)
                curr = curr.left;
            else if (key > curr.key)
                curr = curr.right;
            else {
                // Key already exists, splay and return
                splay(curr);
                return;
            }
        }
        Node newNode = new Node(key);
        newNode.parent = parent;
        if (key < parent.key)
            parent.left = newNode;
        else
            parent.right = newNode;
        splay(newNode);
    }

    /**
     * Delete a key from the Splay Tree.
     */
    public void delete(int key) {
        Node node = findNode(key);
        if (node == null) return; // Not found

        splay(node);

        if (node.left == null) {
            replace(node, node.right);
        } else if (node.right == null) {
            replace(node, node.left);
        } else {
            // Both children exist
            Node min = subtreeMin(node.right);
            if (min.parent != node) {
                replace(min, min.right);
                min.right = node.right;
                if (min.right != null)
                    min.right.parent = min;
            }
            replace(node, min);
            min.left = node.left;
            if (min.left != null)
                min.left.parent = min;
        }
        // Remove references
        node.left = node.right = node.parent = null;
    }

    /**
     * Search for a key in the Splay Tree, splaying the accessed node to the root.
     * Returns the key if found, null otherwise.
     */
    public Integer search(int key) {
        Node node = findNode(key);
        if (node != null) {
            splay(node);
            return node.key;
        }
        return null;
    }

    // Helper: Find node with given key (no splaying)
    private Node findNode(int key) {
        Node curr = root;
        while (curr != null) {
            if (key < curr.key)
                curr = curr.left;
            else if (key > curr.key)
                curr = curr.right;
            else
                return curr;
        }
        return null;
    }

    // Helper: Splay operation
    private void splay(Node x) {
        if (x == null) return;
        while (x.parent != null) {
            Node p = x.parent;
            Node g = p.parent;
            if (g == null) {
                // Zig
                if (x == p.left)
                    rotateRight(p);
                else
                    rotateLeft(p);
            } else if (x == p.left && p == g.left) {
                // Zig-zig
                rotateRight(g);
                rotateRight(p);
            } else if (x == p.right && p == g.right) {
                // Zig-zig
                rotateLeft(g);
                rotateLeft(p);
            } else if (x == p.right && p == g.left) {
                // Zig-zag
                rotateLeft(p);
                rotateRight(g);
            } else if (x == p.left && p == g.right) {
                // Zig-zag
                rotateRight(p);
                rotateLeft(g);
            }
        }
        root = x;
    }

    // Helper: Left rotation
    private void rotateLeft(Node x) {
        Node y = x.right;
        if (y == null) return;
        x.right = y.left;
        if (y.left != null)
            y.left.parent = x;
        y.parent = x.parent;
        if (x.parent == null)
            root = y;
        else if (x == x.parent.left)
            x.parent.left = y;
        else
            x.parent.right = y;
        y.left = x;
        x.parent = y;
    }

    // Helper: Right rotation
    private void rotateRight(Node x) {
        Node y = x.left;
        if (y == null) return;
        x.left = y.right;
        if (y.right != null)
            y.right.parent = x;
        y.parent = x.parent;
        if (x.parent == null)
            root = y;
        else if (x == x.parent.left)
            x.parent.left = y;
        else
            x.parent.right = y;
        y.right = x;
        x.parent = y;
    }

    // Helper: Replace subtree u with v in the tree
    private void replace(Node u, Node v) {
        if (u.parent == null)
            root = v;
        else if (u == u.parent.left)
            u.parent.left = v;
        else
            u.parent.right = v;
        if (v != null)
            v.parent = u.parent;
    }

    // Helper: Find minimum node in subtree
    private Node subtreeMin(Node node) {
        while (node != null && node.left != null)
            node = node.left;
        return node;
    }

    // Optional: For debugging, in-order traversal
    public void printInOrder() {
        printInOrder(root);
        System.out.println();
    }
    private void printInOrder(Node node) {
        if (node == null) return;
        printInOrder(node.left);
        System.out.print(node.key + " ");
        printInOrder(node.right);
    }

    // Example usage
    public static void main(String[] args) {
        SplayTree st = new SplayTree();
        st.insert(10);
        st.insert(20);
        st.insert(5);
        st.insert(15);
        st.printInOrder(); // 5 10 15 20

        System.out.println("Search 15: " + st.search(15)); // 15
        st.printInOrder();

        st.delete(10);
        st.printInOrder(); // 5 15 20

        System.out.println("Search 99: " + st.search(99)); // null
    }
}