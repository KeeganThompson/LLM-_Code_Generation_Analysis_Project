/**
 * A self-contained Java class that implements an integer set using a Splay Tree.
 * A splay tree is a self-adjusting binary search tree with the additional property
 * that recently accessed elements are quick to access again.
 */
public class SplayTree {

    /**
     * Represents a node in the Splay Tree.
     * It is a private static inner class as it's tightly coupled with SplayTree
     * and doesn't need to access instance members of the outer class.
     */
    private static class Node {
        int key;
        Node left;
        Node right;

        Node(int key) {
            this.key = key;
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
     * Performs a right rotation on the subtree rooted at node x.
     *
     * @param x The root of the subtree to rotate.
     * @return The new root of the subtree after rotation.
     */
    private Node rightRotate(Node x) {
        Node y = x.left;
        x.left = y.right;
        y.right = x;
        return y;
    }

    /**
     * Performs a left rotation on the subtree rooted at node x.
     *
     * @param x The root of the subtree to rotate.
     * @return The new root of the subtree after rotation.
     */
    private Node leftRotate(Node x) {
        Node y = x.right;
        x.right = y.left;
        y.left = x;
        return y;
    }

    /**
     * The core splaying operation. It moves the node with the given key
     * (or the last accessed node on the search path) to the root of the tree.
     * This implementation uses the top-down, iterative approach.
     *
     * @param key The key to splay on.
     */
    private void splay(int key) {
        if (root == null) {
            return;
        }

        // A dummy node to simplify the logic of linking subtrees.
        // header.left will point to the Right tree, header.right to the Left tree.
        Node header = new Node(0);
        Node leftTreeMax = header;
        Node rightTreeMin = header;
        Node current = root;

        while (true) {
            if (key < current.key) {
                if (current.left == null) {
                    break;
                }
                // Zig-Zig (Left-Left) case: Rotate right first
                if (key < current.left.key) {
                    current = rightRotate(current);
                    if (current.left == null) {
                        break;
                    }
                }
                // Link the current root to the right tree
                rightTreeMin.left = current;
                rightTreeMin = current;
                current = current.left;
            } else if (key > current.key) {
                if (current.right == null) {
                    break;
                }
                // Zig-Zig (Right-Right) case: Rotate left first
                if (key > current.right.key) {
                    current = leftRotate(current);
                    if (current.right == null) {
                        break;
                    }
                }
                // Link the current root to the left tree
                leftTreeMax.right = current;
                leftTreeMax = current;
                current = current.right;
            } else {
                // Key found
                break;
            }
        }

        // Reassemble the tree
        leftTreeMax.right = current.left;
        rightTreeMin.left = current.right;
        current.left = header.right;
        current.right = header.left;

        root = current;
    }

    /**
     * Searches for a key in the tree. If the key is found, the corresponding
     * node is splayed to the root.
     *
     * @param key The key to search for.
     * @return The key if it is found, otherwise null.
     */
    public Integer search(int key) {
        if (root == null) {
            return null;
        }
        splay(key);
        // After splaying, the key should be at the root if it exists.
        if (root.key == key) {
            return root.key;
        }
        return null;
    }

    /**
     * Inserts a key into the splay tree.
     * If the key already exists, the node with the key is splayed to the root.
     *
     * @param key The key to insert.
     */
    public void insert(int key) {
        if (root == null) {
            root = new Node(key);
            return;
        }

        // Splay the tree on the key. The closest node will become the new root.
        splay(key);

        // If the key is already in the tree, we are done.
        if (root.key == key) {
            return;
        }

        Node newNode = new Node(key);
        if (key < root.key) {
            newNode.right = root;
            newNode.left = root.left;
            root.left = null;
        } else { // key > root.key
            newNode.left = root;
            newNode.right = root.right;
            root.right = null;
        }
        root = newNode;
    }

    /**
     * Deletes a key from the splay tree.
     *
     * @param key The key to delete.
     */
    public void delete(int key) {
        if (root == null) {
            return;
        }

        // Splay the tree on the key. If the key exists, it will become the root.
        splay(key);

        // If the key is not at the root after splaying, it's not in the tree.
        if (root.key != key) {
            return;
        }

        // The node to delete is now the root.
        Node leftSubtree = root.left;
        Node rightSubtree = root.right;

        if (leftSubtree == null) {
            // If there is no left child, the right child becomes the new root.
            root = rightSubtree;
        } else {
            // Make the left subtree the new tree.
            root = leftSubtree;
            // Splay on the (deleted) key again in the new tree. This brings the
            // largest element in the left subtree (the predecessor of the deleted key)
            // to the root of the new tree.
            splay(key);
            // After splaying, the new root has no right child.
            // Attach the original right subtree as the right child of the new root.
            root.right = rightSubtree;
        }
    }
}