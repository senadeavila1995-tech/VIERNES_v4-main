"""
VIERNES_v4 - RUNTIME REGRESSION SUITE
"""

import subprocess
import sys
import os


ROOT = os.getcwd()


TESTS = [
    (
        "test_multi_fk_runtime.py",
        None,
    ),

    (
        "test_multi_fk_fastapi_runtime.py",
        [
            "workspace/multi_fk_test/src",
            "workspace/multi_fk_test/src/backend",
        ],
    ),

    (
        "test_multi_fk_nullable_runtime.py",
        [
            "workspace/multi_fk_nullable_runtime_test/src",
            "workspace/multi_fk_nullable_runtime_test/src/backend",
        ],
    ),

    (
        "test_multi_fk_nullable_mysql_runtime.py",
        [
            "workspace/multi_fk_nullable_runtime_test/src",
            "workspace/multi_fk_nullable_runtime_test/src/backend",
        ],
    ),

    (
        "test_relationship_api_runtime.py",
        None,
    ),
]


print("=" * 80)
print("VIERNES_v4 RUNTIME REGRESSION SUITE")
print("=" * 80)


failed = []


for test, paths in TESTS:

    print()
    print("=" * 80)
    print("EJECUTANDO:", test)
    print("=" * 80)


    env = os.environ.copy()


    if paths:

        env["PYTHONPATH"] = ":".join(
            paths
        )


    result = subprocess.run(
        [
            sys.executable,
            test,
        ],
        env=env,
    )


    if result.returncode != 0:

        failed.append(test)

        print()
        print("ERROR:", test)



print()
print("=" * 80)


if failed:

    print("REGRESIONES FALLIDAS:")

    for item in failed:
        print("-", item)

    sys.exit(1)


else:

    print("TODAS LAS REGRESIONES PASARON")
    print("=" * 80)
