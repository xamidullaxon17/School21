import pstats

def analyze_profiling():
    stats = pstats.Stats("profiling-tottime.prof")
    stats.strip_dirs().sort_stats("cumulative").print_stats(5)

if __name__ == "__main__":
    analyze_profiling()
