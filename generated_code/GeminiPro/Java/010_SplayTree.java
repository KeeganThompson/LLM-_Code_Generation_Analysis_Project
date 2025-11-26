/**
 * A self-contained Java class implementing a Splay Tree for an integer set.
 * Splay trees are self-balancing binary search trees with the additional property
 * that recently accessed elements are quick to access again.
 */
public class SplayTree {

    /**
     * Inner class representing a node in the splay tree.
     */
    private class Node {
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

    // --- Private Helper Methods for Rotations ---

    /**
     * Performs a right rotation on the subtree rooted at x.
     *      x           y
     *     / \         / \
     *    y   T3  ->  T1  x
     *   / \             / \
     *  T1  T2          T2  T3
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
     *    x             y
     *   / \           / \
     *  T1  y    ->   x   T3
     *     / \       / \
     *    T2  T3    T1  T2
     * @param x The root of the subtree to rotate.
     * @return The new root of the subtree.
     */
    private Node leftRotate(Node x) {
        Node y = x.right;
        x.right = y.left;
        y.left = x;
        return y;
    }

    // --- Splay Operation ---

    /**
     * The main splay operation. It brings the node with the given key to the root.
     * If the key is not in the tree, the last accessed node is brought to the root.
     * This is a recursive, bottom-up splaying implementation.
     *
     * @param root The root of the current subtree.
     * @param key The key to splay.
     * @return The new root of the splayed subtree.
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
            // Key is not in tree, we are done
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

    // --- Public API Methods ---

    /**
     * Inserts a key into the splay tree.
     * If the key already exists, the tree remains unchanged.
     * After insertion, the new node becomes the root of the tree.
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

        // If the key is already present, do nothing.
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
        else {
            newNode.left = root;
            newNode.right = root.right;
            root.right = null;
        }
        root = newNode;
    }

    /**
     * Searches for a key in the splay tree.
     * This operation performs splaying. If the key is found, its node is moved
     * to the root. If not found, the last accessed node on the search path
     * is moved to the root.
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
            return root.key;
        } else {
            return null;
        }
    }

    /**
     * Deletes a key from the splay tree.
     * If the key is not in the tree, the tree is splayed based on the search for the key.
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

        // At this point, the node to be deleted is the root.
        Node leftSubtree = root.left;
        Node rightSubtree = root.right;

        if (leftSubtree == null) {
            // If there's no left subtree, the right subtree becomes the new tree.
            root = rightSubtree;
        } else {
            // Splay the left subtree to bring its largest element to its root.
            // The largest element in the left subtree has no right child.
            Node newRoot = splay(leftSubtree, key); // Searching for 'key' finds max
            
            // Join the right subtree to the new root.
            newRoot.right = rightSubtree;
            root = newRoot;
        }
    }
}