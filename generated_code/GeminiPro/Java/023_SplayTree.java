/**
 * A self-contained Java class implementing a Splay Tree for an integer set.
 * A Splay Tree is a self-balancing binary search tree with the additional
 * property that recently accessed elements are quick to access again.
 * It performs basic operations such as insertion, deletion, and search.
 * After a search or an access, the accessed node is moved to the root of the tree
 * through a series of rotations, which is known as the "splaying" operation.
 */
public class SplayTree {

    /**
     * Represents a node in the Splay Tree.
     */
    private class Node {
        int key;
        Node left, right;

        /**
         * Constructs a new node with the given key.
         * @param key The integer key for the node.
         */
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
     * Performs a right rotation on the subtree rooted at node x.
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
     * Performs a left rotation on the subtree rooted at node x.
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
     * The main splaying operation. It brings the node with the given key
     * (or the last accessed node if the key is not found) to the root of the
     * subtree rooted at 'node'.
     *
     * @param node The root of the subtree to splay.
     * @param key  The key to splay for.
     * @return The new root of the splayed subtree.
     */
    private Node splay(Node node, int key) {
        if (node == null || node.key == key) {
            return node;
        }

        if (key < node.key) {
            // Key is in the left subtree
            if (node.left == null) {
                return node; // Key not found, splay the parent
            }

            if (key < node.left.key) {
                // Zig-Zig (Left-Left)
                node.left.left = splay(node.left.left, key);
                node = rightRotate(node);
            } else if (key > node.left.key) {
                // Zig-Zag (Left-Right)
                node.left.right = splay(node.left.right, key);
                if (node.left.right != null) {
                    node.left = leftRotate(node.left);
                }
            }
            // Perform the second rotation for Zig-Zig or the only rotation for Zig
            return (node.left == null) ? node : rightRotate(node);

        } else { // key > node.key
            // Key is in the right subtree
            if (node.right == null) {
                return node; // Key not found, splay the parent
            }

            if (key > node.right.key) {
                // Zig-Zig (Right-Right)
                node.right.right = splay(node.right.right, key);
                node = leftRotate(node);
            } else if (key < node.right.key) {
                // Zig-Zag (Right-Left)
                node.right.left = splay(node.right.left, key);
                if (node.right.left != null) {
                    node.right = rightRotate(node.right);
                }
            }
            // Perform the second rotation for Zig-Zig or the only rotation for Zig
            return (node.right == null) ? node : leftRotate(node);
        }
    }

    /**
     * Searches for a key in the tree. If the key is found, the corresponding
     * node is splayed to the root.
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
     * Inserts a key into the Splay Tree. Duplicates are not allowed.
     * The newly inserted node becomes the new root of the tree.
     *
     * @param key The key to insert.
     */
    public void insert(int key) {
        // If the tree is empty, create a new root
        if (root == null) {
            root = new Node(key);
            return;
        }

        // Splay the tree to bring the closest key to the root
        root = splay(root, key);

        // If the key is already present, do nothing
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

        // Splay the tree to bring the node to be deleted to the root
        root = splay(root, key);

        // If the key is not in the tree, do nothing
        if (root.key != key) {
            return;
        }

        // Now, the node to be deleted is the root
        Node leftSubtree = root.left;
        Node rightSubtree = root.right;

        if (leftSubtree == null) {
            root = rightSubtree;
        } else {
            // Splay the left subtree to bring its maximum element to its root.
            // Since `key` is greater than any element in the left subtree,
            // splaying for `key` will achieve this.
            leftSubtree = splay(leftSubtree, key);

            // The new root of the left subtree will have a null right child.
            // Attach the right subtree to it.
            leftSubtree.right = rightSubtree;
            root = leftSubtree;
        }
    }
}