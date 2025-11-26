/**
 * A complete, self-contained implementation of an integer set using a Splay Tree.
 * Splay trees are self-balancing binary search trees with the additional property
 * that recently accessed elements are quick to access again. An access to a node
 * (e.g., via search, insertion, or deletion) triggers a "splaying" operation,
 * which moves that node to the root of the tree through a series of rotations.
 */
public class SplayTree {

    /**
     * Represents a node in the Splay Tree.
     * It is a static inner class as it does not need to access instance members of SplayTree.
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
     * Constructs an empty SplayTree.
     */
    public SplayTree() {
        this.root = null;
    }

    // --- Private Helper Methods for Rotations and Splaying ---

    /**
     * Performs a right rotation on the subtree rooted at y.
     * @param y The root of the subtree to rotate.
     * @return The new root of the rotated subtree.
     */
    private Node rightRotate(Node y) {
        Node x = y.left;
        y.left = x.right;
        x.right = y;
        return x;
    }

    /**
     * Performs a left rotation on the subtree rooted at x.
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
     * The main splay operation. It brings the node with the given key
     * (or the last accessed node on the search path) to the root of the tree.
     * This is a recursive top-down splaying implementation.
     * @param root The root of the tree (or subtree) to perform the splay on.
     * @param key The key to search for and splay.
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

            // Do second rotation for root
            return (root.right == null) ? root : leftRotate(root);
        }
    }


    // --- Public API Methods ---

    /**
     * Searches for a key in the tree. If the key is found, the node containing
     * the key is splayed to the root. If not found, the last accessed node on
     * the search path is splayed to the root.
     *
     * @param key The key to search for.
     * @return The key if found, otherwise null.
     */
    public Integer search(int key) {
        this.root = splay(this.root, key);
        if (this.root != null && this.root.key == key) {
            return this.root.key;
        }
        return null;
    }

    /**
     * Inserts a key into the splay tree. If the key already exists, the tree
     * is splayed on that key but not modified. If the key is new, it is inserted
     * and becomes the new root of the tree.
     *
     * @param key The key to insert.
     */
    public void insert(int key) {
        // If the tree is empty, create a new root
        if (this.root == null) {
            this.root = new Node(key);
            return;
        }

        // Splay the tree to bring the closest node to the root
        this.root = splay(this.root, key);

        // If the key is already present, do nothing (as this is a set)
        if (this.root.key == key) {
            return;
        }

        Node newNode = new Node(key);

        // If the new key is smaller than the root's key, make it the new root.
        // The old root becomes the right child of the new root.
        // The new root's left child becomes the old root's left child.
        if (key < this.root.key) {
            newNode.right = this.root;
            newNode.left = this.root.left;
            this.root.left = null;
        }
        // If the new key is greater than the root's key, make it the new root.
        // The old root becomes the left child of the new root.
        // The new root's right child becomes the old root's right child.
        else {
            newNode.left = this.root;
            newNode.right = this.root.right;
            this.root.right = null;
        }
        this.root = newNode;
    }

    /**
     * Deletes a key from the splay tree. If the key is found, it is splayed to the
     * root and then deleted. The tree is then restructured by joining the remaining
     * left and right subtrees.
     *
     * @param key The key to delete.
     */
    public void delete(int key) {
        // If the tree is empty, do nothing
        if (this.root == null) {
            return;
        }

        // Splay the key to the root
        this.root = splay(this.root, key);

        // If the key is not at the root after splaying, it's not in the tree
        if (this.root.key != key) {
            return;
        }

        // Now, the node to be deleted is the root.
        // We need to join its two subtrees.
        Node leftSubtree = this.root.left;
        Node rightSubtree = this.root.right;

        if (leftSubtree == null) {
            // If there's no left subtree, the right subtree becomes the new tree
            this.root = rightSubtree;
        } else {
            // Splay the largest element in the left subtree to its root.
            // A splay for 'key' (or any value larger than all keys in the left
            // subtree) will bring the max element to the top.
            leftSubtree = splay(leftSubtree, key);

            // The new root of the left subtree (which is the max element)
            // will have a null right child. We attach the original right subtree there.
            leftSubtree.right = rightSubtree;
            this.root = leftSubtree;
        }
    }
}