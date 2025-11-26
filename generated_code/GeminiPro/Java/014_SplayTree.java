/**
 * A complete, self-contained Java class implementing an integer set using a Splay Tree.
 * A splay tree is a self-balancing binary search tree with the additional property
 * that recently accessed elements are quick to access again.
 */
public class SplayTree {

    /**
     * Inner class representing a node in the Splay Tree.
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
     * The core splay operation. It moves the node with the given key to the root
     * of the tree rooted at {@code node}. If the key is not in the tree, the last
     * accessed node on the search path is moved to the root. This is a top-down splay.
     *
     * @param node The root of the tree (or subtree) to splay.
     * @param key  The key to splay around.
     * @return The new root of the splayed tree.
     */
    private Node splay(Node node, int key) {
        if (node == null) {
            return null;
        }

        // Use a dummy node to simplify linking of left and right subtrees.
        Node dummy = new Node(0);
        Node leftTree = dummy;
        Node rightTree = dummy;

        while (true) {
            if (key < node.key) {
                if (node.left == null) {
                    break;
                }
                // Zig-Zig (left-left) case: Rotate right
                if (key < node.left.key) {
                    Node temp = node.left;
                    node.left = temp.right;
                    temp.right = node;
                    node = temp;
                    if (node.left == null) {
                        break;
                    }
                }
                // Link the current root to the right tree
                rightTree.left = node;
                rightTree = node;
                node = node.left;
            } else if (key > node.key) {
                if (node.right == null) {
                    break;
                }
                // Zig-Zig (right-right) case: Rotate left
                if (key > node.right.key) {
                    Node temp = node.right;
                    node.right = temp.left;
                    temp.left = node;
                    node = temp;
                    if (node.right == null) {
                        break;
                    }
                }
                // Link the current root to the left tree
                leftTree.right = node;
                leftTree = node;
                node = node.right;
            } else {
                // Key found
                break;
            }
        }

        // Reassemble the tree
        leftTree.right = node.left;
        rightTree.left = node.right;
        node.left = dummy.right;
        node.right = dummy.left;

        return node;
    }

    /**
     * Searches for a key in the tree. If the key is found, it is splayed to the
     * root. If not found, the last accessed node on the search path is splayed
     * to the root.
     *
     * @param key The key to search for.
     * @return The key if found, otherwise null.
     */
    public Integer search(int key) {
        if (root == null) {
            return null;
        }
        root = splay(root, key);
        if (root.key == key) {
            return root.key;
        }
        return null;
    }

    /**
     * Inserts a key into the tree. If the key already exists, the node is
     * splayed to the root, and the tree remains unchanged.
     *
     * @param key The key to insert.
     */
    public void insert(int key) {
        // If the tree is empty, create a new root.
        if (root == null) {
            root = new Node(key);
            return;
        }

        // Splay the tree around the key. This brings the node with the key (if it exists)
        // or the would-be parent to the root.
        root = splay(root, key);

        // If the key is already at the root, we're done.
        if (root.key == key) {
            return;
        }

        // Insert the new node as the new root.
        Node newNode = new Node(key);
        if (key < root.key) {
            newNode.right = root;
            newNode.left = root.left;
            root.left = null; // Detach the old left subtree
        } else { // key > root.key
            newNode.left = root;
            newNode.right = root.right;
            root.right = null; // Detach the old right subtree
        }
        root = newNode;
    }

    /**
     * Deletes a key from the tree. If the key is found and deleted, the tree is
     * re-structured by splaying.
     *
     * @param key The key to delete.
     */
    public void delete(int key) {
        if (root == null) {
            return;
        }

        // Splay the tree around the key.
        root = splay(root, key);

        // If the key is not at the root after splaying, it's not in the tree.
        if (root.key != key) {
            return;
        }

        // The node to delete is now the root.
        Node leftSubtree = root.left;
        Node rightSubtree = root.right;

        if (leftSubtree == null) {
            // If there's no left subtree, the right subtree becomes the new tree.
            root = rightSubtree;
        } else {
            // Find the maximum element in the left subtree.
            Node maxNode = leftSubtree;
            while (maxNode.right != null) {
                maxNode = maxNode.right;
            }
            // Splay the left subtree around its maximum element. This makes the max
            // element the root of the left subtree, and it will have no right child.
            leftSubtree = splay(leftSubtree, maxNode.key);

            // Attach the original right subtree as the right child of the new root.
            leftSubtree.right = rightSubtree;
            root = leftSubtree;
        }
    }
}