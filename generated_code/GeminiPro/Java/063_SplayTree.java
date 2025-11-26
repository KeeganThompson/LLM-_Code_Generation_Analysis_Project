/**
 * A self-contained Java class implementing a Splay Tree for an integer set.
 * Splay trees are self-balancing binary search trees with the additional property
 * that recently accessed elements are quick to access again.
 */
public class SplayTree {

    /**
     * Represents a node in the Splay Tree.
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
     * @return The new root of the rotated subtree.
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
     * @return The new root of the rotated subtree.
     */
    private Node leftRotate(Node x) {
        Node y = x.right;
        x.right = y.left;
        y.left = x;
        return y;
    }

    /**
     * The core splay operation. Moves the node with the given key (or the last
     * accessed node if the key is not found) to the root of the tree.
     * This implementation uses the top-down splaying technique.
     *
     * @param key The key to splay around.
     */
    private void splay(int key) {
        if (root == null) {
            return;
        }

        // Create a dummy node to simplify linking
        Node dummy = new Node(0);
        Node leftTree = dummy;
        Node rightTree = dummy;
        Node current = root;

        while (true) {
            if (key < current.key) {
                if (current.left == null) {
                    break;
                }
                // Zig-Zig (Left-Left) case
                if (key < current.left.key) {
                    current = rightRotate(current);
                    if (current.left == null) {
                        break;
                    }
                }
                // Link current to the right tree
                rightTree.left = current;
                rightTree = current;
                current = current.left;
            } else if (key > current.key) {
                if (current.right == null) {
                    break;
                }
                // Zig-Zig (Right-Right) case
                if (key > current.right.key) {
                    current = leftRotate(current);
                    if (current.right == null) {
                        break;
                    }
                }
                // Link current to the left tree
                leftTree.right = current;
                leftTree = current;
                current = current.right;
            } else { // key == current.key
                break;
            }
        }

        // Reassemble the tree
        leftTree.right = current.left;
        rightTree.left = current.right;
        current.left = dummy.right;
        current.right = dummy.left;
        root = current;
    }

    /**
     * Searches for a key in the tree. If the key is found, it is splayed
     * to the root.
     *
     * @param key The key to search for.
     * @return The key if found, otherwise null.
     */
    public Integer search(int key) {
        if (root == null) {
            return null;
        }
        splay(key);
        // After splaying, the root is the closest node to the key.
        // We check if it's an exact match.
        if (root.key == key) {
            return key;
        }
        return null;
    }

    /**
     * Inserts a key into the Splay Tree. Duplicates are not allowed.
     *
     * @param key The key to insert.
     */
    public void insert(int key) {
        if (root == null) {
            root = new Node(key);
            return;
        }

        // Splay the tree around the key. If the key is present, it becomes the root.
        // If not, the node that would be its parent becomes the root.
        splay(key);

        // If the key is already at the root, it's a duplicate; do nothing.
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
     * Deletes a key from the Splay Tree.
     *
     * @param key The key to delete.
     */
    public void delete(int key) {
        if (root == null) {
            return;
        }

        // Splay the key to the root.
        splay(key);

        // If the key is not at the root, it's not in the tree.
        if (root.key != key) {
            return;
        }

        // Now, the node to delete is the root.
        Node leftSubtree = root.left;
        Node rightSubtree = root.right;

        if (leftSubtree == null) {
            // If there's no left subtree, the right subtree becomes the new tree.
            root = rightSubtree;
        } else {
            // Make the left subtree the main tree.
            root = leftSubtree;
            
            // Splay for the key we just deleted in the new tree (the left subtree).
            // This will bring the largest element in the left subtree (the predecessor
            // of the deleted key) to the root.
            splay(key);
            
            // The new root (max of the left subtree) is guaranteed to have no right child.
            // Attach the original right subtree as its right child.
            root.right = rightSubtree;
        }
    }
}