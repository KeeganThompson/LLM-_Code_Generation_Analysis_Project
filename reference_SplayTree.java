public class reference_SplayTree
 {
     private SplayNode root;
     private int count = 0;
 
     public reference_SplayTree()
     {
         root = null;
     }
 
     public boolean isEmpty()
     {
         return root == null;
     }
     public void clear()
     {
         root = null;
         count = 0;
     }
 
     public void insert(int ele)
     {
         SplayNode z = root;
         SplayNode p = null;
         while (z != null)
         {
             p = z;
             if (ele > p.element)
                 z = z.right;
             else
                 z = z.left;
         }
         z = new SplayNode();
         z.element = ele;
         z.parent = p;
         if (p == null)
             root = z;
         else if (ele > p.element)
             p.right = z;
         else
             p.left = z;
         Splay(z);
         count++;
     }
     public void makeLeftChildParent(SplayNode c, SplayNode p)
     {
         if ((c == null) || (p == null) || (p.left != c) || (c.parent != p))
             throw new RuntimeException("WRONG");
 
         if (p.parent != null)
         {
             if (p == p.parent.left)
                 p.parent.left = c;
             else 
                 p.parent.right = c;
         }
         if (c.right != null)
             c.right.parent = p;
 
         c.parent = p.parent;
         p.parent = c;
         p.left = c.right;
         c.right = p;
     }
 
     public void makeRightChildParent(SplayNode c, SplayNode p)
     {
         if ((c == null) || (p == null) || (p.right != c) || (c.parent != p))
             throw new RuntimeException("WRONG");
         if (p.parent != null)
         {
             if (p == p.parent.left)
                 p.parent.left = c;
             else
                 p.parent.right = c;
         }
         if (c.left != null)
             c.left.parent = p;
         c.parent = p.parent;
         p.parent = c;
         p.right = c.left;
         c.left = p;
     }
 
     private void Splay(SplayNode x)
     {
         while (x.parent != null)
         {
             SplayNode Parent = x.parent;
             SplayNode GrandParent = Parent.parent;
             if (GrandParent == null)
             {
                 if (x == Parent.left)
                     makeLeftChildParent(x, Parent);
                 else
                     makeRightChildParent(x, Parent);                 
             } 
             else
             {
                 if (x == Parent.left)
                 {
                     if (Parent == GrandParent.left)
                     {
                         makeLeftChildParent(Parent, GrandParent);
                         makeLeftChildParent(x, Parent);
                     }
                     else 
                     {
                         makeLeftChildParent(x, x.parent);
                         makeRightChildParent(x, x.parent);
                     }
                 }
                 else 
                 {
                     if (Parent == GrandParent.left)
                     {
                         makeRightChildParent(x, x.parent);
                         makeLeftChildParent(x, x.parent);
                     } 
                     else 
                     {
                         makeRightChildParent(Parent, GrandParent);
                         makeRightChildParent(x, Parent);
                     }
                 }
             }
         }
         root = x;
     }
 
     public void delete(int ele)
     {
         SplayNode node = findNode(ele);
        delete(node);
     }
 
     private void delete(SplayNode node)
     {
         if (node == null)
             return;
 
         Splay(node);
         if( (node.left != null) && (node.right !=null))
         { 
             SplayNode min = node.left;
             while(min.right!=null)
                 min = min.right;
 
             min.right = node.right;
             node.right.parent = min;
             node.left.parent = null;
             root = node.left;
         }
         else if (node.right != null)
         {
             node.right.parent = null;
             root = node.right;
         } 
         else if( node.left !=null)
         {
             node.left.parent = null;
             root = node.left;
         }
         else
         {
             root = null;
         }
         node.parent = null;
         node.left = null;
         node.right = null;
         node = null;
         count--;
     }
 
     public int countNodes()
     {
         return count;
     }
 
     public boolean search(int val)
     {
         return findNode(val) != null;
     }
 
     private SplayNode findNode(int ele)
     {
    	SplayNode PrevNode = null;
        SplayNode z = root;

        if (z == null) {
            return null;
        }
            while (z != null)
        {
        	 PrevNode = z;
             if (ele > z.element)
                 z = z.right;
             else if (ele < z.element)
                 z = z.left;
             else if(ele == z.element) {
                 Splay(z);
                 return z;
             }
 
         }
         if(PrevNode != null)
         {
             Splay(PrevNode);
             return null;
         }
         return null;
     }
 
     public void inorder()
     {
         inorder(root);
     }
     private void inorder(SplayNode r)
     {
         if (r != null)
         {
             inorder(r.left);
             System.out.print(r.element +" ");
             inorder(r.right);
         }
     }
 
     public void preorder()
     {
         preorder(root);
     }
     private void preorder(SplayNode r)
     {
         if (r != null)
         {
             System.out.print(r.element +" ");
             preorder(r.left);             
             preorder(r.right);
         }
     }
 
     public void postorder()
     {
         postorder(root);
     }
     private void postorder(SplayNode r)
     {
         if (r != null)
         {
             postorder(r.left);             
             postorder(r.right);
             System.out.print(r.element +" ");
         }
     }   
     private static reference_SplayTree splayTree = new reference_SplayTree();

    public static void main(String[] args) {

        int N = Integer.parseInt(args[0]);
        int M = Integer.parseInt(args[1]);
        int MIN_KEY = Integer.parseInt(args[2]);

        long startTime = System.currentTimeMillis();

        for (int i = MIN_KEY; i < N + MIN_KEY; i++) {
            splayTree.insert(i);
        }

        for (int i = 0; i < M; i++) {
            splayTree.search(MIN_KEY);
        }

        long endTime = System.currentTimeMillis();
        long duration = endTime - startTime;

        System.out.println("Execution time in ms: " + duration); 
    }
 }