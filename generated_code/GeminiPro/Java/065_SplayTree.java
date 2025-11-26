/**
 * A self-contained Java class implementing a Splay Tree for an integer set.
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
         * Constructor for a Node.
         * @param key The integer key for this node.
         */
        Node(int key) {
            this.key = key;
            this.left = null;
            this.right = null;
        }
    }

    private Node root;

    /**
     * Default constructor to create an empty Splay Tree.
     */
    public SplayTree() {
        this.root = null;
    }

    //
    // --- Private Helper Methods for Rotations ---
    //

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

    //
    // --- Splaying Operation ---
    //

    /**
     * The main splay operation. It brings the node with the given key
     * (or the last accessed node if the key is not found) to the root of the tree.
     * This is a recursive, bottom-up splay implementation.
     *
     * @param node The root of the current subtree.
     * @param key The key to search for and splay.
     * @return The new root of the tree after splaying.
     */
    private Node splay(Node node, int key) {
        // Base case: node is null or key is at the root of the subtree.
        if (node == null || node.key == key) {
            return node;
        }

        // Key is in the left subtree
        if (key < node.key) {
            // If left child is null, the key is not in the tree.
            if (node.left == null) {
                return node;
            }

            // Zig-Zig (Left-Left)
            if (key < node.left.key) {
                // Recursively bring the key to the root of the left-left grandchild's subtree.
                node.left.left = splay(node.left.left, key);
                // Perform the first rotation for the grandparent (current node).
                node = rightRotate(node);
            }
            // Zig-Zag (Left-Right)
            else if (key > node.left.key) {
                // Recursively bring the key to the root of the left-right grandchild's subtree.
                node.left.right = splay(node.left.right, key);
                // Perform the first rotation for the parent (node.left).
                if (node.left.right != null) {
                    node.left = leftRotate(node.left);
                }
            }

            // Perform the second rotation for the grandparent (or parent if it was a simple Zig).
            // A null check is needed in case the child became null after rotations.
            return (node.left == null) ? node : rightRotate(node);

        } else { // Key is in the right subtree
            // If right child is null, the key is not in the tree.
            if (node.right == null) {
                return node;
            }

            // Zig-Zag (Right-Left)
            if (key < node.right.key) {
                // Recursively bring the key to the root of the right-left grandchild's subtree.
                node.right.left = splay(node.right.left, key);
                // Perform the first rotation for the parent (node.right).
                if (node.right.left != null) {
                    node.right = rightRotate(node.right);
                }
            }
            // Zig-Zig (Right-Right)
            else if (key > node.right.key) {
                // Recursively bring the key to the root of the right-right grandchild's subtree.
                node.right.right = splay(node.right.right, key);
                // Perform the first rotation for the grandparent (current node).
                node = leftRotate(node);
            }

            // Perform the second rotation for the grandparent (or parent if it was a simple Zig).
            return (node.right == null) ? node : leftRotate(node);
        }
    }

    //
    // --- Public API Methods ---
    //

    /**
     * Searches for a key in the tree. If the key is found, it is splayed
     * to the root.
     *
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
     * Inserts a key into the splay tree. If the key already exists,
     * the tree remains unchanged (as it's a set).
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

        // If the key is already at the root, it's a duplicate, so do nothing.
        if (root.key == key) {
            return;
        }

        // Create the new node.
        Node newNode = new Node(key);

        // The new node becomes the new root. The old root and its subtrees
        // are attached as children of the new root.
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
     * Deletes a key from the splay tree. If the key is not found,
     * the tree remains unchanged.
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
        // We need to merge its left and right subtrees.
        Node leftSubtree = root.left;
        Node rightSubtree = root.right;

        if (leftSubtree == null) {
            // If there's no left subtree, the right subtree becomes the new tree.
            root = rightSubtree;
        } else {
            // Splay the left subtree to bring its maximum element to the root.
            // This maximum element will have no right child.
            leftSubtree = splay(leftSubtree, key); // or Integer.MAX_VALUE

            // Attach the original right subtree as the right child of the new root.
            leftSubtree.right = rightSubtree;
            root = leftSubtree;
        }
    }
}