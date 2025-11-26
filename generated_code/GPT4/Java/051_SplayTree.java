public class SplayTree {
    // Node class representing each node in the Splay Tree
    private class Node {
        int key;
        Node left, right, parent;

        Node(int key) {
            this.key = key;
        }
    }

    private Node root;

    // Public method to insert a key into the Splay Tree
    public void insert(int key) {
        if (root == null) {
            root = new Node(key);
            return;
        }

        Node node = root;
        Node parent = null;
        while (node != null) {
            parent = node;
            if (key < node.key) {
                node = node.left;
            } else if (key > node.key) {
                node = node.right;
            } else {
                // Key already exists, splay and return
                splay(node);
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

    // Public method to delete a key from the Splay Tree
    public void delete(int key) {
        Node node = findNode(key);
        if (node == null) {
            return; // Key not found, do nothing
        }
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
                if (min.right != null) {
                    min.right.parent = min;
                }
            }
            replace(node, min);
            min.left = node.left;
            if (min.left != null) {
                min.left.parent = min;
            }
        }
        node.left = node.right = node.parent = null; // Help GC
    }

    // Public method to search for a key in the Splay Tree
    // Returns the key if found, or null if not found
    public Integer search(int key) {
        Node node = findNode(key);
        if (node != null) {
            splay(node);
            return node.key;
        }
        return null;
    }

    // Helper: Find the node with the specified key
    private Node findNode(int key) {
        Node node = root;
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

    // Helper: Find the minimum node in a subtree
    private Node subtreeMin(Node node) {
        while (node.left != null) {
            node = node.left;
        }
        return node;
    }

    // Splaying operation: brings the given node to the root
    private void splay(Node x) {
        if (x == null) return;
        while (x.parent != null) {
            if (x.parent.parent == null) {
                // Zig case
                if (x == x.parent.left) {
                    rightRotate(x.parent);
                } else {
                    leftRotate(x.parent);
                }
            } else if (x == x.parent.left && x.parent == x.parent.parent.left) {
                // Zig-Zig case (left-left)
                rightRotate(x.parent.parent);
                rightRotate(x.parent);
            } else if (x == x.parent.right && x.parent == x.parent.parent.right) {
                // Zig-Zig case (right-right)
                leftRotate(x.parent.parent);
                leftRotate(x.parent);
            } else if (x == x.parent.right && x.parent == x.parent.parent.left) {
                // Zig-Zag case (left-right)
                leftRotate(x.parent);
                rightRotate(x.parent);
            } else {
                // Zig-Zag case (right-left)
                rightRotate(x.parent);
                leftRotate(x.parent);
            }
        }
    }

    // Left rotation at node x
    private void leftRotate(Node x) {
        Node y = x.right;
        if (y == null) return;
        x.right = y.left;
        if (y.left != null) {
            y.left.parent = x;
        }
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

    // Right rotation at node x
    private void rightRotate(Node x) {
        Node y = x.left;
        if (y == null) return;
        x.left = y.right;
        if (y.right != null) {
            y.right.parent = x;
        }
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

    // Optional: For testing, in-order traversal
    /*
    public void inorder() {
        inorder(root);
        System.out.println();
    }

    private void inorder(Node node) {
        if (node != null) {
            inorder(node.left);
            System.out.print(node.key + " ");
            inorder(node.right);
        }
    }
    */
}