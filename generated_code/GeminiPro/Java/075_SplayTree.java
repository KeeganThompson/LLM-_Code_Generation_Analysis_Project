/**
 * A complete, self-contained Java class that implements an integer set using a Splay Tree.
 * The splay tree is a self-balancing binary search tree with the additional property
 * that recently accessed elements are quick to access again.
 */
public class SplayTree {

    /**
     * Inner class representing a node in the splay tree.
     * It is kept private to encapsulate the tree's internal structure.
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

    private Node root;

    /**
     * Default constructor initializes an empty Splay Tree.
     */
    public SplayTree() {
        this.root = null;
    }

    // --- Core Splay Tree Operations: Rotations and Splaying ---

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
     * The splay operation. It brings the node with the given key to the root of the tree.
     * If the key is not present, the last accessed node (the one that would be the parent
     * of the key if it were present) is brought to the root.
     * This is a recursive, bottom-up implementation.
     *
     * @param node The root of the current subtree.
     * @param key The key to splay.
     * @return The new root of the splayed tree.
     */
    private Node splay(Node node, int key) {
        // Base cases: if the node is null or the key is at the root
        if (node == null || node.key == key) {
            return node;
        }

        // Key is in the left subtree
        if (key < node.key) {
            // If the left child is null, the key is not in the tree
            if (node.left == null) {
                return node;
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
            // Perform the second rotation (or the first if it's a Zig case)
            return (node.left == null) ? node : rightRotate(node);
        }
        // Key is in the right subtree
        else {
            // If the right child is null, the key is not in the tree
            if (node.right == null) {
                return node;
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
            // Perform the second rotation (or the first if it's a Zig case)
            return (node.right == null) ? node : leftRotate(node);
        }
    }

    // --- Public API for the Integer Set ---

    /**
     * Searches for a key in the tree. If found, the node containing the key is
     * splayed to the root.
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
     * Inserts a new key into the splay tree. Duplicates are not allowed.
     *
     * @param key The key to insert.
     */
    public void insert(int key) {
        // Handle the case of an empty tree
        if (root == null) {
            root = new Node(key);
            return;
        }

        // Splay the tree around the key. The closest node becomes the root.
        root = splay(root, key);

        // If the key is already present, do nothing.
        if (root.key == key) {
            return;
        }

        // Create the new node
        Node newNode = new Node(key);

        // The old root becomes a child of the new node
        if (key < root.key) {
            newNode.right = root;
            newNode.left = root.left;
            root.left = null;
        } else { // key > root.key
            newNode.left = root;
            newNode.right = root.right;
            root.right = null;
        }
        // The new node is the new root
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

        // Splay the tree to bring the node to delete to the root
        root = splay(root, key);

        // If the key is not in the tree, do nothing
        if (root.key != key) {
            return;
        }

        // The node to delete is now the root.
        // We need to merge its left and right subtrees.
        Node leftSubtree = root.left;
        Node rightSubtree = root.right;

        if (leftSubtree == null) {
            // If there's no left subtree, the right subtree becomes the new tree
            root = rightSubtree;
        } else {
            // Find the maximum element in the left subtree by splaying for the key
            // (which is guaranteed to be the largest). This brings the max element
            // to the root of the left subtree.
            leftSubtree = splay(leftSubtree, key);

            // Attach the original right subtree to the new root of the left subtree.
            leftSubtree.right = rightSubtree;
            root = leftSubtree;
        }
    }
}