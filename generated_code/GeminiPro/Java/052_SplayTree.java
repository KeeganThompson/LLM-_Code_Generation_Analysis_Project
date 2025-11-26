/**
 * A self-contained Java class that implements an integer set using a Splay Tree.
 * A splay tree is a self-balancing binary search tree with the additional property
 * that recently accessed elements are quick to access again.
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
     * Performs the splay operation. It brings the node with the given key
     * (or the last accessed node on the search path) to the root of the tree.
     *
     * @param root The root of the tree (or subtree) to splay.
     * @param key The key to splay for.
     * @return The new root of the splayed tree.
     */
    private Node splay(Node root, int key) {
        if (root == null || root.key == key) {
            return root;
        }

        if (key < root.key) {
            // Key is in the left subtree
            if (root.left == null) {
                return root;
            }

            // Zig-Zig (Left-Left)
            if (key < root.left.key) {
                root.left.left = splay(root.left.left, key);
                root = rightRotate(root);
            }
            // Zig-Zag (Left-Right)
            else if (key > root.left.key) {
                root.left.right = splay(root.left.right, key);
                if (root.left.right != null) {
                    root.left = leftRotate(root.left);
                }
            }
            // Second rotation for root (if necessary)
            return (root.left == null) ? root : rightRotate(root);

        } else { // key > root.key
            // Key is in the right subtree
            if (root.right == null) {
                return root;
            }

            // Zig-Zag (Right-Left)
            if (key < root.right.key) {
                root.right.left = splay(root.right.left, key);
                if (root.right.left != null) {
                    root.right = rightRotate(root.right);
                }
            }
            // Zig-Zig (Right-Right)
            else if (key > root.right.key) {
                root.right.right = splay(root.right.right, key);
                root = leftRotate(root);
            }
            // Second rotation for root (if necessary)
            return (root.right == null) ? root : leftRotate(root);
        }
    }

    /**
     * Inserts a key into the splay tree.
     * If the key already exists, the tree remains unchanged.
     * After insertion, the new node becomes the root of the tree.
     *
     * @param key The integer key to insert.
     */
    public void insert(int key) {
        // Case 1: The tree is empty.
        if (root == null) {
            root = new Node(key);
            return;
        }

        // Splay the tree for the key. This brings the closest node to the root.
        root = splay(root, key);

        // If the key is already present, do nothing.
        if (root.key == key) {
            return;
        }

        Node newNode = new Node(key);

        // The new node becomes the new root. The old root is split and attached.
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
     * If the key is not found, the tree remains unchanged.
     *
     * @param key The integer key to delete.
     */
    public void delete(int key) {
        if (root == null) {
            return;
        }

        // Splay the tree for the key.
        root = splay(root, key);

        // If the key is not at the root, it's not in the tree.
        if (root.key != key) {
            return;
        }

        // Now, delete the root.
        Node leftSubtree = root.left;
        Node rightSubtree = root.right;

        if (leftSubtree == null) {
            // If there's no left subtree, the right subtree becomes the new tree.
            root = rightSubtree;
        } else {
            // Splay the left subtree to bring its maximum element to its root.
            // The key we are deleting is guaranteed to be larger than any element
            // in the left subtree, so splaying for it will achieve this.
            Node newRoot = splay(leftSubtree, key);
            
            // The new root of the joined tree will not have a right child.
            // Attach the original right subtree to it.
            newRoot.right = rightSubtree;
            root = newRoot;
        }
    }

    /**
     * Searches for a key in the splay tree.
     * This operation performs a splay, moving the accessed node (or the last
     * node on the search path) to the root.
     *
     * @param key The integer key to search for.
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
}