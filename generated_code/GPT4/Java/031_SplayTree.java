public class SplayTree {
    private class Node {
        int key;
        Node left, right, parent;

        Node(int key) {
            this.key = key;
        }
    }

    private Node root;

    // Public method: Insert key into the set
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
                return; // already exists, do not insert duplicates
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

    // Public method: Delete key from the set
    public void delete(int key) {
        Node node = find(root, key);
        if (node == null)
            return;
        splay(node);
        // Now node is root
        if (node.left != null) {
            Node maxLeft = subtreeMax(node.left);
            splay(maxLeft);
            // maxLeft is now root of left subtree
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

    // Public method: Search for key, splay if found, return key or null
    public Integer search(int key) {
        Node node = find(root, key);
        if (node != null) {
            splay(node);
            return node.key;
        }
        return null;
    }

    // Helper: Find node with key
    private Node find(Node curr, int key) {
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

    // Splaying operation: move x to root
    private void splay(Node x) {
        if (x == null)
            return;
        while (x.parent != null) {
            if (x.parent.parent == null) {
                // Zig step
                if (x.parent.left == x)
                    rightRotate(x.parent);
                else
                    leftRotate(x.parent);
            } else if (x.parent.left == x && x.parent.parent.left == x.parent) {
                // Zig-zig step
                rightRotate(x.parent.parent);
                rightRotate(x.parent);
            } else if (x.parent.right == x && x.parent.parent.right == x.parent) {
                // Zig-zig step
                leftRotate(x.parent.parent);
                leftRotate(x.parent);
            } else if (x.parent.left == x && x.parent.parent.right == x.parent) {
                // Zig-zag step
                rightRotate(x.parent);
                leftRotate(x.parent);
            } else {
                // Zig-zag step
                leftRotate(x.parent);
                rightRotate(x.parent);
            }
        }
        root = x;
    }

    // Left rotation at x
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

    // Right rotation at x
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

    // Find max node in subtree
    private Node subtreeMax(Node x) {
        while (x.right != null)
            x = x.right;
        return x;
    }

    // Optional: for debugging, in-order traversal
    public void inorder() {
        inorder(root);
        System.out.println();
    }
    private void inorder(Node x) {
        if (x != null) {
            inorder(x.left);
            System.out.print(x.key + " ");
            inorder(x.right);
        }
    }

    // Optional main method for demonstration
    public static void main(String[] args) {
        SplayTree st = new SplayTree();
        st.insert(10);
        st.insert(20);
        st.insert(30);
        st.insert(40);
        st.insert(50);
        st.inorder(); // 10 20 30 40 50
        System.out.println("Search 30: " + st.search(30)); // 30
        st.inorder(); // 10 20 30 40 50, but 30 is now root
        st.delete(20);
        st.inorder(); // 10 30 40 50
        System.out.println("Search 100: " + st.search(100)); // null
    }
}