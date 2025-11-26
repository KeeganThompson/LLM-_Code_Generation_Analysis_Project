/**
 * A self-contained Java class implementing an integer set using a Splay Tree.
 * A splay tree is a self-adjusting binary search tree with the additional property
 * that recently accessed elements are quick to access again.
 */
public class SplayTree {

    private Node root;

    /**
     * Private static inner class to represent a node in the tree.
     */
    private static class Node {
        int key;
        Node left, right;

        Node(int key) {
            this.key = key;
            this.left = null;
            this.right = null;
        }
    }

    /**
     * Constructs an empty SplayTree.
     */
    public SplayTree() {
        this.root = null;
    }

    /**
     * Performs a right rotation on the given node.
     *
     * @param x The node to rotate.
     * @return The new root of the rotated subtree.
     */
    private Node rightRotate(Node x) {
        Node y = x.left;
        x.left = y.right;
        y.right = x;
        return y;
    }

    /**
     * Performs a left rotation on the given node.
     *
     * @param x The node to rotate.
     * @return The new root of the rotated subtree.
     */
    private Node leftRotate(Node x) {
        Node y = x.right;
        x.right = y.left;
        y.left = x;
        return y;
    }

    /**
     * The core splay operation. Moves the node with the given key to the root.
     * If the key is not in the tree, the last accessed node is moved to the root.
     * This is a top-down splay implementation.
     *
     * @param key The key of the node to splay to the root.
     */
    private void splay(int key) {
        if (root == null) {
            return;
        }

        Node dummy = new Node(0); // Dummy node to simplify linking
        Node leftTreeMax = dummy;
        Node rightTreeMin = dummy;
        Node current = root;

        while (true) {
            if (key < current.key) {
                if (current.left == null) {
                    break;
                }
                // Zig-Zig (Right-Right)
                if (key < current.left.key) {
                    current = rightRotate(current);
                    if (current.left == null) {
                        break;
                    }
                }
                // Link current to the right tree of the new assembly
                rightTreeMin.left = current;
                rightTreeMin = current;
                current = current.left;
            } else if (key > current.key) {
                if (current.right == null) {
                    break;
                }
                // Zig-Zig (Left-Left)
                if (key > current.right.key) {
                    current = leftRotate(current);
                    if (current.right == null) {
                        break;
                    }
                }
                // Link current to the left tree of the new assembly
                leftTreeMax.right = current;
                leftTreeMax = current;
                current = current.right;
            } else {
                // Key found
                break;
            }
        }

        // Reassemble the tree
        leftTreeMax.right = current.left;
        rightTreeMin.left = current.right;
        current.left = dummy.right;
        current.right = dummy.left;
        root = current;
    }

    /**
     * Inserts a key into the Splay Tree.
     * If the key already exists, the tree remains unchanged, but the node
     * with the existing key is splayed to the root.
     *
     * @param key The integer key to insert.
     */
    public void insert(int key) {
        if (root == null) {
            root = new Node(key);
            return;
        }

        // Splay the tree for the key. The closest node will become the root.
        splay(key);

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
     * Searches for a key in the Splay Tree.
     * If the key is found, the corresponding node is splayed to the root.
     * If not found, the last accessed node is splayed to the root.
     *
     * @param key The integer key to search for.
     * @return The key if found, otherwise null.
     */
    public Integer search(int key) {
        if (root == null) {
            return null;
        }
        splay(key);
        // After splaying, if the key exists, it will be at the root.
        if (root.key == key) {
            return key;
        }
        return null;
    }

    /**
     * Deletes a key from the Splay Tree.
     * If the key is found and deleted, the parent of the deleted node is splayed to the root.
     *
     * @param key The integer key to delete.
     */
    public void delete(int key) {
        if (root == null) {
            return;
        }

        // Splay the tree for the key. If it exists, it becomes the root.
        splay(key);

        // If the key is not in the tree, do nothing.
        if (root.key != key) {
            return;
        }

        // Now, the node to delete is the root.
        Node leftSubtree = root.left;
        Node rightSubtree = root.right;

        if (leftSubtree == null) {
            // No left child, so the right subtree becomes the new tree.
            root = rightSubtree;
        } else {
            // Make the left subtree the new tree.
            root = leftSubtree;
            // Splay the largest element in the left subtree to its root.
            // This can be done by splaying for the key we just deleted,
            // as it is guaranteed to be larger than any key in the left subtree.
            splay(key);
            // After the splay, the new root has no right child.
            // Attach the original right subtree.
            root.right = rightSubtree;
        }
    }
}