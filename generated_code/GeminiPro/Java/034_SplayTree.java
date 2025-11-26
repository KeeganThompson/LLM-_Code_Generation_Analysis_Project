/**
 * A complete, self-contained Java class that implements a Splay Tree for an integer set.
 * A Splay Tree is a self-balancing binary search tree with the property that recently
 * accessed elements are quick to access again. It performs basic operations such as
 * insertion, deletion, and search in O(log n) amortized time.
 */
public class SplayTree {

    /**
     * Represents a node in the Splay Tree.
     * It is a static inner class as it does not need to access instance members of SplayTree.
     */
    private static class Node {
        int key;
        Node left;
        Node right;

        /**
         * Constructor for a Node.
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

    // --- Core Splaying Logic and Rotations ---

    /**
     * Performs a right rotation on the subtree rooted at node x.
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
     * Splays the tree for a given key. This operation moves the node with the given key
     * (or the last accessed node on the search path if the key is not found) to the root.
     * @param node The root of the current subtree.
     * @param key The key to splay for.
     * @return The new root of the tree after splaying.
     */
    private Node splay(Node node, int key) {
        // Base case: node is null or key is present at root
        if (node == null || node.key == key) {
            return node;
        }

        if (key < node.key) {
            // Key is in the left subtree
            if (node.left == null) {
                return node; // Key not found, return last accessed node
            }
            // Zig-Zig (Left-Left)
            if (key < node.left.key) {
                node.left.left = splay(node.left.left, key);
                node = rightRotate(node);
            } 
            // Zig-Zag (Left-Right)
            else if (key > node.left.key) {
                node.left.right = splay(node.left.right, key);
                if (node.left.right != null) {
                    node.left = leftRotate(node.left);
                }
            }
            // Do second rotation for Zig-Zig/Zig-Zag, or the only rotation for Zig
            return (node.left == null) ? node : rightRotate(node);
        } else { // key > node.key
            // Key is in the right subtree
            if (node.right == null) {
                return node; // Key not found, return last accessed node
            }
            // Zig-Zig (Right-Right)
            if (key > node.right.key) {
                node.right.right = splay(node.right.right, key);
                node = leftRotate(node);
            } 
            // Zig-Zag (Right-Left)
            else if (key < node.right.key) {
                node.right.left = splay(node.right.left, key);
                if (node.right.left != null) {
                    node.right = rightRotate(node.right);
                }
            }
            // Do second rotation for Zig-Zig/Zig-Zag, or the only rotation for Zig
            return (node.right == null) ? node : leftRotate(node);
        }
    }

    // --- Public API Methods ---

    /**
     * Searches for a key in the tree. If the key is found, it is splayed
     * to the root. If not found, the last accessed node is splayed to the root.
     * @param key The key to search for.
     * @return The key as an Integer if found, otherwise null.
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
     * Inserts a key into the Splay Tree. As this is a set, duplicates are not allowed.
     * After insertion, the new node becomes the root of the tree.
     * @param key The key to insert.
     */
    public void insert(int key) {
        // If the tree is empty, create a new root
        if (root == null) {
            root = new Node(key);
            return;
        }

        // Splay the tree for the key. The node closest to the key will become the root.
        root = splay(root, key);

        // If key is already present, do nothing.
        if (root.key == key) {
            return;
        }

        Node newNode = new Node(key);

        // The new node becomes the new root. The old root and one of its subtrees
        // become children of the new node.
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
     * @param key The key to delete.
     */
    public void delete(int key) {
        if (root == null) {
            return;
        }

        // Splay the tree for the key. If the key exists, it becomes the root.
        root = splay(root, key);

        // If key is not in the tree, do nothing.
        if (root.key != key) {
            return;
        }

        // Key is at the root. Now perform the deletion.
        Node leftSubtree = root.left;
        Node rightSubtree = root.right;

        if (leftSubtree == null) {
            // If no left child, the right subtree becomes the new tree.
            root = rightSubtree;
        } else {
            // Make the left subtree the new root.
            root = leftSubtree;
            // Splay the new tree for the key we just deleted. This brings the
            // largest element (predecessor) of the left subtree to its root.
            // This new root is guaranteed to have a null right child.
            root = splay(root, key);
            // Attach the original right subtree to the new root.
            root.right = rightSubtree;
        }
    }
}