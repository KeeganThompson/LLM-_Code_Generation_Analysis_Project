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
        Node z = root, p = null;
        while (z != null) {
            p = z;
            if (key < z.key) {
                z = z.left;
            } else if (key > z.key) {
                z = z.right;
            } else {
                // Key already exists, splay it to root
                splay(z);
                return;
            }
        }
        Node n = new Node(key);
        n.parent = p;
        if (key < p.key) {
            p.left = n;
        } else {
            p.right = n;
        }
        splay(n);
    }

    /** Deletes a key from the splay tree. */
    public void delete(int key) {
        Node node = find(root, key);
        if (node == null) return;
        splay(node);
        if (node.left != null) {
            Node max = subtreeMax(node.left);
            splay(max);
            max.right = node.right;
            if (node.right != null) node.right.parent = max;
            root = max;
            max.parent = null;
        } else if (node.right != null) {
            root = node.right;
            root.parent = null;
        } else {
            root = null;
        }
    }

    /** Searches for a key and splays the accessed node to the root. Returns the key or null if not found. */
    public Integer search(int key) {
        Node node = find(root, key);
        if (node != null) {
            splay(node);
            return node.key;
        } else if (lastAccessed != null) {
            splay(lastAccessed);
        }
        return null;
    }

    // --- Internal helpers ---

    // To help splay the last accessed node during failed search
    private Node lastAccessed = null;

    /** Finds node with key, or last accessed node if not found. */
    private Node find(Node node, int key) {
        Node curr = node;
        lastAccessed = null;
        while (curr != null) {
            lastAccessed = curr;
            if (key < curr.key) {
                curr = curr.left;
            } else if (key > curr.key) {
                curr = curr.right;
            } else {
                return curr;
            }
        }
        return null;
    }

    /** Splays the given node to the root. */
    private void splay(Node x) {
        if (x == null) return;
        while (x.parent != null) {
            Node p = x.parent;
            Node gp = p.parent;
            if (gp == null) {
                // Zig
                if (x == p.left) {
                    rightRotate(p);
                } else {
                    leftRotate(p);
                }
            } else if (x == p.left && p == gp.left) {
                // Zig-Zig
                rightRotate(gp);
                rightRotate(p);
            } else if (x == p.right && p == gp.right) {
                // Zig-Zig
                leftRotate(gp);
                leftRotate(p);
            } else if (x == p.right && p == gp.left) {
                // Zig-Zag
                leftRotate(p);
                rightRotate(gp);
            } else if (x == p.left && p == gp.right) {
                // Zig-Zag
                rightRotate(p);
                leftRotate(gp);
            }
        }
        root = x;
    }

    /** Left rotation at node x. */
    private void leftRotate(Node x) {
        Node y = x.right;
        if (y == null) return;
        x.right = y.left;
        if (y.left != null) y.left.parent = x;
        y.parent = x.parent;
        if (x.parent == null) {
            root = y;
        } else if (x == x.parent.left) {
            x.parent.left = y;
        } else {
            x.parent.right = y;
        }
        y.left = x;
        x.parent = y;
    }

    /** Right rotation at node x. */
    private void rightRotate(Node x) {
        Node y = x.left;
        if (y == null) return;
        x.left = y.right;
        if (y.right != null) y.right.parent = x;
        y.parent = x.parent;
        if (x.parent == null) {
            root = y;
        } else if (x == x.parent.left) {
            x.parent.left = y;
        } else {
            x.parent.right = y;
        }
        y.right = x;
        x.parent = y;
    }

    /** Returns the maximum node in subtree rooted at x. */
    private Node subtreeMax(Node x) {
        while (x.right != null) x = x.right;
        return x;
    }

    // For testing/debugging (not required by prompt)
    /*
    public void inorder() {
        inorder(root);
        System.out.println();
    }

    private void inorder(Node node) {
        if (node == null) return;
        inorder(node.left);
        System.out.print(node.key + " ");
        inorder(node.right);
    }
    */
}