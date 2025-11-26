/**
 * A complete, self-contained Java class that implements an integer set using a Splay Tree.
 * Splay trees are self-balancing binary search trees with the property that recently
 * accessed elements are quick to access again. This implementation supports insert, delete,
 * and search operations. The search operation splays the accessed node to the root.
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
     * The core splay operation. It moves the node with the given key (or the last
     * accessed node if the key is not present) to the root of the tree.
     * This is a top-down splay implementation.
     *
     * @param node The root of the tree (or subtree) to splay.
     * @param key  The key to splay around.
     * @return The new root of the splayed tree.
     */
    private Node splay(Node node, int key) {
        if (node == null) {
            return null;
        }

        // Use a dummy node to simplify linking
        Node dummy = new Node(0);
        Node leftTreeMax = dummy;
        Node rightTreeMin = dummy;

        while (true) {
            if (key < node.key) {
                if (node.left == null) {
                    break;
                }
                // Zig-Zig case (left-left)
                if (key < node.left.key) {
                    // Rotate right
                    Node temp = node.left;
                    node.left = temp.right;
                    temp.right = node;
                    node = temp;
                    if (node.left == null) {
                        break;
                    }
                }
                // Link to the right tree
                rightTreeMin.left = node;
                rightTreeMin = node;
                node = node.left;
            } else if (key > node.key) {
                if (node.right == null) {
                    break;
                }
                // Zig-Zig case (right-right)
                if (key > node.right.key) {
                    // Rotate left
                    Node temp = node.right;
                    node.right = temp.left;
                    temp.left = node;
                    node = temp;
                    if (node.right == null) {
                        break;
                    }
                }
                // Link to the left tree
                leftTreeMax.right = node;
                leftTreeMax = node;
                node = node.right;
            } else {
                // Key found
                break;
            }
        }

        // Reassemble the tree
        leftTreeMax.right = node.left;
        rightTreeMin.left = node.right;
        node.left = dummy.right;
        node.right = dummy.left;

        return node;
    }

    /**
     * Inserts a key into the Splay Tree. If the key already exists,
     * the node containing the key is splayed to the root.
     *
     * @param key The key to insert.
     */
    public void insert(int key) {
        if (root == null) {
            root = new Node(key);
            return;
        }

        // Splay the tree around the key. The new root will be the node
        // with the key or the closest value.
        root = splay(root, key);

        // If key is already present, do nothing.
        if (root.key == key) {
            return;
        }

        Node newNode = new Node(key);
        if (key < root.key) {
            newNode.left = root.left;
            newNode.right = root;
            root.left = null;
            root = newNode;
        } else { // key > root.key
            newNode.right = root.right;
            newNode.left = root;
            root.right = null;
            root = newNode;
        }
    }

    /**
     * Searches for a key in the tree. If the key is found, it is splayed
     * to the root. If not found, the last accessed node on the search path
     * is splayed to the root.
     *
     * @param key The key to search for.
     * @return The key as an Integer if found, otherwise null.
     */
    public Integer search(int key) {
        root = splay(root, key);
        if (root == null || root.key != key) {
            return null;
        }
        return root.key;
    }

    /**
     * Deletes a key from the Splay Tree. If the key is found, it is removed
     * and the tree is rebalanced.
     *
     * @param key The key to delete.
     */
    public void delete(int key) {
        if (root == null) {
            return;
        }

        // Splay the node to be deleted to the root.
        root = splay(root, key);

        // If the key is not in the tree, do nothing.
        if (root.key != key) {
            return;
        }

        Node leftSubtree = root.left;
        Node rightSubtree = root.right;

        if (leftSubtree == null) {
            root = rightSubtree;
        } else {
            // Splay the left subtree to bring its maximum element to its root.
            // Splaying for 'key' in the left subtree will achieve this because 'key'
            // is greater than any element in the left subtree.
            Node newRoot = splay(leftSubtree, key);
            newRoot.right = rightSubtree;
            root = newRoot;
        }
    }
}