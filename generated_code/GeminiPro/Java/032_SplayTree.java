/**
 * A self-contained Java class implementing a Splay Tree for an integer set.
 * A splay tree is a self-balancing binary search tree with the additional
 * property that recently accessed elements are quick to access again.
 * It performs basic operations such as insertion, deletion, and search.
 * When an element is accessed (e.g., through search, insertion, or deletion),
 * it is moved to the root of the tree through a series of rotations, an
 * operation known as "splaying".
 */
public class SplayTree {

    /**
     * Represents a node in the Splay Tree.
     * This is a private static nested class as it's only used by SplayTree.
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

    /**
     * Performs a right rotation on the subtree rooted at y.
     *
     *      y           x
     *     / \         / \
     *    x   T3  ->  T1  y
     *   / \             / \
     *  T1 T2           T2 T3
     *
     * @param y The root of the subtree to rotate.
     * @return The new root of the rotated subtree (x).
     */
    private Node rotateRight(Node y) {
        Node x = y.left;
        y.left = x.right;
        x.right = y;
        return x;
    }

    /**
     * Performs a left rotation on the subtree rooted at x.
     *
     *    x             y
     *   / \           / \
     *  T1  y   ->    x   T3
     *     / \       / \
     *    T2 T3     T1 T2
     *
     * @param x The root of the subtree to rotate.
     * @return The new root of the rotated subtree (y).
     */
    private Node rotateLeft(Node x) {
        Node y = x.right;
        x.right = y.left;
        y.left = x;
        return y;
    }

    /**
     * Splays the node with the given key to the root of the tree.
     * If the key is not in the tree, the last accessed node on the search path
     * is splayed to the root.
     * This is a recursive, bottom-up splay implementation.
     *
     * @param node The root of the current subtree.
     * @param key The key to splay.
     * @return The new root of the tree after splaying.
     */
    private Node splay(Node node, int key) {
        if (node == null || node.key == key) {
            return node;
        }

        if (key < node.key) {
            // Key is in the left subtree
            if (node.left == null) {
                return node; // Key not found, return last accessed node
            }
            if (key < node.left.key) { // Zig-Zig (Left-Left)
                node.left.left = splay(node.left.left, key);
                node = rotateRight(node);
            } else if (key > node.left.key) { // Zig-Zag (Left-Right)
                node.left.right = splay(node.left.right, key);
                if (node.left.right != null) {
                    node.left = rotateLeft(node.left);
                }
            }
            // Do second rotation for Zig-Zig or Zig-Zag
            return (node.left == null) ? node : rotateRight(node);
        } else { // key > node.key
            // Key is in the right subtree
            if (node.right == null) {
                return node; // Key not found, return last accessed node
            }
            if (key > node.right.key) { // Zig-Zig (Right-Right)
                node.right.right = splay(node.right.right, key);
                node = rotateLeft(node);
            } else if (key < node.right.key) { // Zig-Zag (Right-Left)
                node.right.left = splay(node.right.left, key);
                if (node.right.left != null) {
                    node.right = rotateRight(node.right);
                }
            }
            // Do second rotation for Zig-Zig or Zig-Zag
            return (node.right == null) ? node : rotateLeft(node);
        }
    }

    /**
     * Searches for a key in the tree.
     * As a side effect, the accessed node (or the last node on the path if
     * the key is not found) is splayed to the root.
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
     * Inserts a key into the Splay Tree.
     * If the key already exists, the tree is splayed at that key, but no new node is added.
     *
     * @param key The key to insert.
     */
    public void insert(int key) {
        // If the tree is empty, create a new root.
        if (root == null) {
            root = new Node(key);
            return;
        }

        // Splay the tree around the key.
        root = splay(root, key);

        // If the key is already present, do nothing.
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
     * Deletes a key from the Splay Tree.
     *
     * @param key The key to delete.
     */
    public void delete(int key) {
        if (root == null) {
            return;
        }

        // Splay the tree around the key.
        root = splay(root, key);

        // If the key is not in the tree, do nothing.
        if (root.key != key) {
            return;
        }

        // Now the node to be deleted is the root.
        Node leftSubtree = root.left;
        Node rightSubtree = root.right;

        if (leftSubtree == null) {
            // If there's no left child, the right subtree becomes the new tree.
            root = rightSubtree;
        } else {
            // Splay the left subtree to bring its maximum element to its root.
            leftSubtree = splay(leftSubtree, key); // or Integer.MAX_VALUE
            
            // The new root of the left subtree has no right child.
            // Attach the original right subtree there.
            leftSubtree.right = rightSubtree;
            root = leftSubtree;
        }
    }
}