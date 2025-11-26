/**
 * A complete, self-contained implementation of an integer set using a Splay Tree.
 * Splay trees are self-balancing binary search trees with the additional
 * property that recently accessed elements are quick to access again. This
 * implementation supports insert, delete, and search operations.
 */
public class SplayTree {

    /**
     * Inner class representing a node in the Splay Tree.
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
     * Searches for a key in the tree. If the key is found, it is splayed
     * to the root. If not found, the last accessed node is splayed to the root.
     *
     * @param key The key to search for.
     * @return The key if it is found, otherwise null.
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
     * Inserts a key into the splay tree. If the key already exists, the node
     * containing the key is splayed to the root.
     *
     * @param key The key to insert.
     */
    public void insert(int key) {
        // If the tree is empty, create a new root.
        if (root == null) {
            root = new Node(key);
            return;
        }

        // Splay the tree to bring the closest node to the root.
        root = splay(root, key);

        // If the key is already present, the splay operation has already
        // moved it to the root, so we are done.
        if (root.key == key) {
            return;
        }

        Node newNode = new Node(key);
        if (key < root.key) {
            newNode.right = root;
            newNode.left = root.left;
            root.left = null;
        } else {
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

        // Splay the key to the root.
        root = splay(root, key);

        // If the key is not at the root, it's not in the tree.
        if (root.key != key) {
            return;
        }

        // The node to delete is now the root.
        Node leftSubtree = root.left;
        Node rightSubtree = root.right;

        if (leftSubtree == null) {
            // If there's no left child, the right subtree becomes the new tree.
            root = rightSubtree;
        } else {
            // Splay the left subtree for the key 'key'. Since 'key' is larger
            // than any element in the left subtree, this will bring the maximum
            // element of the left subtree to its root.
            Node newRoot = splay(leftSubtree, key);
            
            // The new root's right child will be null after the splay.
            // Attach the original right subtree there.
            newRoot.right = rightSubtree;
            root = newRoot;
        }
    }

    /**
     * Performs a right rotation on the subtree rooted at node x.
     *
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
     *
     * @param x The root of the subtree to rotate.
     * @return The new root of the rotated subtree.
     */
    private Node leftRotate(Node x) {
        Node y = x.right;
        x.right = y.left;
        y.left = x;
        return y;
    }

    /**
     * The core splaying operation (top-down).
     * This method searches for the given key and brings the accessed node
     * (or the last node on the search path) to the root of the tree.
     *
     * @param node The root of the tree to splay.
     * @param key The key to splay around.
     * @return The new root of the splayed tree.
     */
    private Node splay(Node node, int key) {
        if (node == null) {
            return null;
        }

        // A dummy node to simplify linking.
        Node header = new Node(0);
        Node leftTreeMax = header;
        Node rightTreeMin = header;

        Node current = node;

        while (true) {
            if (key < current.key) {
                if (current.left == null) break;
                // Zig-Zig (Right Rotation)
                if (key < current.left.key) {
                    current = rightRotate(current);
                    if (current.left == null) break;
                }
                // Link to the right tree
                rightTreeMin.left = current;
                rightTreeMin = current;
                current = current.left;
            } else if (key > current.key) {
                if (current.right == null) break;
                // Zig-Zig (Left Rotation)
                if (key > current.right.key) {
                    current = leftRotate(current);
                    if (current.right == null) break;
                }
                // Link to the left tree
                leftTreeMax.right = current;
                leftTreeMax = current;
                current = current.right;
            } else { // Found the key
                break;
            }
        }

        // Reassemble the trees
        leftTreeMax.right = current.left;
        rightTreeMin.left = current.right;
        current.left = header.right;
        current.right = header.left;

        return current;
    }
}