/**
 * A complete, self-contained Java class that implements an integer set using a Splay Tree.
 *
 * A splay tree is a self-balancing binary search tree with the additional
 * property that recently accessed elements are quick to access again.
 * It performs basic operations such as insertion, look-up, and removal
 * in O(log n) amortized time. All core operations (insert, delete, search)
 * perform a "splay" operation, which moves the accessed (or inserted/deleted)
 * node to the root of the tree.
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
        public Node(int key) {
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
        root = null;
    }

    /**
     * Performs a right rotation on the subtree rooted at x.
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
     * Performs a left rotation on the subtree rooted at x.
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
     * Splays the node with the given key to the root of the tree.
     * If the key is not found, the last accessed node on the search path is splayed to the root.
     * This is a recursive, bottom-up splaying implementation.
     *
     * @param h The root of the current subtree.
     * @param key The key to splay towards the root.
     * @return The new root of the splayed subtree.
     */
    private Node splay(Node h, int key) {
        if (h == null || h.key == key) {
            return h;
        }

        if (key < h.key) {
            // Key is in the left subtree
            if (h.left == null) {
                // Key not found, return the last accessed node
                return h;
            }
            if (key < h.left.key) { // Zig-Zig (Left-Left)
                h.left.left = splay(h.left.left, key);
                h = rightRotate(h);
            } else if (key > h.left.key) { // Zig-Zag (Left-Right)
                h.left.right = splay(h.left.right, key);
                if (h.left.right != null) {
                    h.left = leftRotate(h.left);
                }
            }
            // Second rotation for Zig-Zig or the only rotation for Zig
            return (h.left == null) ? h : rightRotate(h);
        } else { // key > h.key
            // Key is in the right subtree
            if (h.right == null) {
                // Key not found, return the last accessed node
                return h;
            }
            if (key > h.right.key) { // Zig-Zig (Right-Right)
                h.right.right = splay(h.right.right, key);
                h = leftRotate(h);
            } else if (key < h.right.key) { // Zig-Zag (Right-Left)
                h.right.left = splay(h.right.left, key);
                if (h.right.left != null) {
                    h.right = rightRotate(h.right);
                }
            }
            // Second rotation for Zig-Zig or the only rotation for Zig
            return (h.right == null) ? h : leftRotate(h);
        }
    }

    /**
     * Searches for a key in the tree. If the key is found, it is splayed
     * to the root, and the key is returned. If not found, the last-accessed
     * node is splayed to the root, and null is returned.
     *
     * @param key The key to search for.
     * @return The key if found, otherwise null.
     */
    public Integer search(int key) {
        root = splay(root, key);
        if (root != null && root.key == key) {
            return key;
        }
        return null;
    }

    /**
     * Inserts a key into the splay tree.
     * If the key already exists, the tree is splayed on that key but not modified.
     *
     * @param key The key to insert.
     */
    public void insert(int key) {
        // If tree is empty, create a new root
        if (root == null) {
            root = new Node(key);
            return;
        }

        // Splay the tree to bring the closest node to the root
        root = splay(root, key);

        // If key is already present, do nothing (it's a set)
        if (root.key == key) {
            return;
        }

        // Otherwise, create the new node and make it the root
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
     * If the key is not found, the tree is splayed on the last-accessed node
     * but not modified.
     *
     * @param key The key to delete.
     */
    public void delete(int key) {
        if (root == null) {
            return;
        }

        // Splay the tree for the key
        root = splay(root, key);

        // If key is not in the tree, do nothing
        if (root.key != key) {
            return;
        }

        // Now, the node to be deleted is at the root.
        // We need to join its left and right subtrees.
        Node leftSubtree = root.left;
        Node rightSubtree = root.right;

        if (leftSubtree == null) {
            // If there's no left subtree, the right subtree becomes the new tree
            root = rightSubtree;
        } else {
            // Splay the left subtree to bring its maximum element to its root.
            // This max element will become the new root of the combined tree.
            // Splaying for a key larger than any in the subtree (like the deleted key)
            // achieves this.
            Node newRoot = splay(leftSubtree, key);

            // The new root (max of left subtree) has no right child, so
            // we can attach the original right subtree there.
            newRoot.right = rightSubtree;
            root = newRoot;
        }
    }
}