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
        Node z = root, p = null;
        while (z != null) {
            p = z;
            if (key < z.key) {
                z = z.left;
            } else if (key > z.key) {
                z = z.right;
            } else {
                splay(z);
                return; // Key already exists, no duplicates allowed
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

    // Public delete method
    public void delete(int key) {
        Node node = searchNode(key);
        if (node == null) {
            return; // Key not found, nothing to delete
        }
        splay(node);
        // Now node is at root
        if (node.left != null) {
            Node maxLeft = subtreeMax(node.left);
            splay(maxLeft);
            maxLeft.right = node.right;
            if (node.right != null) node.right.parent = maxLeft;
            root = maxLeft;
            maxLeft.parent = null;
        } else if (node.right != null) {
            root = node.right;
            root.parent = null;
        } else {
            root = null;
        }
    }

    // Public search method
    public Integer search(int key) {
        Node x = root, prev = null;
        while (x != null) {
            prev = x;
            if (key < x.key) {
                x = x.left;
            } else if (key > x.key) {
                x = x.right;
            } else {
                splay(x);
                return x.key;
            }
        }
        if (prev != null) splay(prev); // Splay the last accessed node
        return null;
    }

    // Helper: search node, but don't splay
    private Node searchNode(int key) {
        Node x = root;
        while (x != null) {
            if (key < x.key) {
                x = x.left;
            } else if (key > x.key) {
                x = x.right;
            } else {
                return x;
            }
        }
        return null;
    }

    // Helper: Splay the node to root
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

    // Helper: Find maximum in subtree
    private Node subtreeMax(Node x) {
        while (x.right != null) x = x.right;
        return x;
    }

    // (Optional) For testing: Inorder traversal
    // public void inorder() {
    //     inorder(root);
    //     System.out.println();
    // }

    // private void inorder(Node x) {
    //     if (x != null) {
    //         inorder(x.left);
    //         System.out.print(x.key + " ");
    //         inorder(x.right);
    //     }
    // }
}