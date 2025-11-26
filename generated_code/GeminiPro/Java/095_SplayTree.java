/**
 * A complete, self-contained implementation of a Splay Tree for an integer set.
 * A splay tree is a self-balancing binary search tree with the additional
 * property that recently accessed elements are quick to access again.
 * It performs basic operations such as insertion, look-up and removal in O(log n)
 * amortized time.
 */
public class SplayTree {

    /**
     * Represents a node in the Splay Tree.
     * This is a private static nested class as its implementation is tied to the SplayTree.
     */
    private static class Node {
        int key;
        Node left, right;

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

    // --- Public API Methods ---

    /**
     * Searches for a key in the tree.
     * If the key is found, it is splayed to the root. If not found, the last
     * accessed node on the search path is splayed to the root.
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
            return key;
        }
        return null;
    }

    /**
     * Inserts a key into the Splay Tree.
     * If the key is not already in the tree, it is inserted and becomes the new root.
     * If the key already exists, the existing node is splayed to the root.
     * This implementation maintains the set property (no duplicate keys).
     *
     * @param key The key to insert.
     */
    public void insert(int key) {
        // Case 1: The tree is empty.
        if (root == null) {
            root = new Node(key);
            return;
        }

        // Splay the tree for the key. This brings the node with the key, or its
        // would-be parent, to the root.
        root = splay(root, key);

        // Case 2: The key is already present. Do nothing as this is a set.
        if (root.key == key) {
            return;
        }

        // Case 3: The key is not present. Insert it as the new root.
        Node newNode = new Node(key);
        if (key < root.key) {
            // The new key is smaller than the root.
            // The new root's right child is the old root.
            // The new root's left child is the old root's left child.
            newNode.right = root;
            newNode.left = root.left;
            root.left = null; // The old root no longer has a left child.
        } else { // key > root.key
            // The new key is larger than the root.
            // The new root's left child is the old root.
            // The new root's right child is the old root's right child.
            newNode.left = root;
            newNode.right = root.right;
            root.right = null; // The old root no longer has a right child.
        }
        root = newNode;
    }

    /**
     * Deletes a key from the Splay Tree.
     * If the key is found, it is first splayed to the root and then removed.
     * The tree is then re-formed by joining the remaining subtrees.
     *
     * @param key The key to delete.
     */
    public void delete(int key) {
        if (root == null) {
            return;
        }

        // Splay the key to bring it to the root.
        root = splay(root, key);

        // If the key is not at the root after splaying, it wasn't in the tree.
        if (root.key != key) {
            return;
        }

        // Now, the node to delete is the root.
        Node leftSubtree = root.left;
        Node rightSubtree = root.right;

        if (leftSubtree == null) {
            // If there's no left subtree, the right subtree becomes the new tree.
            root = rightSubtree;
        } else {
            // Splay on the left subtree to bring its maximum element to its root.
            // Since `key` is guaranteed to be greater than any element in the
            // left subtree, splaying for `key` will bring the max element up.
            leftSubtree = splay(leftSubtree, key);

            // The new root of the left subtree (the max element) now has no right child.
            // We can attach the original right subtree there.
            leftSubtree.right = rightSubtree;
            root = leftSubtree;
        }
    }

    // --- Private Helper Methods ---

    /**
     * Performs a right rotation on the given node y.
     *
     *      y           x
     *     / \         / \
     *    x   T3  ->  T1  y
     *   / \             / \
     *  T1  T2          T2  T3
     *
     * @param y The root of the subtree to rotate.
     * @return The new root of the rotated subtree (x).
     */
    private Node rotateRight(Node y) {
        Node x = y.left;
        y.left = x.right;
        x.right = y;
        return x;
    }

    /**
     * Performs a left rotation on the given node x.
     *
     *    x             y
     *   / \           / \
     *  T1  y    ->   x   T3
     *     / \       / \
     *    T2  T3    T1  T2
     *
     * @param x The root of the subtree to rotate.
     * @return The new root of the rotated subtree (y).
     */
    private Node rotateLeft(Node x) {
        Node y = x.right;
        x.right = y.left;
        y.left = x;
        return y;
    }

    /**
     * The core splaying operation (top-down).
     * This operation moves the node with the given key (or the last accessed node on the
     * search path if the key is not found) to the root of the tree.
     *
     * @param node The root of the tree to splay.
     * @param key  The key to splay towards the root.
     * @return The new root of the splayed tree.
     */
    private Node splay(Node node, int key) {
        if (node == null || node.key == key) {
            return node;
        }

        // Create a dummy node to act as the head of the Left and Right subtrees.
        // The key in the dummy node is irrelevant.
        Node dummy = new Node(0);
        Node leftTreeMax = dummy;
        Node rightTreeMin = dummy;
        Node current = node;

        while (true) {
            if (key < current.key) {
                if (current.left == null) break;
                // Zig-Zig (Left-Left case)
                if (key < current.left.key) {
                    current = rotateRight(current);
                    if (current.left == null) break;
                }
                // Link current node to the right tree (it's larger than the key)
                rightTreeMin.left = current;
                rightTreeMin = current;
                current = current.left;
            } else if (key > current.key) {
                if (current.right == null) break;
                // Zig-Zig (Right-Right case)
                if (key > current.right.key) {
                    current = rotateLeft(current);
                    if (current.right == null) break;
                }
                // Link current node to the left tree (it's smaller than the key)
                leftTreeMax.right = current;
                leftTreeMax = current;
                current = current.right;
            } else { // key == current.key
                break;
            }
        }

        // Reassemble the tree
        leftTreeMax.right = current.left;   // Attach final left child
        rightTreeMin.left = current.right;  // Attach final right child
        current.left = dummy.right;         // Set new root's left child
        current.right = dummy.left;         // Set new root's right child

        return current;
    }
}