/**
 * A complete, self-contained Java class that implements an integer set using a Splay Tree.
 * A splay tree is a self-balancing binary search tree with the additional property that
 * recently accessed elements are quick to access again. It performs basic operations
 * such as insertion, deletion, and search. After any access, the accessed node is
 * moved to the root of the tree (an operation called "splaying").
 */
public class SplayTree {

    /**
     * Represents a node in the Splay Tree.
     * This is a private static inner class as it does not need to access instance
     * members of the outer SplayTree class.
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
     * Constructs an empty SplayTree.
     */
    public SplayTree() {
        this.root = null;
    }

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
     * The core splay operation. It brings the node with the given key
     * to the root of the tree. If the key is not in the tree, the last
     * accessed node on the search path is brought to the root.
     * This is a recursive, bottom-up splaying implementation.
     *
     * @param root The root of the current subtree.
     * @param key The key to splay.
     * @return The new root of the splayed tree.
     */
    private Node splay(Node root, int key) {
        // Base case: root is null or key is present at root
        if (root == null || root.key == key) {
            return root;
        }

        // Key lies in the left subtree
        if (key < root.key) {
            // Key is not in the tree, we are done with this subtree
            if (root.left == null) {
                return root;
            }

            // Zig-Zig (Left Left)
            if (key < root.left.key) {
                // Recursively bring the key as root of left-left
                root.left.left = splay(root.left.left, key);
                // Do first rotation for root
                root = rightRotate(root);
            }
            // Zig-Zag (Left Right)
            else if (key > root.left.key) {
                // Recursively bring the key as root of left-right
                root.left.right = splay(root.left.right, key);
                // Do first rotation for root.left
                if (root.left.right != null) {
                    root.left = leftRotate(root.left);
                }
            }

            // Do second rotation for root (if necessary)
            return (root.left == null) ? root : rightRotate(root);
        }
        // Key lies in the right subtree
        else {
            // Key is not in the tree, we are done with this subtree
            if (root.right == null) {
                return root;
            }

            // Zig-Zag (Right Left)
            if (key < root.right.key) {
                // Recursively bring the key as root of right-left
                root.right.left = splay(root.right.left, key);
                // Do first rotation for root.right
                if (root.right.left != null) {
                    root.right = rightRotate(root.right);
                }
            }
            // Zig-Zig (Right Right)
            else if (key > root.right.key) {
                // Recursively bring the key as root of right-right
                root.right.right = splay(root.right.right, key);
                // Do first rotation for root
                root = leftRotate(root);
            }

            // Do second rotation for root (if necessary)
            return (root.right == null) ? root : leftRotate(root);
        }
    }

    /**
     * Searches for a key in the splay tree.
     * This operation splays the tree, moving the accessed node (or the last
     * node on the search path if the key is not found) to the root.
     *
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
     * Inserts a key into the splay tree.
     * If the key already exists, the tree is splayed on that key, and no
     * new node is inserted, maintaining the set property.
     *
     * @param key The key to insert.
     */
    public void insert(int key) {
        // If the tree is empty, create a new root
        if (root == null) {
            root = new Node(key);
            return;
        }

        // Splay the tree around the key. If the key exists, it becomes the root.
        // If not, the last accessed node on the path becomes the root.
        root = splay(root, key);

        // If key is already present at the root, we are done.
        if (root.key == key) {
            return;
        }

        Node newNode = new Node(key);

        // The splay operation partitions the tree. The new key will become the new root.
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
            return;
        }

        // Splay the key to bring it to the root
        root = splay(root, key);

        // If the key is not at the root after splaying, it's not in the tree.
        if (root.key != key) {
            return;
        }

        // Now the node to be deleted is at the root.
        // We need to join its left and right subtrees.
        Node leftSubtree = root.left;
        Node rightSubtree = root.right;

        if (leftSubtree == null) {
            // If there's no left subtree, the right subtree becomes the new tree.
            root = rightSubtree;
        } else {
            // Splay the left subtree to bring its maximum element to its root.
            // Since `key` is greater than any element in the left subtree, splaying
            // for `key` will bring the max element to the root of the left subtree.
            leftSubtree = splay(leftSubtree, key);

            // After splaying, the new root of the left subtree has no right child.
            // We can safely attach the original right subtree there.
            leftSubtree.right = rightSubtree;
            root = leftSubtree;
        }
    }
}