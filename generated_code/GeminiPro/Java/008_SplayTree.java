/**
 * A complete, self-contained Java class that implements an integer set using a Splay Tree.
 * A splay tree is a self-adjusting binary search tree with the additional
 * property that recently accessed elements are quick to access again.
 * It performs basic operations such as insertion, deletion, and search.
 * After a search, insert, or delete operation, the accessed node is moved
 * to the root of the tree (an operation called "splaying").
 */
public class SplayTree {

    /**
     * Represents a node in the Splay Tree.
     * It is a private static inner class as it is tightly coupled with the SplayTree
     * and does not need access to SplayTree's instance members.
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
     * Performs a right rotation on the given node y.
     *
     *      y           x
     *     / \         / \
     *    x   T3  ->  T1  y
     *   / \             / \
     *  T1  T2          T2  T3
     *
     * @param y The node to rotate.
     * @return The new root of the rotated subtree.
     */
    private Node rightRotate(Node y) {
        Node x = y.left;
        y.left = x.right;
        x.right = y;
        return x;
    }

    /**
     * Performs a left rotation on the given node x.
     *
     *    x             y
     *   / \           / \
     *  T1  y   ->    x   T3
     *     / \       / \
     *    T2  T3    T1  T2
     *
     * @param x The node to rotate.
     * @return The new root of the rotated subtree.
     */
    private Node leftRotate(Node x) {
        Node y = x.right;
        x.right = y.left;
        y.left = x;
        return y;
    }

    /**
     * The main splaying operation. It brings the node with the given key
     * (or the last accessed node if the key is not found) to the root of the tree.
     * This is a recursive, bottom-up splay implementation.
     *
     * @param node The root of the subtree to splay.
     * @param key The key to search for and bring to the root.
     * @return The new root of the splayed subtree.
     */
    private Node splay(Node node, int key) {
        // Base case: node is null or key is at root
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
            // Do second rotation for root
            return (node.left == null) ? node : rightRotate(node);
        }
        // Key lies in the right subtree
        else {
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
            // Do second rotation for root
            return (node.right == null) ? node : leftRotate(node);
        }
    }

    /**
     * Searches for a key in the tree. If the key is found, it is splayed
     * to the root. If not found, the last accessed node is splayed to the root.
     *
     * @param key The key to search for.
     * @return The key as an Integer object if found, otherwise null.
     */
    public Integer search(int key) {
        if (root == null) {
            return null;
        }
        root = splay(root, key);
        // After splaying, if the key exists, it will be at the root.
        if (root.key == key) {
            return key;
        }
        return null;
    }

    /**
     * Inserts a key into the splay tree. If the key already exists,
     * the tree is splayed on that key but not modified, maintaining the set property.
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
     * Deletes a key from the splay tree. If the key is not found,
     * the tree is splayed on the last accessed node, but no deletion occurs.
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

        // Now, the node to delete is the root. We need to merge its two subtrees.
        Node leftSubtree = root.left;
        Node rightSubtree = root.right;

        if (leftSubtree == null) {
            // If there's no left subtree, the right subtree becomes the new tree
            root = rightSubtree;
        } else {
            // Make the left subtree the new tree
            root = leftSubtree;
            
            // Find the maximum element in the new tree (the rightmost node of the left subtree)
            // and splay it to the root of this new tree.
            Node maxNode = root;
            while (maxNode.right != null) {
                maxNode = maxNode.right;
            }
            root = splay(root, maxNode.key);

            // After splaying, the new root (the max element from the left subtree)
            // has no right child. We can now attach the original right subtree there.
            root.right = rightSubtree;
        }
    }
}