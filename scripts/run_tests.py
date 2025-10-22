# scripts/run_tests.py
import os, csv, traceback
from typing import Any, Callable

# ---------- Problem specs ----------
PROBLEMS = [
    {
        "idx": 0,
        "id": "HumanEval_0",
        "func": "add",
        "tests": [
            (("a", 1, 2), 3),
            (("b", -5, 5), 0),
            (("c", 0, 0), 0),
            (("d", 10**6, 10**6), 2*10**6),
        ]
    },
    {
        "idx": 1,
        "id": "HumanEval_1",
        "func": "is_palindrome",
        "tests": [
            (("a", "racecar"), True),
            (("b", "RaceCar"), True),
            (("c", "A man, a plan, a canal: Panama!"), True),
            (("d", "hello"), False),
            (("e", ""), True),
        ]
    },
    {
        "idx": 2,
        "id": "HumanEval_2",
        "func": "factorial",
        "tests": [
            (("a", 0), 1),
            (("b", 1), 1),
            (("c", 5), 120),
            (("d", 8), 40320),
        ],
        "errors": [
            (("neg", -1), ValueError),
        ]
    },
    {
        "idx": 3,
        "id": "HumanEval_3",
        "func": "fib",
        "tests": [
            (("a", 0), 0),
            (("b", 1), 1),
            (("c", 2), 1),
            (("d", 10), 55),
            (("e", 20), 6765),
        ],
        "errors": [
            (("neg", -3), ValueError),
        ]
    },
    {
        "idx": 4,
        "id": "HumanEval_4",
        "func": "reverse_words",
        "tests": [
            (("a", "hello world"), "world hello"),
            (("b", "  multiple   spaces here  "), "here spaces multiple"),
            (("c", ""), ""),
            (("d", "one"), "one"),
        ]
    },
    {
        "idx": 5,
        "id": "HumanEval_5",
        "func": "sum_of_squares",
        "tests": [
            (("a", [1,2,3]), 14),
            (("b", []), 0),
            (("c", [-1,2,-3]), 14),
            (("d", [10**3]), 10**6),
        ]
    },
    {
        "idx": 6,
        "id": "HumanEval_6",
        "func": "flatten",
        "tests": [
            (("a", [1, [2, 3], 4]), [1,2,3,4]),
            (("b", [[[]]]), []),
            (("c", [1,[2,[3,[4]]]]), [1,2,3,4]),
            (("d", []), []),
            (("e", ["a", ["b", ["c"]]]), ["a","b","c"]),
        ]
    },
    {
        "idx": 7,
        "id": "HumanEval_7",
        "func": "count_vowels",
        "tests": [
            (("a", "hello"), 2),
            (("b", "xyz"), 0),
            (("c", "AEIOU"), 5),
            (("d", ""), 0),
            (("e", "quick brown fox"), 4),
        ]
    },
    # ✅ fixed: all outputs ascending
    {
        "idx": 8,
        "id": "HumanEval_8",
        "func": "max_product_pair",
        "tests": [
            (("a", [1,2,3]), (2,3)),
            (("b", [-10,-3,1,2]), (-10,-3)),
            (("c", [0, 100, -1, -2]), (-2,-1)),  # fixed order
            (("d", [5,5,2]), (5,5)),
        ],
        "errors": [
            (("short", [1]), ValueError),
        ]
    },
    {
        "idx": 9,
        "id": "HumanEval_9",
        "func": "remove_duplicates",
        "tests": [
            (("a", [1,1,2,2,3,1]), [1,2,3]),
            (("b", []), []),
            (("c", ["a","a","b","A"]), ["a","b","A"]),
        ]
    },
]

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GEN_DIR = os.path.join(ROOT, "generations", "HumanEval_X")
RESULTS_DIR = os.path.join(ROOT, "results")
os.makedirs(RESULTS_DIR, exist_ok=True)

