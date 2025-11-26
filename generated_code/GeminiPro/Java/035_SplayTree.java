/**
 * A complete, self-contained Java class that implements an integer set using a Splay Tree.
 * Splay trees are self-balancing binary search trees with the additional property that
 * recently accessed elements are quick to access again. The splay operation moves an
 * accessed element to the root of the tree.
 */
public class SplayTree {

    /**
     * Represents a node in the splay tree.
     */
    private class Node {
        int key;
        Node left, right;

        /**
         * Constructs a node with the given key.
         * @param key The integer key for the node.
         */
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
     * Performs the top-down splay operation. It brings the node with the given key
     * (or the last accessed node on the search path if the key is not found)
     * to the root of the tree.
     *
     * @param node The root of the tree/subtree to splay.
     * @param key The key to splay for.
     * @return The new root of the splayed tree.
     */
    private Node splay(Node node, int key) {
        if (node == null) {
            return null;
        }

        // Dummy node to act as a header for the left and right subtrees being built.
        // The key in the dummy node is irrelevant.
        Node dummy = new Node(0);
        Node leftTree = dummy;
        Node rightTree = dummy;

        while (true) {
            if (key < node.key) {
                if (node.left == null) {
                    break;
                }
                // Zig-Zig case (right rotation)
                if (key < node.left.key) {
                    node = rightRotate(node);
                    if (node.left == null) {
                        break;
                    }
                }
                // Link current root to the right tree
                rightTree.left = node;
                rightTree = node;
                node = node.left;
            } else if (key > node.key) {
                if (node.right == null) {
                    break;
                }
                // Zig-Zig case (left rotation)
                if (key > node.right.key) {
                    node = leftRotate(node);
                    if (node.right == null) {
                        break;
                    }
                }
                // Link current root to the left tree
                leftTree.right = node;
                leftTree = node;
                node = node.right;
            } else {
                // Key found
                break;
            }
        }

        // Reassemble the tree
        leftTree.right = node.left;
        rightTree.left = node.right;
        node.left = dummy.right;
        node.right = dummy.left;

        return node;
    }

    /**
     * Inserts a key into the splay tree.
     * If the key already exists, the tree remains unchanged but the existing node is splayed.
     * After insertion of a new key, the new node becomes the root of the tree.
     *
     * @param key The integer key to insert.
     */
    public void insert(int key) {
        if (root == null) {
            root = new Node(key);
            return;
        }

        // Splay the tree around the key. The closest node becomes the root.
        root = splay(root, key);

        // If key is already present, do nothing more.
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
     * Searches for a key in the splay tree.
     * This operation performs splaying. If the key is found, it is splayed to the root.
     * If not found, the last accessed node on the search path is splayed to the root.
     *
     * @param key The integer key to search for.
     * @return The key if found, otherwise null.
     */
    public Integer search(int key) {
        if (root == null) {
            return null;
        }
        root = splay(root, key);
        if (root.key == key) {
            return root.key;
        }
        return null;
    }

    /**
     * Deletes a key from the splay tree.
     * If the key is not in the tree, the tree is splayed around the key's would-be position
     * but remains structurally unchanged regarding its elements.
     *
     * @param key The integer key to delete.
     */
    public void delete(int key) {
        if (root == null) {
            return;
        }

        // Splay the key to the root.
        root = splay(root, key);

        // If the key is not at the root after splaying, it wasn't in the tree.
        if (root.key != key) {
            return;
        }

        // The node to delete is now the root.
        Node leftSubtree = root.left;
        Node rightSubtree = root.right;

        if (leftSubtree == null) {
            root = rightSubtree;
        } else {
            // Find the maximum element in the left subtree by splaying for a large value.
            // This makes the maximum element the new root of the left subtree.
            leftSubtree = splay(leftSubtree, Integer.MAX_VALUE);
            
            // The new root of the left subtree (the max element) now has no right child.
            // Attach the original right subtree to it.
            leftSubtree.right = rightSubtree;
            root = leftSubtree;
        }
    }
}