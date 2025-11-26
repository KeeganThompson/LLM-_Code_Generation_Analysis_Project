/**
 * A self-contained Java class implementing a Splay Tree for a set of integers.
 * A Splay Tree is a self-balancing binary search tree with the additional property
 * that recently accessed elements are quick to access again. It performs basic
 * operations such as insertion, deletion, and search. After any of these operations,
 * the accessed node is moved to the root of the tree through a process called "splaying".
 */
public class SplayTree {

    /**
     * Represents a node in the Splay Tree.
     * This is a private static inner class to encapsulate the node structure.
     */
    private static class Node {
        int key;
        Node left, right;

        /**
         * Constructs a new node with the given key.
         *
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
     * The core splaying operation. Moves the node with the given key, or the last
     * accessed node if the key is not found, to the root of the tree.
     * This implementation uses the top-down splaying technique.
     *
     * @param key The key to splay.
     */
    private void splay(int key) {
        if (root == null) {
            return;
        }

        // Dummy node to simplify linking. header.right will be the root of the
        // "left" tree (elements smaller than the key) and header.left will be
        // the root of the "right" tree (elements larger than the key).
        Node header = new Node(0); // Dummy node, key value is irrelevant.
        Node leftTreeMax = header;
        Node rightTreeMin = header;

        Node current = root;

        while (true) {
            if (key < current.key) {
                if (current.left == null) {
                    break;
                }
                // Zig-Zig case (Right Rotation)
                if (key < current.left.key) {
                    Node temp = current.left;
                    current.left = temp.right;
                    temp.right = current;
                    current = temp;
                    if (current.left == null) {
                        break;
                    }
                }
                // Link to the right tree
                rightTreeMin.left = current;
                rightTreeMin = current;
                current = current.left;
            } else if (key > current.key) {
                if (current.right == null) {
                    break;
                }
                // Zig-Zig case (Left Rotation)
                if (key > current.right.key) {
                    Node temp = current.right;
                    current.right = temp.left;
                    temp.left = current;
                    current = temp;
                    if (current.right == null) {
                        break;
                    }
                }
                // Link to the left tree
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
     * Searches for a key in the tree. If the key is found, it is splayed
     * to the root. If not found, the last accessed node is splayed to the root.
     *
     * @param key The key to search for.
     * @return The key if found, otherwise null.
     */
    public Integer search(int key) {
        if (root == null) {
            return null;
        }
        splay(key);
        if (root.key == key) {
            return key;
        }
        return null;
    }

    /**
     * Inserts a key into the tree. Duplicates are not allowed.
     * The newly inserted node becomes the new root of the tree.
     *
     * @param key The key to insert.
     */
    public void insert(int key) {
        // If the tree is empty, create a new root.
        if (root == null) {
            root = new Node(key);
            return;
        }

        // Splay the tree for the key.
        splay(key);

        // If the key is already present, do nothing.
        if (root.key == key) {
            return;
        }

        Node newNode = new Node(key);

        // The new node becomes the root. The old root becomes a child.
        if (key < root.key) {
            newNode.left = root.left;
            newNode.right = root;
            root.left = null;
        } else { // key > root.key
            newNode.right = root.right;
            newNode.left = root;
            root.right = null;
        }
        root = newNode;
    }

    /**
     * Deletes a key from the tree.
     * After deletion, the parent of the deleted node (or a nearby node) is splayed to the root.
     *
     * @param key The key to delete.
     */
    public void delete(int key) {
        if (root == null) {
            return;
        }

        // Splay the tree for the key. If the key exists, it becomes the root.
        splay(key);

        // If the key is not at the root, it's not in the tree.
        if (root.key != key) {
            return;
        }

        // Now, the node to be deleted is the root.
        Node leftSubtree = root.left;
        Node rightSubtree = root.right;

        if (leftSubtree == null) {
            // If there's no left subtree, the right subtree becomes the new tree.
            root = rightSubtree;
        } else {
            // Make the left subtree the main tree.
            root = leftSubtree;
            // Splay the left subtree for the key 'key'. This will bring the largest
            // element in the left subtree (the predecessor of the deleted key)
            // to the root of this new tree.
            splay(key);

            // The new root (the max of the old left subtree) has no right child.
            // Attach the original right subtree to it.
            root.right = rightSubtree;
        }
    }
}