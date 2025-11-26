/**
 * A complete, self-contained implementation of a Splay Tree.
 * Splay Trees are self-balancing binary search trees with the additional
 * property that recently accessed elements are quick to access again.
 * This implementation stores a set of unique integers.
 */
public class SplayTree {

    /**
     * Represents a node in the Splay Tree.
     */
    private static class Node {
        int key;
        Node left, right;

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

    // --- Core Splay Operations ---

    /**
     * Performs a right rotation on the given node.
     *
     * @param x The node to rotate.
     * @return The new root of the rotated subtree.
     */
    private Node rightRotate(Node x) {
        Node y = x.left;
        x.left = y.right;
        y.right = x;
        return y;
    }

    /**
     * Performs a left rotation on the given node.
     *
     * @param x The node to rotate.
     * @return The new root of the rotated subtree.
     */
    private Node leftRotate(Node x) {
        Node y = x.right;
        x.right = y.left;
        y.left = x;
        return y;
    }

    /**
     * The main splay operation. It brings the node with the given key
     * (or the last accessed node if the key is not found) to the root of the tree.
     * This is a bottom-up, recursive implementation.
     *
     * @param root The root of the tree (or subtree) to splay.
     * @param key The key to splay to the root.
     * @return The new root of the splayed tree.
     */
    private Node splay(Node root, int key) {
        // Base cases: root is null or key is present at root
        if (root == null || root.key == key) {
            return root;
        }

        // Key lies in the left subtree
        if (key < root.key) {
            // Key is not in the tree, we are done
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
            // Second rotation for root (Zig case)
            return (root.left == null) ? root : rightRotate(root);
        }
        // Key lies in the right subtree
        else { // key > root.key
            // Key is not in the tree, we are done
            if (root.right == null) {
                return root;
            }

            // Zig-Zag (Right Left)
            if (key < root.right.key) {
                root.right.left = splay(root.right.left, key);
                if (root.right.left != null) {
                    root.right = rightRotate(root.right);
                }
            }
            // Zig-Zig (Right Right)
            else if (key > root.right.key) {
                root.right.right = splay(root.right.right, key);
                root = leftRotate(root);
            }
            // Second rotation for root (Zig case)
            return (root.right == null) ? root : leftRotate(root);
        }
    }

    // --- Public API ---

    /**
     * Inserts a key into the splay tree.
     * If the key already exists, the tree remains unchanged, but the existing node is splayed to the root.
     * If the key does not exist, a new node is created and becomes the root.
     *
     * @param key The integer key to insert.
     */
    public void insert(int key) {
        if (root == null) {
            root = new Node(key);
            return;
        }

        // Splay the key to bring the closest node to the root.
        root = splay(root, key);

        // If the key is already present, do nothing.
        if (root.key == key) {
            return;
        }

        Node newNode = new Node(key);

        // If the new key is smaller than the root's key
        if (key < root.key) {
            newNode.right = root;
            newNode.left = root.left;
            root.left = null;
        }
        // If the new key is greater than the root's key
        else {
            newNode.left = root;
            newNode.right = root.right;
            root.right = null;
        }
        root = newNode;
    }

    /**
     * Searches for a key in the splay tree.
     * This operation performs splaying: the accessed node (if found)
     * or the last accessed node on the search path (if not found) is moved to the root.
     *
     * @param key The key to search for.
     * @return The key if found, otherwise null.
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
     * Deletes a key from the splay tree.
     * If the key is not found, the tree structure may change due to the splay operation
     * but no node will be removed.
     *
     * @param key The key to delete.
     */
    public void delete(int key) {
        if (root == null) {
            return;
        }

        // Splay the key to bring the node to the root, if it exists.
        root = splay(root, key);

        // If the key is not in the tree, do nothing.
        if (root.key != key) {
            return;
        }

        // The node to be deleted is now the root.
        Node leftSubtree = root.left;
        Node rightSubtree = root.right;

        if (leftSubtree == null) {
            // If there's no left child, the right child becomes the new root.
            root = rightSubtree;
        } else {
            // Make the left subtree the new tree.
            root = leftSubtree;
            // Splay the largest element in the left subtree to its root.
            // This is done by splaying for the original (deleted) key, which is guaranteed
            // to be larger than any key in the left subtree.
            root = splay(root, key);
            // Attach the original right subtree as the right child of the new root.
            root.right = rightSubtree;
        }
    }
}