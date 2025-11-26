/**
 * A self-contained Java class implementing a Splay Tree for an integer set.
 * A splay tree is a self-balancing binary search tree with the additional
 * property that recently accessed elements are quick to access again.
 * It performs basic operations such as insertion, deletion, and search.
 * After a search or an access, the accessed node is moved to the root of the tree
 * through a series of rotations, which is known as the "splaying" operation.
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
    private void rotateLeft(Node x) {
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
    private void rotateRight(Node y) {
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
     * Performs the splay operation on a node x, moving it to the root.
     *
     * @param x The node to splay.
     */
    private void splay(Node x) {
        if (x == null) {
            return;
        }
        while (x.parent != null) {
            Node parent = x.parent;
            Node grandParent = parent.parent;

            if (grandParent == null) { // Zig step
                if (x == parent.left) {
                    rotateRight(parent);
                } else {
                    rotateLeft(parent);
                }
            } else {
                if (x == parent.left) {
                    if (parent == grandParent.left) { // Zig-Zig step
                        rotateRight(grandParent);
                        rotateRight(parent);
                    } else { // Zig-Zag step
                        rotateRight(parent);
                        rotateLeft(grandParent);
                    }
                } else {
                    if (parent == grandParent.left) { // Zig-Zag step
                        rotateLeft(parent);
                        rotateRight(grandParent);
                    } else { // Zig-Zig step
                        rotateLeft(grandParent);
                        rotateLeft(parent);
                    }
                }
            }
        }
    }

    /**
     * Inserts a key into the splay tree.
     * If the key already exists, the existing node is splayed to the root.
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
                // Key already exists, splay it and return
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
     * Searches for a key in the splay tree.
     * If the key is found, the corresponding node is splayed to the root and the key is returned.
     * If the key is not found, the last accessed node on the search path is splayed to the root and null is returned.
     *
     * @param key The integer key to search for.
     * @return The key if found, otherwise null.
     */
    public Integer search(int key) {
        if (root == null) {
            return null;
        }

        Node current = root;
        Node lastVisited = root;
        
        while (current != null) {
            lastVisited = current;
            if (key < current.key) {
                current = current.left;
            } else if (key > current.key) {
                current = current.right;
            } else {
                splay(current);
                return key;
            }
        }

        // Key not found, splay the last visited node
        splay(lastVisited);
        
        // After splaying, the last visited node is the root.
        // Check if its key matches (it won't, but this is for correctness).
        if (root.key == key) {
             return key;
        }
        return null;
    }

    /**
     * Deletes a key from the splay tree.
     *
     * @param key The integer key to delete.
     */
    public void delete(int key) {
        // First, search for the key. This will bring the node (or its closest neighbor) to the root.
        search(key);

        // If the tree is empty or the key was not found, the root will not have the specified key.
        if (root == null || root.key != key) {
            return;
        }

        // The node to delete is now at the root.
        Node leftSubtree = root.left;
        Node rightSubtree = root.right;

        if (leftSubtree == null) {
            // If there's no left subtree, the right subtree becomes the new tree.
            root = rightSubtree;
            if (root != null) {
                root.parent = null;
            }
        } else {
            // Disconnect the left subtree from the old root.
            leftSubtree.parent = null;
            
            // Find the maximum node in the left subtree.
            Node maxInLeft = leftSubtree;
            while (maxInLeft.right != null) {
                maxInLeft = maxInLeft.right;
            }
            
            // Splay this maximum node to the root of the left subtree.
            // Temporarily set the root to the left subtree to perform the splay operation correctly.
            this.root = leftSubtree;
            splay(maxInLeft);

            // After splaying, `maxInLeft` is the new root. Its right child is guaranteed to be null.
            // Attach the original right subtree as the right child of the new root.
            this.root.right = rightSubtree;
            if (rightSubtree != null) {
                rightSubtree.parent = this.root;
            }
        }
    }
}