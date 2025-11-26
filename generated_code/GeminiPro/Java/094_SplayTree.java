/**
 * A self-contained Java class implementing a Splay Tree for an integer set.
 * Splay trees are self-balancing binary search trees with the additional property
 * that recently accessed elements are quick to access again.
 */
public class SplayTree {

    /**
     * Inner class to represent a node in the Splay Tree.
     * It includes a parent reference, which is crucial for the splay operation.
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
     * Constructs an empty SplayTree.
     */
    public SplayTree() {
        this.root = null;
    }

    // --- Public API ---

    /**
     * Inserts a key into the splay tree.
     * If the key already exists, the tree is splayed on that key.
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
                // Key already exists, splay the node and return
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

        splay(newNode);
    }

    /**
     * Deletes a key from the splay tree.
     * If the key is not found, the tree structure is modified by splaying the last accessed node.
     *
     * @param key The integer key to delete.
     */
    public void delete(int key) {
        if (root == null) {
            return;
        }

        // Search for the key and splay the last accessed node to the root.
        search(key);

        // After search, if the root's key doesn't match, the key was not in the tree.
        if (root.key != key) {
            return;
        }

        // The node to delete is now the root.
        Node leftSubtree = root.left;
        Node rightSubtree = root.right;

        if (leftSubtree == null) {
            // No left child, the right subtree becomes the new tree.
            this.root = rightSubtree;
            if (this.root != null) {
                this.root.parent = null;
            }
        } else {
            // Disconnect the left subtree to work on it.
            leftSubtree.parent = null;

            // Find the maximum node in the left subtree.
            Node maxNode = leftSubtree;
            while (maxNode.right != null) {
                maxNode = maxNode.right;
            }

            // To use our splay method, we temporarily set the main root to the left subtree's root.
            this.root = leftSubtree;
            splay(maxNode); // maxNode is now the root of the modified left subtree.

            // `this.root` now points to maxNode. Attach the original right subtree.
            this.root.right = rightSubtree;
            if (rightSubtree != null) {
                rightSubtree.parent = this.root;
            }
        }
    }

    /**
     * Searches for a key in the splay tree.
     * This operation performs a splay. If the key is found, the node containing the key
     * is moved to the root. If the key is not found, the last non-null node accessed
     * during the search is moved to the root.
     *
     * @param key The integer key to search for.
     * @return The key if found, otherwise null.
     */
    public Integer search(int key) {
        if (root == null) {
            return null;
        }

        Node current = root;
        Node lastNode = root; // To splay the last visited node

        while (current != null) {
            lastNode = current;
            if (key < current.key) {
                current = current.left;
            } else if (key > current.key) {
                current = current.right;
            } else {
                // Key found
                splay(current);
                return key;
            }
        }

        // Key not found, splay the last visited node
        splay(lastNode);

        // After splaying, if the new root's key is not what we looked for,
        // it means the key was not in the tree.
        if (root != null && root.key == key) {
            return key;
        } else {
            return null;
        }
    }

    // --- Private Helper Methods ---

    /**
     * Performs the splay operation on a node x, moving it to the root.
     *
     * @param x The node to splay.
     */
    private void splay(Node x) {
        if (x == null) return;

        while (x.parent != null) {
            Node parent = x.parent;
            Node grandParent = parent.parent;

            if (grandParent == null) { // Zig case
                if (x == parent.left) {
                    rightRotate(parent);
                } else {
                    leftRotate(parent);
                }
            } else { // Zig-Zig or Zig-Zag
                if (x == parent.left && parent == grandParent.left) { // Zig-Zig (left-left)
                    rightRotate(grandParent);
                    rightRotate(parent);
                } else if (x == parent.right && parent == grandParent.right) { // Zig-Zig (right-right)
                    leftRotate(grandParent);
                    leftRotate(parent);
                } else if (x == parent.right && parent == grandParent.left) { // Zig-Zag (left-right)
                    leftRotate(parent);
                    rightRotate(grandParent);
                } else { // Zig-Zag (right-left)
                    rightRotate(parent);
                    leftRotate(grandParent);
                }
            }
        }
        this.root = x;
    }

    /**
     * Performs a left rotation on the given node.
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
     * Performs a right rotation on the given node.
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
}