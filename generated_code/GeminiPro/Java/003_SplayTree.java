/**
 * A complete, self-contained implementation of an integer set using a Splay Tree.
 * A splay tree is a self-adjusting binary search tree with the additional property
 * that recently accessed elements are quick to access again. It performs basic
 * operations such as insertion, look-up and removal in O(log n) amortized time.
 */
public class SplayTree {

    private Node root;

    /**
     * Represents a node in the Splay Tree.
     * This is a private static inner class to encapsulate the node structure.
     */
    private static class Node {
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
     *
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
     * Performs the top-down splay operation.
     * Moves the node with the given key (or the last accessed node if the key is not found)
     * to the root of the tree.
     *
     * @param root The root of the tree to splay.
     * @param key  The key to splay for.
     * @return The new root of the splayed tree.
     */
    private Node splay(Node root, int key) {
        if (root == null) {
            return null;
        }

        // Use a dummy node to simplify linking
        Node dummy = new Node(0);
        Node leftTreeMax = dummy;
        Node rightTreeMin = dummy;
        Node current = root;

        while (true) {
            if (key < current.key) {
                if (current.left == null) break;
                // Zig-Zig (Right Rotation)
                if (key < current.left.key) {
                    current = rightRotate(current);
                    if (current.left == null) break;
                }
                // Link current to the right tree
                rightTreeMin.left = current;
                rightTreeMin = current;
                current = current.left;
            } else if (key > current.key) {
                if (current.right == null) break;
                // Zig-Zig (Left Rotation)
                if (key > current.right.key) {
                    current = leftRotate(current);
                    if (current.right == null) break;
                }
                // Link current to the left tree
                leftTreeMax.right = current;
                leftTreeMax = current;
                current = current.right;
            } else {
                // Key found
                break;
            }
        }

        // Reassemble the tree
        leftTreeMax.right = current.left;
        rightTreeMin.left = current.right;
        current.left = dummy.right;
        current.right = dummy.left;

        return current;
    }

    /**
     * Searches for a key in the tree and splays the accessed node to the root.
     *
     * @param key The key to search for.
     * @return The key if found, otherwise null.
     */
    public Integer search(int key) {
        root = splay(root, key);
        if (root == null || root.key != key) {
            return null;
        }
        return root.key;
    }

    /**
     * Inserts a key into the tree.
     * If the key already exists, the existing node is splayed to the root.
     * If the key is new, it is inserted and becomes the new root.
     *
     * @param key The key to insert.
     */
    public void insert(int key) {
        // If tree is empty, create a new root
        if (root == null) {
            root = new Node(key);
            return;
        }

        // Splay the tree for the key. The closest node will become the root.
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
     * Deletes a key from the tree.
     * The node (or its parent if not found) is splayed to the root before deletion.
     *
     * @param key The key to delete.
     */
    public void delete(int key) {
        if (root == null) return;

        // Splay the node to be deleted (or its parent) to the root
        root = splay(root, key);

        // If the key is not in the tree, do nothing
        if (root.key != key) {
            return;
        }

        // Now the key to be deleted is at the root
        Node leftSubtree = root.left;
        Node rightSubtree = root.right;

        if (leftSubtree == null) {
            root = rightSubtree;
        } else {
            // Splay the largest element in the left subtree to its root
            // This element becomes the new root of the whole tree
            Node newRoot = splay(leftSubtree, key);
            newRoot.right = rightSubtree;
            root = newRoot;
        }
    }
}