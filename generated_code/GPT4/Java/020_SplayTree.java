public class SplayTree {
    private class Node {
        int key;
        Node left, right, parent;

        Node(int key) {
            this.key = key;
        }
    }

    private Node root;

    /** Inserts a key into the set (no duplicates). */
    public void insert(int key) {
        if (root == null) {
            root = new Node(key);
            return;
        }
        Node z = root, p = null;
        while (z != null) {
            p = z;
            if (key < z.key)
                z = z.left;
            else if (key > z.key)
                z = z.right;
            else {
                splay(z);
                return; // key already exists, no duplicates
            }
        }
        Node n = new Node(key);
        n.parent = p;
        if (key < p.key)
            p.left = n;
        else
            p.right = n;
        splay(n);
    }

    /** Deletes a key from the set (if exists). */
    public void delete(int key) {
        Node node = findNode(key);
        if (node == null)
            return;
        splay(node);
        // Remove node
        if (node.left == null) {
            replace(node, node.right);
        } else if (node.right == null) {
            replace(node, node.left);
        } else {
            // Find max in left subtree
            Node max = subtreeMax(node.left);
            if (max.parent != node) {
                replace(max, max.left);
                max.left = node.left;
                if (max.left != null)
                    max.left.parent = max;
            }
            replace(node, max);
            max.right = node.right;
            if (max.right != null)
                max.right.parent = max;
        }
        // Remove all references
        node.left = node.right = node.parent = null;
    }

    /** Searches for a key. Splays the node to root if found. Returns the key, or null if not found. */
    public Integer search(int key) {
        Node node = findNode(key);
        if (node != null) {
            splay(node);
            return node.key;
        }
        return null;
    }

    // --------- Internal Helper Methods ---------

    private Node findNode(int key) {
        Node z = root;
        while (z != null) {
            if (key < z.key)
                z = z.left;
            else if (key > z.key)
                z = z.right;
            else
                return z;
        }
        return null;
    }

    // Splaying operation: moves x to the root
    private void splay(Node x) {
        if (x == null)
            return;
        while (x.parent != null) {
            if (x.parent.parent == null) {
                // Zig
                if (x.parent.left == x)
                    rightRotate(x.parent);
                else
                    leftRotate(x.parent);
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

    private void leftRotate(Node x) {
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

    private void rightRotate(Node x) {
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

    // Replace node u with node v in the tree
    private void replace(Node u, Node v) {
        if (u.parent == null)
            root = v;
        else if (u == u.parent.left)
            u.parent.left = v;
        else
            u.parent.right = v;
        if (v != null)
            v.parent = u.parent;
    }

    // Finds the maximum node in a subtree
    private Node subtreeMax(Node x) {
        while (x.right != null)
            x = x.right;
        return x;
    }

    // --------- Optional: Utility Methods ---------

    /** Inorder traversal as a string, for debugging. */
    @Override
    public String toString() {
        StringBuilder sb = new StringBuilder();
        inorder(root, sb);
        return sb.toString();
    }

    private void inorder(Node node, StringBuilder sb) {
        if (node == null)
            return;
        inorder(node.left, sb);
        sb.append(node.key).append(' ');
        inorder(node.right, sb);
    }

    // --------- Main method for demonstration ---------
    public static void main(String[] args) {
        SplayTree st = new SplayTree();
        st.insert(10);
        st.insert(20);
        st.insert(30);
        st.insert(40);
        st.insert(50);
        System.out.println("Tree (inorder): " + st);

        System.out.println("Search 30: " + st.search(30)); // Should splay 30 to root
        System.out.println("Tree (inorder): " + st);

        st.delete(20);
        System.out.println("After deleting 20: " + st);

        System.out.println("Search 60: " + st.search(60)); // Not found
        System.out.println("Tree (inorder): " + st);
    }
}