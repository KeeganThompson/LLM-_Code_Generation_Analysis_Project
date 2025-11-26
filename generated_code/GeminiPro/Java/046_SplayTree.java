/**
 * A Splay Tree implementation that stores a set of integers.
 *
 * A splay tree is a self-balancing binary search tree with the additional
 * property that recently accessed elements are quick to access again.
 * It performs basic operations such as insertion, deletion, and search.
 * After a search or an access, the accessed node is moved to the root of the tree
 * through a series of rotations, a process known as "splaying". This implementation
 * does not allow duplicate keys.
 */
public class SplayTree {

    /**
     * Inner class representing a node in the splay tree.
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
     * Constructs an empty SplayTree.
     */
    public SplayTree() {
        this.root = null;
    }

    /**
     * Performs a right rotation on the given node.
     *
     * @param x The node to be rotated.
     * @return The new root of the subtree.
     */
    private Node rightRotate(Node x) {
        Node y = x.left;
        x.left = y.right;
        y.right = x;
        return y;
    }

    /**
     * Performs a left rotation on the given node.
     *
     * @param x The node to be rotated.
     * @return The new root of the subtree.
     */
    private Node leftRotate(Node x) {
        Node y = x.right;
        x.right = y.left;
        y.left = x;
        return y;
    }

    /**
     * The core splaying operation.
     * This method searches for a key and moves the last accessed node to the root.
     * This is a top-down splaying implementation.
     *
     * @param root The root of the tree (or subtree) to splay.
     * @param key The key to splay around.
     * @return The new root of the splayed tree.
     */
    private Node splay(Node root, int key) {
        if (root == null) {
            return null;
        }

        // Dummy node to simplify linking. header.right points to the left tree (L),
        // and header.left points to the right tree (R).
        Node header = new Node(0);
        Node leftTreeMax = header;
        Node rightTreeMin = header;

        while (true) {
            if (key < root.key) {
                if (root.left == null) break;
                // Zig-Zig case (right rotation)
                if (key < root.left.key) {
                    root = rightRotate(root);
                    if (root.left == null) break;
                }
                // Link the current root to the right tree
                rightTreeMin.left = root;
                rightTreeMin = root;
                root = root.left;
            } else if (key > root.key) {
                if (root.right == null) break;
                // Zig-Zig case (left rotation)
                if (key > root.right.key) {
                    root = leftRotate(root);
                    if (root.right == null) break;
                }
                // Link the current root to the left tree
                leftTreeMax.right = root;
                leftTreeMax = root;
                root = root.right;
            } else { // Found the key
                break;
            }
        }

        // Reassemble the tree
        leftTreeMax.right = root.left;
        rightTreeMin.left = root.right;
        root.left = header.right;
        root.right = header.left;

        return root;
    }

    /**
     * Searches for a key in the tree.
     * If the key is found, it is splayed to the root.
     *
     * @param key The key to search for.
     * @return The key if found, otherwise null.
     */
    public Integer search(int key) {
        root = splay(root, key);
        if (root != null && root.key == key) {
            return root.key;
        }
        return null;
    }

    /**
     * Inserts a key into the splay tree.
     * If the key already exists, the tree remains unchanged.
     * After insertion, the new node becomes the root of the tree.
     *
     * @param key The key to insert.
     */
    public void insert(int key) {
        // Handle case for an empty tree
        if (root == null) {
            root = new Node(key);
            return;
        }

        // Splay the tree around the key. The closest node will become the root.
        root = splay(root, key);

        // If the key is already present, do nothing.
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
     * If the key is not in the tree, the tree remains unchanged.
     *
     * @param key The key to delete.
     */
    public void delete(int key) {
        if (root == null) {
            return;
        }

        // Splay the tree to bring the node to delete (or its closest value) to the root.
        root = splay(root, key);

        // If the key is not in the tree, do nothing.
        if (root.key != key) {
            return;
        }

        // The node to delete is now the root.
        Node leftSubtree = root.left;
        Node rightSubtree = root.right;

        if (leftSubtree == null) {
            // If there's no left subtree, the right subtree becomes the new tree.
            root = rightSubtree;
        } else {
            // Splay the left subtree to bring its largest element to its root.
            // Splaying for the key 'key' guarantees the max element is the new root
            // because 'key' is larger than any element in the left subtree.
            leftSubtree = splay(leftSubtree, key);

            // The new root of the left subtree has no right child.
            // Attach the original right subtree there.
            leftSubtree.right = rightSubtree;
            root = leftSubtree;
        }
    }
}