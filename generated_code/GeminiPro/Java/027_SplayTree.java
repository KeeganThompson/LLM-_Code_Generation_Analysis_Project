import java.util.NoSuchElementException;

/**
 * A self-contained implementation of an integer set using a Splay Tree.
 * A splay tree is a self-balancing binary search tree with the additional
 * property that recently accessed elements are quick to access again.
 * It performs basic operations such as insertion, deletion, and search.
 * After a search or an access, the accessed node is moved to the root of the
 * tree via a series of rotations, which is called "splaying".
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
     * Constructs an empty SplayTree.
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
     *        y           x
     *       / \         / \
     *      x   C  -->  A   y
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
     * Brings the given node to the root of the tree using a series of rotations.
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
        this.root = x;
    }

    /**
     * Searches for a key in the tree. If the key is found, the corresponding node
     * is splayed to the root. If not found, the last accessed node on the search
     * path is splayed to the root.
     *
     * @param key The key to search for.
     * @return The key if found, otherwise null.
     */
    public Integer search(int key) {
        if (root == null) {
            return null;
        }

        Node current = root;
        Node lastAccessed = root;

        while (current != null) {
            lastAccessed = current;
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

        // Key not found, splay the last accessed node
        splay(lastAccessed);

        // After splaying, the root might be the key if the last accessed node was it
        // (This check is redundant given the logic above, but safe)
        if (root.key == key) {
            return root.key;
        }

        return null;
    }

    /**
     * Inserts a key into the splay tree.
     * If the key already exists, the tree remains unchanged (as it's a set).
     * The newly inserted node (or the existing node if the key was a duplicate)
     * becomes the new root of the tree.
     *
     * @param key The key to insert.
     */
    public void insert(int key) {
        // Handle empty tree case
        if (root == null) {
            root = new Node(key);
            return;
        }

        // Splay the tree on the key. This brings the closest node to the root.
        search(key);

        // If key is already present, search would have splayed it to the root.
        if (root.key == key) {
            return;
        }

        // Create the new node
        Node newNode = new Node(key);

        // Split the tree and insert the new node as the new root
        if (key < root.key) {
            newNode.right = root;
            newNode.left = root.left;
            if (root.left != null) {
                root.left.parent = newNode;
            }
            root.left = null;
            root.parent = newNode;
        } else { // key > root.key
            newNode.left = root;
            newNode.right = root.right;
            if (root.right != null) {
                root.right.parent = newNode;
            }
            root.right = null;
            root.parent = newNode;
        }
        
        // The new node is the new root
        root = newNode;
    }

    /**
     * Deletes a key from the splay tree.
     * If the key is not in the tree, the tree is splayed on the last accessed
     * node and remains structurally unchanged otherwise.
     *
     * @param key The key to delete.
     */
    public void delete(int key) {
        if (root == null) {
            return;
        }

        // Splay the node (or its neighbor) to the root
        search(key);

        // If key is not at the root after splaying, it's not in the tree.
        if (root.key != key) {
            return;
        }

        // Now, the node to delete is at the root.
        Node leftSubtree = root.left;
        Node rightSubtree = root.right;

        if (leftSubtree == null) {
            // If there's no left child, the right child becomes the new root.
            root = rightSubtree;
            if (root != null) {
                root.parent = null;
            }
        } else {
            // Make the left subtree the main tree for now.
            leftSubtree.parent = null;

            // Find the maximum node in the left subtree.
            Node maxNode = leftSubtree;
            while (maxNode.right != null) {
                maxNode = maxNode.right;
            }

            // Splay this max node. It becomes the new root of the left part.
            // After this splay, maxNode will be the root and have no right child.
            this.root = leftSubtree; // Temporarily change root to perform splay on the subtree
            splay(maxNode);

            // Join the original right subtree.
            this.root.right = rightSubtree;
            if (rightSubtree != null) {
                rightSubtree.parent = this.root;
            }
        }
    }
}