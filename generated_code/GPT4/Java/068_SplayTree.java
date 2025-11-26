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
            if (key < z.key) z = z.left;
            else if (key > z.key) z = z.right;
            else {
                splay(z);
                return; // key already exists, do nothing
            }
        }
        Node n = new Node(key);
        n.parent = p;
        if (key < p.key) p.left = n;
        else p.right = n;
        splay(n);
    }

    // Public delete method
    public void delete(int key) {
        Node node = find(root, key);
        if (node == null) return;
        splay(node);
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
        Node node = find(root, key);
        if (node != null) {
            splay(node);
            return node.key;
        }
        return null;
    }

    // Helper: find node with given key
    private Node find(Node curr, int key) {
        while (curr != null) {
            if (key < curr.key) curr = curr.left;
            else if (key > curr.key) curr = curr.right;
            else return curr;
        }
        return null;
    }

    // Helper: splay node to root
    private void splay(Node x) {
        if (x == null) return;
        while (x.parent != null) {
            Node p = x.parent;
            Node g = p.parent;
            if (g == null) {
                // Zig
                if (x == p.left) rightRotate(p);
                else leftRotate(p);
            } else if (x == p.left && p == g.left) {
                // Zig-Zig
                rightRotate(g);
                rightRotate(p);
            } else if (x == p.right && p == g.right) {
                // Zig-Zig
                leftRotate(g);
                leftRotate(p);
            } else if (x == p.right && p == g.left) {
                // Zig-Zag
                leftRotate(p);
                rightRotate(g);
            } else if (x == p.left && p == g.right) {
                // Zig-Zag
                rightRotate(p);
                leftRotate(g);
            }
        }
        root = x;
    }

    // Helper: right rotate
    private void rightRotate(Node x) {
        Node y = x.left;
        if (y == null) return;
        x.left = y.right;
        if (y.right != null) y.right.parent = x;
        y.parent = x.parent;
        if (x.parent == null) root = y;
        else if (x == x.parent.left) x.parent.left = y;
        else x.parent.right = y;
        y.right = x;
        x.parent = y;
    }

    // Helper: left rotate
    private void leftRotate(Node x) {
        Node y = x.right;
        if (y == null) return;
        x.right = y.left;
        if (y.left != null) y.left.parent = x;
        y.parent = x.parent;
        if (x.parent == null) root = y;
        else if (x == x.parent.left) x.parent.left = y;
        else x.parent.right = y;
        y.left = x;
        x.parent = y;
    }

    // Helper: subtree maximum
    private Node subtreeMax(Node x) {
        while (x.right != null) x = x.right;
        return x;
    }

    // Optional: for testing
    public void inorder() {
        inorder(root);
        System.out.println();
    }

    private void inorder(Node n) {
        if (n == null) return;
        inorder(n.left);
        System.out.print(n.key + " ");
        inorder(n.right);
    }

    // Main for demonstration (not required)
    public static void main(String[] args) {
        SplayTree st = new SplayTree();
        st.insert(10);
        st.insert(20);
        st.insert(5);
        st.insert(8);
        st.insert(15);
        st.inorder(); // 5 8 10 15 20

        System.out.println(st.search(15)); // 15
        st.inorder(); // 5 8 10 15 20 (but 15 is root internally)

        st.delete(10);
        st.inorder(); // 5 8 15 20
        System.out.println(st.search(100)); // null
    }
}