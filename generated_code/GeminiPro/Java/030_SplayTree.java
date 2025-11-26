/**
 * A complete, self-contained Java class that implements an integer set using a Splay Tree.
 * A splay tree is a self-adjusting binary search tree with the property that
 * recently accessed elements are quick to access again. It performs basic
 * operations such as insertion, deletion, and search in O(log n) amortized time.
 */
public class SplayTree {

    /**
     * Represents a node in the Splay Tree.
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

    private Node root;

    /**
     * Constructs an empty Splay Tree.
     */
    public SplayTree() {
        this.root = null;
    }

    // --- Private Helper Methods for Splay and Rotations ---

    /**
     * Performs a right rotation on the subtree rooted at node y.
     * @param y The root of the subtree to rotate.
     * @return The new root of the subtree.
     */
    private Node rotateRight(Node y) {
        Node x = y.left;
        y.left = x.right;
        x.right = y;
        return x;
    }

    /**
     * Performs a left rotation on the subtree rooted at node x.
     * @param x The root of the subtree to rotate.
     * @return The new root of the subtree.
     */
    private Node rotateLeft(Node x) {
        Node y = x.right;
        x.right = y.left;
        y.left = x;
        return y;
    }

    /**
     * The splay operation moves the node with the given key (or the last accessed
     * node if the key is not found) to the root of the tree. This method uses a
     * top-down, iterative approach.
     * @param key The key of the node to splay to the root.
     */
    private void splay(int key) {
        if (root == null) {
            return;
        }

        // Use a dummy node to simplify linking of left and right subtrees.
        Node dummy = new Node(0);
        Node leftTreeMax = dummy;
        Node rightTreeMin = dummy;
        Node current = root;

        while (true) {
            if (key < current.key) {
                if (current.left == null) break;
                // Zig-Zig (left-left)
                if (key < current.left.key) {
                    current = rotateRight(current);
                    if (current.left == null) break;
                }
                // Link current to the right tree (nodes > key)
                rightTreeMin.left = current;
                rightTreeMin = current;
                current = current.left;
            } else if (key > current.key) {
                if (current.right == null) break;
                // Zig-Zig (right-right)
                if (key > current.right.key) {
                    current = rotateLeft(current);
                    if (current.right == null) break;
                }
                // Link current to the left tree (nodes < key)
                leftTreeMax.right = current;
                leftTreeMax = current;
                current = current.right;
            } else {
                // Key found
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
     * Inserts a key into the splay tree. If the key already exists, the tree
     * is splayed on that key, but no new node is inserted.
     *
     * @param key The integer key to insert.
     */
    public void insert(int key) {
        if (root == null) {
            root = new Node(key);
            return;
        }

        splay(key);

        // If key is already present, do nothing (tree is already splayed)
        if (root.key == key) {
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
     * Deletes a key from the splay tree. If the key is not in the tree,
     * the tree is splayed on the last accessed node and no deletion occurs.
     *
     * @param key The integer key to delete.
     */
    public void delete(int key) {
        if (root == null) {
            return;
        }

        splay(key);

        // If key is not in the tree, do nothing
        if (root.key != key) {
            return;
        }

        // Key is at the root, now remove it
        Node leftSubtree = root.left;
        Node rightSubtree = root.right;

        if (leftSubtree == null) {
            root = rightSubtree;
        } else {
            // Splay the largest element in the left subtree to its root.
            // This is achieved by splaying for the deleted key (which is guaranteed
            // to be larger than any key in the left subtree), causing the
            // maximum element to rise to the root of the left subtree.
            root = leftSubtree;
            splay(key);
            
            // Attach the original right subtree
            root.right = rightSubtree;
        }
    }

    /**
     * Searches for a key in the tree and splays the accessed node to the root.
     *
     * @param key The key to search for.
     * @return The key if found, otherwise {@code null}.
     */
    public Integer search(int key) {
        if (root == null) {
            return null;
        }
        splay(key);
        if (root.key == key) {
            return key;
        }
        return null;
    }
}