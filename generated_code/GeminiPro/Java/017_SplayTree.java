/**
 * A complete, self-contained implementation of a Splay Tree that stores integers.
 * This class functions as an integer set, disallowing duplicate values.
 * The core feature is the splay operation, which moves an accessed element
 * to the root of the tree to optimize for future accesses.
 */
public class SplayTree {

    /**
     * Represents a node within the Splay Tree.
     * It is a private static inner class as it's tightly coupled with SplayTree.
     */
    private static class Node {
        int key;
        Node left;
        Node right;

        /**
         * Constructs a new node with the given integer key.
         *
         * @param key The integer value for this node.
         */
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

    // --- Rotation Helper Methods ---

    /**
     * Performs a right rotation on the subtree rooted at node x.
     * This is a helper method for the splay operation.
     *
     * @param x The root of the subtree to rotate.
     * @return The new root of the rotated subtree.
     */
    private Node rightRotate(Node x) {
        Node y = x.left;
        x.left = y.right;
        y.right = x;
        return y;
    }

    /**
     * Performs a left rotation on the subtree rooted at node x.
     * This is a helper method for the splay operation.
     *
     * @param x The root of the subtree to rotate.
     * @return The new root of the rotated subtree.
     */
    private Node leftRotate(Node x) {
        Node y = x.right;
        x.right = y.left;
        y.left = x;
        return y;
    }

    // --- Core Splay Operation ---

    /**
     * Performs the top-down splay operation on the given key.
     * This operation moves the node with the specified key to the root of the tree.
     * If the key is not found, the last accessed node on the search path is
     * moved to the root instead.
     *
     * @param key The key to splay towards the root.
     */
    private void splay(int key) {
        if (root == null) {
            return;
        }

        // Use a dummy node to simplify linking of left and right subtrees.
        Node header = new Node(0);
        Node leftTreeMax = header;
        Node rightTreeMin = header;

        Node current = root;

        while (true) {
            if (key < current.key) {
                if (current.left == null) {
                    break;
                }
                // Zig-Zig case (Right-Right)
                if (key < current.left.key) {
                    current = rightRotate(current);
                    if (current.left == null) {
                        break;
                    }
                }
                // Link current to the right tree
                rightTreeMin.left = current;
                rightTreeMin = current;
                current = current.left;
            } else if (key > current.key) {
                if (current.right == null) {
                    break;
                }
                // Zig-Zig case (Left-Left)
                if (key > current.right.key) {
                    current = leftRotate(current);
                    if (current.right == null) {
                        break;
                    }
                }
                // Link current to the left tree
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
        current.left = header.right;
        current.right = header.left;

        root = current;
    }

    // --- Public API Methods ---

    /**
     * Inserts a key into the Splay Tree.
     * If the key already exists, the tree is splayed on that key, but no new
     * node is added, as this is an integer set.
     *
     * @param key The integer key to insert.
     */
    public void insert(int key) {
        if (root == null) {
            root = new Node(key);
            return;
        }

        splay(key);

        // If the key is already at the root, it exists in the set.
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
     * Deletes a key from the Splay Tree.
     * If the key is found, it is removed, and the tree is restructured.
     * If the key is not found, the tree is splayed on the last accessed node,
     * but no deletion occurs.
     *
     * @param key The integer key to delete.
     */
    public void delete(int key) {
        if (root == null) {
            return;
        }

        splay(key);

        // If the key is not at the root after splaying, it's not in the tree.
        if (root.key != key) {
            return;
        }

        // The node to delete is now the root.
        Node leftSubtree = root.left;
        Node rightSubtree = root.right;

        if (leftSubtree == null) {
            // If there's no left child, the right subtree becomes the new tree.
            root = rightSubtree;
        } else {
            // The new root will be the largest element in the left subtree.
            // Temporarily make the left subtree the main tree.
            root = leftSubtree;
            // Splay for the (deleted) key. Since this key is larger than any
            // key in the new tree, this will bring the max element to the root.
            splay(key);
            // After splaying, the new root has no right child.
            // Attach the original right subtree here.
            root.right = rightSubtree;
        }
    }

    /**
     * Searches for a key in the tree and performs the splay operation.
     * This method moves the found node to the root. If the node is not found,
     * the last accessed node in the search path is moved to the root.
     *
     * @param key The key to search for.
     * @return The key if it is found; otherwise, returns null.
     */
    public Integer search(int key) {
        if (root == null) {
            return null;
        }
        splay(key);
        // After splaying, the key, if it exists, will be at the root.
        if (root.key == key) {
            return key;
        }
        return null;
    }
}