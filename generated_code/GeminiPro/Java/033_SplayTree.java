/**
 * A self-contained Java class implementing a Splay Tree for an integer set.
 * Splay trees are self-balancing binary search trees with the additional property
 * that recently accessed elements are quick to access again.
 */
public class SplayTree {

    /**
     * Inner class representing a node in the Splay Tree.
     */
    private class Node {
        int key;
        Node left, right;

        /**
         * Constructor for a Node.
         * @param key The integer key for the node.
         */
        Node(int key) {
            this.key = key;
            this.left = null;
            this.right = null;
        }
    }

    private Node root;

    /**
     * Constructs an empty SplayTree.
     */
    public SplayTree() {
        this.root = null;
    }

    // --- Private Helper Methods for Rotations ---

    /**
     * Performs a right rotation on the subtree rooted at x.
     * @param x The root of the subtree to rotate.
     * @return The new root of the subtree after rotation.
     */
    private Node rightRotate(Node x) {
        Node y = x.left;
        x.left = y.right;
        y.right = x;
        return y;
    }

    /**
     * Performs a left rotation on the subtree rooted at x.
     * @param x The root of the subtree to rotate.
     * @return The new root of the subtree after rotation.
     */
    private Node leftRotate(Node x) {
        Node y = x.right;
        x.right = y.left;
        y.left = x;
        return y;
    }

    // --- Splay Operation ---

    /**
     * The main splay operation. It brings the node with the given key
     * (or the last accessed node on the search path if the key is not found)
     * to the root of the tree. This is a top-down splay implementation.
     *
     * @param key The key to splay around.
     */
    private void splay(int key) {
        if (root == null) {
            return;
        }

        // A dummy node to simplify linking of left and right subtrees.
        Node header = new Node(0);
        Node leftTreeMax = header;
        Node rightTreeMin = header;
        Node t = root;

        while (true) {
            if (key < t.key) {
                if (t.left == null) break;
                // Zig-Zig (Right-Right) case
                if (key < t.left.key) {
                    t = rightRotate(t);
                    if (t.left == null) break;
                }
                // Link Right: Add current root `t` to the right tree
                rightTreeMin.left = t;
                rightTreeMin = t;
                t = t.left;
            } else if (key > t.key) {
                if (t.right == null) break;
                // Zig-Zig (Left-Left) case
                if (key > t.right.key) {
                    t = leftRotate(t);
                    if (t.right == null) break;
                }
                // Link Left: Add current root `t` to the left tree
                leftTreeMax.right = t;
                leftTreeMax = t;
                t = t.right;
            } else {
                // Key found, break the loop
                break;
            }
        }

        // Reassemble the tree
        leftTreeMax.right = t.left;
        rightTreeMin.left = t.right;
        t.left = header.right;
        t.right = header.left;
        root = t;
    }

    // --- Public API Methods ---

    /**
     * Inserts a key into the splay tree.
     * If the key already exists, the tree is splayed on that key.
     *
     * @param key The integer key to insert.
     */
    public void insert(int key) {
        // If the tree is empty, the new node becomes the root.
        if (root == null) {
            root = new Node(key);
            return;
        }

        // Splay the tree around the key. If the key is present, it becomes the root.
        // If not, the last accessed node on the search path becomes the root.
        splay(key);

        // If the key is already at the root, we are done.
        if (root.key == key) {
            return;
        }

        Node newNode = new Node(key);
        if (key < root.key) {
            newNode.right = root;
            newNode.left = root.left;
            root.left = null;
            root = newNode;
        } else { // key > root.key
            newNode.left = root;
            newNode.right = root.right;
            root.right = null;
            root = newNode;
        }
    }

    /**
     * Searches for a key in the splay tree.
     * This operation performs a splay, moving the accessed node (or the last
     * node on the search path) to the root.
     *
     * @param key The key to search for.
     * @return The key if found, otherwise null.
     */
    public Integer search(int key) {
        if (root == null) {
            return null;
        }
        splay(key);
        // After splaying, if the root's key matches, the key was found.
        if (root.key == key) {
            return root.key;
        }
        return null;
    }

    /**
     * Deletes a key from the splay tree.
     * If the key is found, it is deleted, and the tree is rebalanced.
     * The splay operation is performed on the key before deletion.
     *
     * @param key The key to delete.
     */
    public void delete(int key) {
        if (root == null) {
            return;
        }

        // Splay the tree to bring the node to delete (or its parent) to the root.
        splay(key);

        // If the key is not in the tree, the root will be the closest node, but not the key.
        if (root.key != key) {
            return; // Key not found, nothing to delete.
        }

        // Now, the node to delete is the root.
        Node leftSubtree = root.left;
        Node rightSubtree = root.right;

        if (leftSubtree == null) {
            // If there's no left child, the right child becomes the new root.
            root = rightSubtree;
        } else {
            // Make the left subtree the main tree.
            root = leftSubtree;
            // Splay on the key we are deleting. Since this key is larger than any element
            // in the left subtree, this will bring the maximum element of the left subtree
            // to its root.
            splay(key);
            // Attach the original right subtree to the new root.
            root.right = rightSubtree;
        }
    }
}