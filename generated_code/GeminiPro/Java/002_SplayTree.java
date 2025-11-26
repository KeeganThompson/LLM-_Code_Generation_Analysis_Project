/**
 * A complete, self-contained implementation of an integer set using a Splay Tree.
 * <p>
 * A splay tree is a self-adjusting binary search tree with the additional
 * property that recently accessed elements are quick to access again.
 * It performs basic operations such as insertion, look-up and removal in
 * O(log n) amortized time.
 */
public class SplayTree {

    /**
     * Inner class representing a node in the Splay Tree.
     */
    private class Node {
        int key;
        Node left, right;

        public Node(int key) {
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
     * Performs a right rotation on the subtree rooted at x.
     * @param x The root of the subtree to rotate.
     * @return The new root of the subtree.
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
     * @return The new root of the subtree.
     */
    private Node leftRotate(Node x) {
        Node y = x.right;
        x.right = y.left;
        y.left = x;
        return y;
    }

    /**
     * The splay operation. Moves the node with the given key (or the last accessed
     * node on the search path) to the root of the tree.
     *
     * @param root The root of the tree (or subtree) to splay.
     * @param key  The key to search for and splay.
     * @return The new root of the tree after splaying.
     */
    private Node splay(Node root, int key) {
        // Base cases: root is null or key is present at root
        if (root == null || root.key == key) {
            return root;
        }

        // Key lies in the left subtree
        if (key < root.key) {
            // Key is not in tree, we are done
            if (root.left == null) {
                return root;
            }

            // Zig-Zig (Left-Left)
            if (key < root.left.key) {
                // Recursively bring the key as root of left-left
                root.left.left = splay(root.left.left, key);
                // Do first rotation for root
                root = rightRotate(root);
            }
            // Zig-Zag (Left-Right)
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

        } else { // Key lies in the right subtree
            // Key is not in tree, we are done
            if (root.right == null) {
                return root;
            }

            // Zig-Zag (Right-Left)
            if (key < root.right.key) {
                // Recursively bring the key as root of right-left
                root.right.left = splay(root.right.left, key);
                // Do first rotation for root.right
                if (root.right.left != null) {
                    root.right = rightRotate(root.right);
                }
            }
            // Zig-Zig (Right-Right)
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

    // --- Public API ---

    /**
     * Searches for a key in the tree.
     * This operation performs splaying on the accessed node (or the last accessed
     * node in the search path), moving it to the root.
     *
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
     * Inserts a key into the splay tree.
     * If the key already exists, the tree is splayed on that key but not modified,
     * maintaining the set property.
     *
     * @param key The integer key to insert.
     */
    public void insert(int key) {
        // If the tree is empty, create a new root
        if (root == null) {
            root = new Node(key);
            return;
        }

        // Splay the tree around the key. This brings the closest node to the root.
        root = splay(root, key);

        // If key is already present, do nothing
        if (root.key == key) {
            return;
        }

        Node newNode = new Node(key);

        // If the new key is smaller than the root's key, make the new node
        // the new root. The old root becomes the right child of the new node,
        // and the old root's left subtree becomes the new node's left subtree.
        if (key < root.key) {
            newNode.right = root;
            newNode.left = root.left;
            root.left = null;
            root = newNode;
        }
        // If the new key is greater than the root's key, do the symmetric operation.
        else {
            newNode.left = root;
            newNode.right = root.right;
            root.right = null;
            root = newNode;
        }
    }

    /**
     * Deletes a key from the splay tree.
     *
     * @param key The integer key to delete.
     */
    public void delete(int key) {
        // If tree is empty, do nothing
        if (root == null) {
            return;
        }

        // Splay the tree to bring the node to delete (or the last accessed node) to the root
        root = splay(root, key);

        // If key is not present in the tree, do nothing
        if (root.key != key) {
            return;
        }

        // Now, the node to be deleted is the root.
        Node leftSubtree = root.left;
        Node rightSubtree = root.right;

        if (leftSubtree == null) {
            // If there's no left child, the right child becomes the new root.
            root = rightSubtree;
        } else {
            // If there is a left child, we need to join the two subtrees.
            // Splay the left subtree to bring its maximum element to its root.
            // Since `key` is guaranteed to be greater than any element in the
            // left subtree, splaying for `key` will bring the max element to the top.
            leftSubtree = splay(leftSubtree, key);

            // The new root of the left subtree (the max element) will now have
            // a null right child. We attach the original right subtree there.
            leftSubtree.right = rightSubtree;
            root = leftSubtree;
        }
    }
}