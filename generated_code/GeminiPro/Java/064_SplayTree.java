/**
 * A complete, self-contained implementation of an integer Splay Tree.
 *
 * A splay tree is a self-adjusting binary search tree with the additional
 * property that recently accessed elements are quick to access again.
 * It performs basic operations such as insertion, look-up and removal in
 * O(log n) amortized time.
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

        /**
         * Constructs a new node with the given key.
         * @param key The integer key for the node.
         */
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
     *      x           y
     *     / \         / \
     *    A   y  -->  x   C
     *       / \     / \
     *      B   C   A   B
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
     * Performs a right rotation on the given node y.
     *
     *        y           x
     *       / \         / \
     *      x   C  -->  A   y
     *     / \             / \
     *    A   B           B   C
     *
     * @param y The node to rotate.
     */
    private void rightRotate(Node y) {
        Node x = y.left;
        if (x != null) {
            y.left = x.right;
            if (x.right != null) {
                x.right.parent = y;
            }
            x.parent = y.parent;
            if (y.parent == null) {
                this.root = x;
            } else if (y == y.parent.left) {
                y.parent.left = x;
            } else {
                y.parent.right = x;
            }
            x.right = y;
            y.parent = x;
        }
    }

    /**
     * Performs the splay operation on a node x, moving it to the root.
     * @param x The node to splay.
     */
    private void splay(Node x) {
        if (x == null) {
            return;
        }
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
        this.root = x;
    }

    /**
     * Searches for a key in the tree.
     * If the key is found, the node containing the key is splayed to the root.
     * If the key is not found, the last accessed node is splayed to the root.
     *
     * @param key The key to search for.
     * @return The key if found, otherwise null.
     */
    public Integer search(int key) {
        Node current = root;
        Node lastVisited = null;

        while (current != null) {
            lastVisited = current;
            if (key < current.key) {
                current = current.left;
            } else if (key > current.key) {
                current = current.right;
            } else {
                splay(current);
                return key;
            }
        }

        // Key not found, splay the last visited node
        if (lastVisited != null) {
            splay(lastVisited);
        }
        return null;
    }

    /**
     * Inserts a key into the splay tree.
     * If the key already exists, the node with that key is splayed to the root.
     * If the key is new, it is inserted and then the new node is splayed to the root.
     *
     * @param key The key to insert.
     */
    public void insert(int key) {
        Node current = this.root;
        Node parent = null;

        // 1. Find position to insert (standard BST insert)
        while (current != null) {
            parent = current;
            if (key < current.key) {
                current = current.left;
            } else if (key > current.key) {
                current = current.right;
            } else {
                // Key already exists, splay it and return
                splay(current);
                return;
            }
        }

        // 2. Create and link the new node
        Node newNode = new Node(key);
        newNode.parent = parent;

        if (parent == null) {
            this.root = newNode; // Tree was empty
        } else if (key < parent.key) {
            parent.left = newNode;
        } else {
            parent.right = newNode;
        }

        // 3. Splay the new node to the root
        splay(newNode);
    }

    /**
     * Deletes a key from the splay tree.
     *
     * @param key The key to delete.
     */
    public void delete(int key) {
        // Search for the key. This will splay the node (or its closest neighbor) to the root.
        search(key);

        // If the tree is empty or the key was not found, the root won't match.
        if (root == null || root.key != key) {
            return; // Key not found, nothing to delete.
        }

        // The node to delete is now the root.
        Node leftSubtree = root.left;
        Node rightSubtree = root.right;

        if (leftSubtree == null) {
            // No left child, so the right subtree becomes the new tree.
            root = rightSubtree;
            if (root != null) {
                root.parent = null;
            }
        } else {
            // Disconnect the left subtree.
            leftSubtree.parent = null;

            // Find the maximum node in the left subtree.
            Node maxNode = leftSubtree;
            while (maxNode.right != null) {
                maxNode = maxNode.right;
            }

            // Splay this maximum node to the root of the left subtree.
            // After this, the new root of the left subtree (maxNode) will have no right child.
            splay(maxNode);

            // The splay operation updates the global root, so we set it to maxNode.
            root = maxNode;
            
            // Attach the original right subtree to the new root.
            root.right = rightSubtree;
            if (rightSubtree != null) {
                rightSubtree.parent = root;
            }
        }
    }
}