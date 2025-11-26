/**
 * A self-contained implementation of an integer set using a Splay Tree.
 * A splay tree is a self-balancing binary search tree with the additional
 * property that recently accessed elements are quick to access again.
 */
public class SplayTree {

    /**
     * Inner class representing a node in the Splay Tree.
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

    // --- Core Splay Operation ---

    /**
     * Moves the given node x to the root of the tree using a series of rotations.
     * This is the core operation that gives the splay tree its self-balancing property.
     * @param x The node to move to the root.
     */
    private void splay(Node x) {
        if (x == null) {
            return;
        }

        while (x.parent != null) {
            Node parent = x.parent;
            Node grandParent = parent.parent;

            if (grandParent == null) { // Zig case: Parent is the root
                if (x == parent.left) {
                    rightRotate(parent);
                } else {
                    leftRotate(parent);
                }
            } else { // Zig-Zig or Zig-Zag cases
                if (x == parent.left) {
                    if (parent == grandParent.left) { // Zig-Zig (left-left)
                        rightRotate(grandParent);
                        rightRotate(parent);
                    } else { // Zig-Zag (left-right)
                        rightRotate(parent);
                        leftRotate(grandParent);
                    }
                } else { // x is the right child
                    if (parent == grandParent.left) { // Zig-Zag (right-left)
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

    // --- Rotation Helpers ---

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

    // --- Public API ---

    /**
     * Inserts a key into the splay tree.
     * If the key already exists, the node with that key is splayed to the root.
     * @param key The integer key to insert.
     */
    public void insert(int key) {
        Node current = this.root;
        Node parent = null;

        // 1. Find position for new node (standard BST insert)
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

        // 3. Splay the newly inserted node to make it the new root
        splay(newNode);
    }

    /**
     * Searches for a key in the tree.
     * If found, the corresponding node is splayed to the root and the key is returned.
     * If not found, the last non-null node accessed on the search path is splayed
     * to the root, and null is returned.
     * @param key The integer key to search for.
     * @return The key as an Integer if found, otherwise null.
     */
    public Integer search(int key) {
        Node current = root;
        Node lastNode = null;

        while (current != null) {
            lastNode = current;
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
        if (lastNode != null) {
            splay(lastNode);
        }
        return null;
    }

    /**
     * Deletes a key from the splay tree.
     * @param key The integer key to delete.
     */
    public void delete(int key) {
        // 1. Search for the key. This splays the node (if found) or its
        // would-be parent to the root.
        search(key);

        // 2. After search, if the root's key doesn't match, the key was not in the tree.
        if (root == null || root.key != key) {
            return;
        }

        // 3. The node to delete is now the root.
        Node leftSubtree = root.left;
        Node rightSubtree = root.right;

        if (leftSubtree == null) {
            // If there's no left subtree, the right subtree becomes the new tree.
            this.root = rightSubtree;
            if (rightSubtree != null) {
                rightSubtree.parent = null;
            }
        } else {
            // Disconnect the left subtree to work on it.
            leftSubtree.parent = null;

            // Find the maximum node in the left subtree.
            Node maxNodeInLeft = leftSubtree;
            while (maxNodeInLeft.right != null) {
                maxNodeInLeft = maxNodeInLeft.right;
            }

            // Splay this maximum node. It will become the new root of the combined tree.
            // Temporarily set the root to the left subtree to perform the splay within it.
            this.root = leftSubtree;
            splay(maxNodeInLeft);

            // After splaying, maxNodeInLeft is the root and has no right child.
            // Attach the original right subtree as its right child.
            this.root.right = rightSubtree;
            if (rightSubtree != null) {
                rightSubtree.parent = this.root;
            }
        }
    }
}