// SimpleTestRunner - custom test runner without JUnit dependencies
// Run with: java -cp bin SimpleTestRunner

import java.lang.reflect.Method;

public class SimpleTestRunner {

    private static int passed = 0;
    private static int failed = 0;
    private static int total = 0;

    public static void main(String[] args) throws Exception {
        System.out.println("=".repeat(60));
        System.out.println("CS1OP Simple Test Runner");
        System.out.println("=".repeat(60));
        System.out.println();

        runTests(GameTest.class);
        runTests(GameTestSuite.class);
        runTests(TestGameLogic.class);

        System.out.println();
        System.out.println("=".repeat(60));
        System.out.println("RESULTS: " + total + " tests, " + passed + " passed, " + failed + " failed");
        System.out.println("=".repeat(60));

        if (failed > 0) {
            System.exit(1);
        }
    }

    private static void runTests(Class<?> testClass) throws Exception {
        System.out.println("\n[Running " + testClass.getSimpleName() + "]");
        System.out.println("-".repeat(40));

        Object instance = testClass.getDeclaredConstructor().newInstance();
        for (Method method : testClass.getDeclaredMethods()) {
            if (method.getName().startsWith("test")) {
                total++;
                try {
                    method.invoke(instance);
                    System.out.println("  [PASS] " + method.getName());
                    passed++;
                } catch (Exception e) {
                    System.out.println("  [FAIL] " + method.getName() + " - " + e.getCause());
                    failed++;
                }
            }
        }
    }
}