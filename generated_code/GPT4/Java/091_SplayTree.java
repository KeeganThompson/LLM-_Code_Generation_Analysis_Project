public class SplayTree {
    private class Node {
        int key;
        Node left, right, parent;

        Node(int key) {
            this.key = key;
        }
    }

    private Node root;

    // Right rotation
    private void rotateRight(Node x) {
        Node y = x.left;
        if (y == null) return;
        x.left = y.right;
        if (y.right != null)
            y.right.parent = x;
        y.parent = x.parent;
        if (x.parent == null)
            root = y;
        else if (x == x.parent.left)
            x.parent.left = y;
        else
            x.parent.right = y;
        y.right = x;
        x.parent = y;
    }

    // Left rotation
    private void rotateLeft(Node x) {
        Node y = x.right;
        if (y == null) return;
        x.right = y.left;
        if (y.left != null)
            y.left.parent = x;
        y.parent = x.parent;
        if (x.parent == null)
            root = y;
        else if (x == x.parent.left)
            x.parent.left = y;
        else
            x.parent.right = y;
        y.left = x;
        x.parent = y;
    }

    // Splay operation: brings x to the root
    private void splay(Node x) {
        if (x == null) return;
        while (x.parent != null) {
            if (x.parent.parent == null) {
                // Zig
                if (x.parent.left == x)
                    rotateRight(x.parent);
                else
                    rotateLeft(x.parent);
            } else if (x.parent.left == x && x.parent.parent.left == x.parent) {
                // Zig-Zig (left-left)
                rotateRight(x.parent.parent);
                rotateRight(x.parent);
            } else if (x.parent.right == x && x.parent.parent.right == x.parent) {
                // Zig-Zig (right-right)
                rotateLeft(x.parent.parent);
                rotateLeft(x.parent);
            } else if (x.parent.left == x && x.parent.parent.right == x.parent) {
                // Zig-Zag (left-right)
                rotateRight(x.parent);
                rotateLeft(x.parent);
            } else {
                // Zig-Zag (right-left)
                rotateLeft(x.parent);
                rotateRight(x.parent);
            }
        }
    }

    // Search for a key, splay the found node (or last accessed node)
    // Returns key if found, else null
    public Integer search(int key) {
        Node x = root;
        Node last = null;
        while (x != null) {
            last = x;
            if (key < x.key)
                x = x.left;
            else if (key > x.key)
                x = x.right;
            else
                break;
        }
        if (last != null)
            splay(last);
        if (x != null && x.key == key)
            return x.key;
        return null;
    }

    // Insert a key if not present
    public void insert(int key) {
        if (root == null) {
            root = new Node(key);
            return;
        }
        Node x = root, parent = null;
        while (x != null) {
            parent = x;
            if (key < x.key)
                x = x.left;
            else if (key > x.key)
                x = x.right;
            else {
                splay(x); // Key already exists, splay it
                return;
            }
        }
        Node newNode = new Node(key);
        newNode.parent = parent;
        if (key < parent.key)
            parent.left = newNode;
        else
            parent.right = newNode;
        splay(newNode);
    }

    // Delete a key if present
    public void delete(int key) {
        if (root == null) return;
        Integer found = search(key);
        if (found == null) return; // Not found

        // Now root holds the node to delete
        Node left = root.left;
        Node right = root.right;

        if (left != null) left.parent = null;
        if (right != null) right.parent = null;

        // Remove root
        root = null;

        if (left == null) {
            root = right;
        } else {
            // Find the max node in left subtree
            Node max = left;
            while (max.right != null) max = max.right;
            splay(max); // Splay max to root of left subtree
            // Now max has no right child
            max.right = right;
            if (right != null) right.parent = max;
            root = max;
        }
    }

    // Optional: For testing, print tree (inorder)
    private void inorder(Node x) {
        if (x != null) {
            inorder(x.left);
            System.out.print(x.key + " ");
            inorder(x.right);
        }
    }

    // For testing purposes
    public void printInOrder() {
        inorder(root);
        System.out.println();
    }

    // Main method for simple testing
    public static void main(String[] args) {
        SplayTree set = new SplayTree();
        set.insert(10);
        set.insert(20);
        set.insert(5);
        set.insert(8);
        set.insert(15);
        set.printInOrder(); // Should print 5 8 10 15 20

        System.out.println(set.search(15)); // 15, moved to root
        set.printInOrder();

        set.delete(10);
        set.printInOrder(); // 5 8 15 20

        System.out.println(set.search(99)); // null
    }
}