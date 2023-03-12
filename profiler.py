from GraphiD.debugger import logger as dbg
dbg.debug("LOAD INTERN MODULES", extra={'classname': ''})

import colorama
colorama.init()
from colorama import Fore, Style

import cProfile
import pstats

import os
import sys


#modules to profile
dbg.debug("LOAD USER MODULES", extra={'classname': ''})
import test_script.test_file_explorer as test_file_explorer
import test_script.test_rectbutton as test_rectbutton
import test_script.test_tictactoe as test_tictactoe
import test_script.test_minimal as test_minimal
dbg.debug("FINISH LOADING INTERN MODULES", extra={'classname': ''})


#settings to register module import it like the others above
#and add it to this tuple
MODULES = (test_file_explorer, test_rectbutton, test_tictactoe, test_minimal)

#the default path for the profiling results
TEST_DATA_DIR = "test_data/"

#this will be generated automatically
dbg.debug("PREPARING MODULE INFORMATION'S", extra={'classname': ''})
MODULES_NAMES = [m.__name__.split(".", 1)[1] for m in MODULES]
MODULE_DICT = {MODULES_NAMES[i]: MODULES[i] for i in range(len(MODULES))}
dbg.debug("FINISHED PREPARING MODULE INFORMATION'S", extra={'classname': ''})
dbg.debug(f"MODULES LOADED: {MODULES_NAMES}", extra={'classname':''})
dbg.debug(f"MODULES LOADED: {MODULE_DICT}", extra={'classname':''})

def profile(function_name: str, profile_result_file: str) -> None:
    profiler = cProfile.Profile()
    profiler.runctx(function_name, globals(), locals())
    profiler.dump_stats(profile_result_file)

def generate_output_file_path(test_data_dir: str, profiling_target_module: str) -> str:
    if not profiling_target_module.startswith("test_"):
        profiling_target_module = "test_" + profiling_target_module
    file_path = os.path.join(test_data_dir, profiling_target_module)
    file_path += ".pro"
    return file_path

def color_input(prompt):
    print(f"{Fore.CYAN}{prompt}{Fore.MAGENTA}", end="")
    answer = input()
    print(f"{Fore.RESET}\n", end="")
    return answer

def chose_output_path(profile_target_function: str, profiling_target_module: str) -> str:
    #set default file path
    profile_result_file = generate_output_file_path(TEST_DATA_DIR, profiling_target_module)

    #ask i user wants to ue different name
    new_profiling_result_file = color_input(f"OUTPUT <{profile_result_file}> (enter new path or leave plank to use this): ")

    #user uses different path
    if new_profiling_result_file != "":
        profile_result_file = new_profiling_result_file

    return profile_result_file

def chose_profiling_target() -> str:
    profile_target_function = ""
    while True:
        #get the target function to start the profiling
        if profile_target_function.endswith("#overwrite"):
            profile_target_function = profile_target_function.removesuffix("#overwrite")
        else:
            profile_target_function = color_input("Profile target: ")

        #get only the name of the target module
        profiling_target_split = profile_target_function.split(".", 1)
        if "" in profiling_target_split:
            profiling_target_split.remove("")

        if len(profiling_target_split) != 2:
            dbg.error(f"check your target function, there might be an syntax error: {profile_target_function}", extra={'classname':''})
            continue

        profiling_target_module = profiling_target_split[0]
        profile_target_function_name = profiling_target_split[1]

        #check if the module exists/is registered to profiling
        module_exists = False
        for module_name in MODULES_NAMES:
            if profiling_target_module == module_name:
                #module exists/is registered
                module_exists = True
                break

        if not module_exists:
            dbg.error(f"your requested profiling target module doesn't exists: {profiling_target_module}", extra={'classname':''})
            continue

        profiling_module_obj = MODULE_DICT.get(profiling_target_module)
        if profiling_module_obj is None:
            dbg.error(f"your requested profiling target module doesn't exists: {profiling_target_module}", extra={'classname':''})
            continue

        profile_target_function_name_clean = profile_target_function_name.removeprefix(".").removesuffix("()")
        if not hasattr(profiling_module_obj, profile_target_function_name_clean):
            dbg.error(f"the testing module: {profiling_target_module} has no function/method called: {profile_target_function_name}", extra={'classname':''})
            continue

        if not profile_target_function.endswith("()"):
            dbg.warning(f"your not calling the target function, this still profiles something but its very likely that that is not what you want.\nenter anything to change it or leave it plank to continue!:\nadd #+ to the begin to only add something to the target\ncurrently: {profile_target_function}", extra={'classname':''})
            overwrite = color_input("change: ")
            if overwrite != "":
                if overwrite.startswith("#+"):
                    profile_target_function += overwrite.removeprefix("#+")
                else:
                    profile_target_function = overwrite
                profile_target_function += "#overwrite"
                continue
        return profile_target_function, profiling_target_module

def setup_profiling() -> None:
    dbg.info("Possible choices:", extra={'classname':''})
    for module in MODULES:
        dbg.info(f" * {module.__name__}", extra={'classname':''})

    profile_target_function, profiling_target_module = chose_profiling_target()
    profile_result_path = chose_output_path(profile_target_function, profiling_target_module)

    profile(profile_target_function, profile_result_path)
    dbg.info(f"\nOutput in \"{profile_result_path}\"", extra={'classname':''})

def title() -> None:
    print("\n\n\033[32m░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░")
    print("░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░")
    print("░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█▀█░█▀▄░█▀█░█░█░▀█▀░█░░░█▀▀░█▀▄░░░█░█░▀█░░░░░▄▀▄░░░░▀▀▄░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░")
    print("░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█▀▀░█▀▄░█░█░▀▄▀░░█░░█░░░█▀▀░█▀▄░░░▀▄▀░░█░░░░░█/█░░░░▄▀░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░")
    print("░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀░░░▀░▀░▀▀▀░░▀░░▀▀▀░▀▀▀░▀▀▀░▀░▀░░░░▀░░▀▀▀░▀░░░▀░░▀░░▀▀▀░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░")
    print("░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░")
    print("░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░")
    print("░░░░░░░░░░██▄░▀▄▀░░░█▀▄░▄▀▄░█▄▒▄█░█░█▄░█░█░█▄▀░░░█▄▀▒█▀▄▒██▀░█▄░█░█▄░█░░░░░░░█▀█░█▄░░░█▀█░▀██░░░▀█░█▀█░▀█░▀██░░░░░░░░░░░░░░░░░░")
    print("░░░░░░░░░░█▄█░▒█▒▒░▒█▄▀░▀▄▀░█▒▀▒█░█░█▒▀█░█░█▒█▒░░█▒█░█▀▄░█▄▄░█▒▀█░█▒▀█▒░▒░▒░░█▄█░▄█░▄░█▄█░▄▄█░▄░█▄░█▄█░█▄░▄▄█░░░░░░░░░░░░░░░░░░")
    print("░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░")
    print("░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░\033[0m\n\n")

def main() -> None:
    title()
    setup_profiling()

if __name__ == '__main__':
    main()
