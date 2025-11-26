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
     * Inserts key into the splay tree. If the key already exists, does nothing.
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
            if (key < curr.key) {
                curr = curr.left;
            } else if (key > curr.key) {
                curr = curr.right;
            } else {
                // Key already exists, splay it to root
                splay(curr);
                return;
            }
        }

        Node newNode = new Node(key);
        newNode.parent = parent;
        if (key < parent.key) {
            parent.left = newNode;
        } else {
            parent.right = newNode;
        }
        splay(newNode);
    }

    /**
     * Deletes key from the splay tree. If not found, does nothing.
     */
    public void delete(int key) {
        Node node = findNode(key);
        if (node == null) return;

        splay(node);

        if (node.left == null) {
            transplant(node, node.right);
        } else if (node.right == null) {
            transplant(node, node.left);
        } else {
            // Find minimum of right subtree
            Node min = subtreeMin(node.right);
            if (min.parent != node) {
                transplant(min, min.right);
                min.right = node.right;
                if (min.right != null) min.right.parent = min;
            }
            transplant(node, min);
            min.left = node.left;
            if (min.left != null) min.left.parent = min;
        }
    }

    /**
     * Searches for key in the splay tree.
     * If found, splays the node to the root and returns the key.
     * Otherwise, returns null.
     */
    public Integer search(int key) {
        Node node = findNode(key);
        if (node != null) {
            splay(node);
            return node.key;
        }
        return null;
    }

    // Helper: Find node with given key, no splaying
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

    // Helper: Splay the node to the root
    private void splay(Node x) {
        if (x == null) return;
        while (x.parent != null) {
            if (x.parent.parent == null) {
                // Zig
                if (x.parent.left == x) {
                    rotateRight(x.parent);
                } else {
                    rotateLeft(x.parent);
                }
            } else if (x.parent.left == x && x.parent.parent.left == x.parent) {
                // Zig-Zig
                rotateRight(x.parent.parent);
                rotateRight(x.parent);
            } else if (x.parent.right == x && x.parent.parent.right == x.parent) {
                // Zig-Zig
                rotateLeft(x.parent.parent);
                rotateLeft(x.parent);
            } else if (x.parent.left == x && x.parent.parent.right == x.parent) {
                // Zig-Zag
                rotateRight(x.parent);
                rotateLeft(x.parent);
            } else {
                // Zig-Zag
                rotateLeft(x.parent);
                rotateRight(x.parent);
            }
        }
        root = x;
    }

    // Helper: Left rotation
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

    // Helper: Right rotation
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

    // Helper: Replace subtree u with v
    private void transplant(Node u, Node v) {
        if (u.parent == null) {
            root = v;
        } else if (u == u.parent.left) {
            u.parent.left = v;
        } else {
            u.parent.right = v;
        }
        if (v != null) v.parent = u.parent;
    }

    // Helper: Find minimum node in subtree
    private Node subtreeMin(Node node) {
        while (node.left != null) node = node.left;
        return node;
    }

    // Optional: For debugging, inorder traversal
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

    // Optional: For debugging, print root
    public Integer getRootKey() {
        return root != null ? root.key : null;
    }
}