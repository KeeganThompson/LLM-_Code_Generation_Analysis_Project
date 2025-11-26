public class SplayTree {
    private class Node {
        int key;
        Node left, right, parent;

        Node(int key, Node parent) {
            this.key = key;
            this.parent = parent;
        }
    }

    private Node root;

    /**
     * Inserts the key into the splay tree.
     * Duplicate keys are ignored.
     */
    public void insert(int key) {
        if (root == null) {
            root = new Node(key, null);
            return;
        }
        Node curr = root, parent = null;
        while (curr != null) {
            parent = curr;
            if (key < curr.key)
                curr = curr.left;
            else if (key > curr.key)
                curr = curr.right;
            else
                return; // Duplicate, do nothing
        }
        Node newNode = new Node(key, parent);
        if (key < parent.key)
            parent.left = newNode;
        else
            parent.right = newNode;
        splay(newNode);
    }

    /**
     * Deletes the key from the splay tree.
     * If the key does not exist, nothing happens.
     */
    public void delete(int key) {
        Node node = findNode(key);
        if (node == null) return;
        splay(node);

        // Now node is root
        if (node.left == null) {
            replaceRoot(node.right);
        } else if (node.right == null) {
            replaceRoot(node.left);
        } else {
            // Both children exist
            Node maxLeft = subtreeMaximum(node.left);
            splay(maxLeft); // Splay the maximum in left subtree to root's left child
            // maxLeft is now root's left child, and has no right child
            maxLeft.right = node.right;
            if (node.right != null)
                node.right.parent = maxLeft;
            replaceRoot(maxLeft);
        }
        // Help GC
        node.left = node.right = node.parent = null;
    }

    /**
     * Searches for the key, splays it to the root if found.
     * Returns the key if found, else null.
     */
    public Integer search(int key) {
        Node node = findNode(key);
        if (node != null) {
            splay(node);
            return node.key;
        }
        return null;
    }

    // --- Helper methods ---

    // Splay the given node to the root
    private void splay(Node x) {
        if (x == null) return;
        while (x.parent != null) {
            Node p = x.parent;
            Node g = p.parent;
            if (g == null) {
                // Zig step
                if (x == p.left)
                    rightRotate(p);
                else
                    leftRotate(p);
            } else if (x == p.left && p == g.left) {
                // Zig-Zig step (left-left)
                rightRotate(g);
                rightRotate(p);
            } else if (x == p.right && p == g.right) {
                // Zig-Zig step (right-right)
                leftRotate(g);
                leftRotate(p);
            } else if (x == p.right && p == g.left) {
                // Zig-Zag step (left-right)
                leftRotate(p);
                rightRotate(g);
            } else if (x == p.left && p == g.right) {
                // Zig-Zag step (right-left)
                rightRotate(p);
                leftRotate(g);
            }
        }
        root = x;
    }

    // Right rotation at node y
    private void rightRotate(Node y) {
        Node x = y.left;
        if (x == null) return;
        y.left = x.right;
        if (x.right != null) x.right.parent = y;
        x.parent = y.parent;
        if (y.parent == null)
            root = x;
        else if (y == y.parent.left)
            y.parent.left = x;
        else
            y.parent.right = x;
        x.right = y;
        y.parent = x;
    }

    // Left rotation at node x
    private void leftRotate(Node x) {
        Node y = x.right;
        if (y == null) return;
        x.right = y.left;
        if (y.left != null) y.left.parent = x;
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

    // Find node with key
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

    // Replace root with node (can be null)
    private void replaceRoot(Node node) {
        root = node;
        if (node != null)
            node.parent = null;
    }

    // Returns the maximum node in the given subtree
    private Node subtreeMaximum(Node node) {
        while (node.right != null)
            node = node.right;
        return node;
    }

    // --- Optional: For debugging or testing only ---
    // public void inOrder() { inOrder(root); System.out.println(); }
    // private void inOrder(Node n) {
    //     if (n == null) return;
    //     inOrder(n.left);
    //     System.out.print(n.key + " ");
    //     inOrder(n.right);
    // }
}