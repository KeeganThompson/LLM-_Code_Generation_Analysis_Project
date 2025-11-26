/**
 * A complete, self-contained Java class that implements an integer set using a Splay Tree.
 * A splay tree is a self-adjusting binary search tree with the additional property
 * that recently accessed elements are quick to access again. All major operations
 * (insert, delete, search) perform a "splaying" operation, which moves the accessed

 * (or inserted/deleted) node to the root of the tree.
 */
public class SplayTree {

    /**
     * Inner class representing a node in the Splay Tree.
     * It includes a parent pointer to facilitate the rotation operations.
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

    public SplayTree() {
        this.root = null;
    }

    /**
     * Performs a left rotation on the given node x.
     *
     *      x               y
     *     / \             / \
     *    A   y    -->    x   C
     *       / \         / \
     *      B   C       A   B
     *
     * @param x The node to rotate.
     */
    private void leftRotate(Node x) {
        Node y = x.right;
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

    /**
     * Performs a right rotation on the given node y.
     *
     *        y           x
     *       / \         / \
     *      x   C  -->  A   y
     *     / \             / \
     *    A   B           B   C
     *
     * @param y The node to rotate.
     */
    private void rightRotate(Node y) {
        Node x = y.left;
        y.left = x.right;
        if (x.right != null) {
            x.right.parent = y;
        }
        x.parent = y.parent;
        if (y.parent == null) {
            this.root = x;
        } else if (y == y.parent.right) {
            y.parent.right = x;
        } else {
            y.parent.left = x;
        }
        x.right = y;
        y.parent = x;
    }

    /**
     * Performs the splay operation on a node, moving it to the root.
     * The splay operation consists of a sequence of rotations (Zig, Zig-Zig, Zig-Zag).
     *
     * @param x The node to splay to the root.
     */
    private void splay(Node x) {
        while (x.parent != null) {
            Node parent = x.parent;
            Node grandParent = parent.parent;

            if (grandParent == null) { // Zig step
                if (x == parent.left) {
                    rightRotate(parent);
                } else {
                    leftRotate(parent);
                }
            } else {
                if (x == parent.left) {
                    if (parent == grandParent.left) { // Zig-Zig step (Left-Left)
                        rightRotate(grandParent);
                        rightRotate(parent);
                    } else { // Zig-Zag step (Right-Left)
                        rightRotate(parent);
                        leftRotate(grandParent);
                    }
                } else { // x is the right child
                    if (parent == grandParent.left) { // Zig-Zag step (Left-Right)
                        leftRotate(parent);
                        rightRotate(grandParent);
                    } else { // Zig-Zig step (Right-Right)
                        leftRotate(grandParent);
                        leftRotate(parent);
                    }
                }
            }
        }
    }

    /**
     * Searches for a key in the tree.
     * If the key is found, the node containing the key is splayed to the root
     * and the key is returned. If the key is not found, the last accessed node
     * before the search failed is splayed to the root, and null is returned.
     *
     * @param key The integer key to search for.
     * @return The key if found, otherwise null.
     */
    public Integer search(int key) {
        if (root == null) {
            return null;
        }

        Node current = root;
        Node lastNode = root;

        while (current != null) {
            lastNode = current;
            if (key < current.key) {
                current = current.left;
            } else if (key > current.key) {
                current = current.right;
            } else {
                // Key found, splay the node and return the key
                splay(current);
                return current.key;
            }
        }

        // Key not found, splay the last accessed node
        splay(lastNode);
        return null;
    }

    /**
     * Inserts a key into the splay tree.
     * If the key already exists, the node with that key is splayed to the root.
     * If the key does not exist, a new node is created, inserted, and then
     * splayed to the root.
     *
     * @param key The integer key to insert.
     */
    public void insert(int key) {
        Node node = root;
        Node parent = null;

        // 1. Find position for new node (standard BST insert)
        while (node != null) {
            parent = node;
            if (key < node.key) {
                node = node.left;
            } else if (key > node.key) {
                node = node.right;
            } else {
                // Key already exists, splay the node and we are done
                splay(node);
                return;
            }
        }

        // 2. Insert the new node
        Node newNode = new Node(key);
        newNode.parent = parent;

        if (parent == null) {
            root = newNode; // Tree was empty
        } else if (key < parent.key) {
            parent.left = newNode;
        } else {
            parent.right = newNode;
        }

        // 3. Splay the newly inserted node to the root
        splay(newNode);
    }

    /**
     * Deletes a key from the splay tree.
     * The deletion process involves splaying the node to the root, then removing it
     * and joining the remaining two subtrees.
     *
     * @param key The integer key to delete.
     */
    public void delete(int key) {
        // First, search for the key. This will splay the node (or its closest neighbor)
        // to the root.
        search(key);

        // If the key was not found, the new root's key will not match.
        if (root == null || root.key != key) {
            return; // Key not in tree, nothing to delete.
        }

        // Now, the node to delete is the root.
        Node leftSubtree = root.left;
        Node rightSubtree = root.right;

        if (leftSubtree == null) {
            // No left child, the right subtree becomes the new tree.
            root = rightSubtree;
            if (root != null) {
                root.parent = null;
            }
        } else {
            // Disconnect the left subtree.
            leftSubtree.parent = null;

            // Find the maximum node in the left subtree.
            Node maxNode = leftSubtree;
            while (maxNode.right != null) {
                maxNode = maxNode.right;
            }

            // Make the left subtree the current tree and splay its max node.
            // This makes the max node the new root of the combined tree.
            root = leftSubtree;
            splay(maxNode);

            // The new root (maxNode) has no right child, so we can attach
            // the original right subtree there.
            root.right = rightSubtree;
            if (rightSubtree != null) {
                rightSubtree.parent = root;
            }
        }
    }
}