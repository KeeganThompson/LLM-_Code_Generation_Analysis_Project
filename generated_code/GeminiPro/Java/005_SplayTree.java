/**
 * A complete, self-contained implementation of an integer set using a Splay Tree.
 * A Splay Tree is a self-balancing binary search tree with the additional property
 * that recently accessed elements are quick to access again. It performs basic
 * operations such as insertion, look-up and removal in O(log n) amortized time.
 */
public class SplayTree {

    /**
     * Represents a node in the Splay Tree. This is a private inner class
     * as it's an implementation detail of the SplayTree.
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
     * Performs a right rotation on the subtree rooted at x.
     * @param x The root of the subtree to rotate.
     * @return The new root of the subtree.
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
     * @return The new root of the subtree.
     */
    private Node leftRotate(Node x) {
        Node y = x.right;
        x.right = y.left;
        y.left = x;
        return y;
    }

    /**
     * Splays the node with the given key to the root of the tree.
     * If the key is not in the tree, the last accessed node on the search path
     * is splayed to the root. This is a top-down splay implementation.
     *
     * @param root The root of the tree/subtree to splay.
     * @param key The key to splay on.
     * @return The new root of the tree after splaying.
     */
    private Node splay(Node root, int key) {
        if (root == null || root.key == key) {
            return root;
        }

        // Use a dummy node to simplify linking of left and right subtrees.
        Node dummy = new Node(0);
        Node leftTreeMax = dummy;
        Node rightTreeMin = dummy;
        Node current = root;

        while (true) {
            if (key < current.key) {
                if (current.left == null) {
                    break;
                }
                // Zig-Zig (Right-Right) case
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
                // Zig-Zig (Left-Left) case
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

        return current;
    }

    /**
     * Searches for a key in the tree.
     * This operation performs a splay on the accessed node (or the last node on the search path),
     * moving it to the root, as required by the splay tree property.
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
            return root.key;
        }
        return null;
    }

    /**
     * Inserts a key into the Splay Tree.
     * If the key already exists, the tree is splayed on that key, but no new node is added.
     *
     * @param key The key to insert.
     */
    public void insert(int key) {
        // If the tree is empty, create a new root
        if (root == null) {
            root = new Node(key);
            return;
        }

        // Splay the tree on the key. This brings the closest node to the root.
        root = splay(root, key);

        // If the key already exists, do nothing (as this is a set)
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
     *
     * @param key The key to delete.
     */
    public void delete(int key) {
        if (root == null) {
            return;
        }

        // Splay the tree on the key. If the key is present, it becomes the root.
        root = splay(root, key);

        // If the key is not in the tree, the root's key won't match. Do nothing.
        if (root.key != key) {
            return;
        }

        // The node to be deleted is now the root. We need to merge its subtrees.
        Node leftSubtree = root.left;
        Node rightSubtree = root.right;

        if (leftSubtree == null) {
            // If there's no left subtree, the right subtree becomes the new tree.
            root = rightSubtree;
        } else {
            // Splay the left subtree to bring its maximum element to its root.
            // We can splay on the key being deleted, as it's guaranteed to be
            // larger than any key in the left subtree.
            leftSubtree = splay(leftSubtree, key);

            // After splaying, the new root of the left subtree (the max element)
            // has no right child. We can attach the original right subtree there.
            leftSubtree.right = rightSubtree;
            root = leftSubtree;
        }
    }
}