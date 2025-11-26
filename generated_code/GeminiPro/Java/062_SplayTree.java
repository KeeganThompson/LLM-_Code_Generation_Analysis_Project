/**
 * A self-contained Java class implementing a Splay Tree for an integer set.
 * A Splay Tree is a self-adjusting binary search tree with the additional
 * property that recently accessed elements are quick to access again.
 * It performs basic operations such as insertion, deletion, and search.
 * Its performance is amortized O(log n) per operation.
 */
public class SplayTree {

    /**
     * Inner class representing a node in the Splay Tree.
     * It holds the integer key and references to its parent, left child, and right child.
     */
    private class Node {
        int key;
        Node parent;
        Node left;
        Node right;

        /**
         * Constructs a new node with the given key.
         * @param key The integer key for the node.
         */
        public Node(int key) {
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

    // ------------------ Public API Methods ------------------

    /**
     * Inserts a key into the Splay Tree.
     * If the key already exists, the existing node is splayed to the root.
     * If the key does not exist, a new node is created, inserted, and then splayed to the root.
     *
     * @param key The integer key to insert.
     */
    public void insert(int key) {
        Node current = this.root;
        Node parent = null;

        // 1. Find the position for the new node (standard BST insert)
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

        // 2. Create and link the new node
        Node newNode = new Node(key);
        newNode.parent = parent;
        if (parent == null) {
            this.root = newNode; // The tree was empty
        } else if (key < parent.key) {
            parent.left = newNode;
        } else {
            parent.right = newNode;
        }

        // 3. Splay the newly inserted node to the root
        splay(newNode);
    }

    /**
     * Searches for a key in the Splay Tree.
     * If the key is found, the corresponding node is splayed to the root and the key is returned.
     * If the key is not found, the last accessed node in the search path is splayed to the root and null is returned.
     *
     * @param key The integer key to search for.
     * @return The key if found, otherwise null.
     */
    public Integer search(int key) {
        Node resultNode = findNode(key);
        if (resultNode != null) {
            splay(resultNode);
            // After splaying, check if the root has the key
            if (this.root.key == key) {
                return this.root.key;
            }
        }
        return null;
    }



    /**
     * Deletes a key from the Splay Tree.
     * The tree is first searched for the key, which brings the node (or a nearby one) to the root.
     * If the key is found at the root, it is removed, and its subtrees are joined.
     *
     * @param key The integer key to delete.
     */
    public void delete(int key) {
        // Search for the key, splaying the accessed node to the root.
        search(key);

        // If the key is not in the tree, the root will not have the key after the search.
        if (root == null || root.key != key) {
            return; // Key not found, nothing to delete.
        }

        // Now, the node to delete is the root.
        Node leftSubtree = root.left;
        Node rightSubtree = root.right;

        if (leftSubtree == null) {
            // If there's no left subtree, the right subtree becomes the new tree.
            this.root = rightSubtree;
            if (rightSubtree != null) {
                rightSubtree.parent = null;
            }
        } else {
            // Disconnect the left subtree from the old root.
            leftSubtree.parent = null;

            // Find the maximum node in the left subtree.
            Node maxInLeft = leftSubtree;
            while (maxInLeft.right != null) {
                maxInLeft = maxInLeft.right;
            }

            // Splay this maximum node to the root of the (now separate) left subtree.
            splay(maxInLeft);

            // The new root (maxInLeft) now has the rest of the left subtree as its left child.
            // Its right child is guaranteed to be null. Attach the original right subtree here.
            maxInLeft.right = rightSubtree;
            if (rightSubtree != null) {
                rightSubtree.parent = maxInLeft;
            }
            this.root = maxInLeft;
        }
    }

    // ------------------ Splay and Rotation Helper Methods ------------------

    /**
     * Performs the splay operation on a given node, moving it to the root.
     *
     * @param x The node to splay.
     */
    private void splay(Node x) {
        if (x == null) return;

        while (x.parent != null) {
            Node p = x.parent;
            Node g = p.parent;

            if (g == null) { // Zig step
                if (x == p.left) {
                    rightRotate(p);
                } else {
                    leftRotate(p);
                }
            } else {
                if (x == p.left && p == g.left) { // Zig-Zig step (left-left)
                    rightRotate(g);
                    rightRotate(p);
                } else if (x == p.right && p == g.right) { // Zig-Zig step (right-right)
                    leftRotate(g);
                    leftRotate(p);
                } else if (x == p.right && p == g.left) { // Zig-Zag step (left-right)
                    leftRotate(p);
                    rightRotate(g);
                } else { // Zig-Zag step (right-left)
                    rightRotate(p);
                    leftRotate(g);
                }
            }
        }
        this.root = x;
    }

    /**
     * Performs a left rotation on the subtree rooted at node x.
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
     * Performs a right rotation on the subtree rooted at node x.
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
            } else if (x == x.parent.left) {
                x.parent.left = y;
            } else {
                x.parent.right = y;
            }
            y.right = x;
            x.parent = y;
        }
    }

    // ------------------ Search Helper Method ------------------

    /**
     * Finds a node with the given key using a standard BST search.
     *
     * @param key The key to find.
     * @return The node with the key if found, or the last non-null node on the search path.
     *         Returns null if the tree is empty.
     */
    private Node findNode(int key) {
        Node current = root;
        Node last = null;
        while (current != null) {
            last = current;
            if (key < current.key) {
                current = current.left;
            } else if (key > current.key) {
                current = current.right;
            } else {
                return current; // Found
            }
        }
        return last; // Not found, return the last accessed node
    }
}