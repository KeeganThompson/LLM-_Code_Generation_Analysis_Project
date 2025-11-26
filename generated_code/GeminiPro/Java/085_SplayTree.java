/**
 * A complete, self-contained implementation of a Splay Tree for an integer set.
 * Splay trees are self-balancing binary search trees with the additional property
 * that recently accessed elements are quick to access again.
 */
public class SplayTree {

    /**
     * Represents a node in the Splay Tree.
     * It is a static inner class as it does not need to access instance members of SplayTree.
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
     * The core splay operation. It brings the node with the given key
     * (or the last accessed node if the key is not found) to the root of the tree.
     * @param currentRoot The root of the current subtree.
     * @param key The key to splay.
     * @return The new root of the splayed tree.
     */
    private Node splay(Node currentRoot, int key) {
        // Base case: root is null or key is at root
        if (currentRoot == null || currentRoot.key == key) {
            return currentRoot;
        }

        // Key is in the left subtree
        if (key < currentRoot.key) {
            // Key is not in the tree, we are done
            if (currentRoot.left == null) {
                return currentRoot;
            }

            // Zig-Zig (Left Left)
            if (key < currentRoot.left.key) {
                currentRoot.left.left = splay(currentRoot.left.left, key);
                currentRoot = rightRotate(currentRoot);
            }
            // Zig-Zag (Left Right)
            else if (key > currentRoot.left.key) {
                currentRoot.left.right = splay(currentRoot.left.right, key);
                if (currentRoot.left.right != null) {
                    currentRoot.left = leftRotate(currentRoot.left);
                }
            }
            // Do second rotation for root
            return (currentRoot.left == null) ? currentRoot : rightRotate(currentRoot);
        }
        // Key is in the right subtree
        else {
            // Key is not in the tree, we are done
            if (currentRoot.right == null) {
                return currentRoot;
            }

            // Zig-Zag (Right Left)
            if (key < currentRoot.right.key) {
                currentRoot.right.left = splay(currentRoot.right.left, key);
                if (currentRoot.right.left != null) {
                    currentRoot.right = rightRotate(currentRoot.right);
                }
            }
            // Zig-Zig (Right Right)
            else if (key > currentRoot.right.key) {
                currentRoot.right.right = splay(currentRoot.right.right, key);
                currentRoot = leftRotate(currentRoot);
            }
            // Do second rotation for root
            return (currentRoot.right == null) ? currentRoot : leftRotate(currentRoot);
        }
    }

    /**
     * Searches for a key in the splay tree.
     * If the key is found, the corresponding node is splayed to become the new root.
     * If not found, the last accessed node on the search path is splayed to the root.
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
     * Inserts a key into the splay tree.
     * If the key already exists, the tree is splayed on that key.
     * If the key is new, it is inserted and becomes the new root of the tree.
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

        // If the key is already present, do nothing.
        if (root.key == key) {
            return;
        }

        // Create the new node
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
        // The new node becomes the new root
        root = newNode;
    }

    /**
     * Deletes a key from the splay tree.
     * If the key exists, it is deleted, and the tree is restructured.
     * The parent of the deleted node (or a neighbor) becomes the new root.
     * @param key The key to delete.
     */
    public void delete(int key) {
        if (root == null) {
            return;
        }

        // Splay the tree for the key.
        // If the key is in the tree, it will become the root.
        root = splay(root, key);

        // If the key is not at the root, it's not in the tree.
        if (root.key != key) {
            return;
        }

        // Now, the node to delete is the root.
        Node leftSubtree = root.left;
        Node rightSubtree = root.right;

        if (leftSubtree == null) {
            // If there's no left child, the right child becomes the new root.
            root = rightSubtree;
        } else {
            // Splay the left subtree to bring its maximum element to its root.
            // This maximum element is the predecessor of the key we are deleting.
            leftSubtree = splay(leftSubtree, key);

            // The original right subtree becomes the right child of this new root.
            leftSubtree.right = rightSubtree;
            root = leftSubtree;
        }
    }
}