import cProfile
import pstats
import ui

if __name__ == '__main__':
    profiler = cProfile.Profile()
    profiler.runctx('ui.main()', globals(), locals())