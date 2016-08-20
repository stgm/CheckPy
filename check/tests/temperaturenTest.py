import test as t
import lib
import assertlib

@t.test
def matches(test):
    expected = ["96.8", "98.6", "99.5", "100.4", "102.2"]

    def testMethod(fileName):
        result = lib.outputOf(fileName)
        regex = ".*\["
        for i, answer in enumerate(expected):
            regex += answer.split(".")[0] + "\." + answer.split(".")[1] + (".*,.*" if i != len(expected) - 1 else ".*")
        regex += "\].*"
        testResult = assertlib.match(result, regex)
        return testResult, result
    test.test = testMethod
    
    test.description = lambda : "output contains all expected values"
    test.fail = lambda result : "output %s does not contain all expected values %s" %(result, str(expected))