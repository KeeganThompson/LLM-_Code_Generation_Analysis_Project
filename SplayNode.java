public class SplayNode
 {    
     SplayNode left, right, parent;
     int element;
 
     public SplayNode()
     {
         this(0, null, null, null);
     }          
     public SplayNode(int ele)
     {
         this(ele, null, null, null);
     } 
     public SplayNode(int ele, SplayNode left, SplayNode right, SplayNode parent)
     {
         this.left = left;
         this.right = right;
         this.parent = parent;
         this.element = ele;         
     }    
 }