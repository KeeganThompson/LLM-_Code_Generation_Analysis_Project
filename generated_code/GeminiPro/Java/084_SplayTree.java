/**
 * A complete, self-contained implementation of an integer set using a Splay Tree.
 * Splay trees are self-balancing binary search trees with the additional property
 * that recently accessed elements are quick to access again. This implementation
 * supports insert, delete, and search operations.
 */
public class SplayTree {

    private Node root;

    /**
     * Private static inner class to represent a node in the tree.
     */
    private static class Node {
        int key;
        Node left, right;

        Node(int key) {
            this.key = key;
        }
    }

    /**
     * Constructs an empty SplayTree.
     */
    public SplayTree() {
        this.root = null;
    }

    // --- Core Splay Operation ---

    /**
     * Performs the splay operation on the given key.
     * It rearranges the tree so that the node with the given key (or the last
     * accessed node if the key is not found) is moved to the root.
     * This is a top-down splay implementation.
     *
     * @param node The root of the tree/subtree to splay.
     * @param key The key to splay for.
     * @return The new root of the splayed tree.
     */
    private Node splay(Node node, int key) {
        if (node == null) {
            return null;
        }

        // Dummy node to simplify linking.
        // leftTree's right child chain will store nodes smaller than the key.
        // rightTree's left child chain will store nodes larger than the key.
        Node dummy = new Node(0);
        Node leftTree = dummy;
        Node rightTree = dummy;
        Node current = node;

        while (true) {
            if (key < current.key) {
                if (current.left == null) break;
                // Zig-Zig (right-right)
                if (key < current.left.key) {
                    current = rightRotate(current);
                    if (current.left == null) break;
                }
                // Link current to the right tree
                rightTree.left = current;
                rightTree = current;
                current = current.left;
            } else if (key > current.key) {
                if (current.right == null) break;
                // Zig-Zig (left-left)
                if (key > current.right.key) {
                    current = leftRotate(current);
                    if (current.right == null) break;
                }
                // Link current to the left tree
                leftTree.right = current;
                leftTree = current;
                current = current.right;
            } else {
                // Key found
                break;
            }
        }

        // Reassemble the tree
        leftTree.right = current.left;
        rightTree.left = current.right;
        current.left = dummy.right;
        current.right = dummy.left;

        return current;
    }

    // --- Tree Rotations ---

    private Node rightRotate(Node y) {
        Node x = y.left;
        y.left = x.right;
        x.right = y;
        return x;
    }

    private Node leftRotate(Node x) {
        Node y = x.right;
        x.right = y.left;
        y.left = x;
        return y;
    }

    // --- Public API Methods ---

    /**
     * Inserts a key into the splay tree.
     * If the key already exists, the tree is splayed on that key, but the set remains unchanged.
     *
     * @param key The integer key to insert.
     */
    public void insert(int key) {
        if (root == null) {
            root = new Node(key);
            return;
        }

        root = splay(root, key);

        // If key is already present, we are done.
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
     * Searches for a key in the splay tree.
     * This operation performs a splay, moving the accessed node (or the last
     * node on the search path) to the root of the tree.
     *
     * @param key The integer key to search for.
     * @return The key if found, otherwise null.
     */
    public Integer search(int key) {
        root = splay(root, key);
        if (root != null && root.key == key) {
            return key;
        }
        return null;
    }

    /**
     * Deletes a key from the splay tree.
     * If the key is not found, the tree is splayed on the last accessed node,
     * but the set remains unchanged.
     *
     * @param key The integer key to delete.
     */
    public void delete(int key) {
        if (root == null) {
            return;
        }

        root = splay(root, key);

        // If the key is not in the tree, do nothing.
        if (root.key != key) {
            return;
        }

        // Now, the node to be deleted is at the root.
        Node leftSubtree = root.left;
        Node rightSubtree = root.right;

        if (leftSubtree == null) {
            root = rightSubtree;
        } else {
            // Find the maximum element in the left subtree.
            Node maxNode = leftSubtree;
            while (maxNode.right != null) {
                maxNode = maxNode.right;
            }
            // Splay the max element to the root of the left subtree.
            leftSubtree = splay(leftSubtree, maxNode.key);
            
            // Join the right subtree with the new root of the left subtree.
            leftSubtree.right = rightSubtree;
            root = leftSubtree;
        }
    }
}