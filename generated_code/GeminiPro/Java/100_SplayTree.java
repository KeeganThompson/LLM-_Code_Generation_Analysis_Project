/**
 * A self-contained Java class implementing a Splay Tree for an integer set.
 * Splay trees are self-balancing binary search trees with the additional property
 * that recently accessed elements are quick to access again.
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

    public SplayTree() {
        this.root = null;
    }

    /**
     * Rotates the subtree rooted at node x to the left.
     * This is a helper function for the splay operation.
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
     * Rotates the subtree rooted at node y to the right.
     * This is a helper function for the splay operation.
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
            } else if (y == y.parent.right) {
                y.parent.right = x;
            } else {
                y.parent.left = x;
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
            } else {
                if (x == parent.left) {
                    if (parent == grandParent.left) { // Zig-Zig case
                        rightRotate(grandParent);
                        rightRotate(parent);
                    } else { // Zig-Zag case
                        rightRotate(parent);
                        leftRotate(grandParent);
                    }
                } else { // x is right child
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
     * Searches for a key in the tree. If the key is found, the corresponding
     * node is splayed to the root. If not found, the last accessed node is splayed.
     *
     * @param key The key to search for.
     * @return The key if found, otherwise null.
     */
    public Integer search(int key) {
        if (root == null) {
            return null;
        }

        Node current = root;
        Node lastVisited = root;
        while (current != null) {
            lastVisited = current;
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
        splay(lastVisited);
        return null;
    }

    /**
     * Inserts a key into the Splay Tree. If the key already exists, the node
     * with that key is splayed to the root. Otherwise, a new node is inserted
     * and then splayed to the root.
     *
     * @param key The key to insert.
     */
    public void insert(int key) {
        // Standard BST insert
        Node newNode = new Node(key);
        Node parent = null;
        Node current = this.root;

        while (current != null) {
            parent = current;
            if (newNode.key < current.key) {
                current = current.left;
            } else if (newNode.key > current.key) {
                current = current.right;
            } else {
                // Key already exists. Splay the found node and return.
                splay(current);
                return;
            }
        }

        newNode.parent = parent;
        if (parent == null) {
            this.root = newNode; // Tree was empty
        } else if (newNode.key < parent.key) {
            parent.left = newNode;
        } else {
            parent.right = newNode;
        }

        // Splay the newly inserted node to the root
        splay(newNode);
    }

    /**
     * Deletes a key from the Splay Tree.
     *
     * @param key The key to delete.
     */
    public void delete(int key) {
        if (root == null) {
            return;
        }

        // Splay the node with the given key (or its neighbor) to the root.
        // First, perform a search to find the node to splay.
        Node nodeToSplay = root;
        Node lastVisited = root;
        while (nodeToSplay != null) {
            lastVisited = nodeToSplay;
            if (key < nodeToSplay.key) {
                nodeToSplay = nodeToSplay.left;
            } else if (key > nodeToSplay.key) {
                nodeToSplay = nodeToSplay.right;
            } else {
                break; // Found the node
            }
        }
        splay(lastVisited);

        // After splaying, the node (if it exists) or its neighbor is at the root.
        // If the key is not at the root, it was not in the tree.
        if (root.key != key) {
            return;
        }

        // The node to delete is now the root.
        Node leftSubtree = root.left;
        Node rightSubtree = root.right;

        if (leftSubtree == null) {
            root = rightSubtree;
            if (root != null) {
                root.parent = null;
            }
        } else {
            // Disconnect the left subtree
            leftSubtree.parent = null;

            // Find the maximum element in the left subtree
            Node maxNode = leftSubtree;
            while (maxNode.right != null) {
                maxNode = maxNode.right;
            }

            // Splay this max element. It will become the new root of the left subtree.
            // We temporarily set the main root to the left subtree to perform this splay.
            this.root = leftSubtree;
            splay(maxNode);

            // The new root (maxNode) now takes the original right subtree.
            this.root.right = rightSubtree;
            if (rightSubtree != null) {
                rightSubtree.parent = this.root;
            }
        }
    }
}