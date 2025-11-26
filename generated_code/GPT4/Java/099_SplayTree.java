public class SplayTree {
    private class Node {
        int key;
        Node left, right, parent;

        Node(int key, Node parent) {
            this.key = key;
            this.parent = parent;
        }
    }

    private Node root;

    /** Inserts the key into the set. Duplicates are ignored. */
    public void insert(int key) {
        if (root == null) {
            root = new Node(key, null);
            return;
        }

        Node curr = root, parent = null;
        while (curr != null) {
            parent = curr;
            if (key < curr.key) {
                curr = curr.left;
            } else if (key > curr.key) {
                curr = curr.right;
            } else {
                // Duplicate key, do nothing
                splay(curr);
                return;
            }
        }

        Node newNode = new Node(key, parent);
        if (key < parent.key) {
            parent.left = newNode;
        } else {
            parent.right = newNode;
        }
        splay(newNode);
    }

    /** Deletes the key from the set, if present. */
    public void delete(int key) {
        Node node = findNode(key);
        if (node == null) {
            return;
        }
        splay(node);

        if (node.left == null) {
            replace(node, node.right);
        } else if (node.right == null) {
            replace(node, node.left);
        } else {
            Node min = subtreeMin(node.right);
            if (min.parent != node) {
                replace(min, min.right);
                min.right = node.right;
                if (min.right != null) min.right.parent = min;
            }
            replace(node, min);
            min.left = node.left;
            if (min.left != null) min.left.parent = min;
        }
    }

    /** Searches for the key. Splays the accessed node to root if found.
     *  @return Integer key if found, else null.
     */
    public Integer search(int key) {
        Node node = findNode(key);
        if (node != null) {
            splay(node);
            return node.key;
        }
        return null;
    }

    // Helper: Find node with key
    private Node findNode(int key) {
        Node curr = root, last = null;
        while (curr != null) {
            last = curr;
            if (key < curr.key)
                curr = curr.left;
            else if (key > curr.key)
                curr = curr.right;
            else
                return curr;
        }
        return null;
    }

    // Helper: Replace node u with node v in tree
    private void replace(Node u, Node v) {
        if (u.parent == null) {
            root = v;
        } else if (u == u.parent.left) {
            u.parent.left = v;
        } else {
            u.parent.right = v;
        }
        if (v != null)
            v.parent = u.parent;
    }

    // Helper: Subtree min node
    private Node subtreeMin(Node node) {
        while (node.left != null)
            node = node.left;
        return node;
    }

    // Splay operation: moves node x to root
    private void splay(Node x) {
        if (x == null) return;
        while (x.parent != null) {
            Node p = x.parent;
            Node g = p.parent;
            if (g == null) {
                // Zig
                if (x == p.left)
                    rotateRight(p);
                else
                    rotateLeft(p);
            } else if (x == p.left && p == g.left) {
                // Zig-Zig
                rotateRight(g);
                rotateRight(p);
            } else if (x == p.right && p == g.right) {
                // Zig-Zig
                rotateLeft(g);
                rotateLeft(p);
            } else if (x == p.right && p == g.left) {
                // Zig-Zag
                rotateLeft(p);
                rotateRight(g);
            } else if (x == p.left && p == g.right) {
                // Zig-Zag
                rotateRight(p);
                rotateLeft(g);
            }
        }
    }

    // Rotate x to left
    private void rotateLeft(Node x) {
        Node y = x.right;
        if (y == null) return;
        x.right = y.left;
        if (y.left != null)
            y.left.parent = x;
        y.parent = x.parent;
        if (x.parent == null) {
            root = y;
        } else if (x == x.parent.left) {
            x.parent.left = y;
        } else {
            x.parent.right = y;
        }
        y.left = x;
        x.parent = y;
    }

    // Rotate x to right
    private void rotateRight(Node x) {
        Node y = x.left;
        if (y == null) return;
        x.left = y.right;
        if (y.right != null)
            y.right.parent = x;
        y.parent = x.parent;
        if (x.parent == null) {
            root = y;
        } else if (x == x.parent.left) {
            x.parent.left = y;
        } else {
            x.parent.right = y;
        }
        y.right = x;
        x.parent = y;
    }

    // Optional: For debugging
    @Override
    public String toString() {
        StringBuilder sb = new StringBuilder();
        inorder(root, sb);
        return sb.toString();
    }

    private void inorder(Node node, StringBuilder sb) {
        if (node == null) return;
        inorder(node.left, sb);
        sb.append(node.key).append(" ");
        inorder(node.right, sb);
    }

    // --- For testing purposes ---
    public static void main(String[] args) {
        SplayTree set = new SplayTree();
        set.insert(10);
        set.insert(20);
        set.insert(5);
        set.insert(7);
        set.insert(15);
        System.out.println("Tree: " + set); // Should print 5 7 10 15 20

        System.out.println("Search 7: " + set.search(7)); // 7, splayed to root
        System.out.println("Tree: " + set);

        set.delete(10);
        System.out.println("After deleting 10: " + set);

        System.out.println("Search 100: " + set.search(100)); // null
        set.insert(10);
        System.out.println("After re-inserting 10: " + set);
    }
}