/**
 * A complete, self-contained implementation of a Splay Tree in Java.
 * This class implements a set of integers with standard operations like
 * insert, delete, and search. The key feature of a splay tree is that
 * recently accessed elements are moved to the root of the tree to optimize
 * for locality of reference.
 */
public class SplayTree {

    /**
     * Inner class representing a node in the Splay Tree.
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

    // --- Public API Methods ---

    /**
     * Searches for a key in the tree.
     * If the key is found, it is splayed to the root.
     * If not found, the last accessed node on the search path is splayed to the root.
     *
     * @param key The key to search for.
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
     * Inserts a key into the tree.
     * If the key already exists, the existing node is splayed to the root.
     * If the key is new, it is inserted and becomes the new root of the tree.
     *
     * @param key The key to insert.
     */
    public void insert(int key) {
        // If the tree is empty, create a new root
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

        Node newNode = new Node(key);

        // The old root is split based on the new key
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
     * Deletes a key from the tree.
     * If the key is found, it is first splayed to the root and then removed.
     * The remaining subtrees are then joined.
     *
     * @param key The key to delete.
     */
    public void delete(int key) {
        if (root == null) {
            return;
        }

        // Splay the key to the root
        root = splay(root, key);

        // If the key is not in the tree, do nothing
        if (root.key != key) {
            return;
        }

        // Now, the node to delete is the root.
        // We need to join its left and right subtrees.
        Node leftSubtree = root.left;
        Node rightSubtree = root.right;

        if (leftSubtree == null) {
            root = rightSubtree;
        } else {
            // Splay the maximum element in the left subtree to its root.
            // This new root will have no right child.
            leftSubtree = splay(leftSubtree, findMax(leftSubtree).key);
            
            // Attach the original right subtree as the right child of the new root.
            leftSubtree.right = rightSubtree;
            root = leftSubtree;
        }
    }

    // --- Private Helper Methods ---

    /**
     * Finds the node with the maximum key in a given subtree.
     */
    private Node findMax(Node node) {
        if (node == null) {
            return null;
        }
        while (node.right != null) {
            node = node.right;
        }
        return node;
    }

    /**
     * Performs a right rotation on the subtree rooted at x.
     */
    private Node rightRotate(Node x) {
        Node y = x.left;
        x.left = y.right;
        y.right = x;
        return y;
    }

    /**
     * Performs a left rotation on the subtree rooted at x.
     */
    private Node leftRotate(Node x) {
        Node y = x.right;
        x.right = y.left;
        y.left = x;
        return y;
    }

    /**
     * The splay operation. It moves the node with the given key (or the last
     * accessed node if the key is not found) to the root of the tree using
     * a series of rotations. This is a bottom-up, recursive implementation.
     *
     * @param root The root of the current subtree.
     * @param key  The key to splay.
     * @return The new root of the splayed subtree.
     */
    private Node splay(Node root, int key) {
        // Base case: root is null or key is at root
        if (root == null || root.key == key) {
            return root;
        }

        // Key lies in the left subtree
        if (key < root.key) {
            // Key is not in the tree, we are done with this subtree
            if (root.left == null) {
                return root;
            }

            // Zig-Zig (Left Left)
            if (key < root.left.key) {
                root.left.left = splay(root.left.left, key);
                root = rightRotate(root);
            }
            // Zig-Zag (Left Right)
            else if (key > root.left.key) {
                root.left.right = splay(root.left.right, key);
                if (root.left.right != null) {
                    root.left = leftRotate(root.left);
                }
            }

            // Perform the second rotation for root (if necessary)
            return (root.left == null) ? root : rightRotate(root);

        } else { // key > root.key
            // Key lies in the right subtree
            // Key is not in the tree, we are done with this subtree
            if (root.right == null) {
                return root;
            }

            // Zag-Zag (Right Right)
            if (key > root.right.key) {
                root.right.right = splay(root.right.right, key);
                root = leftRotate(root);
            }
            // Zag-Zig (Right Left)
            else if (key < root.right.key) {
                root.right.left = splay(root.right.left, key);
                if (root.right.left != null) {
                    root.right = rightRotate(root.right);
                }
            }

            // Perform the second rotation for root (if necessary)
            return (root.right == null) ? root : leftRotate(root);
        }
    }
}