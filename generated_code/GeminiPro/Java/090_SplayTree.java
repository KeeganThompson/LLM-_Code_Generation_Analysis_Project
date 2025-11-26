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
     * The core splay operation. Moves the node with the given key to the root of the tree.
     * If the key is not in the tree, the last accessed node is moved to the root.
     * This implementation uses a top-down splaying approach.
     *
     * @param root The root of the tree to splay.
     * @param key  The key to splay to the root.
     * @return The new root of the splayed tree.
     */
    private Node splay(Node root, int key) {
        if (root == null) {
            return null;
        }

        // Dummy node to simplify linking of left and right subtrees.
        Node header = new Node(0);
        Node leftTreeMax = header;
        Node rightTreeMin = header;

        while (true) {
            if (key < root.key) {
                if (root.left == null) break;
                // Zig-Zig (Right-Right)
                if (key < root.left.key) {
                    root = rightRotate(root);
                    if (root.left == null) break;
                }
                // Link to the right tree
                rightTreeMin.left = root;
                rightTreeMin = root;
                root = root.left;
            } else if (key > root.key) {
                if (root.right == null) break;
                // Zig-Zig (Left-Left)
                if (key > root.right.key) {
                    root = leftRotate(root);
                    if (root.right == null) break;
                }
                // Link to the left tree
                leftTreeMax.right = root;
                leftTreeMax = root;
                root = root.right;
            } else { // key == root.key
                break;
            }
        }

        // Reassemble the tree
        leftTreeMax.right = root.left;
        rightTreeMin.left = root.right;
        root.left = header.right;
        root.right = header.left;

        return root;
    }

    /**
     * Searches for a key in the tree. If found, the node is splayed to the root.
     *
     * @param key The key to search for.
     * @return The key if found, otherwise null.
     */
    public Integer search(int key) {
        if (root == null) {
            return null;
        }
        root = splay(root, key);
        // After splaying, if the key exists, it will be at the root.
        if (root.key == key) {
            return root.key;
        }
        return null;
    }

    /**
     * Inserts a key into the splay tree.
     * If the key already exists, the tree remains unchanged.
     *
     * @param key The key to insert.
     */
    public void insert(int key) {
        // If the tree is empty, create a new root.
        if (root == null) {
            root = new Node(key);
            return;
        }

        // Splay the tree around the key. The closest node (or the node itself) will become the root.
        root = splay(root, key);

        // If the key is already in the tree, do nothing.
        if (root.key == key) {
            return;
        }

        // Create the new node.
        Node newNode = new Node(key);

        // The new node becomes the root. The old root becomes a child.
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
     * @param key The key to delete.
     */
    public void delete(int key) {
        if (root == null) {
            return; // Tree is empty.
        }

        // Splay the key to the root.
        root = splay(root, key);

        // If the key is not in the tree, the root will be a neighbor.
        // If the root's key doesn't match, the key wasn't present.
        if (root.key != key) {
            return;
        }

        // Now, the node to delete is at the root.
        Node leftSubtree = root.left;
        Node rightSubtree = root.right;

        if (leftSubtree == null) {
            // If there's no left subtree, the right subtree becomes the new tree.
            root = rightSubtree;
        } else {
            // Splay the left subtree to bring its largest element to its root.
            // Splaying for the key we are deleting achieves this, as it's larger than any element in the left subtree.
            Node newRoot = splay(leftSubtree, key);
            
            // The new root's right child will be null after the splay.
            // Attach the original right subtree there.
            newRoot.right = rightSubtree;
            root = newRoot;
        }
    }
}