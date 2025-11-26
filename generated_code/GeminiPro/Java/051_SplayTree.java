/**
 * A self-contained Java class implementing a Splay Tree for an integer set.
 * Splay trees are self-balancing binary search trees with the additional property
 * that recently accessed elements are quick to access again.
 */
public class SplayTree {

    /**
     * Represents a node in the Splay Tree.
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

    /**
     * Performs a right rotation on the subtree rooted at node x.
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
     * Performs a left rotation on the subtree rooted at node y.
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
     * The core splaying operation. It brings the node with the given key to the root.
     * If the key is not present, the last accessed node is brought to the root.
     * This operation modifies the tree structure.
     *
     * @param node The root of the current subtree.
     * @param key The key to splay towards the root.
     * @return The new root of the splayed subtree.
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

            // Do second rotation for both Zig-Zig and Zig-Zag
            return (node.left == null) ? node : rightRotate(node);
        }
        // Key lies in the right subtree
        else {
            // Key is not in tree, we are done
            if (node.right == null) {
                return node;
            }

            // Zig-Zag (Right Left)
            if (key < node.right.key) {
                // Bring the key as root of right-left
                node.right.left = splay(node.right.left, key);
                // Do first rotation for node.right
                if (node.right.left != null) {
                    node.right = rightRotate(node.right);
                }
            }
            // Zig-Zig (Right Right)
            else if (key > node.right.key) {
                // Bring the key as root of right-right
                node.right.right = splay(node.right.right, key);
                // Do first rotation for node
                node = leftRotate(node);
            }

            // Do second rotation for Zig-Zig and Zig-Zag
            return (node.right == null) ? node : leftRotate(node);
        }
    }

    /**
     * Inserts a key into the splay tree. If the key already exists, the tree remains unchanged.
     * After insertion, the new node becomes the root of the tree.
     *
     * @param key The key to insert.
     */
    public void insert(int key) {
        // If the tree is empty
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

        // The new node becomes the new root. The old root becomes a child.
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
     * Searches for a key in the tree and performs the splaying operation on the accessed node.
     * This moves the found node (or the last node on the search path) to the root.
     *
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
     * Deletes a key from the splay tree.
     *
     * @param key The key to delete.
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

        // Now, the node to delete is the root. We need to join its subtrees.
        Node leftSubtree = root.left;
        Node rightSubtree = root.right;

        if (leftSubtree == null) {
            root = rightSubtree;
        } else {
            // Splay the left subtree to bring its largest element (the predecessor of the deleted key) to its root.
            leftSubtree = splay(leftSubtree, key);

            // The new root of the left subtree (the predecessor) has no right child.
            // We can safely attach the original right subtree there.
            leftSubtree.right = rightSubtree;
            root = leftSubtree;
        }
    }
}