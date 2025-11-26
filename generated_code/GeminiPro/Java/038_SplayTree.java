/**
 * A complete, self-contained Java class that implements an integer set using a Splay Tree.
 * A splay tree is a self-adjusting binary search tree with the additional property
 * that recently accessed elements are quick to access again.
 */
public class SplayTree {

    /**
     * Inner class representing a node in the Splay Tree.
     */
    private class Node {
        int key;
        Node left, right;

        public Node(int key) {
            this.key = key;
            this.left = null;
            this.right = null;
        }
    }

    private Node root;

    public SplayTree() {
        this.root = null;
    }

    /**
     * Performs a right rotation on the subtree rooted at y.
     *
     * @param y The root of the subtree to rotate.
     * @return The new root of the subtree after rotation.
     */
    private Node rightRotate(Node y) {
        Node x = y.left;
        y.left = x.right;
        x.right = y;
        return x;
    }

    /**
     * Performs a left rotation on the subtree rooted at x.
     *
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
     * The main splay operation. Brings the node with the given key (or the last
     * accessed node if the key is not found) to the root of the tree.
     *
     * @param node The root of the current subtree.
     * @param key  The key to search for and splay.
     * @return The new root of the tree after splaying.
     */
    private Node splay(Node node, int key) {
        // Base cases: node is null or key is present at root
        if (node == null || node.key == key) {
            return node;
        }

        // Key lies in the left subtree
        if (key < node.key) {
            // Key is not in the tree, we are done
            if (node.left == null) {
                return node;
            }

            // Zig-Zig (Left-Left)
            if (key < node.left.key) {
                // Recursively bring the key as root of left-left
                node.left.left = splay(node.left.left, key);
                // First rotation for node
                node = rightRotate(node);
            }
            // Zig-Zag (Left-Right)
            else if (key > node.left.key) {
                // Recursively bring the key as root of left-right
                node.left.right = splay(node.left.right, key);
                // Do first rotation for node.left
                if (node.left.right != null) {
                    node.left = leftRotate(node.left);
                }
            }

            // Do second rotation for node (if required)
            return (node.left == null) ? node : rightRotate(node);

        } else { // Key lies in the right subtree
            // Key is not in tree, we are done
            if (node.right == null) {
                return node;
            }

            // Zig-Zag (Right-Left)
            if (key < node.right.key) {
                // Recursively bring the key as root of right-left
                node.right.left = splay(node.right.left, key);
                // Do first rotation for node.right
                if (node.right.left != null) {
                    node.right = rightRotate(node.right);
                }
            }
            // Zig-Zig (Right-Right)
            else if (key > node.right.key) {
                // Recursively bring the key as root of right-right
                node.right.right = splay(node.right.right, key);
                // First rotation for node
                node = leftRotate(node);
            }

            // Do second rotation for node (if required)
            return (node.right == null) ? node : leftRotate(node);
        }
    }

    /**
     * Inserts a key into the Splay Tree. If the key already exists,
     * the node is splayed to the root.
     *
     * @param key The integer key to insert.
     */
    public void insert(int key) {
        // If the tree is empty, create a new root
        if (root == null) {
            root = new Node(key);
            return;
        }

        // Splay the tree to bring the closest node to the root
        root = splay(root, key);

        // If key is already present, we are done (it's now the root)
        if (root.key == key) {
            return;
        }

        // Otherwise, create a new node and make it the root
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
     * Searches for a key in the Splay Tree. If the key is found, the corresponding
     * node is splayed to the root.
     *
     * @param key The integer key to search for.
     * @return The key if found, otherwise null.
     */
    public Integer search(int key) {
        root = splay(root, key);

        if (root != null && root.key == key) {
            return key;
        }
        return null;
    }

    /**
     * Deletes a key from the Splay Tree.
     *
     * @param key The integer key to delete.
     */
    public void delete(int key) {
        if (root == null) {
            return;
        }

        // Splay the tree to bring the node to delete (or its parent) to the root
        root = splay(root, key);

        // If the key is not in the tree, do nothing
        if (root.key != key) {
            return;
        }

        // Now, the node to be deleted is the root
        Node leftSubtree = root.left;
        Node rightSubtree = root.right;

        if (leftSubtree == null) {
            // If there's no left child, the right subtree becomes the new tree
            root = rightSubtree;
        } else {
            // Splay the left subtree to bring its maximum element to its root
            // The max element in the left subtree is now the new root of the combined tree
            leftSubtree = splay(leftSubtree, key);

            // Attach the original right subtree to the new root
            leftSubtree.right = rightSubtree;
            root = leftSubtree;
        }
    }
}