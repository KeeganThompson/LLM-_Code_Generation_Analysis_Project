/**
 * Implements a Splay Tree, a self-balancing binary search tree, for storing a set of integers.
 * Splay trees have the property that recently accessed elements are quick to access again.
 * All major operations (insert, delete, search) perform a "splay" operation, which moves
 * the accessed element (or the last element on the search path) to the root of the tree.
 */
public class SplayTree {

    /**
     * Represents a node in the Splay Tree.
     */
    private static class Node {
        int key;
        Node left;
        Node right;

        Node(int key) {
            this.key = key;
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
     * Performs a right rotation on the subtree rooted at node x.
     * @param x The root of the subtree to rotate.
     * @return The new root of the subtree after rotation.
     */
    private Node rightRotate(Node x) {
        Node y = x.left;
        x.left = y.right;
        y.right = x;
        return y;
    }

    /**
     * Performs a left rotation on the subtree rooted at node x.
     * @param x The root of the subtree to rotate.
     * @return The new root of the subtree after rotation.
     */
    private Node leftRotate(Node x) {
        Node y = x.right;
        x.right = y.left;
        y.left = x;
        return y;
    }

    /**
     * The core splay operation. Moves the node with the given key (or the last accessed
     * node on the search path) to the root of the subtree.
     * This is a top-down splay implementation.
     * @param root The root of the subtree to splay.
     * @param key The key to splay around.
     * @return The new root of the splayed subtree.
     */
    private Node splay(Node root, int key) {
        if (root == null) {
            return null;
        }

        // A dummy node to simplify linking of left and right subtrees.
        Node header = new Node(0);
        Node leftTreeMax = header;
        Node rightTreeMin = header;
        Node current = root;

        while (true) {
            if (key < current.key) {
                if (current.left == null) {
                    break;
                }
                // Zig-Zig (left-left)
                if (key < current.left.key) {
                    current = rightRotate(current);
                    if (current.left == null) {
                        break;
                    }
                }
                // Link to the right tree
                rightTreeMin.left = current;
                rightTreeMin = current;
                current = current.left;
            } else if (key > current.key) {
                if (current.right == null) {
                    break;
                }
                // Zig-Zig (right-right)
                if (key > current.right.key) {
                    current = leftRotate(current);
                    if (current.right == null) {
                        break;
                    }
                }
                // Link to the left tree
                leftTreeMax.right = current;
                leftTreeMax = current;
                current = current.right;
            } else { // key == current.key
                break;
            }
        }

        // Reassemble the tree
        leftTreeMax.right = current.left;
        rightTreeMin.left = current.right;
        current.left = header.right;
        current.right = header.left;

        return current;
    }

    /**
     * Searches for a key in the tree. If found, the node is splayed to the root.
     * If not found, the last accessed node is splayed to the root.
     * @param key The key to search for.
     * @return The key if found, otherwise null.
     */
    public Integer search(int key) {
        root = splay(root, key);
        if (root != null && root.key == key) {
            return root.key;
        }
        return null;
    }

    /**
     * Inserts a key into the Splay Tree. If the key already exists, the tree remains unchanged.
     * The newly inserted node becomes the new root of the tree.
     * @param key The key to insert.
     */
    public void insert(int key) {
        if (root == null) {
            root = new Node(key);
            return;
        }

        // Splay the tree around the key. The closest node will be the root.
        root = splay(root, key);

        // If the key is already present, do nothing.
        if (root.key == key) {
            return;
        }

        Node newNode = new Node(key);
        if (key < root.key) {
            newNode.right = root;
            newNode.left = root.left;
            root.left = null;
        } else { // key > root.key
            newNode.left = root;
            newNode.right = root.right;
            root.right = null;
        }
        root = newNode;
    }

    /**
     * Deletes a key from the Splay Tree. If the key is not found, the tree remains unchanged.
     * @param key The key to delete.
     */
    public void delete(int key) {
        if (root == null) {
            return;
        }

        // Splay the tree around the key. If it exists, it will be the root.
        root = splay(root, key);

        // If the key is not in the tree, do nothing.
        if (root.key != key) {
            return;
        }

        // The node to be deleted is now the root.
        Node leftSubtree = root.left;
        Node rightSubtree = root.right;

        if (leftSubtree == null) {
            root = rightSubtree;
        } else {
            // Splay the largest element in the left subtree to its root.
            // This is done by splaying for the key we are deleting, which is guaranteed
            // to be larger than any element in the left subtree.
            Node newRoot = splay(leftSubtree, key);
            newRoot.right = rightSubtree;
            root = newRoot;
        }
    }
}