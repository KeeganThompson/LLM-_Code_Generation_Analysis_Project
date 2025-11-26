/**
 * A complete, self-contained Java class that implements an integer set using a Splay Tree.
 *
 * A splay tree is a self-balancing binary search tree with the additional
 * property that recently accessed elements are quick to access again. It performs
 * basic operations such as insertion, deletion, and search. When an element is
 * accessed, it is moved to the root of the tree through a series of rotations
 * in an operation called "splaying".
 */
public class SplayTree {

    /**
     * Inner class representing a node in the splay tree.
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
     * Constructs an empty SplayTree.
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
     * The main splay operation. It brings the node with the given key
     * (or the last accessed node if the key is not found) to the root of the tree.
     * This implementation uses the top-down splaying technique.
     *
     * @param root The root of the tree to splay.
     * @param key The key to splay around.
     * @return The new root of the splayed tree.
     */
    private Node splay(Node root, int key) {
        if (root == null || root.key == key) {
            return root;
        }

        // Dummy node to simplify linking of left and right subtrees
        Node header = new Node(0);
        Node leftTreeMax = header;
        Node rightTreeMin = header;

        while (true) {
            if (key < root.key) {
                if (root.left == null) break;
                // Zig-Zig (left-left)
                if (key < root.left.key) {
                    root = rightRotate(root);
                }
                if (root.left == null) break;
                // Link to the right tree
                rightTreeMin.left = root;
                rightTreeMin = root;
                root = root.left;
            } else if (key > root.key) {
                if (root.right == null) break;
                // Zig-Zig (right-right)
                if (key > root.right.key) {
                    root = leftRotate(root);
                }
                if (root.right == null) break;
                // Link to the left tree
                leftTreeMax.right = root;
                leftTreeMax = root;
                root = root.right;
            } else { // key == root.key
                break;
            }
        }

        // Reassemble the trees
        leftTreeMax.right = root.left;
        rightTreeMin.left = root.right;
        root.left = header.right;
        root.right = header.left;

        return root;
    }

    /**
     * Inserts a key into the splay tree.
     * If the key already exists, the tree remains unchanged. After insertion,
     * the new node (or the existing node with the key) becomes the new root.
     *
     * @param key The key to insert.
     */
    public void insert(int key) {
        // Case 1: The tree is empty.
        if (root == null) {
            root = new Node(key);
            return;
        }

        // Splay the tree around the key. The new root will be the closest node to the key.
        root = splay(root, key);

        // Case 2: The key is already in the tree.
        if (root.key == key) {
            return; // No duplicates allowed in the set.
        }

        // Case 3: The key is not in the tree. Insert a new node at the root.
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
     * Searches for a key in the tree. If the key is found, it is splayed
     * to the root. If not found, the last accessed node on the search path is
     * splayed to the root.
     *
     * @param key The key to search for.
     * @return The key if found, otherwise null.
     */
    public Integer search(int key) {
        if (root == null) {
            return null;
        }
        root = splay(root, key);
        // After splaying, if the key exists, it will be at the root.
        if (root.key == key) {
            return root.key;
        }
        return null;
    }

    /**
     * Deletes a key from the splay tree.
     * If the key is found, it is deleted and the tree is rebalanced.
     *
     * @param key The key to delete.
     */
    public void delete(int key) {
        if (root == null) {
            return;
        }

        // Splay the key to the root.
        root = splay(root, key);

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
            // Splay the left subtree to bring its maximum element to its root.
            // Since `key` is larger than any element in the left subtree, splaying
            // for `key` will effectively bring the max element to the root.
            Node newRoot = splay(leftSubtree, key);

            // The new root of the left subtree now has no right child.
            // Attach the original right subtree to it.
            newRoot.right = rightSubtree;
            root = newRoot;
        }
    }
}