# ✅ Distinct strategy handling
FAMILIES = [
    ("GPT5", "SCoT", os.path.join(GEN_DIR, "GPT5", "SCoT")),
    ("CLAUDE", "SCoT", os.path.join(GEN_DIR, "CLAUDE", "SCoT")),
    ("GPT5", "SelfDebug", os.path.join(GEN_DIR, "GPT5", "SelfDebug")),
    ("CLAUDE", "SelfDebug", os.path.join(GEN_DIR, "CLAUDE", "SelfDebug")),
    ("GPT5", "ReflectiveRefine", os.path.join(GEN_DIR, "GPT5", "ReflectiveRefine")),
    ("CLAUDE", "ReflectiveRefine", os.path.join(GEN_DIR, "CLAUDE", "ReflectiveRefine")),

]

def load_func_from_file(py_path: str, func_name: str) -> Callable[..., Any]:
    namespace = {}
    with open(py_path, "r", encoding="utf-8") as f:
        code = f.read()
    exec(compile(code, py_path, "exec"), namespace)
    if func_name not in namespace or not callable(namespace[func_name]):
        raise AttributeError(f"{func_name} not found in {py_path}")
    return namespace[func_name]

def run_problem_tests(func: Callable[..., Any], spec: dict):
    try:
        for (tag, *args), expected in spec["tests"]:
            out = func(*args)
            if out != expected:
                return False, f"Test {tag}: expected {expected!r}, got {out!r}"
        for (tag, *args), err_type in spec.get("errors", []):
            try:
                func(*args)
                return False, f"Test {tag}: expected {err_type.__name__}, but no error raised"
            except Exception as e:
                if not isinstance(e, err_type):
                    return False, f"Test {tag}: expected {err_type.__name__}, got {type(e).__name__}: {e}"
        return True, "OK"
    except Exception as e:
        return False, f"Runtime error: {type(e).__name__}: {e}\n{traceback.format_exc()}"

def discover_candidate_files(dir_path: str):
    files = {}
    if not os.path.isdir(dir_path):
        return files
    for name in os.listdir(dir_path):
        if name.startswith("sample_") and name.endswith(".py"):
            try:
                idx = int(name.split("_")[1].split(".")[0])
                files[idx] = os.path.join(dir_path, name)
            except:
                pass
    return files

def main():
    summary_rows = []
    overall_rows = []

    for fam, strategy, fam_dir in FAMILIES:
        cand = discover_candidate_files(fam_dir)
        passed_count = 0

        for spec in PROBLEMS:
            idx, pid, func_name = spec["idx"], spec["id"], spec["func"]
            py_path = cand.get(idx)

            if not py_path:
                summary_rows.append([pid, fam, strategy, idx, "MISSING", "", ""])
                continue

            ok, note = False, ""
            try:
                fn = load_func_from_file(py_path, func_name)
                ok, note = run_problem_tests(fn, spec)
            except Exception as e:
                ok, note = False, f"Load error: {e}"

            summary_rows.append([pid, fam, strategy, idx, "PASS" if ok else "FAIL", py_path, note])
            if ok:
                passed_count += 1

        total = len(PROBLEMS)
        pass_at_1 = passed_count / total
        overall_rows.append([fam, strategy, total, passed_count, f"{pass_at_1:.2f}"])

    # Write CSVs
    with open(os.path.join(RESULTS_DIR, "summary.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["problem_id", "family", "strategy", "problem_idx", "result", "file", "notes"])
        w.writerows(summary_rows)

    with open(os.path.join(RESULTS_DIR, "overall.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["family", "strategy", "total", "passed", "pass@1"])
        w.writerows(overall_rows)

    print("\n=== Overall pass@1 ===")
    for row in overall_rows:
        print(f"{row[0]:<8} {row[1]:<10} passed {row[3]}/{row[2]}  pass@1={row[4]}")
    print("\nWrote:")
    print(" - results/summary.csv")
    print(" - results/overall.csv")

if __name__ == "__main__":
    main()
