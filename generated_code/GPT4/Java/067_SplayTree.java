public class SplayTree {
    private class Node {
        int key;
        Node left, right, parent;

        Node(int key) {
            this.key = key;
        }
    }

    private Node root;

    /** Inserts a key into the splay tree. */
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
                splay(curr);
                return; // Key already exists
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

    /** Deletes a key from the splay tree if present. */
    public void delete(int key) {
        Node node = findNode(key);
        if (node == null)
            return;
        splay(node);

        if (node.left == null) {
            replace(node, node.right);
        } else if (node.right == null) {
            replace(node, node.left);
        } else {
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
        // node is removed, root may change
    }

    /** Searches for a key and splays the found node to the root; returns the key or null. */
    public Integer search(int key) {
        Node node = findNode(key);
        if (node != null) {
            splay(node);
            return node.key;
        }
        return null;
    }

    // ========== PRIVATE HELPERS ==========

    /** Splays the given node to the root. */
    private void splay(Node x) {
        if (x == null)
            return;
        while (x.parent != null) {
            Node p = x.parent;
            Node gp = p.parent;
            if (gp == null) {
                // Zig
                if (x == p.left)
                    rotateRight(p);
                else
                    rotateLeft(p);
            } else if (x == p.left && p == gp.left) {
                // Zig-zig
                rotateRight(gp);
                rotateRight(p);
            } else if (x == p.right && p == gp.right) {
                // Zig-zig
                rotateLeft(gp);
                rotateLeft(p);
            } else if (x == p.right && p == gp.left) {
                // Zig-zag
                rotateLeft(p);
                rotateRight(gp);
            } else if (x == p.left && p == gp.right) {
                // Zig-zag
                rotateRight(p);
                rotateLeft(gp);
            }
        }
        root = x;
    }

    /** Rotates node x left (x becomes parent of its right child). */
    private void rotateLeft(Node x) {
        Node y = x.right;
        if (y == null)
            return;
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

    /** Rotates node x right (x becomes parent of its left child). */
    private void rotateRight(Node x) {
        Node y = x.left;
        if (y == null)
            return;
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

    /** Finds node with given key (no splaying). */
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

    /** Replaces subtree u with v in the tree. */
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

    /** Returns the minimum node in subtree rooted at x. */
    private Node subtreeMin(Node x) {
        while (x.left != null)
            x = x.left;
        return x;
    }

    // ========== OPTIONAL: For testing/debugging ==========

    /** In-order traversal (for testing/debugging only). */
    public void inorder() {
        inorder(root);
        System.out.println();
    }

    private void inorder(Node x) {
        if (x == null)
            return;
        inorder(x.left);
        System.out.print(x.key + " ");
        inorder(x.right);
    }

    // Main method for demonstration (optional)
    public static void main(String[] args) {
        SplayTree tree = new SplayTree();
        tree.insert(10);
        tree.insert(20);
        tree.insert(5);
        tree.insert(15);
        tree.inorder(); // Should print 5 10 15 20

        System.out.println(tree.search(15)); // 15
        tree.inorder(); // Root should now be 15

        tree.delete(10);
        tree.inorder(); // 5 15 20

        System.out.println(tree.search(42)); // null
    }
}