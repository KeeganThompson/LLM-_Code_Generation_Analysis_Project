/**
 * A complete, self-contained Java class that implements an integer set using a Splay Tree.
 * A splay tree is a self-balancing binary search tree with the additional property that
 * recently accessed elements are quick to access again. All major operations (insert,
 * delete, search) involve a "splaying" step, which moves the accessed node to the root.
 */
public class SplayTree {

    /**
     * Inner class representing a node in the splay tree.
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
     * Performs a right rotation on the given node x.
     *
     * <pre>
     *     y         x
     *    / \       / \
     *   x   C --> A   y
     *  / \           / \
     * A   B         B   C
     * </pre>
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
     * This is the core operation of a splay tree.
     *
     * @param x The node to splay.
     */
    private void splay(Node x) {
        while (x.parent != null) {
            Node parent = x.parent;
            Node grandParent = parent.parent;
            if (grandParent == null) { // Zig step
                if (x == parent.left) {
                    rightRotate(parent);
                } else {
                    leftRotate(parent);
                }
            } else { // Zig-Zig or Zig-Zag step
                if (x == parent.left) {
                    if (parent == grandParent.left) { // Zig-Zig (left-left)
                        rightRotate(grandParent);
                        rightRotate(parent);
                    } else { // Zig-Zag (right-left)
                        rightRotate(parent);
                        leftRotate(grandParent);
                    }
                } else {
                    if (parent == grandParent.left) { // Zig-Zag (left-right)
                        leftRotate(parent);
                        rightRotate(grandParent);
                    } else { // Zig-Zig (right-right)
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
        Node current = this.root;
        Node parent = null;
        while (current != null) {
            parent = current;
            if (key < current.key) {
                current = current.left;
            } else if (key > current.key) {
                current = current.right;
            } else {
                // Key already exists, splay the existing node and return.
                splay(current);
                return;
            }
        }

        Node newNode = new Node(key);
        newNode.parent = parent;

        if (parent == null) {
            this.root = newNode; // Tree was empty
        } else if (key < parent.key) {
            parent.left = newNode;
        } else {
            parent.right = newNode;
        }

        // Splay the newly inserted node to the root.
        splay(newNode);
    }

    /**
     * Searches for a key in the splay tree.
     * If the key is found, the corresponding node is splayed to the root and the key is returned.
     * If the key is not found, the last accessed node in the search path is splayed to the root
     * and null is returned.
     *
     * @param key The key to search for.
     * @return The key as an Integer if found, otherwise null.
     */
    public Integer search(int key) {
        Node nodeToSplay = findNode(key);
        if (nodeToSplay != null) {
            splay(nodeToSplay);
            // After splaying, the node is at the root. Check if its key matches.
            if (this.root.key == key) {
                return this.root.key;
            }
        }
        return null;
    }
    
    /**
     * Helper method to find a node or the last visited node on the search path.
     * This is used to determine which node to splay after an access.
     *
     * @param key The key to find.
     * @return The node containing the key, or the last visited node if not found.
     *         Returns null if the tree is empty.
     */
    private Node findNode(int key) {
        Node current = this.root;
        Node lastNode = null;
        while (current != null) {
            lastNode = current;
            if (key < current.key) {
                current = current.left;
            } else if (key > current.key) {
                current = current.right;
            } else {
                return current; // Found the key
            }
        }
        return lastNode; // Return last visited node if key not found
    }

    /**
     * Deletes a key from the splay tree.
     *
     * @param key The key to delete.
     */
    public void delete(int key) {
        // First, splay the node (or its closest predecessor/successor) to the root.
        Node nodeToSplay = findNode(key);
        if (nodeToSplay == null) {
            return; // Tree is empty
        }
        splay(nodeToSplay);

        // If the key is not at the root after splaying, it's not in the tree.
        if (this.root.key != key) {
            return;
        }

        // The node to delete is now the root.
        Node leftSubtree = this.root.left;
        Node rightSubtree = this.root.right;

        if (leftSubtree == null) {
            // If there's no left subtree, the right subtree becomes the new tree.
            this.root = rightSubtree;
            if (this.root != null) {
                this.root.parent = null;
            }
        } else {
            // Disconnect the left subtree to treat it as its own tree.
            leftSubtree.parent = null;

            // Find the maximum node in the left subtree.
            Node maxInLeft = leftSubtree;
            while (maxInLeft.right != null) {
                maxInLeft = maxInLeft.right;
            }

            // To splay maxInLeft to the root of the left subtree, we can temporarily
            // set the main root to the left subtree's root.
            this.root = leftSubtree;
            splay(maxInLeft); // Now, maxInLeft is the root of the modified left subtree.

            // Join the original right subtree to the new root.
            // After splaying, maxInLeft has no right child.
            this.root.right = rightSubtree;
            if (rightSubtree != null) {
                rightSubtree.parent = this.root;
            }
        }
    }
}