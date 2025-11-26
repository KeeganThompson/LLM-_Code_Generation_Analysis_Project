/**
 * A complete, self-contained implementation of an integer set using a Splay Tree.
 *
 * A splay tree is a self-balancing binary search tree with the additional
 * property that recently accessed elements are quick to access again. It performs
 * basic operations such as insertion, deletion, and search. After a search,
 * insertion, or deletion, the accessed node is moved to the root of the tree
 * by a series of rotations, a process known as the "splaying" operation.
 *
 * This implementation does not allow duplicate keys.
 */
public class SplayTree {

    /**
     * Represents a node in the Splay Tree.
     */
    private class Node {
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
     * Performs a right rotation on the subtree rooted at node x.
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
     * The core splaying operation. It brings the node with the given key
     * (or the last accessed node if the key is not found) to the root of the
     * subtree rooted at 'node'. This is a recursive, bottom-up implementation.
     *
     * @param node The root of the subtree to splay.
     * @param key The key to search for and bring to the top.
     * @return The new root of the splayed subtree.
     */
    private Node splay(Node node, int key) {
        // Base case: if node is null or the key is at the root
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
                // Recursively bring the key as root of left-left
                node.left.left = splay(node.left.left, key);
                // First rotation for root
                node = rightRotate(node);
            }
            // Zig-Zag (Left Right)
            else if (key > node.left.key) {
                // Recursively bring the key as root of left-right
                node.left.right = splay(node.left.right, key);
                // First rotation for node.left
                if (node.left.right != null) {
                    node.left = leftRotate(node.left);
                }
            }

            // Do second rotation for root
            return (node.left == null) ? node : rightRotate(node);
        }
        // Key lies in the right subtree
        else { // key > node.key
            // Key is not in the tree, we are done
            if (node.right == null) {
                return node;
            }

            // Zig-Zag (Right Left)
            if (key < node.right.key) {
                // Recursively bring the key as root of right-left
                node.right.left = splay(node.right.left, key);
                // First rotation for node.right
                if (node.right.left != null) {
                    node.right = rightRotate(node.right);
                }
            }
            // Zig-Zig (Right Right)
            else if (key > node.right.key) {
                // Recursively bring the key as root of right-right
                node.right.right = splay(node.right.right, key);
                // First rotation for root
                node = leftRotate(node);
            }

            // Do second rotation for root
            return (node.right == null) ? node : leftRotate(node);
        }
    }

    /**
     * Searches for a key in the splay tree.
     * If the key is found, the node containing the key is splayed to become the new root.
     * If the key is not found, the last accessed node on the search path is splayed to the root.
     *
     * @param key The integer key to search for.
     * @return The key if found, otherwise null.
     */
    public Integer search(int key) {
        if (root == null) {
            return null;
        }
        root = splay(root, key);
        // After splaying, the key should be at the root if it exists.
        if (root.key == key) {
            return root.key;
        }
        return null;
    }

    /**
     * Inserts a key into the splay tree.
     * If the key already exists, the node is splayed to the root and the tree is unchanged.
     * Duplicates are not allowed.
     *
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

        // If key is already present, then return (no duplicates)
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
        else { // key > root.key
            newNode.left = root;
            newNode.right = root.right;
            root.right = null;
        }
        root = newNode;
    }

    /**
     * Deletes a key from the splay tree.
     * If the key is found, it is deleted and the tree is restructured.
     * If the key is not found, the tree is splayed based on the last accessed node
     * during the search for the key.
     *
     * @param key The integer key to delete.
     */
    public void delete(int key) {
        // If the tree is empty, there is nothing to delete
        if (root == null) {
            return;
        }

        // Splay the tree for the key
        root = splay(root, key);

        // If the key is not in the tree, do nothing
        if (root.key != key) {
            return;
        }

        // Now, the node to be deleted is the root.
        // We need to join its left and right subtrees.
        Node leftSubtree = root.left;
        Node rightSubtree = root.right;

        if (leftSubtree == null) {
            // If there's no left subtree, the right subtree becomes the new tree
            root = rightSubtree;
        } else {
            // Splay the left subtree to bring its maximum element to the top.
            // Splaying for the deleted key (which is guaranteed to be larger than any
            // key in the left subtree) will bring the max element to the root.
            Node newRoot = splay(leftSubtree, key);

            // The new root (max of the original left subtree) will have no right child.
            // We can attach the original right subtree there.
            newRoot.right = rightSubtree;
            root = newRoot;
        }
    }
}