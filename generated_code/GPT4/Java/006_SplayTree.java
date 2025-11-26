public class SplayTree {
    private class Node {
        int key;
        Node left, right, parent;

        Node(int key) {
            this.key = key;
        }
    }

    private Node root;

    // Right rotate x
    private void rotateRight(Node x) {
        Node y = x.left;
        if (y == null) return;
        x.left = y.right;
        if (y.right != null) y.right.parent = x;
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

    // Left rotate x
    private void rotateLeft(Node x) {
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

    // Splay node x to the root
    private void splay(Node x) {
        if (x == null) return;
        while (x.parent != null) {
            if (x.parent.parent == null) {
                // Zig
                if (x == x.parent.left) {
                    rotateRight(x.parent);
                } else {
                    rotateLeft(x.parent);
                }
            } else if (x == x.parent.left && x.parent == x.parent.parent.left) {
                // Zig-zig
                rotateRight(x.parent.parent);
                rotateRight(x.parent);
            } else if (x == x.parent.right && x.parent == x.parent.parent.right) {
                // Zig-zig
                rotateLeft(x.parent.parent);
                rotateLeft(x.parent);
            } else if (x == x.parent.right && x.parent == x.parent.parent.left) {
                // Zig-zag
                rotateLeft(x.parent);
                rotateRight(x.parent);
            } else {
                // Zig-zag
                rotateRight(x.parent);
                rotateLeft(x.parent);
            }
        }
    }

    // Search for key and splay if found
    public Integer search(int key) {
        Node x = root;
        Node last = null;
        while (x != null) {
            last = x;
            if (key < x.key) {
                x = x.left;
            } else if (key > x.key) {
                x = x.right;
            } else {
                splay(x);
                return x.key;
            }
        }
        if (last != null)
            splay(last); // Splay the last accessed node for locality
        return null;
    }

    // Insert key
    public void insert(int key) {
        if (root == null) {
            root = new Node(key);
            return;
        }
        Node x = root, parent = null;
        while (x != null) {
            parent = x;
            if (key < x.key) {
                x = x.left;
            } else if (key > x.key) {
                x = x.right;
            } else {
                splay(x); // Key already exists, splay it
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

    // Delete key
    public void delete(int key) {
        Node x = root;
        while (x != null) {
            if (key < x.key) {
                x = x.left;
            } else if (key > x.key) {
                x = x.right;
            } else {
                break;
            }
        }
        if (x == null) {
            return; // Not found
        }
        splay(x);
        if (x.left == null) {
            transplant(x, x.right);
        } else if (x.right == null) {
            transplant(x, x.left);
        } else {
            Node min = subtreeMin(x.right);
            if (min.parent != x) {
                transplant(min, min.right);
                min.right = x.right;
                if (min.right != null) min.right.parent = min;
            }
            transplant(x, min);
            min.left = x.left;
            if (min.left != null) min.left.parent = min;
        }
        x.left = x.right = x.parent = null; // Help GC
    }

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

    private Node subtreeMin(Node x) {
        while (x.left != null) {
            x = x.left;
        }
        return x;
    }

    // Optional: For debugging - inorder traversal
    public void inorder() {
        inorder(root);
        System.out.println();
    }

    private void inorder(Node x) {
        if (x == null) return;
        inorder(x.left);
        System.out.print(x.key + " ");
        inorder(x.right);
    }
}