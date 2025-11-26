public class medium_TestDriver {

    public static boolean checkSearch(Object result) {
        return result != null;
    }

    public static void runIntermediateComplexity(SplayTree tree) {
        
        if (tree.search(5) != null) throw new RuntimeException("Logical Error: Search returned non-null on an empty tree.");

        tree.insert(10); tree.insert(5); tree.insert(15); tree.insert(7); tree.insert(3); tree.insert(12);
        
        if (tree.search(5) == null) throw new RuntimeException("Logical Error: Key 5 not found after insertion.");
        
        tree.delete(10);
        if (tree.search(10) != null) throw new RuntimeException("Logical Error: Key 10 found after deletion.");

        if (tree.search(12) == null) throw new RuntimeException("Logical Error: Key 12 lost after complex splay.");

        tree.delete(5); tree.delete(7); tree.delete(15); tree.delete(3); tree.delete(12);
        if (tree.search(5) != null) throw new RuntimeException("Logical Error: Tree not empty after all deletions.");
    }
    
    public static void runEfficiencyTest(SplayTree tree, int N, int M, int MIN_KEY) {
        long startTime = System.currentTimeMillis();

        for (int i = MIN_KEY; i < N + MIN_KEY; i++) {
            tree.insert(i);
        }

        for (int i = 0; i < M; i++) {
            tree.search(MIN_KEY);
        }

        long endTime = System.currentTimeMillis();
        long duration = endTime - startTime;
        
        System.out.println("Execution time in ms: " + duration);
    }

    public static void main(String[] args) {
        
        try {
            SplayTree tree = new SplayTree();
            
            runIntermediateComplexity(tree);
            
            int N = 50000;
            int M = 1000000;
            int MIN_KEY = 1;
            runEfficiencyTest(tree, N, M, MIN_KEY);
            
            System.out.println("TEST_PASSED");
            
        } catch (Throwable t) {
            System.out.println("TEST_FAILED: " + t.getMessage());
            System.out.println("Execution time in ms: 0"); 
        }
    }
}