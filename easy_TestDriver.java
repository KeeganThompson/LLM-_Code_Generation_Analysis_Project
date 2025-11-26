public class easy_TestDriver {

    public static boolean checkSearch(Object result) {
        return result != null;
    }

    public static void runEasyTests(SplayTree tree) {
        
        if (tree.search(10) != null) throw new RuntimeException("Logical Error: Search returned non-null on empty tree.");

        tree.insert(10);
        tree.insert(20); 
        tree.insert(5); 

        if (tree.search(20) == null) throw new RuntimeException("Logical Error: Key 20 not found after insertion.");

        tree.delete(5);
        if (tree.search(5) != null) throw new RuntimeException("Logical Error: Key 5 found after deletion.");

        tree.delete(20);
        if (tree.search(20) != null) throw new RuntimeException("Logical Error: Root key 20 found after deletion.");
        
        tree.delete(10);
        if (tree.search(10) != null) throw new RuntimeException("Logical Error: Tree not empty after all deletions.");
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
            
            runEasyTests(tree);
            
            int N = 10000;
            int M = 500000;
            int MIN_KEY = 1;
            
            runEfficiencyTest(tree, N, M, MIN_KEY);
            
            System.out.println("TEST_PASSED");
            
        } catch (Throwable t) {
            System.out.println("TEST_FAILED: " + t.getMessage());
            System.out.println("Execution time in ms: 0"); 
        }
    }
}