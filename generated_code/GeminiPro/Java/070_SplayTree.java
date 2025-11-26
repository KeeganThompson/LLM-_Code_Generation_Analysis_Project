/**
 * A self-contained Java class implementing a Splay Tree for an integer set.
 * Splay trees are self-balancing binary search trees with the additional property
 * that recently accessed elements are quick to access again.
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
     * The core splaying operation. It brings the node with the given key
     * (or the last accessed node if the key is not found) to the root of the tree.
     * This is a recursive, bottom-up splaying implementation.
     *
     * @param node The root of the current subtree.
     * @param key The key to splay for.
     * @return The new root of the splayed subtree.
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
            // Perform the second rotation for Zig-Zig or the only rotation for Zig
            return (node.left == null) ? node : rightRotate(node);
        }
        // Key lies in the right subtree
        else { // key > node.key
            // Key is not in tree, we are done
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
            // Perform the second rotation for Zig-Zig or the only rotation for Zig
            return (node.right == null) ? node : leftRotate(node);
        }
    }

    /**
     * Inserts a key into the splay tree. If the key already exists, the tree remains unchanged.
     * After insertion, the new node becomes the root of the tree.
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

        // If the key is already present, do nothing
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
        // If the new key is larger than the root's key
        else {
            newNode.left = root;
            newNode.right = root.right;
            root.right = null;
        }
        root = newNode; // The new node is the new root
    }

    /**
     * Searches for a key in the splay tree.
     * If the key is found, it is splayed to the root.
     * If the key is not found, the last accessed node on the search path is splayed to the root.
     * @param key The integer key to search for.
     * @return The key if found, otherwise null.
     */
    public Integer search(int key) {
        if (root == null) {
            return null;
        }
        root = splay(root, key);
        if (root.key == key) {
            return root.key; // Autoboxing to Integer
        }
        return null;
    }

    /**
     * Deletes a key from the splay tree.
     * If the key is present, it is first splayed to the root and then removed.
     * The new root will be the largest element in the left subtree.
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

        // Now, the node to be deleted is at the root.
        // If there is no left subtree, the right subtree becomes the new tree.
        if (root.left == null) {
            root = root.right;
        } else {
            // Save the right subtree
            Node rightSubtree = root.right;
            // The new root is the root of the left subtree
            root = root.left;
            // Splay the left subtree to bring its largest element (predecessor of the deleted key) to its root.
            // Splaying for the original key achieves this.
            root = splay(root, key);
            // Attach the original right subtree to the new root.
            // Since the new root is the max element of the left subtree, it has no right child.
            root.right = rightSubtree;
        }
    }
}