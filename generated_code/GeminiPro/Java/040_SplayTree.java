/**
 * A self-contained implementation of an integer set using a Splay Tree.
 * A splay tree is a self-adjusting binary search tree with the additional
 * property that recently accessed elements are quick to access again.
 * It performs basic operations such as insertion, deletion, and search in
 * O(log n) amortized time.
 */
public class SplayTree {

    private Node root;

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

    /**
     * Constructs an empty Splay Tree.
     */
    public SplayTree() {
        this.root = null;
    }

    /**
     * Performs a right rotation on the subtree rooted at y.
     * @param y The root of the subtree to rotate.
     * @return The new root of the rotated subtree.
     */
    private Node rightRotate(Node y) {
        Node x = y.left;
        y.left = x.right;
        x.right = y;
        return x;
    }

    /**
     * Performs a left rotation on the subtree rooted at x.
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
     * This is a top-down splay implementation.
     * @param key The key to splay to the root.
     */
    private void splay(int key) {
        if (root == null) {
            return;
        }

        // Use a dummy node to simplify linking of left and right subtrees.
        Node dummy = new Node(0);
        Node leftTreeMax = dummy;
        Node rightTreeMin = dummy;
        Node current = root;

        while (true) {
            if (key < current.key) {
                if (current.left == null) {
                    break;
                }
                // Zig-Zig (Right-Right rotation)
                if (key < current.left.key) {
                    current = rightRotate(current);
                    if (current.left == null) {
                        break;
                    }
                }
                // Link current node to the right subtree's left-most branch
                rightTreeMin.left = current;
                rightTreeMin = current;
                current = current.left;
            } else if (key > current.key) {
                if (current.right == null) {
                    break;
                }
                // Zig-Zig (Left-Left rotation)
                if (key > current.right.key) {
                    current = leftRotate(current);
                    if (current.right == null) {
                        break;
                    }
                }
                // Link current node to the left subtree's right-most branch
                leftTreeMax.right = current;
                leftTreeMax = current;
                current = current.right;
            } else { // key == current.key
                break;
            }
        }

        // Reassemble the tree
        leftTreeMax.right = current.left;
        rightTreeMin.left = current.right;
        current.left = dummy.right;
        current.right = dummy.left;

        root = current;
    }

    /**
     * Searches for a key in the tree. If found, it splays the node to the root
     * and returns the key. If not found, it splays the last accessed node to the
     * root and returns null.
     *
     * @param key The key to search for.
     * @return The key if found, otherwise null.
     */
    public Integer search(int key) {
        if (root == null) {
            return null;
        }
        splay(key);
        // After splaying, if the key is in the tree, it must be the root.
        if (root.key == key) {
            return key;
        }
        return null;
    }

    /**
     * Inserts a key into the splay tree. If the key already exists,
     * the tree is splayed on that key, but no new node is inserted.
     *
     * @param key The key to insert.
     */
    public void insert(int key) {
        // If the tree is empty, create a new root.
        if (root == null) {
            root = new Node(key);
            return;
        }

        // Splay the tree on the key.
        // If key is present, it moves to the root.
        // If not, the last accessed node moves to the root.
        splay(key);

        // If key is already at the root, we are done (set behavior).
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
     * Deletes a key from the splay tree. If the key is not found,
     * the tree is splayed on the last accessed node, and the tree remains unchanged.
     *
     * @param key The key to delete.
     */
    public void delete(int key) {
        if (root == null) {
            return;
        }

        // Splay the tree on the key. If the key is present, it becomes the root.
        splay(key);

        // If the key is not in the tree, the root's key will not match.
        if (root.key != key) {
            return;
        }

        // Now, the node to be deleted is the root.
        Node leftSubtree = root.left;
        Node rightSubtree = root.right;

        if (leftSubtree == null) {
            root = rightSubtree;
        } else {
            // Find the maximum key in the left subtree.
            Node maxNode = leftSubtree;
            while (maxNode.right != null) {
                maxNode = maxNode.right;
            }
            int maxKey = maxNode.key;

            // Splay the max key to the root of the left subtree.
            // We temporarily treat the left subtree as the whole tree for splaying.
            root = leftSubtree;
            splay(maxKey);

            // After splaying, the new root (which is the max node) has no right child.
            // We can now attach the original right subtree.
            root.right = rightSubtree;
        }
    }
}