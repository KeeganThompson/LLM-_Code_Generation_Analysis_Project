/**
 * A complete, self-contained implementation of a Splay Tree.
 * This class implements a set of integers.
 */
public class SplayTree {

    /**
     * Represents a node in the Splay Tree.
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
     * Performs a right rotation on the subtree rooted at node x.
     *
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
     * Performs a left rotation on the subtree rooted at node x.
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
     * The main splay operation.
     * Brings the node with the given key (or the last accessed node if the key is not found)
     * to the root of the tree rooted at 'node'.
     * This is a recursive, bottom-up splay implementation.
     *
     * @param node The root of the tree/subtree to splay.
     * @param key The key to search for and bring to the root.
     * @return The new root of the splayed tree.
     */
    private Node splay(Node node, int key) {
        // Base case: node is null or key is present at root
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
                // First recursively bring the key as root of left-left
                node.left.left = splay(node.left.left, key);
                // Do first rotation for node, second rotation is done after else
                node = rightRotate(node);
            }
            // Zig-Zag (Left Right)
            else if (key > node.left.key) {
                // First recursively bring the key as root of left-right
                node.left.right = splay(node.left.right, key);
                // Do first rotation for node.left
                if (node.left.right != null) {
                    node.left = leftRotate(node.left);
                }
            }

            // Do second rotation for node
            return (node.left == null) ? node : rightRotate(node);
        }
        // Key lies in the right subtree
        else {
            // Key is not in the tree, we are done
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
                // Bring the key as root of right-right and do first rotation
                node.right.right = splay(node.right.right, key);
                node = leftRotate(node);
            }

            // Do second rotation for node
            return (node.right == null) ? node : leftRotate(node);
        }
    }

    /**
     * Searches for a key in the tree.
     * If the key is found, it is splayed to the root.
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
     * If the key already exists, the tree is splayed on that key but not modified.
     *
     * @param key The key to insert.
     */
    public void insert(int key) {
        // If tree is empty, create a new root
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

        // The new node becomes the new root. The old root and its subtrees
        // are attached as children of the new root.
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
     * If the key is not found, the tree is splayed on the last accessed node.
     *
     * @param key The key to delete.
     */
    public void delete(int key) {
        if (root == null) {
            return;
        }

        // Splay the tree to bring the node to delete (if it exists) to the root
        root = splay(root, key);

        // If the key is not in the tree, do nothing
        if (root.key != key) {
            return;
        }

        // Now the node to be deleted is the root.
        // We need to join its left and right subtrees.
        Node leftSubtree = root.left;
        Node rightSubtree = root.right;

        if (leftSubtree == null) {
            // If there's no left subtree, the right subtree becomes the new tree
            root = rightSubtree;
        } else {
            // Splay the left subtree to bring its maximum element to its root.
            // This maximum element has no right child.
            leftSubtree = splay(leftSubtree, key); // or splay for a very large key

            // Attach the original right subtree as the right child of the new root.
            leftSubtree.right = rightSubtree;
            root = leftSubtree;
        }
    }
}