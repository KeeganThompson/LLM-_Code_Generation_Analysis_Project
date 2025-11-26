/**
 * A complete, self-contained implementation of a Splay Tree for an integer set.
 * A splay tree is a self-adjusting binary search tree with the additional
 * property that recently accessed elements are quick to access again.
 */
public class SplayTree {

    private Node root;

    /**
     * Inner class representing a node in the splay tree.
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
     * Constructs an empty SplayTree.
     */
    public SplayTree() {
        this.root = null;
    }

    /**
     * Searches for a key in the splay tree.
     * This operation performs a splay, moving the accessed node (or the last
     * node on the search path) to the root of the tree.
     *
     * @param key The key to search for.
     * @return The key if it is found, otherwise null.
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
     * If the key already exists, the node with that key is splayed to the root.
     *
     * @param key The key to insert.
     */
    public void insert(int key) {
        // If the tree is empty, create a new root.
        if (root == null) {
            root = new Node(key);
            return;
        }

        // Splay the tree on the key. This brings the node with the key,
        // or its would-be parent, to the root.
        root = splay(root, key);

        // If the key is already in the tree, we're done.
        if (root.key == key) {
            return;
        }

        // Otherwise, insert the new key at the root.
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
     * Deletes a key from the splay tree.
     * If the key is not found, the tree is splayed on the last accessed node.
     *
     * @param key The key to delete.
     */
    public void delete(int key) {
        if (root == null) {
            return;
        }

        // Splay the tree on the key.
        root = splay(root, key);

        // If the key is not at the root, it's not in the tree.
        if (root.key != key) {
            return;
        }

        // The node to delete is now the root.
        // We join its left and right subtrees to form the new tree.
        Node leftSubtree = root.left;
        Node rightSubtree = root.right;

        if (leftSubtree == null) {
            root = rightSubtree;
        } else {
            // Splay the maximum element in the left subtree to its root.
            // Since `key` is greater than any element in the left subtree, splaying
            // for `key` will bring the maximum element to the top.
            Node newRoot = splay(leftSubtree, key);
            // Attach the original right subtree.
            newRoot.right = rightSubtree;
            root = newRoot;
        }
    }

    /**
     * Performs a right rotation on the subtree rooted at x.
     *
     * @param x The root of the subtree.
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
     *
     * @param x The root of the subtree.
     * @return The new root of the subtree after rotation.
     */
    private Node leftRotate(Node x) {
        Node y = x.right;
        x.right = y.left;
        y.left = x;
        return y;
    }

    /**
     * The core splay operation, implemented recursively (bottom-up).
     * It moves the node with the given key (or the last accessed node on the
     * search path) to the root of the subtree.
     *
     * @param root The root of the subtree to splay.
     * @param key The key to splay on.
     * @return The new root of the splayed subtree.
     */
    private Node splay(Node root, int key) {
        // Base case: root is null or key is present at root
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
                root.left.left = splay(root.left.left, key);
                root = rightRotate(root);
            }
            // Zig-Zag (Left Right)
            else if (key > root.left.key) {
                root.left.right = splay(root.left.right, key);
                if (root.left.right != null) {
                    root.left = leftRotate(root.left);
                }
            }
            
            // Do second rotation for root
            return (root.left == null) ? root : rightRotate(root);

        } else { // Key lies in the right subtree
            // Key is not in tree, we are done
            if (root.right == null) {
                return root;
            }

            // Zig-Zag (Right Left)
            if (key < root.right.key) {
                root.right.left = splay(root.right.left, key);
                if (root.right.left != null) {
                    root.right = rightRotate(root.right);
                }
            }
            // Zig-Zig (Right Right)
            else if (key > root.right.key) {
                root.right.right = splay(root.right.right, key);
                root = leftRotate(root);
            }
            
            // Do second rotation for root
            return (root.right == null) ? root : leftRotate(root);
        }
    }
}