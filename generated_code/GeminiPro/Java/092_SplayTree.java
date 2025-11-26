/**
 * A complete, self-contained Java class that implements an integer set using a Splay Tree.
 * Splay trees are self-balancing binary search trees with the property that recently
 * accessed elements are quick to access again.
 */
public class SplayTree {

    /**
     * Represents a node in the Splay Tree.
     * It is a private static inner class to encapsulate the node structure.
     */
    private static class Node {
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

    // --- Private Helper Methods for Rotations and Splaying ---

    /**
     * Performs a right rotation on the subtree rooted at node x.
     * This is a standard BST rotation.
     *
     * @param x The root of the subtree to rotate.
     * @return The new root of the subtree after rotation.
     */
    private Node rotateRight(Node x) {
        Node y = x.left;
        x.left = y.right;
        y.right = x;
        return y;
    }

    /**
     * Performs a left rotation on the subtree rooted at node x.
     * This is a standard BST rotation.
     *
     * @param x The root of the subtree to rotate.
     * @return The new root of the subtree after rotation.
     */
    private Node rotateLeft(Node x) {
        Node y = x.right;
        x.right = y.left;
        y.left = x;
        return y;
    }

    /**
     * The core splay operation. It brings the node with the given key to the root of the tree.
     * If the key is not present, the last accessed node in the search path is brought to the root.
     * This method uses a recursive, bottom-up approach.
     *
     * @param currentRoot The root of the current subtree being considered.
     * @param key The key to be splayed to the top.
     * @return The new root of the tree after the splay operation.
     */
    private Node splay(Node currentRoot, int key) {
        // Base case: root is null or key is present at root
        if (currentRoot == null || currentRoot.key == key) {
            return currentRoot;
        }

        // Key lies in the left subtree
        if (key < currentRoot.key) {
            // Key is not in the tree, we are done
            if (currentRoot.left == null) {
                return currentRoot;
            }

            // Zig-Zig (Left-Left)
            if (key < currentRoot.left.key) {
                // Recursively bring the key as root of the left-left grandchild
                currentRoot.left.left = splay(currentRoot.left.left, key);
                // Perform the first right rotation for the current root
                currentRoot = rotateRight(currentRoot);
            }
            // Zig-Zag (Left-Right)
            else if (key > currentRoot.left.key) {
                // Recursively bring the key as root of the left-right grandchild
                currentRoot.left.right = splay(currentRoot.left.right, key);
                // Perform the first rotation (left) for the child
                if (currentRoot.left.right != null) {
                    currentRoot.left = rotateLeft(currentRoot.left);
                }
            }

            // Perform the second rotation for the current root (if child exists)
            return (currentRoot.left == null) ? currentRoot : rotateRight(currentRoot);
        }
        // Key lies in the right subtree
        else {
            // Key is not in the tree, we are done
            if (currentRoot.right == null) {
                return currentRoot;
            }

            // Zig-Zag (Right-Left)
            if (key < currentRoot.right.key) {
                // Recursively bring the key as root of the right-left grandchild
                currentRoot.right.left = splay(currentRoot.right.left, key);
                // Perform the first rotation (right) for the child
                if (currentRoot.right.left != null) {
                    currentRoot.right = rotateRight(currentRoot.right);
                }
            }
            // Zig-Zig (Right-Right)
            else if (key > currentRoot.right.key) {
                // Recursively bring the key as root of the right-right grandchild
                currentRoot.right.right = splay(currentRoot.right.right, key);
                // Perform the first left rotation for the current root
                currentRoot = rotateLeft(currentRoot);
            }

            // Perform the second rotation for the current root (if child exists)
            return (currentRoot.right == null) ? currentRoot : rotateLeft(currentRoot);
        }
    }

    // --- Public API Methods ---

    /**
     * Inserts a key into the Splay Tree. If the key already exists, the node
     * containing the key is splayed to the root, but no new node is added.
     *
     * @param key The integer key to insert.
     */
    public void insert(int key) {
        // Case 1: The tree is empty
        if (root == null) {
            root = new Node(key);
            return;
        }

        // Splay the tree for the key. The closest node becomes the new root.
        root = splay(root, key);

        // Case 2: The key is already in the tree. Do nothing.
        if (root.key == key) {
            return;
        }

        // Case 3: The key is not in the tree. Insert a new node.
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
     * Searches for a key in the tree. The accessed node (or the last node on the
     * search path if not found) is splayed to become the new root.
     *
     * @param key The key to search for.
     * @return The key as an Integer if found, otherwise null.
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
     * Deletes a key from the Splay Tree. If the key is found, it is first
     * splayed to the root and then removed.
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

        // The key to be deleted is now at the root.
        Node leftSubtree = root.left;
        Node rightSubtree = root.right;

        if (leftSubtree == null) {
            // No left child, the right subtree becomes the new tree.
            root = rightSubtree;
        } else {
            // Splay the left subtree to bring its maximum element to its root.
            // A search for the (just deleted) key will achieve this, as it's larger
            // than any element in the left subtree.
            Node newRoot = splay(leftSubtree, key);
            // The new root of the left subtree has no right child.
            // Attach the original right subtree there.
            newRoot.right = rightSubtree;
            root = newRoot;
        }
    }
}