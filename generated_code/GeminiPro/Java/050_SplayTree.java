/**
 * A complete, self-contained implementation of an integer set using a Splay Tree.
 * Splay trees are self-balancing binary search trees with the additional property
 * that recently accessed elements are quick to access again. This implementation
 * supports insertion, deletion, and search operations.
 */
public class SplayTree {

    /**
     * Represents a node in the Splay Tree.
     * This is a private static inner class to encapsulate the node structure.
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
     * The core splaying operation. It brings the node with the given key
     * (or the last accessed node if the key is not found) to the root of the tree.
     * This is a recursive, bottom-up implementation.
     *
     * @param node The root of the current subtree.
     * @param key The key to splay.
     * @return The new root of the splayed subtree.
     */
    private Node splay(Node node, int key) {
        // Base case: node is null or key is at the root
        if (node == null || node.key == key) {
            return node;
        }

        if (key < node.key) {
            // Key is not in the tree, we are done
            if (node.left == null) {
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
            // Perform the second rotation (or the single Zig rotation)
            return (node.left == null) ? node : rightRotate(node);
        } else { // key > node.key
            // Key is not in the tree, we are done
            if (node.right == null) {
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
            // Perform the second rotation (or the single Zig rotation)
            return (node.right == null) ? node : leftRotate(node);
        }
    }

    /**
     * Searches for a key in the tree.
     * This operation performs a splay on the accessed key, moving it to the root.
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
     * Inserts a key into the Splay Tree.
     * If the key already exists, the tree is splayed on that key, but no new node is added.
     *
     * @param key The key to insert.
     */
    public void insert(int key) {
        if (root == null) {
            root = new Node(key);
            return;
        }

        // Splay the tree on the key. This brings the closest node to the root.
        root = splay(root, key);

        // If the key is already present, we're done.
        if (root.key == key) {
            return;
        }

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
     * If the key is not found, the tree structure is still modified due to the splay operation.
     *
     * @param key The key to delete.
     */
    public void delete(int key) {
        if (root == null) {
            return;
        }

        // Splay the tree on the key.
        root = splay(root, key);

        // If the key is not in the tree, do nothing.
        if (root.key != key) {
            return;
        }

        // The node to be deleted is now at the root.
        Node leftSubtree = root.left;
        Node rightSubtree = root.right;

        if (leftSubtree == null) {
            root = rightSubtree;
        } else {
            // Splay the largest element in the left subtree to its root.
            Node maxNode = leftSubtree;
            while (maxNode.right != null) {
                maxNode = maxNode.right;
            }
            leftSubtree = splay(leftSubtree, maxNode.key);
            
            // The new root of the left subtree has no right child.
            // Attach the original right subtree to it.
            leftSubtree.right = rightSubtree;
            root = leftSubtree;
        }
    }
}