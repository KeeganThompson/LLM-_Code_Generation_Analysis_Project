/**
 * A complete, self-contained Java class that implements an integer set using a Splay Tree.
 * A splay tree is a self-balancing binary search tree with the additional property that
 * recently accessed elements are quick to access again. It performs basic operations
 * such as insertion, deletion, and search. After any of these operations on a key, the
 * node containing that key (or the last node accessed in a search) is moved to the
 * root of the tree through a series of rotations.
 */
public class SplayTree {

    private Node root;

    /**
     * Inner class to represent a node in the Splay Tree.
     */
    private static class Node {
        int key;
        Node left;
        Node right;

        Node(int key) {
            this.key = key;
            this.left = null;
            this.right = null;
        }
    }

    /**
     * Constructs an empty Splay Tree.
     */
    public SplayTree() {
        this.root = null;
    }

    // --- Private Helper Methods ---

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
     * The main splay operation. Brings the node with the given key to the root of the
     * subtree. If the key is not found, the last accessed node is brought to the root.
     * This is a recursive, bottom-up splay implementation.
     *
     * @param node The root of the current subtree.
     * @param key The key to search for and splay.
     * @return The new root of the splayed subtree.
     */
    private Node splay(Node node, int key) {
        // Base cases: node is null or key is present at root
        if (node == null || node.key == key) {
            return node;
        }

        // Key lies in left subtree
        if (key < node.key) {
            // Key is not in tree, we are done
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

            // Do second rotation for node (if required)
            return (node.left == null) ? node : rightRotate(node);
        }
        // Key lies in right subtree
        else {
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

            // Do second rotation for node (if required)
            return (node.right == null) ? node : leftRotate(node);
        }
    }

    // --- Public API Methods ---

    /**
     * Searches for a key in the tree.
     * If the key is found, it is splayed to the root. If not found, the last
     * accessed node on the search path is splayed to the root.
     *
     * @param key The key to search for.
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
     * Inserts a new key into the Splay Tree.
     * If the key already exists, the tree is splayed on that key, and no new node is inserted.
     *
     * @param key The key to insert.
     */
    public void insert(int key) {
        // Case 1: The tree is empty.
        if (root == null) {
            root = new Node(key);
            return;
        }

        // Splay the tree for the key. This brings the closest node to the root.
        root = splay(root, key);

        // Case 2: The key is already in the tree. Do nothing.
        if (root.key == key) {
            return;
        }

        // Case 3: Insert the new key.
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

        // Splay the tree for the key. If the key exists, it becomes the root.
        root = splay(root, key);

        // If the key is not at the root, it's not in the tree.
        if (root.key != key) {
            return;
        }

        // Now, the node to be deleted is the root.
        // We need to join its left and right subtrees.
        Node leftSubtree = root.left;
        Node rightSubtree = root.right;

        if (leftSubtree == null) {
            // If there's no left subtree, the right subtree becomes the new tree.
            root = rightSubtree;
        } else {
            // Find the maximum element in the left subtree by traversing to the rightmost node.
            Node maxNode = leftSubtree;
            while (maxNode.right != null) {
                maxNode = maxNode.right;
            }

            // Splay the left subtree around its maximum element.
            // This makes the maximum element the root of the modified left subtree.
            leftSubtree = splay(leftSubtree, maxNode.key);

            // The new root of the left subtree now has no right child.
            // Attach the original right subtree as its right child.
            leftSubtree.right = rightSubtree;
            root = leftSubtree;
        }
    }
}