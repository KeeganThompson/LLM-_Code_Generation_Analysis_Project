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
                // Key already exists, splay it to root
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
        Node node = findNode(key);
        if (node == null) {
            return;
        }
        splay(node);

        if (node.left == null) {
            replace(node, node.right);
        } else if (node.right == null) {
            replace(node, node.left);
        } else {
            // Find max in left subtree
            Node maxLeft = subtreeMax(node.left);
            if (maxLeft.parent != node) {
                replace(maxLeft, maxLeft.left);
                maxLeft.left = node.left;
                if (maxLeft.left != null)
                    maxLeft.left.parent = maxLeft;
            }
            replace(node, maxLeft);
            maxLeft.right = node.right;
            if (maxLeft.right != null)
                maxLeft.right.parent = maxLeft;
        }
        node.left = node.right = node.parent = null; // Help GC
    }

    // Public search method with splay
    public Integer search(int key) {
        Node node = findNode(key);
        if (node != null) {
            splay(node);
            return node.key;
        }
        return null;
    }

    // Helper: Finds node by key
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

    // Splay operation: moves node x to root
    private void splay(Node x) {
        if (x == null) return;
        while (x.parent != null) {
            if (x.parent.parent == null) {
                // Zig step
                if (x == x.parent.left) {
                    rotateRight(x.parent);
                } else {
                    rotateLeft(x.parent);
                }
            } else if (x == x.parent.left && x.parent == x.parent.parent.left) {
                // Zig-zig step (left-left)
                rotateRight(x.parent.parent);
                rotateRight(x.parent);
            } else if (x == x.parent.right && x.parent == x.parent.parent.right) {
                // Zig-zig step (right-right)
                rotateLeft(x.parent.parent);
                rotateLeft(x.parent);
            } else if (x == x.parent.right && x.parent == x.parent.parent.left) {
                // Zig-zag step (left-right)
                rotateLeft(x.parent);
                rotateRight(x.parent);
            } else if (x == x.parent.left && x.parent == x.parent.parent.right) {
                // Zig-zag step (right-left)
                rotateRight(x.parent);
                rotateLeft(x.parent);
            }
        }
        root = x;
    }

    // Left rotation
    private void rotateLeft(Node x) {
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

    // Right rotation
    private void rotateRight(Node x) {
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

    // Helper: replaces u with v in the tree
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

    // Helper: finds the max node in the subtree rooted at node
    private Node subtreeMax(Node node) {
        while (node.right != null) {
            node = node.right;
        }
        return node;
    }

    // Optional: For testing, inorder traversal (not required)
    /*
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
    */

    // Optional: For testing, get root key (not required)
    /*
    public Integer getRootKey() {
        return root != null ? root.key : null;
    }
    */
}