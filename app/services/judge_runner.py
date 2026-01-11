from app.services.judge0 import run_code
from app.services.test_loader import load_testcases

async def judge_problem(problem_slug, source_code, language_id):
    testcases = load_testcases(problem_slug)
    print("tescases", testcases)
    for index,tc in enumerate(testcases, start=1):
        result = await run_code(source_code, language_id, tc["input"])
        print("judge0 result:", result)
        stdout = (result.get("stdout") or "").strip()
        expected = tc["output"]

        print("judge0 :-" , stdout)
        if(stdout != expected):
            return {
                "verdict" : "Wrong Answer",
                "failed_test" : index,
                "expected" : expected,
                "actual" : stdout
            }
        

        if(result["status"]["description"]!= "Accepted"):
                return {
                "verdict": result["status"]["description"],
                "failed_test": index
            }
        

    return {
        "verdict" : "Accepted",
        "total_tests" : len(testcases)
    }