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
                splay(curr); // Key already exists, splay it
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
            return; // Key not found, do nothing
        }
        splay(node);
        // Now, node is root
        if (node.left != null) {
            Node maxLeft = subtreeMax(node.left);
            splay(maxLeft); // Splay max of left subtree to root
            maxLeft.right = node.right;
            if (node.right != null) {
                node.right.parent = maxLeft;
            }
            root = maxLeft;
            maxLeft.parent = null;
        } else if (node.right != null) {
            root = node.right;
            root.parent = null;
        } else {
            root = null;
        }
        // node is now disconnected and eligible for GC
    }

    // Public search method: returns Integer or null
    public Integer search(int key) {
        Node node = findNode(key);
        if (node != null) {
            splay(node);
            return node.key;
        } else {
            return null;
        }
    }

    // Helper: find node with given key (does not splay)
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

    // Helper: Splay node to root
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
                // Zig-zig
                rightRotate(gp);
                rightRotate(p);
            } else if (x == p.right && p == gp.right) {
                // Zig-zig
                leftRotate(gp);
                leftRotate(p);
            } else if (x == p.right && p == gp.left) {
                // Zig-zag
                leftRotate(p);
                rightRotate(gp);
            } else if (x == p.left && p == gp.right) {
                // Zig-zag
                rightRotate(p);
                leftRotate(gp);
            }
        }
        root = x;
    }

    // Helper: left rotate
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

    // Helper: right rotate
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
        } else if (x == x.parent.left) {
            x.parent.left = y;
        } else {
            x.parent.right = y;
        }
        y.right = x;
        x.parent = y;
    }

    // Helper: Max node in subtree
    private Node subtreeMax(Node x) {
        while (x.right != null) {
            x = x.right;
        }
        return x;
    }

    // Optional: For testing, inorder traversal to print the tree
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
}