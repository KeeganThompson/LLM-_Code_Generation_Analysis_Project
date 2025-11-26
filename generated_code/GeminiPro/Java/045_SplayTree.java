/**
 * A self-contained Java class implementing a Splay Tree for an integer set.
 * A splay tree is a self-balancing binary search tree with the additional
 * property that recently accessed elements are quick to access again.
 * It performs basic operations such as insertion, deletion, and search
- * in O(log n) amortized time.
 */
public class SplayTree {

    /**
     * Represents a node in the Splay Tree.
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
     * Performs a right rotation on the subtree rooted at x.
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
     * The main splay operation. Brings the node with the given key to the root.
     * If the key is not present, it brings the last accessed node to the root.
     * This is a recursive, bottom-up splay implementation.
     *
     * @param root The root of the current subtree.
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

            // Zig-Zig (Left-Left)
            if (key < root.left.key) {
                // Recursively bring the key as root of left-left
                root.left.left = splay(root.left.left, key);
                // First rotation for root
                root = rightRotate(root);
            }
            // Zig-Zag (Left-Right)
            else if (key > root.left.key) {
                // Recursively bring the key as root of left-right
                root.left.right = splay(root.left.right, key);
                // First rotation for root.left
                if (root.left.right != null) {
                    root.left = leftRotate(root.left);
                }
            }

            // Second rotation for root
            return (root.left == null) ? root : rightRotate(root);
        }
        // Key lies in the right subtree
        else {
            // Key is not in the tree, we are done
            if (root.right == null) {
                return root;
            }

            // Zig-Zag (Right-Left)
            if (key < root.right.key) {
                // Recursively bring the key as root of right-left
                root.right.left = splay(root.right.left, key);
                // First rotation for root.right
                if (root.right.left != null) {
                    root.right = rightRotate(root.right);
                }
            }
            // Zig-Zig (Right-Right)
            else if (key > root.right.key) {
                // Recursively bring the key as root of right-right
                root.right.right = splay(root.right.right, key);
                // First rotation for root
                root = leftRotate(root);
            }

            // Second rotation for root
            return (root.right == null) ? root : leftRotate(root);
        }
    }

    /**
     * Searches for a key in the tree.
     * This operation performs a splay on the accessed key, moving it to the root.
     * If the key is not found, the last accessed node in the search path is splayed.
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
     * If the key is already present, the corresponding node is splayed to the root.
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

        // If the key is already present, do nothing
        if (root.key == key) {
            return;
        }

        // Create the new node
        Node newNode = new Node(key);

        // If the new key is smaller than the root's key,
        // make the new node the new root, and the old root its right child.
        if (key < root.key) {
            newNode.right = root;
            newNode.left = root.left;
            root.left = null;
        }
        // If the new key is greater than the root's key,
        // make the new node the new root, and the old root its left child.
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
        // If the tree is empty, there's nothing to delete
        if (root == null) {
            return;
        }

        // Splay the tree to bring the node to delete (or its parent) to the root
        root = splay(root, key);

        // If the key is not in the tree, do nothing
        if (root.key != key) {
            return;
        }

        // Now, the node to be deleted is the root.
        // We need to join the left and right subtrees.
        Node leftSubtree = root.left;
        Node rightSubtree = root.right;

        if (leftSubtree == null) {
            // If the left subtree is null, the new root is just the right subtree
            root = rightSubtree;
        } else {
            // Splay the left subtree for the key we just deleted. This will bring
            // the largest element in the left subtree (the predecessor of the key)
            // to the root of the left subtree.
            leftSubtree = splay(leftSubtree, key);
            
            // The new root of the left subtree is guaranteed to have no right child.
            // We can now attach the original right subtree as its right child.
            leftSubtree.right = rightSubtree;
            root = leftSubtree;
        }
    }
}