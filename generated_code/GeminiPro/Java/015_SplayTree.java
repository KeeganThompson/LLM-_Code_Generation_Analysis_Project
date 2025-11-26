/**
 * A self-contained Java class implementing a Splay Tree for an integer set.
 * Splay trees are self-balancing binary search trees with the additional property
 * that recently accessed elements are quick to access again.
 */
public class SplayTree {

    /**
     * Inner class representing a node in the Splay Tree.
     */
    private static class Node {
        int key;
        Node left, right;

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
     * Performs a right rotation on the given node.
     * This is a helper method for the splay operation.
     *
     *      y           x
     *     / \         / \
     *    x   T3  ->  T1  y
     *   / \             / \
     *  T1  T2          T2  T3
     *
     * @param y The node to rotate.
     * @return The new root of the rotated subtree.
     */
    private Node rightRotate(Node y) {
        Node x = y.left;
        y.left = x.right;
        x.right = y;
        return x;
    }

    /**
     * Performs a left rotation on the given node.
     * This is a helper method for the splay operation.
     *
     *    x             y
     *   / \           / \
     *  T1  y    ->   x   T3
     *     / \       / \
     *    T2  T3    T1  T2
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
     * The core splay operation. It moves the node with the given key to the root.
     * If the key is not in the tree, the last accessed node on the search path
     * is moved to the root.
     * This is a recursive, bottom-up splaying implementation.
     *
     * @param node The root of the current subtree.
     * @param key The key to splay.
     * @return The new root of the splayed tree.
     */
    private Node splay(Node node, int key) {
        // Base case: node is null or key is present at root
        if (node == null || node.key == key) {
            return node;
        }

        // Key lies in the left subtree
        if (key < node.key) {
            // Key is not in tree, we are done
            if (node.left == null) {
                return node;
            }

            // Zig-Zig (Left-Left)
            if (key < node.left.key) {
                // Recursively bring the key as root of left-left
                node.left.left = splay(node.left.left, key);
                // First rotation for grandparent-parent
                node = rightRotate(node);
            }
            // Zig-Zag (Left-Right)
            else if (key > node.left.key) {
                // Recursively bring the key as root of left-right
                node.left.right = splay(node.left.right, key);
                // First rotation for parent-child
                if (node.left.right != null) {
                    node.left = leftRotate(node.left);
                }
            }

            // Second rotation for parent-child (or Zig)
            return (node.left == null) ? node : rightRotate(node);

        } else { // Key lies in the right subtree
            // Key is not in tree, we are done
            if (node.right == null) {
                return node;
            }

            // Zig-Zag (Right-Left)
            if (key < node.right.key) {
                // Recursively bring the key as root of right-left
                node.right.left = splay(node.right.left, key);
                // First rotation for parent-child
                if (node.right.left != null) {
                    node.right = rightRotate(node.right);
                }
            }
            // Zig-Zig (Right-Right)
            else if (key > node.right.key) {
                // Recursively bring the key as root of right-right
                node.right.right = splay(node.right.right, key);
                // First rotation for grandparent-parent
                node = leftRotate(node);
            }

            // Second rotation for parent-child (or Zig)
            return (node.right == null) ? node : leftRotate(node);
        }
    }

    /**
     * Searches for a key in the tree. If found, the node is splayed to the root.
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
        } else {
            return null;
        }
    }

    /**
     * Inserts a key into the Splay Tree. If the key already exists, the tree
     * is splayed on that key, but no new node is added.
     *
     * @param key The key to insert.
     */
    public void insert(int key) {
        // Case 1: The tree is empty
        if (root == null) {
            root = new Node(key);
            return;
        }

        // Splay the tree for the key. The root becomes the node closest to the key.
        root = splay(root, key);

        // If the key is already present, do nothing (it's a set).
        if (root.key == key) {
            return;
        }

        Node newNode = new Node(key);

        // The new node becomes the new root. The old root is attached as a child.
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
     * Deletes a key from the Splay Tree.
     *
     * @param key The key to delete.
     */
    public void delete(int key) {
        if (root == null) {
            return;
        }

        // Splay the tree for the key. If the key exists, it becomes the root.
        root = splay(root, key);

        // If the key is not in the tree, do nothing.
        if (root.key != key) {
            return;
        }

        // Now, the node to be deleted is the root.
        Node leftSubtree = root.left;
        Node rightSubtree = root.right;

        if (leftSubtree == null) {
            // If there's no left child, the right subtree becomes the new tree.
            root = rightSubtree;
        } else {
            // Splay the left subtree to bring its maximum element (the predecessor
            // of the deleted key) to its root.
            leftSubtree = splay(leftSubtree, key);

            // The new root of the left subtree has no right child.
            // Attach the original right subtree there.
            leftSubtree.right = rightSubtree;
            root = leftSubtree;
        }
    }
}