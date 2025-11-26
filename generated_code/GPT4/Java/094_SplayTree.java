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

    /**
     * Inserts the given key into the splay tree.
     */
    public void insert(int key) {
        if (root == null) {
            root = new Node(key, null);
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
                splay(curr); // Key already present, splay to root
                return;
            }
        }
        Node newNode = new Node(key, parent);
        if (key < parent.key)
            parent.left = newNode;
        else
            parent.right = newNode;
        splay(newNode);
    }

    /**
     * Deletes the given key from the splay tree if present.
     */
    public void delete(int key) {
        Node node = find(key);
        if (node == null)
            return;
        splay(node);
        // Now node is root
        if (node.left != null) {
            Node maxLeft = subtreeMax(node.left);
            splay(maxLeft);
            // After splaying, maxLeft becomes root, and its right is null
            maxLeft.right = node.right;
            if (node.right != null)
                node.right.parent = maxLeft;
            root = maxLeft;
            maxLeft.parent = null;
        } else if (node.right != null) {
            root = node.right;
            root.parent = null;
        } else {
            root = null;
        }
        // Help GC
        node.left = node.right = node.parent = null;
    }

    /**
     * Searches for the given key in the splay tree.
     * If found, splays the node to the root and returns the key.
     * Otherwise, returns null.
     */
    public Integer search(int key) {
        Node node = find(key);
        if (node != null) {
            splay(node);
            return node.key;
        }
        return null;
    }

    // ----------------- Private Utilities -----------------

    /**
     * Finds the node with the given key without splaying. Returns null if not found.
     */
    private Node find(int key) {
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

    /**
     * Splays the given node to the root.
     */
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

    /**
     * Rotates the node to the left (x becomes parent of its parent).
     */
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

    /**
     * Rotates the node to the right (x becomes parent of its parent).
     */
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

    /**
     * Returns the node with the maximum key in the given subtree.
     */
    private Node subtreeMax(Node node) {
        while (node.right != null)
            node = node.right;
        return node;
    }

    // ------------- (Optional) For Testing -------------

    // Inorder traversal (for debugging)
    private void inorder(Node node, StringBuilder sb) {
        if (node == null) return;
        inorder(node.left, sb);
        sb.append(node.key).append(' ');
        inorder(node.right, sb);
    }

    /**
     * Returns the in-order traversal of the tree as a string (for debugging).
     */
    public String inorderString() {
        StringBuilder sb = new StringBuilder();
        inorder(root, sb);
        return sb.toString().trim();
    }

    // Main for demonstration (you may remove this before use)
    public static void main(String[] args) {
        SplayTree set = new SplayTree();
        set.insert(10);
        set.insert(20);
        set.insert(5);
        set.insert(15);

        System.out.println("Inorder: " + set.inorderString()); // 5 10 15 20

        System.out.println("Search 15: " + set.search(15)); // 15
        System.out.println("Root after search(15): " + set.root.key); // 15

        set.delete(10);
        System.out.println("Inorder after delete(10): " + set.inorderString()); // 5 15 20

        System.out.println("Search 100: " + set.search(100)); // null
    }
}