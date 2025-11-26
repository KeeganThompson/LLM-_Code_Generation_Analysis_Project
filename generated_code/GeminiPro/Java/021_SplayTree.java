/**
 * A complete, self-contained Java class that implements an integer set using a Splay Tree.
 * A splay tree is a self-adjusting binary search tree with the additional property
 * that recently accessed elements are quick to access again. All major operations
 * (insert, delete, search) perform a "splay" operation, which moves the accessed
 * (or inserted/deleted) node to the root of the tree, restructuring it along the way.
 */
public class SplayTree {

    private Node root;

    /**
     * Inner static class to represent a node in the tree.
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
     * The main splay operation.
     * Brings the node with the given key (or the last accessed node on the search path)
     * to the root of the tree using a series of rotations.
     * @param currentRoot The root of the subtree to splay.
     * @param key The key to splay for.
     * @return The new root of the splayed subtree.
     */
    private Node splay(Node currentRoot, int key) {
        // Base case: root is null or key is present at root
        if (currentRoot == null || currentRoot.key == key) {
            return currentRoot;
        }

        // Key lies in the left subtree
        if (key < currentRoot.key) {
            // Key is not in tree, we are done
            if (currentRoot.left == null) {
                return currentRoot;
            }

            // Zig-Zig (Left Left)
            if (key < currentRoot.left.key) {
                // Recursively bring the key as root of left-left
                currentRoot.left.left = splay(currentRoot.left.left, key);
                // First rotation for root
                currentRoot = rightRotate(currentRoot);
            }
            // Zig-Zag (Left Right)
            else if (key > currentRoot.left.key) {
                // Recursively bring the key as root of left-right
                currentRoot.left.right = splay(currentRoot.left.right, key);
                // First rotation for root.left
                if (currentRoot.left.right != null) {
                    currentRoot.left = leftRotate(currentRoot.left);
                }
            }

            // Second rotation for root
            return (currentRoot.left == null) ? currentRoot : rightRotate(currentRoot);

        } else { // Key lies in the right subtree
            // Key is not in tree, we are done
            if (currentRoot.right == null) {
                return currentRoot;
            }

            // Zig-Zag (Right Left)
            if (key < currentRoot.right.key) {
                // Recursively bring the key as root of right-left
                currentRoot.right.left = splay(currentRoot.right.left, key);
                // First rotation for root.right
                if (currentRoot.right.left != null) {
                    currentRoot.right = rightRotate(currentRoot.right);
                }
            }
            // Zig-Zig (Right Right)
            else if (key > currentRoot.right.key) {
                // Recursively bring the key as root of right-right
                currentRoot.right.right = splay(currentRoot.right.right, key);
                // First rotation for root
                currentRoot = leftRotate(currentRoot);
            }

            // Second rotation for root
            return (currentRoot.right == null) ? currentRoot : leftRotate(currentRoot);
        }
    }

    /**
     * Inserts a key into the splay tree.
     * If the key already exists, the tree remains unchanged, but the existing node is splayed to the root.
     * After insertion of a new key, the new node becomes the root of the tree.
     * @param key The key to insert.
     */
    public void insert(int key) {
        // If the tree is empty, create a new root
        if (root == null) {
            root = new Node(key);
            return;
        }

        // Splay the tree to bring the closest node to the root
        root = splay(root, key);

        // If key is already present, do nothing
        if (root.key == key) {
            return;
        }

        Node newNode = new Node(key);

        // If the new key is smaller than the root's key, the new node becomes the new root.
        // The old root becomes the right child of the new node.
        if (key < root.key) {
            newNode.right = root;
            newNode.left = root.left;
            root.left = null;
        } else { // If the new key is larger than the root's key
            newNode.left = root;
            newNode.right = root.right;
            root.right = null;
        }
        root = newNode;
    }

    /**
     * Searches for a key in the splay tree.
     * This operation performs splaying. If the key is found, the node with the key
     * becomes the new root. If the key is not found, the last accessed node on the
     * search path becomes the new root.
     * @param key The key to search for.
     * @return The key as an Integer object if found, otherwise null.
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
     * If the key is not in the tree, the tree is splayed on the last accessed node and remains otherwise unchanged.
     * If the key is found and deleted, the new root will be the predecessor of the deleted key.
     * @param key The key to delete.
     */
    public void delete(int key) {
        // If tree is empty
        if (root == null) {
            return;
        }

        // Splay the tree for the key
        root = splay(root, key);

        // If the key is not in the tree, do nothing more
        if (root.key != key) {
            return;
        }

        // The node to be deleted is now the root.
        // We need to merge its left and right subtrees.
        Node leftSubtree = root.left;
        Node rightSubtree = root.right;

        if (leftSubtree == null) {
            // If there's no left subtree, the right subtree becomes the new tree
            root = rightSubtree;
        } else {
            // Splay the left subtree to bring its largest element (the predecessor of the deleted key) to its root.
            // Splaying for the deleted key `key` in the left subtree will achieve this.
            leftSubtree = splay(leftSubtree, key);
            
            // Attach the original right subtree as the right child of the new root (the predecessor).
            leftSubtree.right = rightSubtree;
            root = leftSubtree;
        }
    }
}