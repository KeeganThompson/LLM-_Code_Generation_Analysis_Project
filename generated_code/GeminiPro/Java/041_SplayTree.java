/**
 * A complete, self-contained Java class that implements an integer set using a Splay Tree.
 * A splay tree is a self-adjusting binary search tree with the property that
 * recently accessed elements are quick to access again. It performs basic
 * operations such as insertion, deletion, and search. After a search, insertion,
 * or deletion, the accessed node is moved to the root of the tree through a
 * series of rotations in an operation called "splaying".
 */
public class SplayTree {

    /**
     * Represents a node in the Splay Tree.
     * This is a private inner class, making the SplayTree class self-contained.
     */
    private class Node {
        int key;
        Node left, right;

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

    // --- Core Splay Operations ---

    /**
     * Performs a right rotation on the subtree rooted at x.
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
     * Performs a left rotation on the subtree rooted at x.
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
     * The main splay operation. It brings the node with the given key
     * (or the last accessed node if the key is not found) to the root of the tree.
     * This is a recursive top-down splaying implementation.
     *
     * @param node The root of the current subtree.
     * @param key The key to splay towards the root.
     * @return The new root of the splayed tree.
     */
    private Node splay(Node node, int key) {
        // Base case: node is null or key is at the root
        if (node == null || node.key == key) {
            return node;
        }

        // Key is in the left subtree
        if (key < node.key) {
            // Key is not in the tree, we are done
            if (node.left == null) {
                return node;
            }

            // Zig-Zig (Left-Left)
            if (key < node.left.key) {
                // Recursively bring the key as root of left-left
                node.left.left = splay(node.left.left, key);
                // First rotation for root
                node = rightRotate(node);
            }
            // Zig-Zag (Left-Right)
            else if (key > node.left.key) {
                // Recursively bring the key as root of left-right
                node.left.right = splay(node.left.right, key);
                // First rotation for node.left
                if (node.left.right != null) {
                    node.left = leftRotate(node.left);
                }
            }

            // Do second rotation for root (if possible)
            return (node.left == null) ? node : rightRotate(node);
        }
        // Key is in the right subtree
        else { // key > node.key
            // Key is not in the tree, we are done
            if (node.right == null) {
                return node;
            }

            // Zig-Zag (Right-Left)
            if (key < node.right.key) {
                // Recursively bring the key as root of right-left
                node.right.left = splay(node.right.left, key);
                // First rotation for node.right
                if (node.right.left != null) {
                    node.right = rightRotate(node.right);
                }
            }
            // Zig-Zig (Right-Right)
            else if (key > node.right.key) {
                // Recursively bring the key as root of right-right
                node.right.right = splay(node.right.right, key);
                // First rotation for root
                node = leftRotate(node);
            }

            // Do second rotation for root (if possible)
            return (node.right == null) ? node : leftRotate(node);
        }
    }

    // --- Public API Methods ---

    /**
     * Inserts a key into the splay tree.
     * If the key already exists, the tree is splayed on that key but otherwise remains unchanged.
     * After insertion of a new key, the new node becomes the root of the tree.
     *
     * @param key The key to insert.
     */
    public void insert(int key) {
        // If the tree is empty, create a new root
        if (root == null) {
            root = new Node(key);
            return;
        }

        // Splay the tree for the key. This brings the closest node to the root.
        root = splay(root, key);

        // If key is already present, do nothing more.
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
     * If the key is not found, the tree is splayed on the last accessed node
     * but otherwise remains unchanged.
     *
     * @param key The key to delete.
     */
    public void delete(int key) {
        // Splay the tree for the key. If found, it becomes the root.
        root = splay(root, key);

        // If key is not in the tree (or tree is empty), do nothing.
        if (root == null || root.key != key) {
            return;
        }

        Node leftSubtree = root.left;
        Node rightSubtree = root.right;

        if (leftSubtree == null) {
            root = rightSubtree;
        } else {
            // Find the max element in the left subtree by splaying for the largest possible key (our deleted key)
            // This brings the predecessor of the deleted key to the root of the left subtree.
            leftSubtree = splay(leftSubtree, key);
            // After splaying, the new root of the left subtree is the max element and has no right child.
            leftSubtree.right = rightSubtree;
            root = leftSubtree;
        }
    }

    /**
     * Searches for a key in the tree.
     * This operation performs a splay on the accessed node (or the last node on the search path),
     * moving it to the root of the tree.
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
}