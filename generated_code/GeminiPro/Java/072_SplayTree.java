/**
 * A complete, self-contained Java class that implements an integer set
 * using a Splay Tree data structure. A splay tree is a self-balancing binary
 * search tree with the additional property that recently accessed elements
 * are quick to access again.
 */
public class SplayTree {

    /**
     * Inner class representing a node in the Splay Tree.
     * It holds the integer key and references to its parent, left child, and right child.
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
     * Constructs an empty Splay Tree.
     */
    public SplayTree() {
        this.root = null;
    }

    // --- Core Splay Operation ---

    /**
     * Performs the splay operation on a given node x, moving it to the root.
     * The splay operation consists of a sequence of rotations (Zig, Zig-Zig, or Zig-Zag)
     * that bring the node x to the top of the tree.
     *
     * @param x The non-null node to splay.
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
            } else { // Zig-Zig or Zig-Zag cases
                if (x == parent.left) {
                    if (parent == grandParent.left) { // Zig-Zig (left-left)
                        rightRotate(grandParent);
                        rightRotate(parent);
                    } else { // Zig-Zag (left-right)
                        rightRotate(parent);
                        leftRotate(grandParent);
                    }
                } else {
                    if (parent == grandParent.right) { // Zig-Zig (right-right)
                        leftRotate(grandParent);
                        leftRotate(parent);
                    } else { // Zig-Zag (right-left)
                        leftRotate(parent);
                        rightRotate(grandParent);
                    }
                }
            }
        }
        this.root = x;
    }

    // --- Rotation Helpers ---

    /**
     * Performs a left rotation on the given node p.
     *
     * @param p The node to rotate.
     */
    private void leftRotate(Node p) {
        Node r = p.right;
        if (r != null) {
            p.right = r.left;
            if (r.left != null) {
                r.left.parent = p;
            }
            r.parent = p.parent;
            if (p.parent == null) {
                this.root = r;
            } else if (p == p.parent.left) {
                p.parent.left = r;
            } else {
                p.parent.right = r;
            }
            r.left = p;
            p.parent = r;
        }
    }

    /**
     * Performs a right rotation on the given node p.
     *
     * @param p The node to rotate.
     */
    private void rightRotate(Node p) {
        Node l = p.left;
        if (l != null) {
            p.left = l.right;
            if (l.right != null) {
                l.right.parent = p;
            }
            l.parent = p.parent;
            if (p.parent == null) {
                this.root = l;
            } else if (p == p.parent.right) {
                p.parent.right = l;
            } else {
                p.parent.left = l;
            }
            l.right = p;
            p.parent = l;
        }
    }
    
    // --- Search Helper ---
    
    /**
     * Helper method to find a node or the last node on the search path.
     * This method does not perform splaying.
     * @param key The key to find.
     * @return The node containing the key, or the last non-null node on the search path if not found. Returns null if tree is empty.
     */
    private Node findNode(int key) {
        if (root == null) {
            return null;
        }
        Node current = root;
        Node last = null;
        while (current != null) {
            last = current;
            if (key < current.key) {
                current = current.left;
            } else if (key > current.key) {
                current = current.right;
            } else {
                return current; // Found the node
            }
        }
        return last; // Key not found, return last accessed node
    }


    // --- Public API Methods ---

    /**
     * Searches for a key in the splay tree.
     * If the key is found, the corresponding node is splayed to the root and the key is returned.
     * If the key is not found, the last accessed node on the search path is splayed to the root
     * and null is returned.
     *
     * @param key The integer key to search for.
     * @return The key if found, otherwise null.
     */
    public Integer search(int key) {
        Node nodeToSplay = findNode(key);
        if (nodeToSplay != null) {
            splay(nodeToSplay);
            // After splaying, the node is the root. Check if its key matches.
            if (this.root.key == key) {
                return key;
            }
        }
        return null;
    }

    /**
     * Inserts a key into the splay tree.
     * If the key already exists, the existing node is splayed to the root.
     * Otherwise, a new node is created, inserted, and then splayed to the root.
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
                // Key already exists, splay the found node and return.
                splay(current);
                return;
            }
        }

        // Insert the new node
        Node newNode = new Node(key);
        newNode.parent = parent;
        if (key < parent.key) {
            parent.left = newNode;
        } else {
            parent.right = newNode;
        }

        // Splay the newly inserted node
        splay(newNode);
    }

    /**
     * Deletes a key from the splay tree.
     * The tree is first searched for the key, and the accessed node is splayed.
     * If the key is found at the root, it is removed and its subtrees are joined.
     * The new root becomes the maximum element of the left subtree.
     *
     * @param key The integer key to delete.
     */
    public void delete(int key) {
        Node nodeToSplay = findNode(key);
        if (nodeToSplay == null) {
            return; // Tree is empty
        }
        splay(nodeToSplay);

        // After splaying, if the root's key doesn't match, the key wasn't in the tree.
        if (root.key != key) {
            return;
        }

        // At this point, the node to delete is the root.
        Node leftSubtree = root.left;
        Node rightSubtree = root.right;

        if (leftSubtree == null) {
            // No left child, the right subtree becomes the new tree.
            root = rightSubtree;
            if (root != null) {
                root.parent = null;
            }
        } else {
            // Disconnect the left subtree to work on it independently.
            leftSubtree.parent = null;

            // Find the maximum node in the left subtree (the predecessor).
            Node maxInLeft = leftSubtree;
            while (maxInLeft.right != null) {
                maxInLeft = maxInLeft.right;
            }

            // Splay the predecessor to the root of the left subtree.
            // Temporarily set the main root to the left subtree's root
            // to use the global splay and rotation methods.
            this.root = leftSubtree;
            splay(maxInLeft);

            // Now, this.root is the new root of the combined tree (maxInLeft).
            // Its right child is guaranteed to be null.
            // Attach the original right subtree.
            this.root.right = rightSubtree;
            if (rightSubtree != null) {
                rightSubtree.parent = this.root;
            }
        }
    }
}