/**
 * A complete, self-contained implementation of an integer set using a Splay Tree.
 * Splay trees are self-balancing binary search trees with the additional property
 * that recently accessed elements are quick to access again.
 */
public class SplayTree {

    /**
     * Represents a node in the Splay Tree.
     */
    private class Node {
        int key;
        Node left, right;

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

    private Node root;

    /**
     * Constructs an empty Splay Tree.
     */
    public SplayTree() {
        this.root = null;
    }

    /**
     * Performs a right rotation on the given node y.
     * This is a helper function for the splay operation.
     *
     * @param y The node to be rotated.
     * @return The new root of the rotated subtree.
     */
    private Node rightRotate(Node y) {
        Node x = y.left;
        y.left = x.right;
        x.right = y;
        return x;
    }

    /**
     * Performs a left rotation on the given node x.
     * This is a helper function for the splay operation.
     *
     * @param x The node to be rotated.
     * @return The new root of the rotated subtree.
     */
    private Node leftRotate(Node x) {
        Node y = x.right;
        x.right = y.left;
        y.left = x;
        return y;
    }

    /**
     * The core splay operation. It brings the node with the given key
     * (or the last accessed node if the key is not found) to the root of the tree.
     * This implementation uses a top-down splaying approach.
     *
     * @param key The key to splay around.
     */
    private void splay(int key) {
        if (root == null) {
            return;
        }

        // Use a dummy node to simplify linking of left and right subtrees
        Node dummy = new Node(0);
        Node leftTreeMax = dummy;
        Node rightTreeMin = dummy;
        Node current = root;

        while (true) {
            if (key < current.key) {
                if (current.left == null) {
                    break; // Key not found, splay last accessed node
                }
                // Zig-Zig (left-left)
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
                    break; // Key not found, splay last accessed node
                }
                // Zig-Zig (right-right)
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
        current.left = dummy.right;
        current.right = dummy.left;
        root = current;
    }

    /**
     * Inserts a key into the splay tree.
     * If the key already exists, the tree remains unchanged.
     *
     * @param key The integer key to insert.
     */
    public void insert(int key) {
        // If the tree is empty, the new node becomes the root.
        if (root == null) {
            root = new Node(key);
            return;
        }

        // Splay the tree around the key. The closest node will be at the root.
        splay(key);

        // If the key is already present, do nothing.
        if (root.key == key) {
            return;
        }

        // Create the new node and make it the new root.
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
     * Searches for a key in the splay tree.
     * This operation performs a splay, moving the accessed node (or the last
     * node on the search path) to the root.
     *
     * @param key The integer key to search for.
     * @return The key if found, otherwise null.
     */
    public Integer search(int key) {
        if (root == null) {
            return null;
        }
        splay(key);
        // After splaying, if the key exists, it will be at the root.
        if (root.key == key) {
            return key;
        } else {
            return null;
        }
    }

    /**
     * Deletes a key from the splay tree.
     * If the key is not found, the tree remains unchanged.
     *
     * @param key The integer key to delete.
     */
    public void delete(int key) {
        if (root == null) {
            return;
        }

        // Splay the tree around the key.
        splay(key);

        // If the key is not at the root, it's not in the tree.
        if (root.key != key) {
            return;
        }

        // Key is at the root, now delete it.
        Node leftSubtree = root.left;
        Node rightSubtree = root.right;

        if (leftSubtree == null) {
            // If there's no left child, the right child becomes the new root.
            root = rightSubtree;
        } else {
            // Make the left subtree the new tree.
            root = leftSubtree;
            // Splay on the left subtree to bring its max element to the top.
            // Searching for the original (and now deleted) key will do this,
            // as it's guaranteed to be larger than any key in the left subtree.
            splay(key);
            // The new root (max of left subtree) will have a null right child.
            // Attach the original right subtree there.
            root.right = rightSubtree;
        }
    }
}