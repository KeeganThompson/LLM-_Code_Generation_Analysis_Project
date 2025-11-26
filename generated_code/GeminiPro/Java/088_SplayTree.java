/**
 * A complete, self-contained implementation of a Splay Tree for an integer set.
 * Splay trees are self-balancing binary search trees with the additional property
 * that recently accessed elements are quick to access again.
 */
public class SplayTree {

    /**
     * Represents a node in the Splay Tree.
     */
    private static class Node {
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
     * The core splaying operation. Brings the node with the given key
     * (or the last accessed node if the key is not found) to the root of the
     * subtree rooted at h.
     * @param h The root of the subtree.
     * @param key The key to splay.
     * @return The new root of the subtree after splaying.
     */
    private Node splay(Node h, int key) {
        if (h == null || h.key == key) {
            return h;
        }

        if (key < h.key) {
            // Key is in the left subtree
            if (h.left == null) {
                return h; // Key not found, splay the last node (h)
            }

            if (key < h.left.key) { // Zig-Zig (Left-Left)
                h.left.left = splay(h.left.left, key);
                h = rightRotate(h);
            } else if (key > h.left.key) { // Zig-Zag (Left-Right)
                h.left.right = splay(h.left.right, key);
                if (h.left.right != null) {
                    h.left = leftRotate(h.left);
                }
            }
            // The second rotation or the only rotation for Zig
            return (h.left == null) ? h : rightRotate(h);

        } else { // key > h.key
            // Key is in the right subtree
            if (h.right == null) {
                return h; // Key not found, splay the last node (h)
            }

            if (key > h.right.key) { // Zig-Zig (Right-Right)
                h.right.right = splay(h.right.right, key);
                h = leftRotate(h);
            } else if (key < h.right.key) { // Zig-Zag (Right-Left)
                h.right.left = splay(h.right.left, key);
                if (h.right.left != null) {
                    h.right = rightRotate(h.right);
                }
            }
            // The second rotation or the only rotation for Zig
            return (h.right == null) ? h : leftRotate(h);
        }
    }

    /**
     * Searches for a key in the tree. If the key is found, it is splayed
     * to the root. If not found, the last accessed node is splayed to the root.
     *
     * @param key The key to search for.
     * @return The key if found, otherwise null.
     */
    public Integer search(int key) {
        if (root == null) {
            return null;
        }
        root = splay(root, key);
        // After splay, if the key exists, it will be at the root.
        return (root.key == key) ? key : null;
    }

    /**
     * Inserts a key into the Splay Tree. If the key already exists,
     * the tree remains unchanged. After insertion, the new key becomes the root.
     *
     * @param key The key to insert.
     */
    public void insert(int key) {
        // If the tree is empty, create a new root.
        if (root == null) {
            root = new Node(key);
            return;
        }

        // Splay the tree for the key. This brings the closest node to the root.
        root = splay(root, key);

        // If the key is already present, do nothing (it's a set).
        if (root.key == key) {
            return;
        }

        Node newNode = new Node(key);

        // The new node becomes the new root. The old root is split and attached
        // as a child of the new root.
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
     * Deletes a key from the Splay Tree. If the key is not in the tree,
     * the tree remains unchanged.
     *
     * @param key The key to delete.
     */
    public void delete(int key) {
        if (root == null) {
            return;
        }

        // Splay the tree for the key.
        root = splay(root, key);

        // If the key is not at the root after splaying, it's not in the tree.
        if (root.key != key) {
            return;
        }

        // Now the node to be deleted is the root.
        Node leftSubtree = root.left;
        Node rightSubtree = root.right;

        if (leftSubtree == null) {
            // If there's no left child, the right subtree becomes the new tree.
            root = rightSubtree;
        } else {
            // Splay the largest element in the left subtree to its root.
            // A search for the key (which is guaranteed to be the largest) in the
            // left subtree will bring the max element to the top.
            leftSubtree = splay(leftSubtree, key);

            // The new root of the left subtree now has no right child.
            // Attach the original right subtree to it.
            leftSubtree.right = rightSubtree;
            root = leftSubtree;
        }
    }
}