/**
 * A complete, self-contained Java class that implements an integer set using a Splay Tree.
 * Splay trees are self-balancing binary search trees with the property that recently
 * accessed elements are quick to access again. This implementation uses a top-down
 * splaying approach.
 */
public class SplayTree {

    /**
     * Inner class representing a node in the Splay Tree.
     * It is static because it does not need to access instance members of the outer class.
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
     * Constructs an empty Splay Tree.
     */
    public SplayTree() {
        this.root = null;
    }

    // --- Private Helper Methods for Rotations ---

    /**
     * Performs a right rotation on the subtree rooted at node x.
     * @param x The root of the subtree to rotate.
     * @return The new root of the rotated subtree.
     */
    private Node rightRotate(Node x) {
        Node y = x.left;
        x.left = y.right;
        y.right = x;
        return y;
    }

    /**
     * Performs a left rotation on the subtree rooted at node x.
     * @param x The root of the subtree to rotate.
     * @return The new root of the rotated subtree.
     */
    private Node leftRotate(Node x) {
        Node y = x.right;
        x.right = y.left;
        y.left = x;
        return y;
    }

    // --- Core Splay Operation ---

    /**
     * Performs the top-down splay operation. It brings the node with the given key
     * (or the last accessed node on the search path if the key is not found)
     * to the root of the tree.
     *
     * @param node The root of the tree/subtree to splay.
     * @param key The key to splay for.
     * @return The new root of the splayed tree.
     */
    private Node splay(Node node, int key) {
        if (node == null) {
            return null;
        }

        // Use a dummy node to simplify linking of left and right subtrees.
        Node dummy = new Node(0);
        Node leftTreeMax = dummy;
        Node rightTreeMin = dummy;
        Node current = node;

        while (true) {
            if (key < current.key) {
                if (current.left == null) break;
                // Zig-Zig (Left-Left) case
                if (key < current.left.key) {
                    current = rightRotate(current);
                    if (current.left == null) break;
                }
                // Link current node to the right tree (nodes greater than key)
                rightTreeMin.left = current;
                rightTreeMin = current;
                current = current.left;
            } else if (key > current.key) {
                if (current.right == null) break;
                // Zig-Zig (Right-Right) case
                if (key > current.right.key) {
                    current = leftRotate(current);
                    if (current.right == null) break;
                }
                // Link current node to the left tree (nodes smaller than key)
                leftTreeMax.right = current;
                leftTreeMax = current;
                current = current.right;
            } else {
                // Key found, break the loop
                break;
            }
        }

        // Reassemble the tree
        leftTreeMax.right = current.left;
        rightTreeMin.left = current.right;
        current.left = dummy.right;
        current.right = dummy.left;

        return current;
    }

    // --- Public API Methods ---

    /**
     * Searches for a key in the tree. If the key is found, the corresponding node
     * is splayed to become the new root. If not found, the last accessed node on
     * the search path is splayed to the root.
     *
     * @param key The key to search for.
     * @return The key if it is found in the tree, otherwise null.
     */
    public Integer search(int key) {
        if (root == null) {
            return null;
        }
        root = splay(root, key);
        if (root.key == key) {
            return key;
        }
        return null;
    }

    /**
     * Inserts a key into the Splay Tree. If the key already exists, the tree
     * remains unchanged (as it is a set). The new or existing node with the
     * given key is splayed to the root.
     *
     * @param key The key to insert.
     */
    public void insert(int key) {
        if (root == null) {
            root = new Node(key);
            return;
        }

        // Splay the tree for the key. This brings the closest node to the root.
        root = splay(root, key);

        // If the key is already present, we are done.
        if (root.key == key) {
            return;
        }

        // Otherwise, insert the new node as the new root.
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
     * Deletes a key from the Splay Tree. If the key is not in the tree,
     * the tree remains unchanged.
     *
     * @param key The key to delete.
     */
    public void delete(int key) {
        if (root == null) {
            return;
        }

        // Splay the tree for the key.
        root = splay(root, key);

        // If the key is not at the root after splaying, it's not in the tree.
        if (root.key != key) {
            return;
        }

        // The node to delete is now at the root.
        Node leftSubtree = root.left;
        Node rightSubtree = root.right;

        if (leftSubtree == null) {
            // If there's no left subtree, the right subtree becomes the new tree.
            root = rightSubtree;
        } else {
            // Splay the left subtree to bring its maximum element to the top.
            // We splay for the key we are deleting, which is guaranteed to be
            // larger than any key in the left subtree.
            Node newRootForLeft = splay(leftSubtree, key);

            // The new root of the left subtree (its max element) will now have no right child.
            // We can attach the original right subtree to it.
            newRootForLeft.right = rightSubtree;
            root = newRootForLeft;
        }
    }
}