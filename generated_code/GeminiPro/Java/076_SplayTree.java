import java.util.NoSuchElementException;

/**
 * A Splay Tree implementation that stores a set of integers.
 *
 * A splay tree is a self-adjusting binary search tree with the additional
 * property that recently accessed elements are quick to access again.
 * It performs basic operations such as insertion, look-up and removal
 * in O(log n) amortized time.
 */
public class SplayTree {

    /**
     * Represents a node in the Splay Tree.
     */
    private static class Node {
        int key;
        Node parent;
        Node left;
        Node right;

        Node(int key) {
            this.key = key;
            this.parent = null;
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
     * Performs a left rotation on the given node x.
     *
     *      x               y
     *     / \             / \
     *    A   y    -->    x   C
     *       / \         / \
     *      B   C       A   B
     *
     * @param x The node to rotate.
     */
    private void leftRotate(Node x) {
        Node y = x.right;
        if (y != null) {
            x.right = y.left;
            if (y.left != null) {
                y.left.parent = x;
            }
            y.parent = x.parent;
            if (x.parent == null) {
                this.root = y;
            } else if (x == x.parent.left) {
                x.parent.left = y;
            } else {
                x.parent.right = y;
            }
            y.left = x;
            x.parent = y;
        }
    }

    /**
     * Performs a right rotation on the given node x.
     *
     *        x           y
     *       / \         / \
     *      y   C  -->  A   x
     *     / \             / \
     *    A   B           B   C
     *
     * @param x The node to rotate.
     */
    private void rightRotate(Node x) {
        Node y = x.left;
        if (y != null) {
            x.left = y.right;
            if (y.right != null) {
                y.right.parent = x;
            }
            y.parent = x.parent;
            if (x.parent == null) {
                this.root = y;
            } else if (x == x.parent.left) {
                x.parent.left = y;
            } else {
                x.parent.right = y;
            }
            y.right = x;
            x.parent = y;
        }
    }

    /**
     * Moves the given node x to the root of the tree using a series of rotations.
     *
     * @param x The node to move to the root.
     */
    private void splay(Node x) {
        while (x.parent != null) {
            Node parent = x.parent;
            Node grandParent = parent.parent;

            if (grandParent == null) { // Zig case
                if (x == parent.left) {
                    rightRotate(parent);
                } else {
                    leftRotate(parent);
                }
            } else {
                if (x == parent.left && parent == grandParent.left) { // Zig-Zig case (left-left)
                    rightRotate(grandParent);
                    rightRotate(parent);
                } else if (x == parent.right && parent == grandParent.right) { // Zig-Zig case (right-right)
                    leftRotate(grandParent);
                    leftRotate(parent);
                } else if (x == parent.right && parent == grandParent.left) { // Zig-Zag case (left-right)
                    leftRotate(parent);
                    rightRotate(grandParent);
                } else { // Zig-Zag case (right-left)
                    rightRotate(parent);
                    leftRotate(grandParent);
                }
            }
        }
        this.root = x;
    }

    /**
     * Inserts a key into the splay tree.
     * If the key already exists, the node with that key is splayed to the root.
     *
     * @param key The key to insert.
     */
    public void insert(int key) {
        if (root == null) {
            root = new Node(key);
            return;
        }

        Node current = root;
        Node parent = null;
        while (current != null) {
            parent = current;
            if (key < current.key) {
                current = current.left;
            } else if (key > current.key) {
                current = current.right;
            } else {
                // Key already exists, splay the existing node and return
                splay(current);
                return;
            }
        }

        Node newNode = new Node(key);
        newNode.parent = parent;
        if (key < parent.key) {
            parent.left = newNode;
        } else {
            parent.right = newNode;
        }

        // Splay the new node to the root
        splay(newNode);
    }

    /**
     * Searches for a key in the splay tree.
     * If the key is found, the corresponding node is splayed to the root.
     * If the key is not found, the last accessed node is splayed to the root.
     *
     * @param key The key to search for.
     * @return The key if found, otherwise null.
     */
    public Integer search(int key) {
        Node current = root;
        Node lastAccessed = null;

        while (current != null) {
            lastAccessed = current;
            if (key < current.key) {
                current = current.left;
            } else if (key > current.key) {
                current = current.right;
            } else {
                // Key found, splay the node and return the key
                splay(current);
                return current.key;
            }
        }

        // Key not found, splay the last accessed node (if any)
        if (lastAccessed != null) {
            splay(lastAccessed);
        }
        return null;
    }

    /**
     * Deletes a key from the splay tree.
     *
     * @param key The key to delete.
     */
    public void delete(int key) {
        // Search for the key. This will splay the node to the root if it exists,
        // or the last-accessed node if it doesn't.
        search(key);

        // If the key is not in the tree, or the tree is empty, do nothing.
        // After search, if the key was found, it must be at the root.
        if (root == null || root.key != key) {
            return;
        }

        Node leftSubtree = root.left;
        Node rightSubtree = root.right;

        if (leftSubtree == null) {
            // No left child, the right subtree becomes the new tree
            root = rightSubtree;
            if (root != null) {
                root.parent = null;
            }
        } else {
            // Disconnect the left subtree from the old root
            leftSubtree.parent = null;

            // Find the maximum node in the left subtree
            Node maxNode = leftSubtree;
            while (maxNode.right != null) {
                maxNode = maxNode.right;
            }

            // Splay this max node. It becomes the new root of the combined tree.
            // We temporarily set the root to the left subtree to perform the splay within it.
            this.root = leftSubtree;
            splay(maxNode);

            // The new root is now maxNode. Attach the original right subtree.
            // After splaying, maxNode (now the root) has no right child.
            root.right = rightSubtree;
            if (rightSubtree != null) {
                rightSubtree.parent = root;
            }
        }
    }
}