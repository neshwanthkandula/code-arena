from pathlib import Path

def load_testcases(problem_slug: str):
    problempath = Path(".\problems")
    base = problempath / problem_slug / "tests"
    print(base)
    inputs = sorted(base.glob("input*.txt"))
    outputs = sorted(base.glob("output*.txt"))

    if len(inputs) != len(outputs):
        raise ValueError("Testcase count mismatch")

    testcases = []
    for inp, out in zip(inputs, outputs):
        testcases.append({
            "input": inp.read_text(),
            "output": out.read_text().strip()
        })

    return testcases
