public class SplayTree {
    private class Node {
        int key;
        Node left, right, parent;

        Node(int key) {
            this.key = key;
        }
    }

    private Node root;

    // Public insert method
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
                splay(curr);
                return; // key already exists, no duplicates
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

    // Public delete method
    public void delete(int key) {
        Node node = findNode(key);
        if (node == null) return;

        splay(node);

        if (node.left == null) {
            transplant(node, node.right);
        } else if (node.right == null) {
            transplant(node, node.left);
        } else {
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

    // Public search method
    public Integer search(int key) {
        Node curr = root;
        Node last = null;
        while (curr != null) {
            last = curr;
            if (key < curr.key) {
                curr = curr.left;
            } else if (key > curr.key) {
                curr = curr.right;
            } else {
                splay(curr);
                return curr.key;
            }
        }
        if (last != null) splay(last);
        return null;
    }

    // Helper: Splay operation
    private void splay(Node x) {
        if (x == null) return;
        while (x.parent != null) {
            if (x.parent.parent == null) {
                // Zig
                if (x.parent.left == x) {
                    rightRotate(x.parent);
                } else {
                    leftRotate(x.parent);
                }
            } else if (x.parent.left == x && x.parent.parent.left == x.parent) {
                // Zig-Zig
                rightRotate(x.parent.parent);
                rightRotate(x.parent);
            } else if (x.parent.right == x && x.parent.parent.right == x.parent) {
                // Zig-Zig
                leftRotate(x.parent.parent);
                leftRotate(x.parent);
            } else if (x.parent.left == x && x.parent.parent.right == x.parent) {
                // Zig-Zag
                rightRotate(x.parent);
                leftRotate(x.parent);
            } else {
                // Zig-Zag
                leftRotate(x.parent);
                rightRotate(x.parent);
            }
        }
        root = x;
    }

    // Helper: Right rotation
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

    // Helper: Left rotation
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

    // Helper: Find node with given key
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

    // Helper: Transplant node u with node v
    private void transplant(Node u, Node v) {
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

    // Helper: Minimum node in subtree
    private Node subtreeMin(Node node) {
        while (node.left != null) node = node.left;
        return node;
    }

    // Optional: For debugging - inorder traversal
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
}