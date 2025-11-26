/**
 * A complete, self-contained Java class that implements a Splay Tree for a set of integers.
 * A splay tree is a self-balancing binary search tree with the additional property
 * that recently accessed elements are quick to access again. It achieves this by
 * moving any accessed node to the root of the tree through a series of rotations.
 */
public class SplayTree {

    /**
     * Inner class to represent a node in the Splay Tree.
     * It includes a parent pointer to facilitate the splay operation.
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
        this.root = null;
    }

    // --- Core Splay Operations: Rotations and Splay ---

    /**
     * Performs a left rotation on the given node x.
     *
     * <pre>
     *   x           y
     *  / \         / \
     * A   y  -->  x   C
     *    / \     / \
     *   B   C   A   B
     * </pre>
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
     * <pre>
     *     y         x
     *    / \       / \
     *   x   C --> A   y
     *  / \           / \
     * A   B         B   C
     * </pre>
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
     * Performs the splay operation on a node x, moving it to the root of the tree.
     * This is done through a series of Zig, Zig-Zig, or Zig-Zag rotations.
     *
     * @param x The node to splay to the root.
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

    // --- Public API Methods ---

    /**
     * Searches for a key in the tree. As per splay tree properties, this operation
     * moves the accessed node to the root. If the key is not found, the last
     * non-null node on the search path is moved to the root.
     *
     * @param key The key to search for.
     * @return The integer key if found, otherwise null.
     */
    public Integer search(int key) {
        if (root == null) {
            return null;
        }

        Node current = root;
        while (true) {
            if (key < current.key) {
                if (current.left == null) {
                    splay(current); // Key not found, splay last accessed node
                    return null;
                }
                current = current.left;
            } else if (key > current.key) {
                if (current.right == null) {
                    splay(current); // Key not found, splay last accessed node
                    return null;
                }
                current = current.right;
            } else {
                splay(current); // Key found, splay it to the root
                return current.key;
            }
        }
    }

    /**
     * Inserts a key into the splay tree. The tree is a set, so duplicate keys are not inserted.
     * If the key already exists, the node containing it is splayed to the root.
     * Otherwise, the new node is inserted and then splayed to the root.
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
                // Key already exists, splay the node and return.
                splay(current);
                return;
            }
        }

        // Insert the new node as in a standard BST
        Node newNode = new Node(key);
        newNode.parent = parent;
        if (key < parent.key) {
            parent.left = newNode;
        } else {
            parent.right = newNode;
        }

        // Splay the newly inserted node to the root
        splay(newNode);
    }

    /**
     * Deletes a key from the splay tree.
     * The node with the given key (if it exists) is first splayed to the root.
     * The root is then removed, and the remaining left and right subtrees are joined.
     *
     * @param key The key to delete.
     */
    public void delete(int key) {
        // The search operation splays the found node (or last accessed) to the root.
        search(key);

        // If the key is not in the tree, after search, the root will not have the key.
        if (root == null || root.key != key) {
            return; // Key not found, nothing to delete.
        }

        // The node to delete is now at the root.
        Node leftSubtree = root.left;
        Node rightSubtree = root.right;

        if (leftSubtree == null) {
            // If there's no left child, the right child becomes the new root.
            root = rightSubtree;
            if (root != null) {
                root.parent = null;
            }
        } else {
            // Make the left subtree a standalone tree by detaching it.
            leftSubtree.parent = null;
            
            // Find the maximum node in the left subtree.
            Node maxNode = leftSubtree;
            while (maxNode.right != null) {
                maxNode = maxNode.right;
            }
            
            // To splay maxNode to the root of the left subtree, we temporarily
            // set the main SplayTree's root to the left subtree's root.
            this.root = leftSubtree;
            splay(maxNode);

            // After splaying, `this.root` is maxNode (the new root of the merged tree).
            // This new root will have no right child. We can now attach the original
            // right subtree to it.
            this.root.right = rightSubtree;
            if (rightSubtree != null) {
                rightSubtree.parent = this.root;
            }
        }
    }
}