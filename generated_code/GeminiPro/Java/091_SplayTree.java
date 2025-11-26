/**
 * A complete, self-contained implementation of a Splay Tree.
 * This class implements an integer set, supporting insert, delete, and search operations.
 * The splay operation is performed on every access (search, insert, delete)
 * to move the accessed or relevant node to the root, optimizing for future accesses.
 */
public class SplayTree {

    /**
     * Inner class representing a node in the Splay Tree.
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
     * The core splay operation. Brings the node with the given key (or the last
     * accessed node if the key is not found) to the root of the tree.
     *
     * @param root The root of the tree/subtree to splay.
     * @param key  The key to splay for.
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
                // First rotation for root
                root = rightRotate(root);
            }
            // Zig-Zag (Left Right)
            else if (key > root.left.key) {
                // Recursively bring the key as root of left-right
                root.left.right = splay(root.left.right, key);
                // First rotation for root.left
                if (root.left.right != null) {
                    root.left = leftRotate(root.left);
                }
            }
            // Do second rotation for root
            return (root.left == null) ? root : rightRotate(root);
        }
        // Key lies in the right subtree
        else {
            // Key is not in the tree, we are done
            if (root.right == null) {
                return root;
            }

            // Zig-Zag (Right Left)
            if (key < root.right.key) {
                // Recursively bring the key as root of right-left
                root.right.left = splay(root.right.left, key);
                // First rotation for root.right
                if (root.right.left != null) {
                    root.right = rightRotate(root.right);
                }
            }
            // Zig-Zig (Right Right)
            else if (key > root.right.key) {
                // Recursively bring the key as root of right-right
                root.right.right = splay(root.right.right, key);
                // First rotation for root
                root = leftRotate(root);
            }
            // Do second rotation for root
            return (root.right == null) ? root : leftRotate(root);
        }
    }

    /**
     * Searches for a key in the tree.
     * If the key is found, it is splayed to the root.
     * If not found, the last accessed node is splayed to the root.
     *
     * @param key The key to search for.
     * @return The key if found, otherwise null.
     */
    public Integer search(int key) {
        root = splay(root, key);
        if (root != null && root.key == key) {
            return root.key;
        }
        return null;
    }

    /**
     * Inserts a key into the splay tree.
     * If the key already exists, the tree is splayed on that key but not modified.
     *
     * @param key The key to insert.
     */
    public void insert(int key) {
        // If the tree is empty, create a new root
        if (root == null) {
            root = new Node(key);
            return;
        }

        // Splay the tree to bring the closest node to the root
        root = splay(root, key);

        // If key is already present, do nothing (it's now the root)
        if (root.key == key) {
            return;
        }

        Node newNode = new Node(key);

        // If the new key is smaller than the root's key,
        // the new node becomes the new root. The old root becomes its right child,
        // and the old root's left subtree becomes the new root's left child.
        if (key < root.key) {
            newNode.right = root;
            newNode.left = root.left;
            root.left = null;
        }
        // If the new key is greater than the root's key,
        // the new node becomes the new root. The old root becomes its left child,
        // and the old root's right subtree becomes the new root's right child.
        else {
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

        // If the key is not in the tree, do nothing.
        if (root.key != key) {
            return;
        }

        // Now the node to be deleted is the root.
        Node leftSubtree = root.left;
        Node rightSubtree = root.right;

        if (leftSubtree == null) {
            // If there's no left subtree, the right subtree becomes the new tree.
            root = rightSubtree;
        } else {
            // Splay the left subtree to bring its maximum element to its root.
            // Splaying for the deleted key (which is guaranteed to be larger than any
            // key in the left subtree) will achieve this.
            leftSubtree = splay(leftSubtree, key);

            // Attach the original right subtree as the right child of the new root.
            leftSubtree.right = rightSubtree;
            root = leftSubtree;
        }
    }
}