import java.util.NoSuchElementException;

/**
 * A self-contained Java class implementing an integer set using a Splay Tree.
 * A splay tree is a self-balancing binary search tree with the additional
 * property that recently accessed elements are quick to access again.
 * It performs basic operations such as insertion, deletion, and search.
 * After a search, insert, or delete operation, the accessed node is moved
 * to the root of the tree (splayed).
 */
public class SplayTree {

    private Node root;

    /**
     * Represents a node in the Splay Tree.
     */
    private static class Node {
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

    /**
     * Constructs an empty Splay Tree.
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
     * The main splay operation. Brings the node with the given key (or the last
     * accessed node if the key is not found) to the root of the subtree.
     * @param root The root of the subtree.
     * @param key The key to splay.
     * @return The new root of the subtree after splaying.
     */
    private Node splay(Node root, int key) {
        // Base case: root is null or key is present at root
        if (root == null || root.key == key) {
            return root;
        }

        // Key lies in the left subtree
        if (key < root.key) {
            // Key is not in the tree, we are done
            if (root.left == null) {
                return root;
            }

            // Zig-Zig (Left Left)
            if (key < root.left.key) {
                // Recursively bring the key as root of left-left
                root.left.left = splay(root.left.left, key);
                // Do first rotation for root
                root = rightRotate(root);
            }
            // Zig-Zag (Left Right)
            else if (key > root.left.key) {
                // Recursively bring the key as root of left-right
                root.left.right = splay(root.left.right, key);
                // Do first rotation for root.left
                if (root.left.right != null) {
                    root.left = leftRotate(root.left);
                }
            }

            // Do second rotation for root
            return (root.left == null) ? root : rightRotate(root);
        }
        // Key lies in the right subtree
        else { // key > root.key
            // Key is not in the tree, we are done
            if (root.right == null) {
                return root;
            }

            // Zig-Zag (Right Left)
            if (key < root.right.key) {
                // Recursively bring the key as root of right-left
                root.right.left = splay(root.right.left, key);
                // Do first rotation for root.right
                if (root.right.left != null) {
                    root.right = rightRotate(root.right);
                }
            }
            // Zig-Zig (Right Right)
            else if (key > root.right.key) {
                // Recursively bring the key as root of right-right
                root.right.right = splay(root.right.right, key);
                // Do first rotation for root
                root = leftRotate(root);
            }

            // Do second rotation for root
            return (root.right == null) ? root : leftRotate(root);
        }
    }

    /**
     * Searches for a key in the tree.
     * The accessed node (if found) or the last accessed node on the search path
     * is splayed to the root.
     *
     * @param key The key to search for.
     * @return The key if found, otherwise null.
     */
    public Integer search(int key) {
        this.root = splay(this.root, key);
        if (this.root != null && this.root.key == key) {
            return key;
        }
        return null;
    }

    /**
     * Inserts a key into the splay tree. Duplicates are not allowed.
     * The newly inserted node (or the existing node if it's a duplicate)
     * becomes the new root of the tree.
     *
     * @param key The key to insert.
     */
    public void insert(int key) {
        // If the tree is empty
        if (root == null) {
            root = new Node(key);
            return;
        }

        // Splay the tree for the key. This brings the closest node to the root.
        root = splay(root, key);

        // If key is already present, then return (no duplicates)
        if (root.key == key) {
            return;
        }

        Node newNode = new Node(key);

        // If new key is smaller than root's key, make new node the new root
        if (key < root.key) {
            newNode.right = root;
            newNode.left = root.left;
            root.left = null;
        }
        // If new key is greater than root's key, make new node the new root
        else { // key > root.key
            newNode.left = root;
            newNode.right = root.right;
            root.right = null;
        }
        root = newNode;
    }

    /**
     * Deletes a key from the splay tree.
     * If the key is found and deleted, the parent of the deleted node is splayed to the root.
     * If the key is not found, the tree remains unchanged, but the last accessed node
     * during the search is splayed to the root.
     *
     * @param key The key to delete.
     */
    public void delete(int key) {
        // If tree is empty
        if (root == null) {
            return;
        }

        // Splay the given key to the root
        root = splay(root, key);

        // If key is not present in the tree
        if (root.key != key) {
            return;
        }

        // Now, the node to be deleted is at the root.
        Node leftSubtree = root.left;
        Node rightSubtree = root.right;

        if (leftSubtree == null) {
            // If left subtree is null, the new root is the right subtree
            root = rightSubtree;
        } else {
            // Make the left subtree the new tree
            // Splay the largest element in the left subtree to its root.
            // This largest element will become the new root of the combined tree.
            Node maxNode = leftSubtree;
            while (maxNode.right != null) {
                maxNode = maxNode.right;
            }
            // Splay this max node to the root of the (now separated) left subtree
            leftSubtree = splay(leftSubtree, maxNode.key);

            // Attach the original right subtree to the new root's right
            leftSubtree.right = rightSubtree;
            root = leftSubtree;
        }
    }
}