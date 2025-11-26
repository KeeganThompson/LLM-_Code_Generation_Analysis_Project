/**
 * A complete, self-contained Java class that implements an integer set using a Splay Tree.
 * A splay tree is a self-adjusting binary search tree with the property that
 * recently accessed elements are quick to access again. After a search, insertion,
 * or deletion, the accessed node is moved to the root of the tree through a series of
 * rotations in an operation called "splaying".
 */
public class SplayTree {

    /**
     * Inner class to represent a node in the splay tree.
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

    // Helper function to perform a right rotation on the subtree rooted with y.
    private Node rightRotate(Node y) {
        Node x = y.left;
        y.left = x.right;
        x.right = y;
        return x;
    }

    // Helper function to perform a left rotation on the subtree rooted with x.
    private Node leftRotate(Node x) {
        Node y = x.right;
        x.right = y.left;
        y.left = x;
        return y;
    }

    /**
     * The main splay operation. It brings the node with the given key
     * (or the last accessed node if the key is not present) to the root of the subtree.
     * This is a recursive, bottom-up splaying implementation.
     *
     * @param node The root of the subtree to splay.
     * @param key  The key to splay around.
     * @return The new root of the splayed subtree.
     */
    private Node splay(Node node, int key) {
        // Base case: node is null or key is present at root
        if (node == null || node.key == key) {
            return node;
        }

        // Key lies in the left subtree
        if (key < node.key) {
            // Key is not in the tree, we are done with the search path
            if (node.left == null) {
                return node;
            }

            // Zig-Zig (Left Left)
            if (key < node.left.key) {
                // Recursively bring the key as root of left-left
                node.left.left = splay(node.left.left, key);
                // Do first rotation for node
                node = rightRotate(node);
            }
            // Zig-Zag (Left Right)
            else if (key > node.left.key) {
                // Recursively bring the key as root of left-right
                node.left.right = splay(node.left.right, key);
                // Do first rotation for node.left
                if (node.left.right != null) {
                    node.left = leftRotate(node.left);
                }
            }

            // Do second rotation for node (for both Zig-Zig and Zig-Zag)
            // or the single rotation for Zig
            return (node.left == null) ? node : rightRotate(node);
        }
        // Key lies in the right subtree
        else {
            // Key is not in the tree, we are done with the search path
            if (node.right == null) {
                return node;
            }

            // Zig-Zag (Right Left)
            if (key < node.right.key) {
                // Recursively bring the key as root of right-left
                node.right.left = splay(node.right.left, key);
                // Do first rotation for node.right
                if (node.right.left != null) {
                    node.right = rightRotate(node.right);
                }
            }
            // Zig-Zig (Right Right)
            else if (key > node.right.key) {
                // Recursively bring the key as root of right-right
                node.right.right = splay(node.right.right, key);
                // Do first rotation for node
                node = leftRotate(node);
            }

            // Do second rotation for node (for both Zig-Zig and Zig-Zag)
            // or the single rotation for Zig
            return (node.right == null) ? node : leftRotate(node);
        }
    }

    /**
     * Searches for a key in the tree.
     * This operation performs splaying on the accessed key, moving it (or the last
     * accessed node on the search path) to the root.
     *
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
     * Inserts a key into the splay tree. Duplicates are not allowed.
     * After insertion, the new node becomes the root of the tree.
     *
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

        // If key is already present, do nothing (it's a set)
        if (root.key == key) {
            return;
        }

        Node newNode = new Node(key);

        // If the new key is smaller than the root's key,
        // make the new node the new root. The old root becomes the new root's right child.
        if (key < root.key) {
            newNode.right = root;
            newNode.left = root.left;
            root.left = null;
        }
        // If the new key is greater than the root's key,
        // make the new node the new root. The old root becomes the new root's left child.
        else {
            newNode.left = root;
            newNode.right = root.right;
            root.right = null;
        }
        root = newNode;
    }

    /**
     * Deletes a key from the splay tree.
     *
     * @param key The key to delete.
     */
    public void delete(int key) {
        // If the tree is empty, there is nothing to delete
        if (root == null) {
            return;
        }

        // Splay the tree to bring the node to be deleted (if it exists) to the root
        root = splay(root, key);

        // If the key is not in the tree, do nothing
        if (root.key != key) {
            return;
        }

        // Now, the node to be deleted is the root.
        // We need to merge its left and right subtrees.
        Node leftSubtree = root.left;
        Node rightSubtree = root.right;

        if (leftSubtree == null) {
            // If there's no left subtree, the right subtree becomes the new tree
            root = rightSubtree;
        } else {
            // Splay the left subtree for the key 'key'. This brings the maximum element
            // in the left subtree (the predecessor of 'key') to its root.
            Node newRoot = splay(leftSubtree, key);

            // The new root's right child is guaranteed to be null (as it's the max element).
            // We can now attach the original right subtree there.
            newRoot.right = rightSubtree;
            root = newRoot;
        }
    }
}