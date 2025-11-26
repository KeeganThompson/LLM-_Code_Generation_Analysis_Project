public class SplayTree {
    private class Node {
        int key;
        Node left, right;

        Node(int key) {
            this.key = key;
        }
    }

    private Node root;

    public void insert(int key) {
        if (root == null) {
            root = new Node(key);
            return;
        }
        root = splay(root, key);
        if (root.key == key) {
            return; // key already present
        }
        Node node = new Node(key);
        if (key < root.key) {
            node.left = root.left;
            node.right = root;
            root.left = null;
            root = node;
        } else {
            node.right = root.right;
            node.left = root;
            root.right = null;
            root = node;
        }
    }

    public void delete(int key) {
        if (root == null) return;
        root = splay(root, key);
        if (root.key != key) return; // key not present

        if (root.left == null) {
            root = root.right;
        } else {
            Node temp = root.right;
            root = splay(root.left, key);
            root.right = temp;
        }
    }

    public Integer search(int key) {
        if (root == null) return null;
        root = splay(root, key);
        return root.key == key ? root.key : null;
    }

    // Splay operation: brings the node with given key to the root if it exists,
    // or the last accessed node (where the key would be) to the root if not found.
    private Node splay(Node t, int key) {
        if (t == null) return null;

        Node header = new Node(0); // Temporary tree root
        Node LeftTreeMax = header;
        Node RightTreeMin = header;

        while (true) {
            if (key < t.key) {
                if (t.left == null) break;
                if (key < t.left.key) {
                    t = rotateRight(t);
                    if (t.left == null) break;
                }
                // Link to right tree
                RightTreeMin.left = t;
                RightTreeMin = t;
                t = t.left;
            } else if (key > t.key) {
                if (t.right == null) break;
                if (key > t.right.key) {
                    t = rotateLeft(t);
                    if (t.right == null) break;
                }
                // Link to left tree
                LeftTreeMax.right = t;
                LeftTreeMax = t;
                t = t.right;
            } else {
                break;
            }
        }
        // Reassemble
        LeftTreeMax.right = t.left;
        RightTreeMin.left = t.right;
        t.left = header.right;
        t.right = header.left;
        return t;
    }

    private Node rotateRight(Node n) {
        Node l = n.left;
        n.left = l.right;
        l.right = n;
        return l;
    }

    private Node rotateLeft(Node n) {
        Node r = n.right;
        n.right = r.left;
        r.left = n;
        return r;
    }
}