/**
 * A complete, self-contained implementation of an integer Splay Tree.
 *
 * A splay tree is a self-balancing binary search tree with the additional
 * property that recently accessed elements are quick to access again. It performs
 * basic operations such as insertion, deletion, and search. When an element is
 * accessed (e.g., through search, insertion, or deletion), it is "splayed"
 * to become the new root of the tree.
 *
 * This implementation supports the following public methods for an integer set:
 * - insert(int key): Adds a key to the set. If the key already exists, the
 *   existing node is splayed to the root.
 * - delete(int key): Removes a key from the set.
 * - search(int key): Searches for a key. If found, it returns the key and
 *   splays the found node to the root. If not found, it returns null and splays
 *   the last accessed node to the root.
 */
public class SplayTree {

    /**
     * Represents a node in the Splay Tree.
     * It is an inner class to be used only by the SplayTree class.
     */
    private class Node {
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
        root = null;
    }

    /**
     * Performs a left rotation on the given node x.
     *
     *      x
     *     / \
     *    A   y
     *       / \
     *      B   C
     *
     * becomes
     *
     *      y
     *     / \
     *    x   C
     *   / \
     *  A   B
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
     *        x
     *       / \
     *      y   C
     *     / \
     *    A   B
     *
     * becomes
     *
     *      y
     *     / \
     *    A   x
     *       / \
     *      B   C
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
            } else if (x == x.parent.right) {
                x.parent.right = y;
            } else {
                x.parent.left = y;
            }
            y.right = x;
            x.parent = y;
        }
    }

    /**
     * Moves the given node to the root of the tree using a series of rotations.
     *
     * @param x The node to splay.
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
                if (x == parent.left) {
                    if (parent == grandParent.left) { // Zig-Zig case
                        rightRotate(grandParent);
                        rightRotate(parent);
                    } else { // Zig-Zag case
                        rightRotate(parent);
                        leftRotate(grandParent);
                    }
                } else {
                    if (parent == grandParent.left) { // Zig-Zag case
                        leftRotate(parent);
                        rightRotate(grandParent);
                    } else { // Zig-Zig case
                        leftRotate(grandParent);
                        leftRotate(parent);
                    }
                }
            }
        }
    }

    /**
     * Inserts a key into the splay tree.
     * If the key already exists, the node with that key is splayed to the root.
     *
     * @param key The key to insert.
     */
    public void insert(int key) {
        Node node = new Node(key);
        Node parent = null;
        Node current = this.root;

        while (current != null) {
            parent = current;
            if (node.key < current.key) {
                current = current.left;
            } else if (node.key > current.key) {
                current = current.right;
            } else {
                // Key already exists, splay the found node and return
                splay(current);
                return;
            }
        }

        node.parent = parent;
        if (parent == null) {
            root = node; // Tree was empty
        } else if (node.key < parent.key) {
            parent.left = node;
        } else {
            parent.right = node;
        }

        // Splay the newly inserted node
        splay(node);
    }

    /**
     * Searches for a key in the splay tree.
     * If the key is found, the corresponding node is splayed to the root and the
     * key is returned.
     * If the key is not found, the last accessed node on the search path is
     * splayed to the root and null is returned.
     *
     * @param key The key to search for.
     * @return The key if found, otherwise null.
     */
    public Integer search(int key) {
        if (root == null) {
            return null;
        }

        Node current = root;
        Node lastNode = root;

        while (current != null) {
            lastNode = current;
            if (key < current.key) {
                current = current.left;
            } else if (key > current.key) {
                current = current.right;
            } else {
                // Key found
                splay(current);
                return current.key;
            }
        }

        // Key not found, splay the last visited node
        splay(lastNode);

        // After splaying, the new root might be the key if it was found,
        // but our loop logic already handled that. If we are here, key was not found.
        return null;
    }

    /**
     * Deletes a key from the splay tree.
     *
     * @param key The key to delete.
     */
    public void delete(int key) {
        // First, search for the key. This splays the node (or its neighbor) to the root.
        search(key);

        // If root is null or key is not at the root, the key wasn't in the tree.
        if (root == null || root.key != key) {
            return;
        }

        Node nodeToDelete = root;
        Node leftSubtree = nodeToDelete.left;
        Node rightSubtree = nodeToDelete.right;

        // Case 1: No left child. The right child becomes the new root.
        if (leftSubtree == null) {
            root = rightSubtree;
            if (root != null) {
                root.parent = null;
            }
        }
        // Case 2: Has a left child.
        else {
            // Detach the left subtree to work on it independently
            leftSubtree.parent = null;

            // Find the maximum node in the left subtree
            Node maxNode = leftSubtree;
            while (maxNode.right != null) {
                maxNode = maxNode.right;
            }

            // Temporarily make the left subtree the main tree to splay within it
            this.root = leftSubtree;
            splay(maxNode); // maxNode is now the root of the (modified) left subtree

            // The new root of the entire tree is this splayed maxNode
            // Attach the original right subtree
            this.root.right = rightSubtree;
            if (rightSubtree != null) {
                rightSubtree.parent = this.root;
            }
        }
    }
}