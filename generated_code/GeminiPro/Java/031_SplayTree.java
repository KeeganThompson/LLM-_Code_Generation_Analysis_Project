/**
 * A self-contained Java class that implements an integer set using a Splay Tree.
 * A splay tree is a self-balancing binary search tree with the additional property
 * that recently accessed elements are quick to access again. It performs basic
 * operations such as insertion, removal, and search in O(log n) amortized time.
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
     * The splay operation. It brings the node with the given key (or the last
     * accessed node if the key is not found) to the root of the tree.
     * @param node The root of the tree/subtree to splay.
     * @param key The key to splay for.
     * @return The new root of the splayed tree.
     */
    private Node splay(Node node, int key) {
        if (node == null || node.key == key) {
            return node;
        }

        if (key < node.key) {
            // Key is in the left subtree
            if (node.left == null) {
                return node; // Key not found, splay the last accessed node
            }
            if (key < node.left.key) { // Zig-Zig (Left-Left)
                // Recursively bring the key as root of left-left
                node.left.left = splay(node.left.left, key);
                // First rotation for grandparent-parent
                node = rightRotate(node);
            } else if (key > node.left.key) { // Zig-Zag (Left-Right)
                // Recursively bring the key as root of left-right
                node.left.right = splay(node.left.right, key);
                // First rotation for parent-child if necessary
                if (node.left.right != null) {
                    node.left = leftRotate(node.left);
                }
            }
            // Second rotation for parent-child
            return (node.left == null) ? node : rightRotate(node);
        } else { // key > node.key
            // Key is in the right subtree
            if (node.right == null) {
                return node; // Key not found, splay the last accessed node
            }
            if (key > node.right.key) { // Zig-Zig (Right-Right)
                // Recursively bring the key as root of right-right
                node.right.right = splay(node.right.right, key);
                // First rotation for grandparent-parent
                node = leftRotate(node);
            } else if (key < node.right.key) { // Zig-Zag (Right-Left)
                // Recursively bring the key as root of right-left
                node.right.left = splay(node.right.left, key);
                // First rotation for parent-child if necessary
                if (node.right.left != null) {
                    node.right = rightRotate(node.right);
                }
            }
            // Second rotation for parent-child
            return (node.right == null) ? node : leftRotate(node);
        }
    }

    /**
     * Searches for a key in the tree. If the key is found, it is splayed to the root.
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
     * Inserts a key into the splay tree. If the key already exists, the tree remains unchanged.
     * @param key The key to insert.
     */
    public void insert(int key) {
        // If tree is empty, create a new root.
        if (root == null) {
            root = new Node(key);
            return;
        }

        // Splay the tree to bring the closest node to the root.
        root = splay(root, key);

        // If key is already present, do nothing.
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
     * @param key The key to delete.
     */
    public void delete(int key) {
        if (root == null) {
            return;
        }

        // Splay the tree to bring the node to be deleted to the root.
        root = splay(root, key);

        // If the key is not in the tree, do nothing.
        if (root.key != key) {
            return;
        }

        Node leftSubtree = root.left;
        Node rightSubtree = root.right;

        if (leftSubtree == null) {
            root = rightSubtree;
        } else {
            // Splay the left subtree to bring the maximum element to its root.
            // This maximum element is the predecessor of the deleted key.
            // Searching for the key (which is guaranteed to be larger than any
            // element in the left subtree) will splay the max element to the top.
            leftSubtree = splay(leftSubtree, key);
            
            // Attach the right subtree to the new root (the max of the left subtree).
            leftSubtree.right = rightSubtree;
            root = leftSubtree;
        }
    }
}