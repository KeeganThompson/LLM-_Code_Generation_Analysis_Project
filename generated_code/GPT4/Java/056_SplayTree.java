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
     * Inserts a key into the splay tree.
     * If the key already exists, does nothing.
     */
    public void insert(int key) {
        if (root == null) {
            root = new Node(key);
            return;
        }
        Node curr = root, parent = null;
        while (curr != null) {
            parent = curr;
            if (key < curr.key)
                curr = curr.left;
            else if (key > curr.key)
                curr = curr.right;
            else {
                splay(curr);
                return; // Key already in tree
            }
        }
        Node newNode = new Node(key);
        newNode.parent = parent;
        if (key < parent.key)
            parent.left = newNode;
        else
            parent.right = newNode;
        splay(newNode);
    }

    /**
     * Deletes a key from the splay tree if it exists.
     */
    public void delete(int key) {
        Node node = findNode(key);
        if (node == null)
            return;
        splay(node);
        if (node.left != null) {
            Node leftSubtree = node.left;
            leftSubtree.parent = null;
            Node maxLeft = subtreeMaximum(leftSubtree);
            splay(maxLeft);
            maxLeft.right = node.right;
            if (node.right != null)
                node.right.parent = maxLeft;
            root = maxLeft;
            root.parent = null;
        } else if (node.right != null) {
            root = node.right;
            root.parent = null;
        } else {
            root = null;
        }
    }

    /**
     * Searches for a key in the splay tree.
     * If found, splays the node to the root and returns the key.
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

    // Helper: Find node with given key, no splaying
    private Node findNode(int key) {
        Node curr = root;
        while (curr != null) {
            if (key < curr.key)
                curr = curr.left;
            else if (key > curr.key)
                curr = curr.right;
            else
                return curr;
        }
        return null;
    }

    // Helper: Splay the given node to the root
    private void splay(Node x) {
        if (x == null)
            return;
        while (x.parent != null) {
            Node p = x.parent;
            Node g = p.parent;
            if (g == null) {
                // Zig
                if (x == p.left)
                    rotateRight(p);
                else
                    rotateLeft(p);
            } else if (x == p.left && p == g.left) {
                // Zig-Zig
                rotateRight(g);
                rotateRight(p);
            } else if (x == p.right && p == g.right) {
                // Zig-Zig
                rotateLeft(g);
                rotateLeft(p);
            } else if (x == p.right && p == g.left) {
                // Zig-Zag
                rotateLeft(p);
                rotateRight(g);
            } else if (x == p.left && p == g.right) {
                // Zig-Zag
                rotateRight(p);
                rotateLeft(g);
            }
        }
        root = x;
    }

    // Helper: Rotate node x to left (x becomes left child of its right child)
    private void rotateLeft(Node x) {
        Node y = x.right;
        if (y == null)
            return;
        x.right = y.left;
        if (y.left != null)
            y.left.parent = x;
        y.parent = x.parent;
        if (x.parent == null)
            root = y;
        else if (x == x.parent.left)
            x.parent.left = y;
        else
            x.parent.right = y;
        y.left = x;
        x.parent = y;
    }

    // Helper: Rotate node x to right (x becomes right child of its left child)
    private void rotateRight(Node x) {
        Node y = x.left;
        if (y == null)
            return;
        x.left = y.right;
        if (y.right != null)
            y.right.parent = x;
        y.parent = x.parent;
        if (x.parent == null)
            root = y;
        else if (x == x.parent.left)
            x.parent.left = y;
        else
            x.parent.right = y;
        y.right = x;
        x.parent = y;
    }

    // Helper: Return the max node in the subtree rooted at node
    private Node subtreeMaximum(Node node) {
        while (node.right != null)
            node = node.right;
        return node;
    }

    // Optional: For debugging, in-order traversal
    /*
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
    */
}