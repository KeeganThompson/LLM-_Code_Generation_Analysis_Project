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

    /** Inserts a key into the set. Does nothing if key already exists. */
    public void insert(int key) {
        if (root == null) {
            root = new Node(key, null);
            return;
        }

        Node curr = root;
        Node parent = null;
        while (curr != null) {
            parent = curr;
            if (key < curr.key) {
                curr = curr.left;
            } else if (key > curr.key) {
                curr = curr.right;
            } else { // Key already exists, splay it
                splay(curr);
                return;
            }
        }

        Node newNode = new Node(key, parent);
        if (key < parent.key) {
            parent.left = newNode;
        } else {
            parent.right = newNode;
        }
        splay(newNode);
    }

    /** Deletes a key from the set. Does nothing if key does not exist. */
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
            Node maxLeft = subtreeMax(node.left);
            splay(maxLeft); // Splay maxLeft to root of left subtree
            // Now maxLeft is root, with no right child
            maxLeft.right = node.right;
            if (node.right != null) node.right.parent = maxLeft;
            replaceRoot(maxLeft);
        }
    }

    /**
     * Searches for a key. If found, splays the node to the root and returns the key.
     * If not found, returns null.
     */
    public Integer search(int key) {
        Node node = findNode(key);
        if (node != null) {
            splay(node);
            return node.key;
        }
        return null;
    }

    // --- Private utility methods ---

    private Node findNode(int key) {
        Node curr = root;
        while (curr != null) {
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

    private Node subtreeMax(Node node) {
        while (node.right != null) node = node.right;
        return node;
    }

    private void replaceRoot(Node newRoot) {
        root = newRoot;
        if (newRoot != null) newRoot.parent = null;
    }

    /** Splays node x to the root. */
    private void splay(Node x) {
        if (x == null) return;
        while (x.parent != null) {
            if (x.parent.parent == null) {
                // Zig step
                if (x.parent.left == x) {
                    rotateRight(x.parent);
                } else {
                    rotateLeft(x.parent);
                }
            } else if (x.parent.left == x && x.parent.parent.left == x.parent) {
                // Zig-zig step (left-left)
                rotateRight(x.parent.parent);
                rotateRight(x.parent);
            } else if (x.parent.right == x && x.parent.parent.right == x.parent) {
                // Zig-zig step (right-right)
                rotateLeft(x.parent.parent);
                rotateLeft(x.parent);
            } else if (x.parent.left == x && x.parent.parent.right == x.parent) {
                // Zig-zag step (left-right)
                rotateRight(x.parent);
                rotateLeft(x.parent);
            } else {
                // Zig-zag step (right-left)
                rotateLeft(x.parent);
                rotateRight(x.parent);
            }
        }
        root = x;
    }

    private void rotateLeft(Node x) {
        Node y = x.right;
        if (y == null) return;
        x.right = y.left;
        if (y.left != null) y.left.parent = x;
        y.parent = x.parent;
        if (x.parent == null) {
            root = y;
        } else if (x.parent.left == x) {
            x.parent.left = y;
        } else {
            x.parent.right = y;
        }
        y.left = x;
        x.parent = y;
    }

    private void rotateRight(Node x) {
        Node y = x.left;
        if (y == null) return;
        x.left = y.right;
        if (y.right != null) y.right.parent = x;
        y.parent = x.parent;
        if (x.parent == null) {
            root = y;
        } else if (x.parent.left == x) {
            x.parent.left = y;
        } else {
            x.parent.right = y;
        }
        y.right = x;
        x.parent = y;
    }
}