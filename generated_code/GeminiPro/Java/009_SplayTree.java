/**
 * A complete, self-contained implementation of an integer Splay Tree.
 * This class implements a set of integers, meaning it does not store duplicate keys.
 * The main operations (search, insert, delete) are based on the splay operation,
 * which moves the accessed node to the root of the tree to optimize for future
 * accesses.
 */
public class SplayTree {

    /**
     * Inner class representing a node in the Splay Tree.
     */
    private static class Node {
        int key;
        Node left;
        Node right;

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

    // --- Helper Methods for Rotations ---

    /**
     * Performs a right rotation on the subtree rooted at y.
     *      y           x
     *     / \         / \
     *    x   T3  =>  T1  y
     *   / \             / \
     *  T1  T2          T2  T3
     * @param y The root of the subtree to rotate.
     * @return The new root of the rotated subtree (x).
     */
    private Node rightRotate(Node y) {
        Node x = y.left;
        y.left = x.right;
        x.right = y;
        return x;
    }

    /**
     * Performs a left rotation on the subtree rooted at x.
     *    x             y
     *   / \           / \
     *  T1  y    =>   x   T3
     *     / \       / \
     *    T2  T3    T1  T2
     * @param x The root of the subtree to rotate.
     * @return The new root of the rotated subtree (y).
     */
    private Node leftRotate(Node x) {
        Node y = x.right;
        x.right = y.left;
        y.left = x;
        return y;
    }

    // --- Core Splay Operation ---

    /**
     * Splays the tree for the given key. This operation moves the node with the
     * given key to the root of the tree. If the key is not in the tree, the last
     * accessed node (the one that would be the parent of the key if it existed)
     * is moved to the root.
     * This is a recursive, bottom-up splay implementation.
     *
     * @param root The root of the tree/subtree to splay.
     * @param key The key to search for and move to the root.
     * @return The new root of the splayed tree.
     */
    private Node splay(Node root, int key) {
        if (root == null || root.key == key) {
            return root;
        }

        if (key < root.key) {
            // Key is in the left subtree
            if (root.left == null) {
                return root; // Key not found, return last accessed node
            }
            if (key < root.left.key) { // Zig-Zig (Left-Left)
                root.left.left = splay(root.left.left, key);
                root = rightRotate(root);
            } else if (key > root.left.key) { // Zig-Zag (Left-Right)
                root.left.right = splay(root.left.right, key);
                if (root.left.right != null) {
                    root.left = leftRotate(root.left);
                }
            }
            // Second rotation for root (if necessary) to complete zig-zig or zig-zag
            return (root.left == null) ? root : rightRotate(root);

        } else { // key > root.key
            // Key is in the right subtree
            if (root.right == null) {
                return root; // Key not found, return last accessed node
            }
            if (key < root.right.key) { // Zig-Zag (Right-Left)
                root.right.left = splay(root.right.left, key);
                if (root.right.left != null) {
                    root.right = rightRotate(root.right);
                }
            } else if (key > root.right.key) { // Zig-Zig (Right-Right)
                root.right.right = splay(root.right.right, key);
                root = leftRotate(root);
            }
            // Second rotation for root (if necessary) to complete zig-zig or zig-zag
            return (root.right == null) ? root : leftRotate(root);
        }
    }

    // --- Public API Methods ---

    /**
     * Searches for a key in the tree.
     * If the key is found, it is splayed to the root. If not found, the last
     * accessed node is splayed to the root.
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
     * If the key already exists, the tree is splayed for that key and no
     * modification occurs. Otherwise, the new key is inserted and becomes the new root.
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

        // If the key is already present, we are done.
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
     *
     * @param key The key to delete.
     */
    public void delete(int key) {
        if (root == null) {
            return; // Tree is empty
        }

        // Splay the tree for the key. If the key exists, it becomes the root.
        root = splay(root, key);

        // If the key is not in the tree, do nothing.
        if (root.key != key) {
            return;
        }

        // Now, the node to be deleted is the root.
        // We need to join the left and right subtrees.
        Node leftSubtree = root.left;
        Node rightSubtree = root.right;

        if (leftSubtree == null) {
            // If there's no left subtree, the right subtree becomes the new tree.
            root = rightSubtree;
        } else {
            // Find the maximum element in the left subtree.
            Node maxNode = leftSubtree;
            while (maxNode.right != null) {
                maxNode = maxNode.right;
            }
            
            // Splay the largest element in the left subtree to its root.
            // After this splay, this new root will have no right child.
            leftSubtree = splay(leftSubtree, maxNode.key);

            // Attach the original right subtree to the new root's right.
            leftSubtree.right = rightSubtree;
            root = leftSubtree;
        }
    }
}