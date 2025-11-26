/**
 * A complete, self-contained implementation of a Splay Tree that stores integers.
 * Splay trees are self-balancing binary search trees with the property that
 * recently accessed elements are quick to access again. This implementation
 * supports insertion, deletion, and search operations.
 */
public class SplayTree {

    /**
     * Inner class representing a node in the Splay Tree.
     * It includes a parent pointer to simplify rotation and splay operations.
     */
    private class Node {
        int key;
        Node left, right, parent;

        Node(int key) {
            this.key = key;
            this.left = null;
            this.right = null;
            this.parent = null;
        }
    }

    private Node root;

    /**
     * Constructs an empty Splay Tree.
     */
    public SplayTree() {
        this.root = null;
    }

    // --- Core Splay Operations ---

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
     * This is done by a series of rotations (Zig, Zig-Zig, Zig-Zag).
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
                    if (parent == grandParent.right) { // Zig-Zig case
                        leftRotate(grandParent);
                        leftRotate(parent);
                    } else { // Zig-Zag case
                        leftRotate(parent);
                        rightRotate(grandParent);
                    }
                }
            }
        }
    }

    // --- Public API ---

    /**
     * Inserts a key into the splay tree.
     * If the key already exists, the existing node is splayed to the root.
     * Otherwise, a new node is created and splayed to the root.
     *
     * @param key The integer key to insert.
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
                // Key already exists, splay this node and return.
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

        // Splay the newly inserted node to the root.
        splay(newNode);
    }

    /**
     * Searches for a key in the tree and performs the splaying operation.
     * This method will splay the node containing the key to the root if found.
     * If the key is not found, it splays the last accessed node on the search path.
     *
     * @param key The key to search for.
     * @return The key as an Integer if found, otherwise null.
     */
    public Integer search(int key) {
        if (root == null) {
            return null;
        }
        
        Node current = root;
        Node lastNode = root; // Keep track of the last non-null node on the path
        
        while (current != null) {
            lastNode = current;
            if (key < current.key) {
                current = current.left;
            } else if (key > current.key) {
                current = current.right;
            } else {
                // Key found, splay the node and return
                splay(current);
                return current.key;
            }
        }
        
        // Key not found, splay the last visited node
        splay(lastNode);
        
        // After splaying, check if the new root has the key
        if (root.key == key) {
            return root.key;
        } else {
            return null;
        }
    }

    /**
     * Deletes a key from the splay tree.
     * This operation first finds the node, splays it to the root, and then removes it
     * by joining its two subtrees.
     *
     * @param key The key to delete.
     */
    public void delete(int key) {
        // Search for the key. This will bring the node (or a nearby one) to the root.
        search(key);

        // If the key is not at the root after searching, it was not in the tree.
        if (root == null || root.key != key) {
            return;
        }

        // The node to delete is now at the root.
        Node leftSubtree = root.left;
        Node rightSubtree = root.right;

        if (leftSubtree == null) {
            root = rightSubtree;
            if (root != null) {
                root.parent = null;
            }
        } else {
            // Disconnect the left subtree to work on it.
            leftSubtree.parent = null;

            // Find the maximum node in the left subtree.
            Node maxInLeft = leftSubtree;
            while (maxInLeft.right != null) {
                maxInLeft = maxInLeft.right;
            }

            // Splay this max node to the root of the left subtree.
            // Temporarily set the main root to the left subtree's root to use the splay method.
            this.root = leftSubtree;
            splay(maxInLeft);

            // After splaying, `this.root` is the new root (maxInLeft).
            // Now, join the original right subtree.
            this.root.right = rightSubtree;
            if (rightSubtree != null) {
                rightSubtree.parent = this.root;
            }
        }
    }
}