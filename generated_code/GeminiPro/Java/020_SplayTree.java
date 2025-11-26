/**
 * A complete, self-contained Java class that implements an integer set using a Splay Tree.
 * A splay tree is a self-adjusting binary search tree with the additional property
 * that recently accessed elements are quick to access again. All major operations
 * (insertion, deletion, search) involve a "splaying" step, which moves the accessed
 * node to the root of the tree.
 */
public class SplayTree {

    /**
     * Inner class representing a node in the Splay Tree.
     */
    private static class Node {
        int key;
        Node parent;
        Node left;
        Node right;

        /**
         * Constructs a new node with the given key.
         * @param key The integer key for the node.
         */
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
     * This operation is a fundamental building block for the splay operation.
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
     * This operation is a fundamental building block for the splay operation.
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
            } else if (y == y.parent.right) {
                y.parent.right = x;
            } else {
                y.parent.left = x;
            }
            x.right = y;
            y.parent = x;
        }
    }

    /**
     * Performs the splay operation on a node x, moving it to the root of the tree
     * through a series of rotations.
     * @param x The node to splay.
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
                    if (parent == grandParent.left) { // Zig-Zig step
                        rightRotate(grandParent);
                        rightRotate(parent);
                    } else { // Zig-Zag step
                        rightRotate(parent);
                        leftRotate(grandParent);
                    }
                } else {
                    if (parent == grandParent.right) { // Zig-Zig step
                        leftRotate(grandParent);
                        leftRotate(parent);
                    } else { // Zig-Zag step
                        leftRotate(parent);
                        rightRotate(grandParent);
                    }
                }
            }
        }
    }

    /**
     * Searches for a key in the splay tree.
     * If the key is found, the corresponding node is splayed to the root.
     * If the key is not found, the last non-null node on the search path is splayed to the root.
     * @param key The key to search for.
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
                // Key found
                splay(current);
                return current.key;
            }
        }

        // Key not found, splay the last visited node
        splay(lastNode);
        
        return null;
    }
    
    /**
     * Inserts a key into the splay tree.
     * If the key already exists, the node with that key is splayed to the root.
     * Otherwise, a new node is created, inserted, and then splayed to the root.
     * @param key The key to insert.
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
                // Key already exists, splay the node and return as it's a set
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
     * The tree is first searched for the key, which brings the node (or the closest node)
     * to the root. If the key is found at the root, it is removed, and its subtrees
     * are joined.
     * @param key The key to delete.
     */
    public void delete(int key) {
        if (root == null) {
            return;
        }

        // search() will splay the found node or the last accessed node to the root
        search(key);

        // If the key is not at the root after searching, it wasn't in the tree
        if (root.key != key) {
            return;
        }

        // The node to delete is now the root
        Node leftSubtree = root.left;
        Node rightSubtree = root.right;

        if (leftSubtree == null) {
            root = rightSubtree;
            if (root != null) {
                root.parent = null;
            }
        } else {
            // Detach the left subtree to operate on it
            leftSubtree.parent = null;

            // Find the maximum node in the left subtree
            Node maxNode = leftSubtree;
            while (maxNode.right != null) {
                maxNode = maxNode.right;
            }

            // Temporarily make the left subtree the main tree to splay within it
            this.root = leftSubtree;
            splay(maxNode); // maxNode becomes the new root of this subtree

            // Attach the original right subtree
            root.right = rightSubtree;
            if (rightSubtree != null) {
                rightSubtree.parent = root;
            }
        }
    }
}