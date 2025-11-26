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
     * <pre>
     *    x           y
     *   / \         / \
     *  A   y  -->  x   C
     *     / \     / \
     *    B   C   A   B
     * </pre>
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
     * <pre>
     *      y           x
     *     / \         / \
     *    x   C  -->  A   y
     *   / \             / \
     *  A   B           B   C
     * </pre>
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
            } else if (x == x.parent.left) {
                x.parent.left = y;
            } else {
                x.parent.right = y;
            }
            y.right = x;
            x.parent = y;
        }
    }

    /**
     * The main splay operation. Moves the given node x to the root of the tree
     * through a series of rotations (Zig, Zig-Zig, or Zig-Zag).
     *
     * @param x The node to splay.
     */
    private void splay(Node x) {
        while (x.parent != null) {
            Node parent = x.parent;
            Node grandParent = parent.parent;

            if (grandParent == null) { // Zig case
                if (x == parent.left) {
                    rightRotate(parent);
                } else {
                    leftRotate(parent);
                }
            } else {
                if (x == parent.left) {
                    if (parent == grandParent.left) { // Zig-Zig case (left-left)
                        rightRotate(grandParent);
                        rightRotate(parent);
                    } else { // Zig-Zag case (right-left)
                        rightRotate(parent);
                        leftRotate(grandParent);
                    }
                } else { // x is the right child
                    if (parent == grandParent.left) { // Zig-Zag case (left-right)
                        leftRotate(parent);
                        rightRotate(grandParent);
                    } else { // Zig-Zig case (right-right)
                        leftRotate(grandParent);
                        leftRotate(parent);
                    }
                }
            }
        }
    }

    /**
     * Inserts a key into the splay tree.
     * If the key already exists, the node with that key is splayed to the root.
     * Otherwise, a new node is created, inserted, and then splayed to the root.
     *
     * @param key The integer key to insert.
     */
    public void insert(int key) {
        if (root == null) {
            root = new Node(key);
            return;
        }

        // 1. Find the closest node to the key and splay it.
        Node current = root;
        Node parent = null;
        while (current != null) {
            parent = current;
            if (key < current.key) {
                current = current.left;
            } else if (key > current.key) {
                current = current.right;
            } else {
                // Key already exists, splay it and we are done.
                splay(current);
                return;
            }
        }

        splay(parent);

        // After splaying, the root is the node closest to the key.
        // We can now insert the new key by splitting the tree.
        Node newNode = new Node(key);
        if (key < root.key) {
            newNode.right = root;
            newNode.left = root.left;
            root.left = null;
            if (newNode.left != null) {
                newNode.left.parent = newNode;
            }
        } else { // key > root.key
            newNode.left = root;
            newNode.right = root.right;
            root.right = null;
            if (newNode.right != null) {
                newNode.right.parent = newNode;
            }
        }
        root.parent = newNode;
        root = newNode;
    }

    /**
     * Searches for a key in the splay tree.
     * If the key is found, the corresponding node is splayed to the root, and the key is returned.
     * If the key is not found, the last accessed node on the search path is splayed to the root,
     * and null is returned.
     *
     * @param key The integer key to search for.
     * @return The key if found, otherwise null.
     */
    public Integer search(int key) {
        if (root == null) {
            return null;
        }

        Node current = root;
        while (current != null) {
            if (key < current.key) {
                if (current.left == null) {
                    splay(current); // Key not found, splay last accessed node
                    return null;
                }
                current = current.left;
            } else if (key > current.key) {
                if (current.right == null) {
                    splay(current); // Key not found, splay last accessed node
                    return null;
                }
                current = current.right;
            } else {
                splay(current); // Key found, splay the node
                return current.key;
            }
        }
        return null; // Should not be reached if root is not null
    }

    /**
     * Deletes a key from the splay tree.
     * The tree is first searched for the key, which brings the node (or its closest neighbor)
     * to the root. If the key is at the root, it is deleted and its subtrees are joined.
     *
     * @param key The integer key to delete.
     */
    public void delete(int key) {
        if (root == null) {
            return;
        }

        // Search for the key, splaying the accessed node to the root.
        search(key);

        // If the key is not at the root after the search, it was not in the tree.
        if (root.key != key) {
            return;
        }

        // The node to delete is now the root.
        Node leftSubtree = root.left;
        Node rightSubtree = root.right;

        if (leftSubtree == null) {
            root = rightSubtree;
            if (root != null) {
                root.parent = null;
            }
        } else {
            // Detach the left subtree from the root.
            leftSubtree.parent = null;

            // Find the maximum node in the left subtree.
            Node maxInLeft = leftSubtree;
            while (maxInLeft.right != null) {
                maxInLeft = maxInLeft.right;
            }

            // Make the left subtree the main tree temporarily and splay its max node.
            // This makes the max node the new root of the combined left subtree.
            root = leftSubtree;
            splay(maxInLeft);

            // Attach the original right subtree to the new root.
            // Since it was the max, the new root has no right child.
            root.right = rightSubtree;
            if (rightSubtree != null) {
                rightSubtree.parent = root;
            }
        }
    }
}