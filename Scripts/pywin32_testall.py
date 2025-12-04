"""A test runner for pywin32"""

import os
import site
import subprocess
import sys


project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
site_packages = [site.getusersitepackages()] + site.getsitepackages()

failures = []



def run_test(script, cmdline_extras):
    dirname, scriptname = os.path.split(script)
   
    cmd = [sys.executable, "-u", scriptname] + cmdline_extras
    print("--- Running '%s' ---" % script)
    sys.stdout.flush()
    result = subprocess.run(cmd, check=False, cwd=dirname)
    print(f"*** Test script '{script}' exited with {result.returncode}")
    sys.stdout.flush()
    if result.returncode:
        failures.append(script)


def find_and_run(possible_locations, extras):
    for maybe in possible_locations:
        if os.path.isfile(maybe):
            run_test(maybe, extras)
            break
    else:
        raise RuntimeError(
            "Failed to locate a test script in one of %s" % possible_locations
        )


def main():
    import argparse

    code_directories = [project_root] + site_packages

    parser = argparse.ArgumentParser(
        description="A script to trigger tests in all subprojects of PyWin32."
    )
    parser.add_argument(
        "-no-user-interaction",
        default=False,
        action="store_true",
        help="(This is now the default - use `-user-interaction` to include them)",
    )

    parser.add_argument(
        "-user-interaction",
        action="store_true",
        help="Include tests which require user interaction",
    )

    parser.add_argument(
        "-skip-adodbapi",
        default=False,
        action="store_true",
        help="Skip the adodbapi tests; useful for CI where there's no provider",
    )

    args, remains = parser.parse_known_args()

   

    extras = []
    if args.user_interaction:
        extras.append("-user-interaction")
    extras.extend(remains)
    scripts = [
        "win32/test/testall.py",
        "Pythonwin/pywin/test/all.py",
    ]
    for script in scripts:
        maybes = [os.path.join(directory, script) for directory in code_directories]
        find_and_run(maybes, extras)

  
    maybes = [
        os.path.join(directory, "win32com", "test", "testall.py")
        for directory in [os.path.join(project_root, "com")] + site_packages
    ]
    extras = remains + ["1"] 
    find_and_run(maybes, extras)

    
    if not args.skip_adodbapi:
        maybes = [
            os.path.join(directory, "adodbapi", "test", "adodbapitest.py")
            for directory in code_directories
        ]
        find_and_run(maybes, remains)
        
        maybes = [
            os.path.join(directory, "adodbapi", "test", "test_adodbapi_dbapi20.py")
            for directory in code_directories
        ]
        find_and_run(maybes, remains)

    if failures:
        print("The following scripts failed")
        for failure in failures:
            print(">", failure)
        sys.exit(1)
    print("All tests passed \\o/")


if __name__ == "__main__":
    main()

