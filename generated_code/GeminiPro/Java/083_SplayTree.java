/**
 * A complete, self-contained Java class that implements an integer set using a Splay Tree.
 *
 * A Splay Tree is a self-balancing binary search tree with the additional
 * property that recently accessed elements are quick to access again.
 * It performs basic operations such as insertion, deletion, and search.
 * After a search, insertion, or deletion, the accessed node is moved to the root
 * of the tree through a series of rotations, a process called "splaying".
 * This implementation does not allow duplicate keys, adhering to set semantics.
 */
public class SplayTree {

    /**
     * Inner class representing a node in the Splay Tree.
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
     * Constructs an empty Splay Tree.
     */
    public SplayTree() {
        this.root = null;
    }

    /**
     * Helper method to perform a right rotation on the subtree rooted at x.
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
     * Helper method to perform a left rotation on the subtree rooted at y.
     * @param y The root of the subtree to rotate.
     * @return The new root of the rotated subtree.
     */
    private Node leftRotate(Node y) {
        Node x = y.right;
        y.right = x.left;
        x.left = y;
        return x;
    }

    /**
     * The main splay operation. It moves the node with the given key (or the last
     * accessed node if the key is not found) to the root of the tree.
     * This is a recursive, bottom-up splaying implementation.
     *
     * @param node The root of the subtree to splay.
     * @param key The key to splay for.
     * @return The new root of the splayed subtree.
     */
    private Node splay(Node node, int key) {
        // Base cases: node is null or key is at the root
        if (node == null || node.key == key) {
            return node;
        }

        if (key < node.key) {
            // Key lies in the left subtree
            if (node.left == null) {
                // Key not found, splay the last accessed node (node)
                return node;
            }

            // Zig-Zig (Left-Left)
            if (key < node.left.key) {
                node.left.left = splay(node.left.left, key);
                node = rightRotate(node);
            }
            // Zig-Zag (Left-Right)
            else if (key > node.left.key) {
                node.left.right = splay(node.left.right, key);
                if (node.left.right != null) {
                    node.left = leftRotate(node.left);
                }
            }
            // Perform the second rotation for Zig-Zig/Zig-Zag or the single rotation for Zig
            return (node.left == null) ? node : rightRotate(node);

        } else { // key > node.key
            // Key lies in the right subtree
            if (node.right == null) {
                // Key not found, splay the last accessed node (node)
                return node;
            }

            // Zig-Zag (Right-Left)
            if (key < node.right.key) {
                node.right.left = splay(node.right.left, key);
                if (node.right.left != null) {
                    node.right = rightRotate(node.right);
                }
            }
            // Zig-Zig (Right-Right)
            else if (key > node.right.key) {
                node.right.right = splay(node.right.right, key);
                node = leftRotate(node);
            }
            // Perform the second rotation for Zig-Zig/Zig-Zag or the single rotation for Zig
            return (node.right == null) ? node : leftRotate(node);
        }
    }

    /**
     * Searches for a key in the tree. As a side effect, it splays the tree,
     * moving the accessed node (or the last node on the search path) to the root.
     *
     * @param key The key to search for.
     * @return The key if found, otherwise null.
     */
    public Integer search(int key) {
        if (root == null) {
            return null;
        }
        root = splay(root, key);
        // After splaying, if the key exists, it will be at the root.
        if (root.key == key) {
            return root.key;
        }
        return null;
    }

    /**
     * Inserts a key into the Splay Tree. Duplicates are not allowed.
     * The new node (or the existing node if the key was already present) is splayed to the root.
     *
     * @param key The key to insert.
     */
    public void insert(int key) {
        // If the tree is empty, create a new root
        if (root == null) {
            root = new Node(key);
            return;
        }

        // Splay the tree for the key. This brings the closest node to the root.
        root = splay(root, key);

        // If the key is already present, do nothing (set semantics).
        if (root.key == key) {
            return;
        }

        Node newNode = new Node(key);

        // The new key will become the new root. The old root is split into two subtrees.
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

        // Splay the tree for the key. If the key exists, it will become the new root.
        root = splay(root, key);

        // If the key is not in the tree, do nothing.
        if (root.key != key) {
            return;
        }

        // The key is now at the root. We need to delete it and join the two subtrees.
        Node leftSubtree = root.left;
        Node rightSubtree = root.right;

        if (leftSubtree == null) {
            // If there's no left subtree, the right subtree becomes the new tree.
            root = rightSubtree;
        } else {
            // Splay the left subtree to bring its maximum element to its root.
            // Searching for 'key' in the left subtree will bring the max element
            // to the top, as 'key' is larger than any element in the left subtree.
            leftSubtree = splay(leftSubtree, key);

            // The new root of the left subtree has no right child (since it's the max).
            // Attach the original right subtree as its right child.
            leftSubtree.right = rightSubtree;
            root = leftSubtree;
        }
    }
}