/**
 * A complete, self-contained implementation of a Splay Tree.
 * The Splay Tree is a self-balancing binary search tree with the additional
 * property that recently accessed elements are quick to access again.
 * This implementation stores integer keys and functions as a set (no duplicates).
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

    // --- Private Helper Methods ---

    /**
     * Performs a right rotation on the subtree rooted at x.
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
     * Performs a left rotation on the subtree rooted at x.
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
     * The main splay operation. Brings the node with the given key
     * (or the last accessed node if the key is not found) to the root.
     * This is a recursive, bottom-up splay implementation.
     * @param root The root of the tree/subtree to splay.
     * @param key The key to splay towards the root.
     * @return The new root of the splayed tree.
     */
    private Node splay(Node root, int key) {
        // Base case: root is null or key is present at root
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
                // Recursively bring the key as root of left-left
                root.left.left = splay(root.left.left, key);
                // Do first rotation for root
                root = rightRotate(root);
            }
            // Zig-Zag (Left Right)
            else if (key > root.left.key) {
                // Recursively bring the key as root of left-right
                root.left.right = splay(root.left.right, key);
                // Do first rotation for root.left
                if (root.left.right != null) {
                    root.left = leftRotate(root.left);
                }
            }

            // Do second rotation for root (or the single rotation in Zig case)
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
                // Recursively bring the key as root of right-left
                root.right.left = splay(root.right.left, key);
                // Do first rotation for root.right
                if (root.right.left != null) {
                    root.right = rightRotate(root.right);
                }
            }
            // Zig-Zig (Right Right)
            else if (key > root.right.key) {
                // Recursively bring the key as root of right-right
                root.right.right = splay(root.right.right, key);
                // Do first rotation for root
                root = leftRotate(root);
            }

            // Do second rotation for root (or the single rotation in Zig case)
            return (root.right == null) ? root : leftRotate(root);
        }
    }

    // --- Public API ---

    /**
     * Inserts a key into the Splay Tree. If the key already exists,
     * the tree remains unchanged. After insertion, the new node becomes the root.
     * @param key The integer key to insert.
     */
    public void insert(int key) {
        // If the tree is empty, create a new root
        if (root == null) {
            root = new Node(key);
            return;
        }

        // Splay the tree for the key. This brings the closest node to the root.
        root = splay(root, key);

        // If the key is already present, do nothing.
        if (root.key == key) {
            return;
        }

        Node newNode = new Node(key);

        // The new node becomes the new root. The old root and one of its subtrees
        // become the children of the new node. This is a "split" operation.
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
     * Searches for a key in the Splay Tree.
     * This operation splays the found node (or the last accessed node) to the root.
     * @param key The integer key to search for.
     * @return The key as an Integer if found, otherwise null.
     */
    public Integer search(int key) {
        root = splay(root, key);
        if (root != null && root.key == key) {
            return root.key;
        }
        return null;
    }

    /**
     * Deletes a key from the Splay Tree. If the key is not found,
     * the tree is splayed based on the last accessed node and remains otherwise unchanged.
     * @param key The integer key to delete.
     */
    public void delete(int key) {
        // If the tree is empty
        if (root == null) {
            return;
        }

        // Splay the tree for the key. If the key exists, it becomes the root.
        root = splay(root, key);

        // If the key is not in the tree, do nothing.
        if (root.key != key) {
            return;
        }

        // Key is at the root, now we need to join its two subtrees.
        Node leftSubtree = root.left;
        Node rightSubtree = root.right;

        if (leftSubtree == null) {
            root = rightSubtree;
        } else {
            // Splay the left subtree to bring its maximum element to the top.
            // Since `key` is greater than any element in the left subtree, splaying
            // for `key` will bring the max element to the root of the left subtree.
            Node newRoot = splay(leftSubtree, key);
            
            // The new root (max of left subtree) will have no right child.
            // Attach the original right subtree as the right child of the new root.
            newRoot.right = rightSubtree;
            root = newRoot;
        }
    }
}