/**
 * A complete, self-contained implementation of a Splay Tree that functions as an integer set.
 * Splay trees are self-balancing binary search trees with the property that recently
 * accessed elements are moved to the root, making subsequent accesses faster.
 */
public class SplayTree {

    /**
     * Represents a node in the Splay Tree.
     * It is a private static inner class as it's tightly coupled with the SplayTree.
     */
    private static class Node {
        int key;
        Node left;
        Node right;

        /**
         * Constructs a new node with the given key.
         * @param key The integer key for the node.
         */
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

    /**
     * Performs a right rotation on the subtree rooted at node x.
     * This is a helper function for the splay operation.
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
     * This is a helper function for the splay operation.
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
     * The core splay operation. It moves the node with the given key (or the last
     * accessed node if the key is not found) to the root of the tree.
     * This is a top-down splay implementation, which is generally more efficient
     * than a recursive bottom-up approach.
     * @param key The key of the node to splay to the root.
     */
    private void splay(int key) {
        if (root == null) {
            return;
        }

        // Use a dummy node to simplify linking of left and right subtrees.
        Node header = new Node(0); // The key in the dummy node is arbitrary.
        Node leftTreeMax = header;
        Node rightTreeMin = header;

        Node current = root;

        while (true) {
            if (key < current.key) {
                if (current.left == null) {
                    break;
                }
                // Zig-Zig case (left-left): Rotate right
                if (key < current.left.key) {
                    current = rightRotate(current);
                    if (current.left == null) {
                        break;
                    }
                }
                // Link to the right tree (nodes greater than the current path)
                rightTreeMin.left = current;
                rightTreeMin = current;
                current = current.left;
            } else if (key > current.key) {
                if (current.right == null) {
                    break;
                }
                // Zig-Zig case (right-right): Rotate left
                if (key > current.right.key) {
                    current = leftRotate(current);
                    if (current.right == null) {
                        break;
                    }
                }
                // Link to the left tree (nodes smaller than the current path)
                leftTreeMax.right = current;
                leftTreeMax = current;
                current = current.right;
            } else {
                // Key found, break the loop
                break;
            }
        }

        // Reassemble the tree by connecting the left and right subtrees
        // to the new root (the splayed node).
        leftTreeMax.right = current.left;
        rightTreeMin.left = current.right;
        current.left = header.right;
        current.right = header.left;

        root = current;
    }

    /**
     * Inserts a key into the splay tree.
     * If the key already exists, the tree is splayed on that key, but no new node is added,
     * maintaining the set property.
     * @param key The key to insert.
     */
    public void insert(int key) {
        // Case 1: The tree is empty.
        if (root == null) {
            root = new Node(key);
            return;
        }

        // Splay the tree on the key. This brings the closest node to the root.
        splay(key);

        // Case 2: The key is already in the tree. Do nothing.
        if (root.key == key) {
            return;
        }

        Node newNode = new Node(key);
        if (key < root.key) {
            // The new node becomes the new root.
            // The old root becomes the right child of the new node.
            // The old root's left child becomes the left child of the new node.
            newNode.left = root.left;
            newNode.right = root;
            root.left = null;
            root = newNode;
        } else { // key > root.key
            // The new node becomes the new root.
            // The old root becomes the left child of the new node.
            // The old root's right child becomes the right child of the new node.
            newNode.right = root.right;
            newNode.left = root;
            root.right = null;
            root = newNode;
        }
    }

    /**
     * Deletes a key from the splay tree.
     * If the key is not found, the tree is splayed on the last accessed node,
     * and no other action is taken.
     * @param key The key to delete.
     */
    public void delete(int key) {
        if (root == null) {
            return; // Tree is empty.
        }

        // Splay the tree on the key. If the key exists, it becomes the root.
        splay(key);

        // If the key is not in the tree, the root will be the closest node, but not the key.
        if (root.key != key) {
            return; // Key not found, nothing to delete.
        }

        // The node to delete is now the root.
        Node leftSubtree = root.left;
        Node rightSubtree = root.right;

        if (leftSubtree == null) {
            // If there's no left subtree, the right subtree becomes the new tree.
            root = rightSubtree;
        } else {
            // Make the left subtree the main tree temporarily.
            root = leftSubtree;
            // Splay on the (original) key to bring the largest element of the left
            // subtree to its root. The key is guaranteed to be larger than any element
            // in the left subtree, so this splay will bring the max element to the root.
            splay(key);
            // After splaying, the new root of the (former) left subtree has no right child.
            // We can now attach the original right subtree as its right child.
            root.right = rightSubtree;
        }
    }

    /**
     * Searches for a key in the splay tree.
     * This operation performs a splay, moving the accessed node (or the last
     * node on the search path if the key is not found) to the root of the tree.
     * @param key The key to search for.
     * @return The key as an Integer object if found, otherwise null.
     */
    public Integer search(int key) {
        if (root == null) {
            return null;
        }
        splay(key);
        // After splaying, if the key exists, it must be at the root.
        if (root.key == key) {
            return root.key;
        } else {
            return null;
        }
    }
}