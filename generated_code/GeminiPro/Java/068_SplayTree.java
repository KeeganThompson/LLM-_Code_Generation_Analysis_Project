/**
 * A complete, self-contained implementation of a Splay Tree for an integer set.
 * Splay trees are self-balancing binary search trees with the additional property
 * that recently accessed elements are quick to access again. This implementation
 * uses a top-down splaying approach.
 */
public class SplayTree {

    private Node root;

    /**
     * Represents a node in the Splay Tree.
     */
    private static class Node {
        int key;
        Node left;
        Node right;

        /**
         * Constructs a new node with the given key.
         * @param key The integer key for the node.
         */
        Node(int key) {
            this.key = key;
            this.left = null;
            this.right = null;
        }
    }

    /**
     * Constructs an empty Splay Tree.
     */
    public SplayTree() {
        this.root = null;
    }

    /**
     * Right-rotates the subtree rooted at y.
     * @param y The root of the subtree to rotate.
     * @return The new root of the subtree.
     */
    private Node rightRotate(Node y) {
        Node x = y.left;
        y.left = x.right;
        x.right = y;
        return x;
    }

    /**
     * Left-rotates the subtree rooted at x.
     * @param x The root of the subtree to rotate.
     * @return The new root of the subtree.
     */
    private Node leftRotate(Node x) {
        Node y = x.right;
        x.right = y.left;
        y.left = x;
        return y;
    }

    /**
     * Performs the splay operation. Moves the node with the specified key,
     * or the last accessed node if the key is not found, to the root of the tree.
     * This is a top-down splay implementation.
     * @param key The key to splay around.
     */
    private void splay(int key) {
        if (root == null) {
            return;
        }

        // Dummy node to simplify linking
        Node header = new Node(0);
        Node leftTreeMax = header;
        Node rightTreeMin = header;
        Node current = root;

        while (true) {
            if (key < current.key) {
                if (current.left == null) {
                    break;
                }
                // Zig-Zig (Left-Left)
                if (key < current.left.key) {
                    current = rightRotate(current);
                    if (current.left == null) {
                        break;
                    }
                }
                // Link to the right tree
                rightTreeMin.left = current;
                rightTreeMin = current;
                current = current.left;
            } else if (key > current.key) {
                if (current.right == null) {
                    break;
                }
                // Zig-Zig (Right-Right)
                if (key > current.right.key) {
                    current = leftRotate(current);
                    if (current.right == null) {
                        break;
                    }
                }
                // Link to the left tree
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
        current.left = header.right;
        current.right = header.left;

        root = current;
    }

    /**
     * Inserts a key into the set. If the key already exists, the tree remains unchanged.
     * After insertion, the new node becomes the root of the tree.
     * @param key The key to insert.
     */
    public void insert(int key) {
        Node newNode = new Node(key);

        if (root == null) {
            root = newNode;
            return;
        }

        // Splay the tree around the key. The closest node will be at the root.
        splay(key);

        // If key is already present, do nothing (as this is a set).
        if (root.key == key) {
            return;
        }

        if (key < root.key) {
            newNode.left = root.left;
            newNode.right = root;
            root.left = null;
            root = newNode;
        } else { // key > root.key
            newNode.right = root.right;
            newNode.left = root;
            root.right = null;
            root = newNode;
        }
    }

    /**
     * Deletes a key from the set. If the key is not found, the tree remains unchanged.
     * @param key The key to delete.
     */
    public void delete(int key) {
        if (root == null) {
            return;
        }

        // Splay the tree around the key.
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
            // Splay for the key we are deleting. Since this key is larger
            // than any key in the new tree (the left subtree), this will
            // bring the maximum element of the left subtree to the root.
            splay(key);
            // The new root (max of left subtree) will have a null right child.
            // Attach the original right subtree there.
            root.right = rightSubtree;
        }
    }

    /**
     * Searches for a key in the set. If the key is found, the corresponding node
     * is splayed to the root of the tree.
     * @param key The key to search for.
     * @return The key if it is found, otherwise null.
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