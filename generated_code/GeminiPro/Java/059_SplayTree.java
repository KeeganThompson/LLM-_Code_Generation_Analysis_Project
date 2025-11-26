/**
 * A self-contained Java class implementing a Splay Tree for an integer set.
 * A splay tree is a self-balancing binary search tree with the additional
 * property that recently accessed elements are quick to access again.
 * It performs basic operations such as insertion, deletion, and search.
 * After a search or an access, the accessed node is moved to the root of
 * the tree using a series of rotations (splaying).
 */
public class SplayTree {

    /**
     * Inner class representing a node in the splay tree.
     */
    private class Node {
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
     * Constructs an empty SplayTree.
     */
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
        if (x != null) {
            y.left = x.right;
            if (x.right != null) {
                x.right.parent = y;
            }
            x.parent = y.parent;
            if (y.parent == null) {
                this.root = x;
            } else if (y == y.parent.left) {
                y.parent.left = x;
            } else {
                y.parent.right = x;
            }
            x.right = y;
            y.parent = x;
        }
    }

    /**
     * Moves the given node to the root of the tree using splay operations.
     *
     * @param node The node to splay.
     */
    private void splay(Node node) {
        while (node.parent != null) {
            Node parent = node.parent;
            Node grandParent = parent.parent;

            if (grandParent == null) { // Zig case
                if (node == parent.left) {
                    rightRotate(parent);
                } else {
                    leftRotate(parent);
                }
            } else {
                if (node == parent.left) {
                    if (parent == grandParent.left) { // Zig-Zig case
                        rightRotate(grandParent);
                        rightRotate(parent);
                    } else { // Zig-Zag case
                        rightRotate(parent);
                        leftRotate(grandParent);
                    }
                } else {
                    if (parent == grandParent.left) { // Zig-Zag case
                        leftRotate(parent);
                        rightRotate(grandParent);
                    } else { // Zig-Zig case
                        leftRotate(grandParent);
                        leftRotate(parent);
                    }
                }
            }
        }
    }
    
    /**
     * Searches for a key in the tree. If the key is found, the corresponding
     * node is splayed to the root. If not found, the last accessed node on the
     * search path is splayed to the root.
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
                splay(current); // Key found, splay it
                return current.key;
            }
        }
        return null; // Should be unreachable
    }

    /**
     * Inserts a key into the splay tree. If the key already exists, the existing
     * node is splayed to the root. Otherwise, the new node is inserted and then
     * splayed to the root.
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
                // Key already exists, splay the node and return
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
     * The node containing the key is first splayed to the root and then removed.
     * The remaining subtrees are then merged.
     *
     * @param key The integer key to delete.
     */
    public void delete(int key) {
        // Splay the node with the key (or the last accessed node) to the root
        if (search(key) == null) {
             // Key not in tree. search() already splayed the last accessed node.
            return;
        }

        // Now the node to delete is the root
        Node leftSubtree = root.left;
        Node rightSubtree = root.right;

        if (leftSubtree == null) {
            root = rightSubtree;
            if (root != null) {
                root.parent = null;
            }
        } else {
            // Disconnect left subtree
            leftSubtree.parent = null;

            // Find the maximum node in the left subtree
            Node maxInLeft = leftSubtree;
            while (maxInLeft.right != null) {
                maxInLeft = maxInLeft.right;
            }
            
            // Splay the maximum node to the root of the left subtree
            // We can do this by temporarily setting the root to the left subtree's root
            Node originalRoot = this.root;
            this.root = leftSubtree;
            splay(maxInLeft);

            // The new root is maxInLeft. Attach the original right subtree.
            this.root.right = rightSubtree;
            if (rightSubtree != null) {
                rightSubtree.parent = this.root;
            }
        }
    }
}