/**
 * A complete, self-contained implementation of a Splay Tree for an integer set.
 *
 * A splay tree is a self-adjusting binary search tree with the additional
 * property that recently accessed elements are quick to access again. It performs
 * basic operations such as insertion, look-up and removal in O(log n) amortized time.
 *
 * This class provides the following public methods:
 * - {@code insert(int key)}: Adds a key to the set.
 * - {@code delete(int key)}: Removes a key from the set.
 * - {@code search(int key)}: Searches for a key and returns it, or null if not found.
 *
 * The search, insert, and delete operations all perform a "splay" operation, which
 * moves the accessed (or inserted/deleted) node to the root of the tree to optimize
 * future accesses.
 */
public class SplayTree {

    private Node root;

    /**
     * Represents a node in the splay tree.
     * This is a private static inner class as it's only used by SplayTree.
     */
    private static class Node {
        int key;
        Node left;
        Node right;

        Node(int key) {
            this.key = key;
            this.left = null;
            this.right = null;
        }
    }

    /**
     * Constructs an empty SplayTree.
     */
    public SplayTree() {
        this.root = null;
    }

    // --- Private Helper Methods for Rotations ---

    /**
     * Performs a right rotation on the given node `x`.
     * This is a standard tree rotation operation.
     *
     * @param x The node to rotate.
     * @return The new root of the rotated subtree.
     */
    private Node rotateRight(Node x) {
        Node y = x.left;
        x.left = y.right;
        y.right = x;
        return y;
    }

    /**
     * Performs a left rotation on the given node `x`.
     * This is a standard tree rotation operation.
     *
     * @param x The node to rotate.
     * @return The new root of the rotated subtree.
     */
    private Node rotateLeft(Node x) {
        Node y = x.right;
        x.right = y.left;
        y.left = x;
        return y;
    }

    /**
     * The core splaying operation. It moves the node with the given key
     * (or the last accessed node if the key is not found) to the root of the tree.
     * This implementation uses the top-down splaying approach, which restructures
     * the tree as it searches for the key from the root down.
     *
     * @param key The key to splay to the root.
     */
    private void splay(int key) {
        if (root == null) {
            return;
        }

        // Create a dummy node to simplify linking.
        // The left child of the dummy will be the root of the "right tree" (R).
        // The right child of the dummy will be the root of the "left tree" (L).
        Node dummy = new Node(0); // Key doesn't matter
        Node leftTreeMax = dummy;
        Node rightTreeMin = dummy;
        Node current = root;

        while (true) {
            if (key < current.key) {
                if (current.left == null) break;
                // Zig-Zig case (left-left)
                if (key < current.left.key) {
                    current = rotateRight(current);
                    if (current.left == null) break;
                }
                // Add current to the right tree (R)
                rightTreeMin.left = current;
                rightTreeMin = current;
                current = current.left;
            } else if (key > current.key) {
                if (current.right == null) break;
                // Zig-Zig case (right-right)
                if (key > current.right.key) {
                    current = rotateLeft(current);
                    if (current.right == null) break;
                }
                // Add current to the left tree (L)
                leftTreeMax.right = current;
                leftTreeMax = current;
                current = current.right;
            } else { // key == current.key
                break;
            }
        }

        // Reassemble the tree
        leftTreeMax.right = current.left;
        rightTreeMin.left = current.right;
        current.left = dummy.right;
        current.right = dummy.left;
        root = current;
    }

    // --- Public API Methods ---

    /**
     * Inserts a key into the splay tree.
     * If the key already exists in the set, this operation has no effect
     * besides splaying the existing node to the root.
     *
     * @param key The key to insert.
     */
    public void insert(int key) {
        if (root == null) {
            root = new Node(key);
            return;
        }

        splay(key);

        // If key is already present, we are done (it's now the root).
        if (root.key == key) {
            return;
        }

        Node newNode = new Node(key);
        if (key < root.key) {
            newNode.right = root;
            newNode.left = root.left;
            root.left = null;
        } else { // key > root.key
            newNode.left = root;
            newNode.right = root.right;
            root.right = null;
        }
        root = newNode;
    }

    /**
     * Deletes a key from the splay tree.
     * If the key is found and deleted, the parent of the deleted node (or the
     * predecessor, if the deleted node was the root) is splayed to the root.
     * If the key is not found, the tree is splayed on the last accessed node.
     *
     * @param key The key to delete.
     */
    public void delete(int key) {
        if (root == null) {
            return;
        }

        splay(key);

        // If the key is not in the tree, do nothing.
        if (root.key != key) {
            return;
        }

        // Now the node to be deleted is the root.
        Node leftSubtree = root.left;
        Node rightSubtree = root.right;

        if (leftSubtree == null) {
            root = rightSubtree;
        } else {
            // Make the left subtree the new tree.
            root = leftSubtree;
            // Splay for the (now non-existent) key. This brings the largest element
            // in the left subtree (the predecessor of the deleted key) to its root.
            splay(key);
            
            // The new root (predecessor) will have a null right child.
            // Attach the original right subtree there.
            root.right = rightSubtree;
        }
    }

    /**
     * Searches for a key in the splay tree.
     * If the key is found, the corresponding node is splayed to the root.
     * If not found, the last accessed node in the search path is splayed to the root.
     *
     * @param key The key to search for.
     * @return The key if found, otherwise null.
     */
    public Integer search(int key) {
        if (root == null) {
            return null;
        }
        splay(key);
        // After splaying, the root will be the key if it exists.
        if (root.key == key) {
            return key;
        }
        return null;
    }
}