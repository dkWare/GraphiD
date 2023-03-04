import cProfile
import pstats
import sys

import test_script.test_file_explorer as file_explorer
import test_script.test_rectbutton as rectButton
import test_script.test_tictactoe as tictactoe

MODULES = [file_explorer, rectButton, tictactoe]
TEST_DATA_DIR = "test_data/"

def profile(function_name: str, profile_result_file: str) -> None:
    profiler = cProfile.Profile()
    profiler.runctx(function_name, globals(), locals())
    profiler.dump_stats(TEST_DATA_DIR + profile_result_file)

def main() -> None:
    print("Possible choices:")
    for module in MODULES:
        print(f" * {module.__name__}")
    print()

    profile_target = input("Profile target: ")
    profile_result_file = f"test_{profile_target.split('.', 1)[0]}.pro"
    profile(profile_target, profile_result_file)
    print(f"\nOutput in \"{TEST_DATA_DIR}{profile_result_file}\"")

if __name__ == '__main__':
    main()
