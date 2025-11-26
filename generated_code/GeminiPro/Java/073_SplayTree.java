/**
 * A complete, self-contained implementation of a Splay Tree that functions as an integer set.
 * Splay trees are self-balancing binary search trees with the additional property
 * that recently accessed elements are quick to access again. This implementation includes
 * insert, delete, and search operations. The search operation also performs the splaying
 * action, moving the accessed node to the root of the tree.
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
     * @param x The node to be rotated.
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
     * Performs a right rotation on the given node x.
     *
     * @param x The node to be rotated.
     */
    private void rotateRight(Node x) {
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
     * Performs the splay operation on the given node, moving it to the root.
     *
     * @param x The node to splay.
     */
    private void splay(Node x) {
        while (x.parent != null) {
            Node parent = x.parent;
            Node grandParent = parent.parent;

            if (grandParent == null) { // Zig case
                if (x == parent.left) {
                    rotateRight(parent);
                } else {
                    rotateLeft(parent);
                }
            } else {
                if (x == parent.left && parent == grandParent.left) { // Zig-Zig case (left-left)
                    rotateRight(grandParent);
                    rotateRight(parent);
                } else if (x == parent.right && parent == grandParent.right) { // Zig-Zig case (right-right)
                    rotateLeft(grandParent);
                    rotateLeft(parent);
                } else if (x == parent.left && parent == grandParent.right) { // Zig-Zag case (right-left)
                    rotateRight(parent);
                    rotateLeft(grandParent);
                } else { // Zig-Zag case (left-right)
                    rotateLeft(parent);
                    rotateRight(grandParent);
                }
            }
        }
        this.root = x;
    }

    /**
     * Searches for a key in the tree. If the key is found, the corresponding node
     * is splayed to the root. If not found, the last accessed node is splayed.
     *
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
                // Key found, splay the node and return the key
                splay(current);
                return current.key;
            }
        }

        // Key not found, splay the last accessed node
        if (lastNode != null) {
            splay(lastNode);
        }
        return null;
    }

    /**
     * Inserts a key into the Splay Tree. If the key already exists, the existing
     * node is splayed. If the key is new, it is inserted and the new node is splayed.
     *
     * @param key The key to insert.
     */
    public void insert(int key) {
        // If the tree is empty, create a new root
        if (root == null) {
            root = new Node(key);
            return;
        }

        Node current = root;
        Node parent = null;

        // Traverse to find the insertion point or an existing key
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

        // Create and insert the new node
        Node newNode = new Node(key);
        newNode.parent = parent;

        if (key < parent.key) {
            parent.left = newNode;
        } else {
            parent.right = newNode;
        }

        // Splay the newly inserted node to the root
        splay(newNode);
    }

    /**
     * Deletes a key from the Splay Tree.
     *
     * @param key The key to delete.
     */
    public void delete(int key) {
        // Search for the key. This splays the node to the root if found.
        search(key);

        // If the root is null or doesn't have the key, the key was not in the tree.
        if (root == null || root.key != key) {
            return;
        }

        // The node to delete is now the root.
        Node leftSubtree = root.left;
        Node rightSubtree = root.right;

        if (leftSubtree == null) {
            // If there's no left child, the right subtree becomes the new tree.
            this.root = rightSubtree;
            if (this.root != null) {
                this.root.parent = null;
            }
        } else {
            // Find the maximum node in the left subtree.
            Node maxNode = leftSubtree;
            while (maxNode.right != null) {
                maxNode = maxNode.right;
            }

            // Splay this maximum node to the root of the left subtree.
            // To do this, we temporarily treat the left subtree as the main tree.
            leftSubtree.parent = null; // Disconnect for the splay operation
            this.root = leftSubtree;
            splay(maxNode);

            // After splaying, maxNode is the new root. Its right child is null.
            // We can now attach the original right subtree.
            this.root.right = rightSubtree;
            if (rightSubtree != null) {
                rightSubtree.parent = this.root;
            }
        }
    }
}