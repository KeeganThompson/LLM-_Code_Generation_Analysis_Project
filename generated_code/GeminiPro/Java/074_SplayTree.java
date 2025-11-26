/**
 * A complete, self-contained Java class that implements an integer set using a Splay Tree.
 * Splay trees are self-balancing binary search trees with the property that recently
 * accessed elements are moved to the root, providing fast access for future requests.
 */
public class SplayTree {

    /**
     * Inner class representing a node in the Splay Tree.
     */
    private class Node {
        int key;
        Node left, right;

        /**
         * Constructs a new node with the given key.
         * @param key The integer value for the node.
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
     * Performs a right rotation on the subtree rooted at node x.
     * This is a helper function for the splay operation.
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
     * Performs a left rotation on the subtree rooted at node x.
     * This is a helper function for the splay operation.
     * @param x The root of the subtree to rotate.
     * @return The new root of the subtree after rotation.
     */
    private Node leftRotate(Node x) {
        Node y = x.right;
        x.right = y.left;
        y.left = x;
        return y;
    }

    /**
     * Splays the node with the given key (or the last accessed node on the search path)
     * to the root of the tree. This is the core operation of the Splay Tree, which
     * keeps the tree balanced and efficient for recently accessed items.
     * This implementation uses a top-down, iterative approach.
     *
     * @param key The key of the node to splay to the root.
     */
    private void splay(int key) {
        if (root == null) {
            return;
        }

        // Dummy node to simplify linking of left and right subtrees.
        Node dummy = new Node(0);
        Node leftTreeMax = dummy;
        Node rightTreeMin = dummy;
        Node current = root;

        while (true) {
            if (key < current.key) {
                if (current.left == null) break;
                // Zig-Zig case (Right-Right)
                if (key < current.left.key) {
                    current = rightRotate(current);
                    if (current.left == null) break;
                }
                // Link current node to the right tree (R)
                rightTreeMin.left = current;
                rightTreeMin = current;
                current = current.left;
            } else if (key > current.key) {
                if (current.right == null) break;
                // Zig-Zig case (Left-Left)
                if (key > current.right.key) {
                    current = leftRotate(current);
                    if (current.right == null) break;
                }
                // Link current node to the left tree (L)
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
     * Inserts a key into the Splay Tree.
     * If the key already exists, the tree is splayed on that key but otherwise remains unchanged.
     *
     * @param key The integer key to insert.
     */
    public void insert(int key) {
        if (root == null) {
            root = new Node(key);
            return;
        }

        // Splay the tree on the key. The closest node becomes the root.
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
        } else { // key > root.key
            newNode.left = root;
            newNode.right = root.right;
            root.right = null;
        }
        root = newNode;
    }

    /**
     * Searches for a key in the Splay Tree.
     * As a side effect, this operation splays the accessed node (or the last node on the search path)
     * to the root, making subsequent accesses to it faster.
     *
     * @param key The key to search for.
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
        }
        return null;
    }

    /**
     * Deletes a key from the Splay Tree.
     * If the key is not found, the tree is splayed on the last accessed node
     * but otherwise remains unchanged.
     *
     * @param key The key to delete.
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
        if (root.left == null) {
            // If there's no left child, the right child becomes the new root.
            root = root.right;
        } else {
            // If there is a left child, we make it the new tree.
            Node rightSubtree = root.right;
            root = root.left;
            // Splay on the key again in the new tree (the former left subtree).
            // This brings the maximum element of the left subtree (the predecessor of the deleted key)
            // to the root of this new tree.
            splay(key);
            // The new root (predecessor) is guaranteed to have no right child,
            // so we can safely attach the original right subtree there.
            root.right = rightSubtree;
        }
    }
}