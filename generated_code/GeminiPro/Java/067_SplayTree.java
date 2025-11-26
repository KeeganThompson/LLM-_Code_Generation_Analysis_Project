/**
 * A complete, self-contained Java class that implements an integer set using a Splay Tree.
 * Splay trees are self-balancing binary search trees with the property that recently
 * accessed elements are quick to access again. This implementation performs the splaying
 * operation on every search, insert, and delete.
 */
public class SplayTree {

    /**
     * Inner class to represent a node in the Splay Tree.
     * It is static because it does not need to access any instance members of SplayTree.
     */
    private static class Node {
        int key;
        Node left, right;

        /**
         * Constructor for a new node.
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
        root = null;
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
     * The core splay operation. It moves the node with the given key (or the last
     * accessed node on the search path) to the root of the tree.
     * This is a top-down splay implementation.
     *
     * @param root The root of the tree (or subtree) to splay.
     * @param key The key to splay for.
     * @return The new root of the splayed tree.
     */
    private Node splay(Node root, int key) {
        if (root == null) {
            return null;
        }

        // A dummy node to simplify linking of left and right subtrees.
        Node header = new Node(0); // The key value doesn't matter.
        Node leftTreeMax = header;
        Node rightTreeMin = header;

        while (true) {
            if (key < root.key) {
                if (root.left == null) {
                    break;
                }
                // Zig-Zig (Right-Right) case
                if (key < root.left.key) {
                    root = rightRotate(root);
                }
                // If after rotation the left child is null, we are done.
                if (root.left == null) {
                    break;
                }
                // Link Right: Add the current root to the right tree of the new tree.
                rightTreeMin.left = root;
                rightTreeMin = root;
                root = root.left;
            } else if (key > root.key) {
                if (root.right == null) {
                    break;
                }
                // Zig-Zig (Left-Left) case
                if (key > root.right.key) {
                    root = leftRotate(root);
                }
                // If after rotation the right child is null, we are done.
                if (root.right == null) {
                    break;
                }
                // Link Left: Add the current root to the left tree of the new tree.
                leftTreeMax.right = root;
                leftTreeMax = root;
                root = root.right;
            } else {
                // Key found, break the loop.
                break;
            }
        }

        // Reassemble the tree.
        leftTreeMax.right = root.left;
        rightTreeMin.left = root.right;
        root.left = header.right;
        root.right = header.left;

        return root;
    }

    /**
     * Searches for a key in the tree. If the key is found, it is splayed to the root.
     * If not found, the last accessed node on the search path is splayed to the root.
     *
     * @param key The key to search for.
     * @return The key if found, otherwise null.
     */
    public Integer search(int key) {
        if (root == null) {
            return null;
        }
        root = splay(root, key);
        if (root.key == key) {
            return root.key;
        }
        return null;
    }

    /**
     * Inserts a key into the splay tree. If the key already exists,
     * the node with that key is splayed to the root.
     *
     * @param key The key to insert.
     */
    public void insert(int key) {
        // If the tree is empty, create a new root.
        if (root == null) {
            root = new Node(key);
            return;
        }
        
        // Splay the tree around the key. The closest node will be at the root.
        root = splay(root, key);

        // If the key is already in the tree, do nothing.
        if (root.key == key) {
            return;
        }

        Node newNode = new Node(key);
        if (key < root.key) {
            // New node becomes the new root.
            // Old root becomes the right child of the new node.
            // Old root's left subtree becomes the left child of the new node.
            newNode.right = root;
            newNode.left = root.left;
            root.left = null;
            root = newNode;
        } else { // key > root.key
            // New node becomes the new root.
            // Old root becomes the left child of the new node.
            // Old root's right subtree becomes the right child of the new node.
            newNode.left = root;
            newNode.right = root.right;
            root.right = null;
            root = newNode;
        }
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

        // Splay the tree to bring the node to delete (or its successor/predecessor) to the root.
        root = splay(root, key);

        // If the key is not in the tree, do nothing.
        if (root.key != key) {
            return;
        }

        // Now, the node to delete is the root.
        Node leftSubtree = root.left;
        Node rightSubtree = root.right;

        if (leftSubtree == null) {
            // If there's no left child, the right child becomes the new root.
            root = rightSubtree;
        } else {
            // Splay the left subtree to bring its maximum element to its root.
            // Since `key` is guaranteed to be greater than any element in the left subtree,
            // splaying for `key` will bring the max element to the root of the left subtree.
            Node newRoot = splay(leftSubtree, key);
            
            // Attach the original right subtree to the new root.
            // The new root (max of left subtree) is guaranteed to have a null right child.
            newRoot.right = rightSubtree;
            root = newRoot;
        }
    }
}