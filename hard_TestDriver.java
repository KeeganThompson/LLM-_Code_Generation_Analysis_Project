public class hard_TestDriver {

    public static boolean checkSearch(Object result) {
        return result != null;
    }

    public static void runHardTests(SplayTree tree) {
        tree.insert(10);
        tree.insert(20);
        if (tree.search(10) == null) throw new RuntimeException("Logical Error: Key 10 not found after insertion.");
        tree.delete(10);
        if (tree.search(10) != null) throw new RuntimeException("Logical Error: Key 10 found after deletion.");
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
            runHardTests(tree);
            
            int N = 200000;
            int M = 4000000;
            int MIN_KEY = 1;
            runEfficiencyTest(tree, N, M, MIN_KEY);
            
            System.out.println("TEST_PASSED");
            
        } catch (Throwable t) {
            System.out.println("TEST_FAILED: " + t.getMessage());
            System.out.println("Execution time in ms: 0"); 
        }
    }
}