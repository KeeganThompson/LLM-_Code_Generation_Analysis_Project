import java.util.NoSuchElementException;

/**
 * A self-contained implementation of a Splay Tree that stores integers.
 * A Splay Tree is a self-balancing binary search tree with the additional
 * property that recently accessed elements are quick to access again.
 * It performs basic operations such as insertion, deletion, and search.
 * When an element is accessed (e.g., through search, insertion, or deletion),
 * the tree is rearranged using a "splaying" operation to move that element to the root.
 */
public class SplayTree {

    /**
     * Represents a node in the Splay Tree.
     */
    private static class Node {
        int key;
        Node parent;
        Node left;
        Node right;

        Node(int key) {
            this.key = key;
            this.parent = null;
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
     * Performs a left rotation on the given node x.
     *
     *    x               y
     *   / \             / \
     *  A   y    -->    x   C
     *     / \         / \
     *    B   C       A   B
     *
     * @param x The node to rotate.
     */
    private void leftRotate(Node x) {
        Node y = x.right;
        if (y != null) {
            x.right = y.left;
            if (y.left != null) {
                y.left.parent = x;
            }
            y.parent = x.parent;
            if (x.parent == null) {
                this.root = y;
            } else if (x == x.parent.left) {
                x.parent.left = y;
            } else {
                x.parent.right = y;
            }
            y.left = x;
            x.parent = y;
        }
    }

    /**
     * Performs a right rotation on the given node x.
     *
     *      y           x
     *     / \         / \
     *    x   C  -->  A   y
     *   / \             / \
     *  A   B           B   C
     *
     * @param x The node to rotate.
     */
    private void rightRotate(Node x) {
        Node y = x.left;
        if (y != null) {
            x.left = y.right;
            if (y.right != null) {
                y.right.parent = x;
            }
            y.parent = x.parent;
            if (x.parent == null) {
                this.root = y;
            } else if (x == x.parent.right) {
                x.parent.right = y;
            } else {
                x.parent.left = y;
            }
            y.right = x;
            x.parent = y;
        }
    }

    /**
     * Performs the splay operation on a node x, moving it to the root.
     * This is the core operation of the Splay Tree that maintains its balance.
     *
     * @param x The node to splay.
     */
    private void splay(Node x) {
        if (x == null) return;
        while (x.parent != null) {
            Node parent = x.parent;
            Node grandParent = parent.parent;

            if (grandParent == null) { // Zig case
                if (x == parent.left) {
                    rightRotate(parent);
                } else {
                    leftRotate(parent);
                }
            } else { // Zig-Zig or Zig-Zag cases
                if (x == parent.left && parent == grandParent.left) { // Zig-Zig (left-left)
                    rightRotate(grandParent);
                    rightRotate(parent);
                } else if (x == parent.right && parent == grandParent.right) { // Zig-Zig (right-right)
                    leftRotate(grandParent);
                    leftRotate(parent);
                } else if (x == parent.right && parent == grandParent.left) { // Zig-Zag (left-right)
                    leftRotate(parent);
                    rightRotate(grandParent);
                } else { // Zig-Zag (right-left)
                    rightRotate(parent);
                    leftRotate(grandParent);
                }
            }
        }
        this.root = x;
    }

    /**
     * Searches for a key in the tree.
     * If the key is found, the node containing the key is splayed to the root
     * and the key is returned. If the key is not found, the last accessed node
     * on the search path is splayed to the root and null is returned.
     *
     * @param key The integer key to search for.
     * @return The key if found, otherwise null.
     */
    public Integer search(int key) {
        if (root == null) {
            return null;
        }

        Node current = root;
        Node lastAccessed = root;

        while (current != null) {
            lastAccessed = current;
            if (key < current.key) {
                current = current.left;
            } else if (key > current.key) {
                current = current.right;
            } else {
                // Key found
                splay(current);
                return current.key;
            }
        }

        // Key not found, splay the last accessed node.
        splay(lastAccessed);
        return null;
    }

    /**
     * Inserts a key into the splay tree.
     * If the key already exists, the node with the key is splayed to the root.
     * If the key does not exist, a new node is created and then splayed to the root.
     *
     * @param key The integer key to insert.
     */
    public void insert(int key) {
        if (root == null) {
            root = new Node(key);
            return;
        }

        Node current = root;
        Node parent = null;
        while (current != null) {
            parent = current;
            if (key < current.key) {
                current = current.left;
            } else if (key > current.key) {
                current = current.right;
            } else {
                // Key already exists, splay the node and return.
                splay(current);
                return;
            }
        }

        Node newNode = new Node(key);
        newNode.parent = parent;
        if (key < parent.key) {
            parent.left = newNode;
        } else {
            parent.right = newNode;
        }

        splay(newNode);
    }

    /**
     * Deletes a key from the splay tree.
     * The node containing the key (or the last accessed node if not found) is
     * first splayed to the root. If the key is at the root, it is removed,
     * and its two subtrees are joined.
     *
     * @param key The integer key to delete.
     */
    public void delete(int key) {
        if (root == null) {
            return;
        }
        
        // Search for the key. This will splay the node (or last accessed) to the root.
        search(key);

        // After search, if the key is in the tree, it's at the root.
        if (root.key != key) {
            return; // Key was not in the tree.
        }

        // Now, delete the root.
        Node leftSubtree = root.left;
        Node rightSubtree = root.right;

        if (leftSubtree == null) {
            root = rightSubtree;
            if (root != null) {
                root.parent = null;
            }
        } else {
            // Make left subtree the main tree temporarily.
            leftSubtree.parent = null;
            
            // Find the maximum node in the left subtree.
            Node maxInLeft = leftSubtree;
            while (maxInLeft.right != null) {
                maxInLeft = maxInLeft.right;
            }
            
            // Splay this maximum node. It will become the new root of the merged tree.
            // Temporarily set the root to perform the splay within the left subtree.
            this.root = leftSubtree;
            splay(maxInLeft);

            // Attach the original right subtree.
            this.root.right = rightSubtree;
            if (rightSubtree != null) {
                rightSubtree.parent = this.root;
            }
        }
    }
}