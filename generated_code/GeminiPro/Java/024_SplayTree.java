/**
 * A self-contained Java class implementing a Splay Tree for an integer set.
 * Splay trees are self-balancing binary search trees with the additional property
 * that recently accessed elements are quick to access again.
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

    public SplayTree() {
        this.root = null;
    }

    // --- Core Splaying Operations ---

    /**
     * Performs a left rotation on the given node x.
     *
     *    x           y
     *   / \         / \
     *  A   y  -->  x   C
     *     / \     / \
     *    B   C   A   B
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
     *      y          x
     *     / \        / \
     *    x   C -->  A   y
     *   / \            / \
     *  A   B          B   C
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
     * Moves the given node x to the root of the tree using a series of rotations.
     * This is the core operation of the Splay Tree.
     * @param x The node to splay to the root.
     */
    private void splay(Node x) {
        while (x.parent != null) {
            Node p = x.parent;
            Node g = p.parent;
            if (g == null) { // Zig case
                if (x == p.left) {
                    rightRotate(p);
                } else {
                    leftRotate(p);
                }
            } else { // Zig-Zig or Zig-Zag
                if (x == p.left && p == g.left) { // Zig-Zig (left-left)
                    rightRotate(g);
                    rightRotate(p);
                } else if (x == p.right && p == g.right) { // Zig-Zig (right-right)
                    leftRotate(g);
                    leftRotate(p);
                } else if (x == p.left && p == g.right) { // Zig-Zag (right-left)
                    rightRotate(p);
                    leftRotate(g);
                } else { // Zig-Zag (left-right)
                    leftRotate(p);
                    rightRotate(g);
                }
            }
        }
        this.root = x;
    }

    // --- Private Helper Methods ---

    /**
     * Finds a node with the given key. If the key is not found, it returns the
     * last node accessed on the search path. This node is the one that will be splayed.
     * @param key The key to find.
     * @return The node containing the key, or the last accessed node if not found.
     */
    private Node findNode(int key) {
        if (root == null) return null;
        Node current = root;
        while (true) {
            if (key < current.key) {
                if (current.left == null) return current;
                current = current.left;
            } else if (key > current.key) {
                if (current.right == null) return current;
                current = current.right;
            } else {
                return current; // Found
            }
        }
    }

    // --- Public API Methods ---

    /**
     * Inserts a key into the splay tree.
     * If the key already exists, the existing node is splayed to the root.
     *
     * @param key The integer key to insert.
     */
    public void insert(int key) {
        // 1. Standard BST insertion to find the parent
        Node parent = null;
        Node current = this.root;
        while (current != null) {
            parent = current;
            if (key < current.key) {
                current = current.left;
            } else if (key > current.key) {
                current = current.right;
            } else {
                // Key already exists, splay the existing node and return
                splay(current);
                return;
            }
        }

        // 2. Create and link the new node
        Node newNode = new Node(key);
        newNode.parent = parent;

        if (parent == null) {
            this.root = newNode; // Tree was empty
        } else if (key < parent.key) {
            parent.left = newNode;
        } else {
            parent.right = newNode;
        }

        // 3. Splay the new node to the root
        splay(newNode);
    }

    /**
     * Searches for a key in the splay tree.
     * If the key is found, the corresponding node is splayed to the root.
     * If not found, the last accessed node on the search path is splayed.
     *
     * @param key The key to search for.
     * @return The key as an Integer if found, otherwise null.
     */
    public Integer search(int key) {
        Node nodeToSplay = findNode(key);
        if (nodeToSplay != null) {
            splay(nodeToSplay);
        }

        // After splaying, if the key exists, it must be at the root.
        if (root != null && root.key == key) {
            return root.key;
        }
        
        return null;
    }

    /**
     * Deletes a key from the splay tree.
     *
     * @param key The key to delete.
     */
    public void delete(int key) {
        // Splay the node to be deleted (or its parent/successor) to the root
        search(key);

        // If key is not at the root after search, it wasn't in the tree, so do nothing.
        if (root == null || root.key != key) {
            return;
        }

        Node oldRoot = root;
        Node leftSubtree = oldRoot.left;
        Node rightSubtree = oldRoot.right;

        if (leftSubtree == null) {
            // No left child, the right subtree becomes the new tree
            this.root = rightSubtree;
            if (rightSubtree != null) {
                rightSubtree.parent = null;
            }
        } else {
            // Find the maximum node in the left subtree. This will be the new root.
            Node newRoot = leftSubtree;
            while (newRoot.right != null) {
                newRoot = newRoot.right;
            }

            // Splay this max node. It becomes the new root of the entire tree.
            // The old root (the one being deleted) is now in the right subtree of the new root.
            splay(newRoot);

            // Attach the original right subtree to the new root.
            // This effectively removes the old root from the tree.
            root.right = rightSubtree;
            if (rightSubtree != null) {
                rightSubtree.parent = root;
            }
        }
    }
}