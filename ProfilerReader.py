import pstats

# Open a file to write the output
with open('sorted_output.txt', 'w') as f:
    p = pstats.Stats('profiler_output', stream=f)
    
    # Sort and write the stats by cumulative time
    p.sort_stats('cumulative').print_stats()
    
    # Write the top 20 most time-consuming functions
    p.sort_stats('cumulative').print_stats(20)
    
    # Sort and write by time spent within each function
    p.sort_stats('time').print_stats()
    
    # Show only functions with more than 5 calls
    p.print_stats('5')
