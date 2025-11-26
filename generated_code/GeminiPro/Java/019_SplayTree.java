/**
 * A complete, self-contained Java class implementing a Splay Tree for an integer set.
 * Splay trees are self-balancing binary search trees with the additional property
 * that recently accessed elements are quick to access again. This implementation
 * provides insert, delete, and search operations.
 */
public class SplayTree {

    /**
     * Inner class representing a node in the Splay Tree.
     */
    private static class Node {
        int key;
        Node left;
        Node right;

        /**
         * Constructor for a new node.
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
     * Default constructor to create an empty Splay Tree.
     */
    public SplayTree() {
        this.root = null;
    }

    /**
     * Performs a right rotation on the subtree rooted at node x.
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
     * @param x The root of the subtree to rotate.
     * @return The new root of the rotated subtree.
     */
    private Node leftRotate(Node x) {
        Node y = x.right;
        x.right = y.left;
        y.left = x;
        return y;
    }

    /**
     * The core splay operation. It moves the node with the given key to the root of the tree.
     * If the key is not found, the last accessed node is moved to the root.
     * This implementation uses a top-down splaying approach.
     * @param key The key to splay on.
     */
    private void splay(int key) {
        if (root == null) {
            return;
        }

        // Use a dummy node to simplify linking.
        // The left subtree of the dummy will hold the "right tree" (nodes > key).
        // The right subtree of the dummy will hold the "left tree" (nodes < key).
        Node dummy = new Node(0);
        Node leftTreeMax = dummy;
        Node rightTreeMin = dummy;
        Node current = root;

        while (true) {
            if (key < current.key) {
                if (current.left == null) {
                    break;
                }
                // Zig-Zig case (left-left)
                if (key < current.left.key) {
                    current = rightRotate(current);
                    if (current.left == null) {
                        break;
                    }
                }
                // Link the current root to the right tree
                rightTreeMin.left = current;
                rightTreeMin = current;
                current = current.left;
            } else if (key > current.key) {
                if (current.right == null) {
                    break;
                }
                // Zig-Zig case (right-right)
                if (key > current.right.key) {
                    current = leftRotate(current);
                    if (current.right == null) {
                        break;
                    }
                }
                // Link the current root to the left tree
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
     * Searches for a key in the tree.
     * This operation performs a splay on the accessed key, moving it (or the last
     * node on the search path) to the root.
     * @param key The key to search for.
     * @return The Integer key if found, otherwise null.
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

    /**
     * Inserts a key into the Splay Tree.
     * If the key already exists, the tree is splayed on that key but not modified.
     * After a new insertion, the new node becomes the root of the tree.
     * @param key The key to insert.
     */
    public void insert(int key) {
        // If the tree is empty, insert the new key as the root.
        if (root == null) {
            root = new Node(key);
            return;
        }

        // Splay the tree around the key.
        // If the key is present, it becomes the root.
        // If not, the node that would be its parent becomes the root.
        splay(key);

        // If the key is already in the tree, do nothing.
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
     * Deletes a key from the Splay Tree.
     * If the key is found, it is splayed to the root, removed, and the remaining
     * subtrees are joined.
     * @param key The key to delete.
     */
    public void delete(int key) {
        if (root == null) {
            return;
        }

        // Splay the key to the root.
        splay(key);

        // If the key is not in the tree, do nothing.
        if (root.key != key) {
            return;
        }

        // Now the node to be deleted is the root.
        Node leftSubtree = root.left;
        Node rightSubtree = root.right;

        if (leftSubtree == null) {
            // If there's no left child, the right child becomes the new root.
            root = rightSubtree;
        } else {
            // Make the left subtree the new tree.
            root = leftSubtree;
            // Splay on the key `key` in the new tree. Since `key` is larger than any
            // element in this subtree, this will bring the maximum element of the
            // left subtree to the root.
            splay(key);
            // Attach the original right subtree to the new root.
            root.right = rightSubtree;
        }
    }
}