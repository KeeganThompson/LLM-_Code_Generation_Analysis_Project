public class SplayTree {
    private class Node {
        int key;
        Node left, right;

        Node(int key) {
            this.key = key;
        }
    }

    private Node root;

    // Right rotate
    private Node rightRotate(Node x) {
        Node y = x.left;
        x.left = y.right;
        y.right = x;
        return y;
    }

    // Left rotate
    private Node leftRotate(Node x) {
        Node y = x.right;
        x.right = y.left;
        y.left = x;
        return y;
    }

    // Splay the node with given key to the root.
    private Node splay(Node root, int key) {
        if (root == null || root.key == key)
            return root;

        // Key lies in left subtree
        if (key < root.key) {
            if (root.left == null) return root;

            // Zig-Zig (Left Left)
            if (key < root.left.key) {
                root.left.left = splay(root.left.left, key);
                root = rightRotate(root);
            }
            // Zig-Zag (Left Right)
            else if (key > root.left.key) {
                root.left.right = splay(root.left.right, key);
                if (root.left.right != null)
                    root.left = leftRotate(root.left);
            }

            return (root.left == null) ? root : rightRotate(root);
        }
        // Key lies in right subtree
        else {
            if (root.right == null) return root;

            // Zag-Zig (Right Left)
            if (key < root.right.key) {
                root.right.left = splay(root.right.left, key);
                if (root.right.left != null)
                    root.right = rightRotate(root.right);
            }
            // Zag-Zag (Right Right)
            else if (key > root.right.key) {
                root.right.right = splay(root.right.right, key);
                root = leftRotate(root);
            }

            return (root.right == null) ? root : leftRotate(root);
        }
    }

    /**
     * Inserts a key into the set. If the key already exists, does nothing.
     */
    public void insert(int key) {
        if (root == null) {
            root = new Node(key);
            return;
        }
        root = splay(root, key);
        if (root.key == key) {
            // Already exists
            return;
        }
        Node newNode = new Node(key);
        if (key < root.key) {
            newNode.right = root;
            newNode.left = root.left;
            root.left = null;
        } else {
            newNode.left = root;
            newNode.right = root.right;
            root.right = null;
        }
        root = newNode;
    }

    /**
     * Deletes a key from the set. Does nothing if key is not present.
     */
    public void delete(int key) {
        if (root == null) return;
        root = splay(root, key);
        if (root.key != key) {
            // Not found
            return;
        }
        // Now root.key == key
        if (root.left == null) {
            root = root.right;
        } else {
            Node temp = root.right;
            root = splay(root.left, key); // Splay the max of left subtree
            root.right = temp;
        }
    }

    /**
     * Searches for a key in the set. Returns the key if found, else null.
     * The accessed node (if any) is splayed to the root.
     */
    public Integer search(int key) {
        root = splay(root, key);
        if (root != null && root.key == key) {
            return root.key;
        }
        return null;
    }

    // Optional: For testing
    /*
    public void inorder() {
        inorder(root);
        System.out.println();
    }

    private void inorder(Node node) {
        if (node != null) {
            inorder(node.left);
            System.out.print(node.key + " ");
            inorder(node.right);
        }
    }

    public static void main(String[] args) {
        SplayTree st = new SplayTree();
        st.insert(10);
        st.insert(20);
        st.insert(5);
        st.inorder(); // 5 10 20
        System.out.println(st.search(10)); // 10
        st.inorder(); // 5 10 20 (10 is root)
        st.delete(10);
        st.inorder(); // 5 20
        System.out.println(st.search(10)); // null
    }
    */
}