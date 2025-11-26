public class SplayTree {
    private class Node {
        int key;
        Node left, right, parent;

        Node(int key, Node parent) {
            this.key = key;
            this.left = null;
            this.right = null;
            this.parent = parent;
        }
    }

    private Node root;

    public SplayTree() {
        root = null;
    }

    // Public insert method
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
            } else {
                // Already exists, splay it.
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

    // Public delete method
    public void delete(int key) {
        Node node = find(root, key);
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
        node.left = node.right = node.parent = null; // Help GC
    }

    // Public search method (returns Integer or null)
    public Integer search(int key) {
        Node node = root;
        Node last = null;
        while (node != null) {
            last = node;
            if (key < node.key) {
                node = node.left;
            } else if (key > node.key) {
                node = node.right;
            } else {
                splay(node);
                return node.key;
            }
        }
        if (last != null)
            splay(last); // Splay last accessed node for locality
        return null;
    }

    // Helper: Splaying operation
    private void splay(Node x) {
        if (x == null)
            return;
        while (x.parent != null) {
            if (x.parent.parent == null) {
                // Zig
                if (x.parent.left == x) {
                    rotateRight(x.parent);
                } else {
                    rotateLeft(x.parent);
                }
            } else if (x.parent.left == x && x.parent.parent.left == x.parent) {
                // Zig-zig
                rotateRight(x.parent.parent);
                rotateRight(x.parent);
            } else if (x.parent.right == x && x.parent.parent.right == x.parent) {
                // Zig-zig
                rotateLeft(x.parent.parent);
                rotateLeft(x.parent);
            } else if (x.parent.left == x && x.parent.parent.right == x.parent) {
                // Zig-zag
                rotateRight(x.parent);
                rotateLeft(x.parent);
            } else {
                // Zig-zag
                rotateLeft(x.parent);
                rotateRight(x.parent);
            }
        }
        root = x;
    }

    // Helper: Replace node u with node v in the tree
    private void replace(Node u, Node v) {
        if (u.parent == null) {
            root = v;
        } else if (u == u.parent.left) {
            u.parent.left = v;
        } else {
            u.parent.right = v;
        }
        if (v != null) {
            v.parent = u.parent;
        }
    }

    // Helper: Find node with key starting from a node
    private Node find(Node node, int key) {
        while (node != null) {
            if (key < node.key) {
                node = node.left;
            } else if (key > node.key) {
                node = node.right;
            } else {
                return node;
            }
        }
        return null;
    }

    // Helper: subtree minimum
    private Node subtreeMin(Node node) {
        while (node.left != null) {
            node = node.left;
        }
        return node;
    }

    // Helper: rotate left
    private void rotateLeft(Node x) {
        Node y = x.right;
        if (y == null) return;
        x.right = y.left;
        if (y.left != null)
            y.left.parent = x;
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

    // Helper: rotate right
    private void rotateRight(Node x) {
        Node y = x.left;
        if (y == null) return;
        x.left = y.right;
        if (y.right != null)
            y.right.parent = x;
        y.parent = x.parent;
        if (x.parent == null) {
            root = y;
        } else if (x == x.parent.right) {
            x.parent.right = y;
        } else {
            x.parent.left = y;
        }
        y.right = x;
        x.parent = y;
    }

    // Optional: For debugging, in-order traversal
    public void printInOrder() {
        printInOrder(root);
        System.out.println();
    }

    private void printInOrder(Node node) {
        if (node != null) {
            printInOrder(node.left);
            System.out.print(node.key + " ");
            printInOrder(node.right);
        }
    }
}