/**
 * A complete, self-contained Java class that implements an integer set using a Splay Tree.
 * A splay tree is a self-balancing binary search tree with the additional property that
 * recently accessed elements are quick to access again. It performs basic operations
 * such as insertion, look-up and removal in O(log n) amortized time.
 */
public class SplayTree {

    /**
     * Represents a node in the Splay Tree.
     * It is a private static nested class as it is tightly coupled with the SplayTree class.
     */
    private static class Node {
        int key;
        Node parent;
        Node left;
        Node right;

        /**
         * Constructs a new node.
         * @param key The integer key for the node.
         * @param parent The parent of this node.
         */
        Node(int key, Node parent) {
            this.key = key;
            this.parent = parent;
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
     *   x           y
     *  / \         / \
     * A   y  -->  x   C
     *    / \     / \
     *   B   C   A   B
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
     *     y         x
     *    / \       / \
     *   x   C --> A   y
     *  / \           / \
     * A   B         B   C
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
     * Performs the splay operation on a node x, moving it to the root.
     * @param x The node to splay.
     */
    private void splay(Node x) {
        if (x == null) return;

        while (x.parent != null) {
            Node parent = x.parent;
            Node grandParent = parent.parent;

            if (grandParent == null) { // Zig step
                if (x == parent.left) {
                    rightRotate(parent);
                } else {
                    leftRotate(parent);
                }
            } else { // Zig-Zig or Zig-Zag
                if (x == parent.left) {
                    if (parent == grandParent.left) { // Zig-Zig (left-left)
                        rightRotate(grandParent);
                        rightRotate(parent);
                    } else { // Zig-Zag (right-left)
                        rightRotate(parent);
                        leftRotate(grandParent);
                    }
                } else { // x is right child
                    if (parent == grandParent.left) { // Zig-Zag (left-right)
                        leftRotate(parent);
                        rightRotate(grandParent);
                    } else { // Zig-Zig (right-right)
                        leftRotate(grandParent);
                        leftRotate(parent);
                    }
                }
            }
        }
    }

    /**
     * A helper method to find a node with a given key, or the last node
     * accessed on the search path. It then splays this node to the root.
     *
     * @param key The key to search for.
     * @return The new root of the tree after splaying.
     */
    private Node findAndSplay(int key) {
        if (root == null) {
            return null;
        }
        Node current = root;
        while (true) {
            if (key < current.key) {
                if (current.left == null) break;
                current = current.left;
            } else if (key > current.key) {
                if (current.right == null) break;
                current = current.right;
            } else {
                break; // Found the key
            }
        }
        splay(current);
        return this.root;
    }

    /**
     * Searches for a key in the tree. If the key is found, the node containing it
     * is splayed to the root. If not found, the last accessed node in the search
     * path is splayed to the root.
     *
     * @param key The key to search for.
     * @return The key if it's found, otherwise null.
     */
    public Integer search(int key) {
        Node newRoot = findAndSplay(key);
        if (newRoot != null && newRoot.key == key) {
            return newRoot.key;
        }
        return null;
    }

    /**
     * Inserts a key into the splay tree. If the key already exists, the node
     * containing it is splayed to the root. Otherwise, a new node is inserted
     * and then splayed to the root.
     *
     * @param key The key to insert.
     */
    public void insert(int key) {
        if (root == null) {
            root = new Node(key, null);
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
                // Key already exists. Splay it and we're done.
                splay(current);
                return;
            }
        }

        // Key not found, insert it.
        Node newNode = new Node(key, parent);
        if (key < parent.key) {
            parent.left = newNode;
        } else {
            parent.right = newNode;
        }
        splay(newNode);
    }

    /**
     * Deletes a key from the splay tree. The standard splay tree deletion algorithm is used:
     * 1. Splay the node with the key to the root.
     * 2. If the key is not found, do nothing.
     * 3. If found, remove the root, splitting the tree into two subtrees (L and R).
     * 4. Find the maximum element in the left subtree L.
     * 5. Splay this maximum element to the root of L.
     * 6. Attach R as the right child of the new root of L.
     *
     * @param key The key to delete.
     */
    public void delete(int key) {
        findAndSplay(key); // Splay the node (or its neighbor) to the root

        // If root is null or key is not at the root, the key wasn't in the tree.
        if (root == null || root.key != key) {
            return;
        }

        Node leftSubtree = root.left;
        Node rightSubtree = root.right;

        if (leftSubtree == null) {
            root = rightSubtree;
            if (root != null) {
                root.parent = null;
            }
        } else {
            leftSubtree.parent = null;

            // Find the maximum node in the left subtree
            Node maxNode = leftSubtree;
            while (maxNode.right != null) {
                maxNode = maxNode.right;
            }

            // Temporarily set the tree's root to the left subtree to use the splay method
            this.root = leftSubtree;
            splay(maxNode); // maxNode is now the root of this subtree

            // Re-attach the right subtree. The new root (maxNode) has no right child.
            this.root.right = rightSubtree;
            if (rightSubtree != null) {
                rightSubtree.parent = this.root;
            }
        }
    }
}