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
        Node curr = root, parent = null;
        while (curr != null) {
            parent = curr;
            if (key < curr.key)
                curr = curr.left;
            else if (key > curr.key)
                curr = curr.right;
            else {
                splay(curr);
                return; // Key already exists, do nothing
            }
        }
        Node newNode = new Node(key, parent);
        if (key < parent.key)
            parent.left = newNode;
        else
            parent.right = newNode;
        splay(newNode);
    }

    // Public delete method
    public void delete(int key) {
        Node node = findNode(key);
        if (node == null)
            return;
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
                if (min.right != null)
                    min.right.parent = min;
            }
            replace(node, min);
            min.left = node.left;
            if (min.left != null)
                min.left.parent = min;
        }
        node.left = node.right = node.parent = null; // Help GC
    }

    // Public search method
    public Integer search(int key) {
        Node node = findNode(key);
        if (node != null) {
            splay(node);
            return node.key;
        }
        return null;
    }

    // Helper: Find node with key (without splaying)
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

    // Helper: Replace subtree u with v
    private void replace(Node u, Node v) {
        if (u.parent == null) {
            root = v;
        } else if (u == u.parent.left) {
            u.parent.left = v;
        } else {
            u.parent.right = v;
        }
        if (v != null)
            v.parent = u.parent;
    }

    // Helper: Find minimum node in subtree
    private Node subtreeMin(Node node) {
        while (node.left != null)
            node = node.left;
        return node;
    }

    // Splay operation
    private void splay(Node x) {
        if (x == null)
            return;
        while (x.parent != null) {
            if (x.parent.parent == null) {
                // Zig
                if (x == x.parent.left)
                    rotateRight(x.parent);
                else
                    rotateLeft(x.parent);
            } else if (x == x.parent.left && x.parent == x.parent.parent.left) {
                // Zig-zig left
                rotateRight(x.parent.parent);
                rotateRight(x.parent);
            } else if (x == x.parent.right && x.parent == x.parent.parent.right) {
                // Zig-zig right
                rotateLeft(x.parent.parent);
                rotateLeft(x.parent);
            } else if (x == x.parent.right && x.parent == x.parent.parent.left) {
                // Zig-zag left-right
                rotateLeft(x.parent);
                rotateRight(x.parent);
            } else {
                // Zig-zag right-left
                rotateRight(x.parent);
                rotateLeft(x.parent);
            }
        }
    }

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

    // For testing purposes: Inorder traversal
    public void inorder() {
        inorderHelper(root);
        System.out.println();
    }

    private void inorderHelper(Node node) {
        if (node == null)
            return;
        inorderHelper(node.left);
        System.out.print(node.key + " ");
        inorderHelper(node.right);
    }

    // Main for demonstration (can be removed)
    public static void main(String[] args) {
        SplayTree st = new SplayTree();
        st.insert(10);
        st.insert(20);
        st.insert(5);
        st.inorder(); // 5 10 20
        System.out.println(st.search(10)); // 10
        st.inorder(); // 5 10 20
        st.delete(10);
        st.inorder(); // 5 20
        System.out.println(st.search(10)); // null
    }
}