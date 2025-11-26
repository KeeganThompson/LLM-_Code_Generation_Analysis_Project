/**
 * A self-contained Java class implementing a Splay Tree for an integer set.
 * A splay tree is a self-adjusting binary search tree with the additional
 * property that recently accessed elements are quick to access again.
 */
public class SplayTree {

    /**
     * Inner class representing a node in the Splay Tree.
     */
    private static class Node {
        int key;
        Node left;
        Node right;
        Node parent;

        Node(int key) {
            this.key = key;
            this.left = null;
            this.right = null;
            this.parent = null;
        }
    }

    private Node root;

    /**
     * Constructs an empty SplayTree.
     */
    public SplayTree() {
        this.root = null;
    }

    // --- Rotation Helpers ---

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

    // --- Core Splay Operation ---

    /**
     * Performs the splay operation on a node x, moving it to the root.
     * @param x The node to splay.
     */
    private void splay(Node x) {
        if (x == null) {
            return;
        }
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
                if (x == parent.left) {
                    if (parent == grandParent.left) { // Zig-Zig (left-left)
                        rightRotate(grandParent);
                        rightRotate(parent);
                    } else { // Zig-Zag (right-left)
                        rightRotate(parent);
                        leftRotate(grandParent);
                    }
                } else { // x == parent.right
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

    // --- Public Interface ---

    /**
     * Inserts a key into the splay tree.
     * If the key already exists, the tree remains unchanged. After insertion,
     * the new node becomes the root of the tree.
     * @param key The key to insert.
     */
    public void insert(int key) {
        // Case 1: Tree is empty
        if (root == null) {
            root = new Node(key);
            return;
        }

        // Splay the closest node to the insertion point to the root
        splay(findLastAccessed(key));

        // Case 2: Key already exists
        if (root.key == key) {
            return; // No duplicates in a set
        }

        // Case 3: Split the tree and insert the new key as the new root
        Node newNode = new Node(key);
        if (key < root.key) {
            newNode.right = root;
            newNode.left = root.left;
            if (root.left != null) {
                root.left.parent = newNode;
            }
            root.left = null;
        } else { // key > root.key
            newNode.left = root;
            newNode.right = root.right;
            if (root.right != null) {
                root.right.parent = newNode;
            }
            root.right = null;
        }
        root.parent = newNode;
        root = newNode;
    }

    /**
     * Searches for a key in the splay tree.
     * If the key is found, the node containing the key is splayed to the root.
     * If not found, the last accessed node during the search is splayed to the root.
     * @param key The key to search for.
     * @return The key if found, otherwise null.
     */
    public Integer search(int key) {
        Node nodeToSplay = findLastAccessed(key);
        if (nodeToSplay != null) {
            splay(nodeToSplay);
            // After splaying, the found node (or last accessed) is the new root
            if (root.key == key) {
                return root.key;
            }
        }
        return null;
    }

    /**
     * Deletes a key from the splay tree.
     * @param key The key to delete.
     */
    public void delete(int key) {
        if (root == null) {
            return;
        }

        // Splay the node to be deleted (or its closest neighbor) to the root
        splay(findLastAccessed(key));

        // If the key is not at the root after splaying, it wasn't in the tree
        if (root.key != key) {
            return;
        }

        // Now, delete the root by joining its two subtrees
        Node leftSubtree = root.left;
        Node rightSubtree = root.right;

        if (leftSubtree == null) {
            root = rightSubtree;
            if (root != null) {
                root.parent = null;
            }
        } else {
            // Detach the left subtree to operate on it independently
            leftSubtree.parent = null;

            // Find the maximum node in the left subtree
            Node maxInLeft = leftSubtree;
            while (maxInLeft.right != null) {
                maxInLeft = maxInLeft.right;
            }

            // Splay this max node to the top of the left subtree
            // Temporarily set root to leftSubtree to reuse the main splay function
            this.root = leftSubtree;
            splay(maxInLeft); // After this, 'this.root' is maxInLeft

            // Join the original right subtree to the new root
            root.right = rightSubtree;
            if (rightSubtree != null) {
                rightSubtree.parent = root;
            }
        }
    }

    // --- Private Helper ---

    /**
     * Finds the node with the given key, or the last node accessed on the search path.
     * This is the node that will be splayed after an access operation.
     * @param key The key to find.
     * @return The node with the key, or the last accessed node if the key is not found.
     *         Returns null if the tree is empty.
     */
    private Node findLastAccessed(int key) {
        if (root == null) {
            return null;
        }
        Node current = root;
        Node last = root;
        while (current != null) {
            last = current;
            if (key < current.key) {
                current = current.left;
            } else if (key > current.key) {
                current = current.right;
            } else {
                return current; // Found the exact node
            }
        }
        return last; // Return the last non-null node visited
    }
}