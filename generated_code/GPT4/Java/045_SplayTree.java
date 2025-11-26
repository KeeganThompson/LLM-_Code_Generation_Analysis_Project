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
                splay(curr);
                return; // Key already exists
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

    public void delete(int key) {
        Node node = findNode(key);
        if (node == null) return;
        splay(node);

        if (node.left != null) {
            Node leftSubtree = node.left;
            leftSubtree.parent = null;
            if (node.right != null) {
                Node rightSubtree = node.right;
                rightSubtree.parent = null;
                Node maxLeft = subtreeMax(leftSubtree);
                splay(maxLeft);
                maxLeft.right = rightSubtree;
                rightSubtree.parent = maxLeft;
                root = maxLeft;
            } else {
                root = leftSubtree;
            }
        } else if (node.right != null) {
            Node rightSubtree = node.right;
            rightSubtree.parent = null;
            root = rightSubtree;
        } else {
            root = null;
        }
        // Help GC
        node.left = node.right = node.parent = null;
    }

    public Integer search(int key) {
        Node node = findNode(key);
        if (node != null) {
            splay(node);
            return node.key;
        }
        return null;
    }

    // Helper: Splaying operation
    private void splay(Node x) {
        if (x == null) return;
        while (x.parent != null) {
            Node p = x.parent;
            Node gp = p.parent;
            if (gp == null) {
                // Zig step
                if (x == p.left) {
                    rightRotate(p);
                } else {
                    leftRotate(p);
                }
            } else if (x == p.left && p == gp.left) {
                // Zig-Zig step
                rightRotate(gp);
                rightRotate(p);
            } else if (x == p.right && p == gp.right) {
                // Zig-Zig step
                leftRotate(gp);
                leftRotate(p);
            } else if (x == p.right && p == gp.left) {
                // Zig-Zag step
                leftRotate(p);
                rightRotate(gp);
            } else if (x == p.left && p == gp.right) {
                // Zig-Zag step
                rightRotate(p);
                leftRotate(gp);
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

    // Helper: Find maximum node in subtree
    private Node subtreeMax(Node node) {
        if (node == null) return null;
        while (node.right != null) node = node.right;
        return node;
    }

    // Optional: For testing purpose
    // public void inorder() {
    //     inorder(root);
    //     System.out.println();
    // }
    // private void inorder(Node node) {
    //     if (node == null) return;
    //     inorder(node.left);
    //     System.out.print(node.key + " ");
    //     inorder(node.right);
    // }
}