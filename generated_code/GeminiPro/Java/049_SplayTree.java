/**
 * A complete, self-contained implementation of a Splay Tree for an integer set.
 * A splay tree is a self-adjusting binary search tree with the additional
 * property that recently accessed elements are quick to access again. It performs
 * basic operations such as insertion, search, and removal in O(log n) amortized time.
 */
public class SplayTree {

    private Node root;

    /**
     * Inner class to represent a node in the tree.
     */
    private class Node {
        int key;
        Node left, right;

        Node(int key) {
            this.key = key;
            this.left = null;
            this.right = null;
        }
    }

    /**
     * Constructs an empty Splay Tree.
     */
    public SplayTree() {
        this.root = null;
    }

    /**
     * Performs a right rotation on the subtree rooted at node x.
     *
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
     *
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
     * The main splay operation. It brings the node with the given key (or the last
     * accessed node if the key is not found) to the root of the tree.
     * This implementation uses the top-down splaying approach.
     *
     * @param root The root of the tree (or subtree) to splay.
     * @param key  The key to splay around.
     * @return The new root of the splayed tree.
     */
    private Node splay(Node root, int key) {
        if (root == null || root.key == key) {
            return root;
        }

        // Create a dummy node. The right child of dummy will be the new
        // root of the left subtree, and the left child will be the new
        // root of the right subtree.
        Node dummy = new Node(0);
        Node leftTreeMax = dummy;
        Node rightTreeMin = dummy;

        while (true) {
            if (key < root.key) {
                if (root.left == null) break;
                // Zig-Zig (Left-Left)
                if (key < root.left.key) {
                    root = rightRotate(root);
                    if (root.left == null) break;
                }
                // Link Right: Add current root to the right tree
                rightTreeMin.left = root;
                rightTreeMin = root;
                root = root.left;
            } else if (key > root.key) {
                if (root.right == null) break;
                // Zig-Zig (Right-Right)
                if (key > root.right.key) {
                    root = leftRotate(root);
                    if (root.right == null) break;
                }
                // Link Left: Add current root to the left tree
                leftTreeMax.right = root;
                leftTreeMax = root;
                root = root.right;
            } else { // key == root.key
                break;
            }
        }

        // Assemble the final tree
        leftTreeMax.right = root.left;
        rightTreeMin.left = root.right;
        root.left = dummy.right;
        root.right = dummy.left;

        return root;
    }

    /**
     * Searches for a key in the splay tree.
     * This operation performs a splay on the accessed node (or the last
     * node accessed during the search), moving it to the root.
     *
     * @param key The integer key to search for.
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
     * If the key already exists, the tree remains unchanged. After insertion,
     * the new node becomes the root of the tree.
     *
     * @param key The integer key to insert.
     */
    public void insert(int key) {
        // If the tree is empty, create a new root
        if (root == null) {
            root = new Node(key);
            return;
        }

        // Splay the tree around the key. The closest node will become the root.
        root = splay(root, key);

        // If key is already present, do nothing
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
     * @param key The integer key to delete.
     */
    public void delete(int key) {
        if (root == null) {
            return;
        }

        // Splay the key to the root
        root = splay(root, key);

        // If the key is not in the tree, do nothing
        if (root.key != key) {
            return;
        }

        // Now, the node to be deleted is the root
        Node leftSubtree = root.left;
        Node rightSubtree = root.right;

        if (leftSubtree == null) {
            root = rightSubtree;
        } else {
            // Splay the left subtree to bring the maximum element (predecessor) to its root.
            // Splaying for 'key' in the left subtree will bring the max element to the top
            // because 'key' is greater than all elements in the left subtree.
            leftSubtree = splay(leftSubtree, key);

            // The new root of the left subtree has no right child.
            // Attach the right subtree of the original root to it.
            leftSubtree.right = rightSubtree;
            root = leftSubtree;
        }
    }
}