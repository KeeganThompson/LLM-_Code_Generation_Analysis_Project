/**
 * A complete, self-contained implementation of an integer set using a Splay Tree.
 * A splay tree is a self-balancing binary search tree with the additional
 * property that recently accessed elements are quick to access again.
 * It performs basic operations such as insertion, look-up and removal in
 * O(log n) amortized time.
 */
public class SplayTree {

    /**
     * Represents a node in the Splay Tree.
     */
    private static class Node {
        int key;
        Node left;
        Node right;

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
     *      x           y
     *     / \         / \
     *    y   T3  =>  T1  x
     *   / \             / \
     *  T1  T2          T2  T3
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
     *    x             y
     *   / \           / \
     *  T1  y    =>   x   T3
     *     / \       / \
     *    T2  T3    T1  T2
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
     * If the key is not in the tree, the last accessed node on the search path is splayed to the root.
     * This is a recursive top-down splay implementation.
     * @param node The root of the current subtree.
     * @param key The key to splay.
     * @return The new root of the tree after splaying.
     */
    private Node splay(Node node, int key) {
        if (node == null || node.key == key) {
            return node;
        }

        if (key < node.key) {
            // Key is in the left subtree
            if (node.left == null) {
                return node; // Key not found, splay parent
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

            // Perform the second rotation for Zig-Zig or the only rotation for Zig
            return (node.left == null) ? node : rightRotate(node);

        } else { // key > node.key
            // Key is in the right subtree
            if (node.right == null) {
                return node; // Key not found, splay parent
            }

            // Zig-Zag (Right-Left)
            if (key < node.right.key) {
                node.right.left = splay(node.right.left, key);
                if (node.right.left != null) {
                    node.right = rightRotate(node.right);
                }
            } 
            // Zig-Zig (Right-Right)
            else if (key > node.right.key) {
                node.right.right = splay(node.right.right, key);
                node = leftRotate(node);
            }

            // Perform the second rotation for Zig-Zig or the only rotation for Zig
            return (node.right == null) ? node : leftRotate(node);
        }
    }

    /**
     * Inserts a key into the splay tree.
     * If the key already exists, the tree is splayed on that key, but no new node is inserted.
     * @param key The key to insert.
     */
    public void insert(int key) {
        // If the tree is empty, create a new root.
        if (root == null) {
            root = new Node(key);
            return;
        }

        // Splay the tree. If key is present, it becomes the root.
        // If not, the last accessed node on the search path becomes the root.
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
            root = newNode;
        } else { // key > root.key
            newNode.left = root;
            newNode.right = root.right;
            root.right = null;
            root = newNode;
        }
    }

    /**
     * Searches for a key in the splay tree.
     * This operation performs a splay on the accessed key, moving it to the root.
     * If the key is not found, the last accessed node in the search path is splayed to the root.
     * @param key The key to search for.
     * @return The key as an Integer if found, otherwise null.
     */
    public Integer search(int key) {
        root = splay(root, key);
        if (root != null && root.key == key) {
            return root.key;
        }
        return null;
    }

    /**
     * Deletes a key from the splay tree.
     * If the key is not found, the tree is splayed on the last accessed node and remains unchanged.
     * @param key The key to delete.
     */
    public void delete(int key) {
        // Splay the tree for the key. If found, it will be at the root.
        root = splay(root, key);

        // If key is not in the tree, do nothing.
        if (root == null || root.key != key) {
            return;
        }

        // Key is now at the root.
        Node leftSubtree = root.left;
        Node rightSubtree = root.right;

        if (leftSubtree == null) {
            // No left subtree, the right subtree becomes the new tree.
            root = rightSubtree;
        } else {
            // Splay the left subtree to bring its maximum element to its root.
            // Since `key` is larger than any element in the left subtree, splaying for `key`
            // will bring the max element (inorder predecessor) to the top of the left subtree.
            leftSubtree = splay(leftSubtree, key);
            
            // Attach the original right subtree to the new root of the combined left part.
            leftSubtree.right = rightSubtree;
            root = leftSubtree;
        }
    }
}