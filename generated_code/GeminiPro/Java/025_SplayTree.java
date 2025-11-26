/**
 * A self-contained Java class that implements an integer set using a Splay Tree.
 * A splay tree is a self-adjusting binary search tree with the additional property
 * that recently accessed elements are quick to access again.
 */
public class SplayTree {

    /**
     * Represents a node in the Splay Tree.
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

    /**
     * Inserts a key into the splay tree.
     * If the key already exists, the tree remains unchanged.
     * After insertion, the new node becomes the root of the tree.
     *
     * @param key The integer key to insert.
     */
    public void insert(int key) {
        // Case 1: The tree is empty.
        if (root == null) {
            root = new Node(key);
            return;
        }

        // Splay the tree for the key. This brings the node with the key,
        // or the last-accessed node (the parent of where the key would be), to the root.
        root = splay(root, key);

        // If the key is already in the tree, we are done.
        if (root.key == key) {
            return;
        }

        // Case 2: The key is not in the tree. Insert the new node as the new root.
        Node newNode = new Node(key);
        if (key < root.key) {
            // The new root's key is smaller than the old root's key.
            // The new root's right child becomes the old root.
            // The new root's left child becomes the old root's left child.
            newNode.right = root;
            newNode.left = root.left;
            root.left = null;
        } else { // key > root.key
            // The new root's key is larger than the old root's key.
            // The new root's left child becomes the old root.
            // The new root's right child becomes the old root's right child.
            newNode.left = root;
            newNode.right = root.right;
            root.right = null;
        }
        root = newNode;
    }

    /**
     * Searches for a key in the splay tree.
     * If the key is found, the node containing the key is splayed to the root.
     * If the key is not found, the last accessed node in the search path is splayed to the root.
     *
     * @param key The integer key to search for.
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
     * Deletes a key from the splay tree.
     * If the key is not in the tree, the tree remains unchanged.
     *
     * @param key The integer key to delete.
     */
    public void delete(int key) {
        if (root == null) {
            return;
        }

        // Splay the tree for the key. If the key exists, it becomes the root.
        root = splay(root, key);

        // If the key is not at the root, it's not in the tree.
        if (root.key != key) {
            return;
        }

        // The key is at the root. Now we need to remove it.
        // The tree is split into two subtrees: left and right.
        Node leftSubtree = root.left;
        Node rightSubtree = root.right;

        if (leftSubtree == null) {
            // If there's no left subtree, the right subtree becomes the new tree.
            root = rightSubtree;
        } else {
            // Splay the left subtree to bring its maximum element to its root.
            // Since `key` is larger than any element in the left subtree, splaying for `key`
            // will bring the maximum element to the root of the left subtree.
            leftSubtree = splay(leftSubtree, key);

            // The original right subtree becomes the right child of the new root.
            leftSubtree.right = rightSubtree;
            root = leftSubtree;
        }
    }

    /**
     * Performs a right rotation on the subtree rooted at y.
     *
     * @param y The root of the subtree to rotate.
     * @return The new root of the subtree.
     */
    private Node rightRotate(Node y) {
        Node x = y.left;
        y.left = x.right;
        x.right = y;
        return x;
    }

    /**
     * Performs a left rotation on the subtree rooted at x.
     *
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
     * The main splay operation. It brings the node with the given key to the root of the
     * subtree rooted at `node`. If the key is not present, it brings the last accessed
     * node to the root.
     *
     * @param node The root of the current subtree.
     * @param key The key to splay for.
     * @return The new root of the splayed subtree.
     */
    private Node splay(Node node, int key) {
        // Base cases: node is null or the key is at the root.
        if (node == null || node.key == key) {
            return node;
        }

        // Key is in the left subtree.
        if (key < node.key) {
            // If the left child is null, the key is not in the tree.
            if (node.left == null) {
                return node;
            }

            // Zig-Zig (Left-Left)
            if (key < node.left.key) {
                // Recursively bring the key to the root of the left-left grandchild.
                node.left.left = splay(node.left.left, key);
                // Perform the first right rotation on the current node (g).
                node = rightRotate(node);
            }
            // Zig-Zag (Left-Right)
            else if (key > node.left.key) {
                // Recursively bring the key to the root of the left-right grandchild.
                node.left.right = splay(node.left.right, key);
                // Perform the first rotation (left) on the child (p).
                if (node.left.right != null) {
                    node.left = leftRotate(node.left);
                }
            }
            // Perform the second rotation (for Zig-Zig/Zig-Zag) or the only rotation (for Zig).
            return (node.left == null) ? node : rightRotate(node);

        }
        // Key is in the right subtree.
        else { // key > node.key
            // If the right child is null, the key is not in the tree.
            if (node.right == null) {
                return node;
            }

            // Zig-Zag (Right-Left)
            if (key < node.right.key) {
                // Recursively bring the key to the root of the right-left grandchild.
                node.right.left = splay(node.right.left, key);
                // Perform the first rotation (right) on the child (p).
                if (node.right.left != null) {
                    node.right = rightRotate(node.right);
                }
            }
            // Zig-Zig (Right-Right)
            else if (key > node.right.key) {
                // Recursively bring the key to the root of the right-right grandchild.
                node.right.right = splay(node.right.right, key);
                // Perform the first left rotation on the current node (g).
                node = leftRotate(node);
            }
            // Perform the second rotation (for Zig-Zig/Zig-Zag) or the only rotation (for Zig).
            return (node.right == null) ? node : leftRotate(node);
        }
    }
}