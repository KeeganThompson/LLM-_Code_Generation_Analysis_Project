/**
 * A complete, self-contained implementation of an integer set using a Splay Tree.
 * A splay tree is a self-adjusting binary search tree with the additional
 * property that recently accessed elements are quick to access again. All major
 * operations (insert, delete, search) involve a "splaying" step, which moves the
 * accessed or modified node to the root of the tree.
 */
public class SplayTree {

    /**
     * Represents a node in the Splay Tree.
     */
    private class Node {
        int key;
        Node left, right;

        Node(int key) {
            this.key = key;
            this.left = null;
            this.right = null;
        }
    }

    private Node root;

    /**
     * Constructs an empty Splay Tree.
     */
    public SplayTree() {
        this.root = null;
    }

    /**
     * Performs a right rotation on the given node.
     *
     * @param x The node to rotate.
     * @return The new root of the rotated subtree.
     */
    private Node rightRotate(Node x) {
        Node y = x.left;
        x.left = y.right;
        y.right = x;
        return y;
    }

    /**
     * Performs a left rotation on the given node.
     *
     * @param x The node to rotate.
     * @return The new root of the rotated subtree.
     */
    private Node leftRotate(Node x) {
        Node y = x.right;
        x.right = y.left;
        y.left = x;
        return y;
    }

    /**
     * The core splaying operation. It brings the node with the given key
     * (or the last accessed node if the key is not found) to the root of the tree.
     * This is an implementation of the top-down splaying algorithm.
     *
     * @param root The root of the tree (or subtree) to splay.
     * @param key  The key to splay around.
     * @return The new root of the splayed tree.
     */
    private Node splay(Node root, int key) {
        if (root == null || root.key == key) {
            return root;
        }

        // Create a dummy node to simplify linking.
        Node header = new Node(0);
        Node leftTreeMax = header;
        Node rightTreeMin = header;

        while (true) {
            if (key < root.key) {
                if (root.left == null) break;
                // Zig-Zig (left-left)
                if (key < root.left.key) {
                    root = rightRotate(root);
                }
                if (root.left == null) break;
                // Link the old root to the right tree
                rightTreeMin.left = root;
                rightTreeMin = root;
                root = root.left;
            } else if (key > root.key) {
                if (root.right == null) break;
                // Zig-Zig (right-right)
                if (key > root.right.key) {
                    root = leftRotate(root);
                }
                if (root.right == null) break;
                // Link the old root to the left tree
                leftTreeMax.right = root;
                leftTreeMax = root;
                root = root.right;
            } else { // key == root.key
                break;
            }
        }

        // Reassemble the tree
        leftTreeMax.right = root.left;
        rightTreeMin.left = root.right;
        root.left = header.right;
        root.right = header.left;

        return root;
    }

    /**
     * Inserts a key into the Splay Tree. Duplicates are not allowed.
     * After insertion, the new node becomes the root of the tree.
     *
     * @param key The key to insert.
     */
    public void insert(int key) {
        // Case 1: The tree is empty.
        if (root == null) {
            root = new Node(key);
            return;
        }

        // Splay the tree around the key. The node closest to the key will be the new root.
        root = splay(root, key);

        // Case 2: The key is already present, do nothing.
        if (root.key == key) {
            return;
        }

        // Create the new node which will become the new root.
        Node newNode = new Node(key);

        // The old root is split into two subtrees based on the new key.
        if (key < root.key) {
            newNode.right = root;
            newNode.left = root.left;
            root.left = null; // Detach the left subtree from the old root.
        } else { // key > root.key
            newNode.left = root;
            newNode.right = root.right;
            root.right = null; // Detach the right subtree from the old root.
        }
        root = newNode; // The new node is the new root.
    }

    /**
     * Searches for a key in the tree. If the key is found, the corresponding node
     * is splayed to the root. If not found, the last accessed node is splayed.
     *
     * @param key The key to search for.
     * @return The key if found, otherwise null.
     */
    public Integer search(int key) {
        if (root == null) {
            return null;
        }
        root = splay(root, key);
        if (root.key == key) {
            return key;
        }
        return null;
    }

    /**
     * Deletes a key from the Splay Tree.
     *
     * @param key The key to delete.
     */
    public void delete(int key) {
        if (root == null) {
            return; // Tree is empty.
        }

        // Splay the tree to bring the node with the given key to the root.
        root = splay(root, key);

        // If the key is not at the root, it wasn't in the tree.
        if (root.key != key) {
            return; // Key not found.
        }

        // Now, the node to delete is the root.
        Node leftSubtree = root.left;
        Node rightSubtree = root.right;

        if (leftSubtree == null) {
            // If there's no left subtree, the right subtree becomes the new tree.
            root = rightSubtree;
        } else {
            // Splay the left subtree to bring its maximum element to its root.
            // Since `key` is greater than any element in the left subtree, splaying
            // for `key` will achieve this.
            Node newRoot = splay(leftSubtree, key);

            // The new root of the combined tree (which was the max of the left subtree)
            // will have its right child set to the original right subtree.
            newRoot.right = rightSubtree;
            root = newRoot;
        }
    }
}