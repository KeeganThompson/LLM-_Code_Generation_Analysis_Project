/**
 * A complete, self-contained implementation of an integer Splay Tree.
 * Splay trees are self-balancing binary search trees with the property that
 * recently accessed elements are quick to access again. This implementation
 * supports insert, delete, and search operations for a set of integers.
 */
public class SplayTree {

    /**
     * Inner class to represent a node in the Splay Tree.
     * It includes a parent pointer to facilitate the splaying operation.
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

    /**
     * Searches for a key in the tree.
     * If the key is found, the node containing the key is splayed to the root.
     * If the key is not found, the last accessed node before the search failed
     * is splayed to the root.
     *
     * @param key The integer key to search for.
     * @return The key if found, otherwise null.
     */
    public Integer search(int key) {
        Node current = root;
        Node lastNode = null;

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

        // Key not found. Splay the last accessed node if the tree was not empty.
        if (lastNode != null) {
            splay(lastNode);
        }
        return null;
    }

    /**
     * Inserts a key into the Splay Tree.
     * If the key already exists, the existing node is splayed to the root.
     * If the key is new, it is inserted and the new node is splayed to the root.
     *
     * @param key The integer key to insert.
     */
    public void insert(int key) {
        Node node = root;
        Node parent = null;

        // 1. Find position for new node (standard BST insert)
        while (node != null) {
            parent = node;
            if (key < node.key) {
                node = node.left;
            } else if (key > node.key) {
                node = node.right;
            } else {
                // Key already exists, splay it and return
                splay(node);
                return;
            }
        }

        // 2. Insert the new node
        Node newNode = new Node(key);
        newNode.parent = parent;

        if (parent == null) {
            root = newNode; // Tree was empty
        } else if (key < parent.key) {
            parent.left = newNode;
        } else {
            parent.right = newNode;
        }

        // 3. Splay the new node to the root
        splay(newNode);
    }

    /**
     * Deletes a key from the Splay Tree.
     * The tree is first searched for the key, which brings the node (or its
     * would-be parent) to the root. If the key is found at the root, it is
     * removed and the tree is re-joined.
     *
     * @param key The integer key to delete.
     */
    public void delete(int key) {
        // Splay the node with the given key (or its parent) to the root
        search(key);

        // If the key is not in the tree, the root will not have the key.
        if (root == null || root.key != key) {
            return; // Key not found, nothing to delete.
        }

        // Now, the node to delete is the root.
        Node leftSubtree = root.left;
        Node rightSubtree = root.right;

        if (leftSubtree == null) {
            // If there's no left child, the right child becomes the new root.
            root = rightSubtree;
            if (root != null) {
                root.parent = null;
            }
        } else {
            // Detach the left subtree to operate on it independently.
            leftSubtree.parent = null;

            // Find the maximum node in the left subtree.
            Node maxInLeft = leftSubtree;
            while (maxInLeft.right != null) {
                maxInLeft = maxInLeft.right;
            }

            // Splay this maximum node to the top of the left subtree.
            // Temporarily set the main root to the left subtree's root to do this.
            this.root = leftSubtree;
            splay(maxInLeft);

            // After splaying, `this.root` is `maxInLeft`.
            // The new root (`maxInLeft`) has no right child.
            // Attach the original right subtree as its right child.
            this.root.right = rightSubtree;
            if (rightSubtree != null) {
                rightSubtree.parent = this.root;
            }
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

            if (grandParent == null) { // Zig case
                if (x == parent.left) {
                    rightRotate(parent);
                } else {
                    leftRotate(parent);
                }
            } else {
                if (x == parent.left) {
                    if (parent == grandParent.left) { // Zig-Zig case
                        rightRotate(grandParent);
                        rightRotate(parent);
                    } else { // Zig-Zag case
                        rightRotate(parent);
                        leftRotate(grandParent);
                    }
                } else { // x is the right child
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
        // The loop terminates when x is the root. The rotation methods handle
        // updating the main root field when the old root is rotated.
    }

    /**
     * Performs a left rotation on the subtree rooted at node x.
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
            } else if (x == x.parent.right) {
                x.parent.right = y;
            } else {
                x.parent.left = y;
            }
            y.right = x;
            x.parent = y;
        }
    }
}