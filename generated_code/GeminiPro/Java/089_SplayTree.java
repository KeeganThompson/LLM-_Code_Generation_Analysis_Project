/**
 * A self-contained Java class implementing a Splay Tree for an integer set.
 * Splay trees are self-balancing binary search trees with the additional property
 * that recently accessed elements are quick to access again.
 */
public class SplayTree {

    /**
     * Represents a node in the Splay Tree.
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
     * The main splay operation. It brings the node with the given key (or the last
     * accessed node on the search path) to the root of the tree.
     * This is a recursive, bottom-up implementation.
     *
     * @param node The root of the current subtree.
     * @param key The key to splay.
     * @return The new root of the tree after splaying.
     */
    private Node splay(Node node, int key) {
        // Base cases: node is null or key is present at root
        if (node == null || node.key == key) {
            return node;
        }

        // Key lies in the left subtree
        if (key < node.key) {
            // Key is not in the tree, we are done
            if (node.left == null) {
                return node;
            }

            // Zig-Zig (Left Left)
            if (key < node.left.key) {
                node.left.left = splay(node.left.left, key);
                node = rightRotate(node);
            }
            // Zig-Zag (Left Right)
            else if (key > node.left.key) {
                node.left.right = splay(node.left.right, key);
                if (node.left.right != null) {
                    node.left = leftRotate(node.left);
                }
            }
            
            // Do second rotation for root or the only rotation for Zig
            return (node.left == null) ? node : rightRotate(node);
        }
        // Key lies in the right subtree
        else {
            // Key is not in the tree, we are done
            if (node.right == null) {
                return node;
            }

            // Zig-Zag (Right Left)
            if (key < node.right.key) {
                node.right.left = splay(node.right.left, key);
                if (node.right.left != null) {
                    node.right = rightRotate(node.right);
                }
            }
            // Zig-Zig (Right Right)
            else if (key > node.right.key) {
                node.right.right = splay(node.right.right, key);
                node = leftRotate(node);
            }

            // Do second rotation for root or the only rotation for Zig
            return (node.right == null) ? node : leftRotate(node);
        }
    }

    /**
     * Inserts a key into the Splay Tree. If the key already exists, the tree
     * is splayed on that key but no new node is inserted.
     *
     * @param key The integer key to insert.
     */
    public void insert(int key) {
        // Case 1: Tree is empty
        if (root == null) {
            root = new Node(key);
            return;
        }

        // Splay the tree to bring the closest node to the key to the root
        root = splay(root, key);

        // If key is already present, do nothing
        if (root.key == key) {
            return;
        }

        Node newNode = new Node(key);

        // Case 2: New key is smaller than root's key
        if (key < root.key) {
            newNode.right = root;
            newNode.left = root.left;
            root.left = null;
        }
        // Case 3: New key is larger than root's key
        else {
            newNode.left = root;
            newNode.right = root.right;
            root.right = null;
        }
        root = newNode; // New node becomes the root
    }

    /**
     * Searches for a key in the Splay Tree.
     * This operation performs a splay on the accessed key, moving it to the root.
     *
     * @param key The integer key to search for.
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
     * Deletes a key from the Splay Tree. If the key is not found,
     * the tree is splayed on the last accessed node and no changes are made.
     *
     * @param key The integer key to delete.
     */
    public void delete(int key) {
        if (root == null) {
            return;
        }

        // Splay the tree to bring the node to delete (or its closest value) to the root
        root = splay(root, key);

        // If key is not in the tree, do nothing
        if (root.key != key) {
            return;
        }

        // Now, root is the node to be deleted.
        // We need to merge its left and right subtrees.
        Node leftSubtree = root.left;
        Node rightSubtree = root.right;

        if (leftSubtree == null) {
            // If no left child, the right child becomes the new root
            root = rightSubtree;
        } else {
            // Splay the left subtree to bring its maximum element to its root.
            // The max element in the left subtree is the inorder predecessor of the deleted key.
            // Splaying for 'key' in the left subtree will bring the max element to the top
            // because 'key' is larger than any element there.
            leftSubtree = splay(leftSubtree, key);
            
            // The new root of the left subtree now has no right child (since it's the max).
            // Attach the original right subtree to it.
            leftSubtree.right = rightSubtree;
            root = leftSubtree;
        }
    }
}