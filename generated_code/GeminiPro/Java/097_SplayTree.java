/**
 * A self-contained Java class implementing a Splay Tree for an integer set.
 * Splay trees are self-balancing binary search trees with the additional property
 * that recently accessed elements are quick to access again.
 */
public class SplayTree {

    /**
     * Inner class representing a node in the Splay Tree.
     */
    private class Node {
        int key;
        Node left, right;

        /**
         * Constructor for a Node.
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

    // --- Core Splay Operations ---

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
     * The main splay operation. Brings the node with the given key (or the last
     * accessed node if the key is not found) to the root of the tree.
     * @param node The root of the tree (or subtree) to splay.
     * @param key The key to search for and bring to the root.
     * @return The new root of the splayed tree.
     */
    private Node splay(Node node, int key) {
        // Base case: node is null or key is at root
        if (node == null || node.key == key) {
            return node;
        }

        // Key is in the left subtree
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
            // Do second rotation for Zig-Zig or Zig-Zag (or Zig)
            return (node.left == null) ? node : rightRotate(node);
        }
        // Key is in the right subtree
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
            // Do second rotation for Zig-Zig or Zig-Zag (or Zig)
            return (node.right == null) ? node : leftRotate(node);
        }
    }

    // --- Public API Methods ---

    /**
     * Searches for a key in the tree. If the key is found, it is splayed
     * to the root.
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
     * Inserts a key into the Splay Tree. If the key already exists,
     * the tree is splayed on that key but no new node is inserted.
     * @param key The key to insert.
     */
    public void insert(int key) {
        // If the tree is empty, create a new root
        if (root == null) {
            root = new Node(key);
            return;
        }

        // Splay the tree on the key. This brings the closest node to the root.
        root = splay(root, key);

        // If key is already present, do nothing
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
        root = newNode;
    }

    /**
     * Deletes a key from the Splay Tree.
     * @param key The key to delete.
     */
    public void delete(int key) {
        if (root == null) {
            return;
        }

        // Splay the tree on the key. If the key exists, it becomes the root.
        root = splay(root, key);

        // If the key is not at the root, it's not in the tree.
        if (root.key != key) {
            return;
        }

        // Now, the node to be deleted is the root.
        Node leftSubtree = root.left;
        Node rightSubtree = root.right;

        if (leftSubtree == null) {
            // If there's no left subtree, the right subtree becomes the new tree.
            root = rightSubtree;
        } else {
            // Splay the left subtree to bring its largest element to its root.
            // Since all elements in the left subtree are smaller than the deleted key,
            // splaying for the deleted key will bring the max element to the top.
            leftSubtree = splay(leftSubtree, key);

            // The new root of the left subtree has no right child.
            // Attach the original right subtree there.
            leftSubtree.right = rightSubtree;
            root = leftSubtree;
        }
    }
}