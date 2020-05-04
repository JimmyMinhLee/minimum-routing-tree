## CS 170 Project Spring 2020 (Srishti, Jimmy, CJ)

# How to run:
We used a lot of different approaches throughout the project and the code in the latest
push is the newest iteration.

If you want to see all of the changes we've made along the way, you're going to
need to run through the branches and run the solvers.

However, the solver and experimental solver we have here are the two best
output solvers that we have. 'solver.py' will do a simulated annealing approach
to finding the solution tree, based on the dominating set and the L.A.S.T.
defined in the research papers cited in 'research.py'. 'experimental_solver.py'
tries to use the steiner tree approximation given by networkx to find a solution
tree. We ran this last because it was the last idea that came up to us.

If you want to run a quick file that approximates our solutions, run 'quick_solver.py'.
This just uses the L.A.S.T. algorithm we found on all of the inputs, without
using simulated annealing. This gives a pretty good rough approximate to the solutions
we have but is much quicker. For the majority of our outputs, this was the algorithm
that found the answer anyways, and is representative of the final score we got.

To run 'solver.py', you'll need to install the simulated annealing library
for python. 'experimental_solver.py' and 'quick_solver.py' don't use this approach and will run
just as long as you have networkx. In all three of these, we only rewrite the output
file if we found a solution cost better than the one we already had. 

'''
python -m pip install simanneal
python solver.py \\inputs
python experimental_solver.py \\inputs
'''

Do note that the original 'solver.py' will take a while to run. We approximated
the original simulated annealing settings so that it would run for about
a minute on each input, which might be better given your computer's specs,
but would be very infeasible to run on all inputs otherwise. You can run it
and end the script to see what the general approximation cost is.

'experimental_solver.py' and 'quick_solver.py' will run a lot more quickly.

We also used some variation of SPT/MST at some point during the project, but
we simply ran 'experimental_solver.py' with the SPT/MST being constructed
using the functions 'get_spt_tree' and 'get_mst' as defined in 'userutils.py'.
In all of these cases, we call 'repeated_pruning' that uses 'prune' as a subroutine
to prune the output graph until we had the smallest tree that 'is_valid_network'
still returned True on. These are also defined in 'userutils.py'.

All of the other miscellaneous functions in 'userutils.py' helped us
implement our annealer, make construction of the trees easier or outright
constructed the trees using networkx's algorithms, or were used in some approach
that was scrapped as we moved along with the project. Some are left unimplemented
I think because we just never got to trying out the idea.

'testsuite.py' in 'old_files' are all of the tests we had to make sure
that the functions defined worked properly. We just made a small graph of size
6 and ran the functions on it, printing out the results and checking by hand
if it was the correct output.

'local.py' and 'local_mac.py' were our local testing environments, where we'd run a certain approach
or a combination of them on a specific input to see how well it would do. We
primarily used them to try and better certain outputs if we were scoring badly
by messing around with 'find_last' and it's alpha parameter, while running
annealing on the initial tree solution and also the final tree.

'research.py' outlines the research papers we found and the pseudocode that they
had. We implemented them in there, would test it in 'local_research.py' and then
moved it to 'userutils.py' when we were happy with it. I think we really only
used the code from 'find_last' as we couldn't really figure out how to
fully implement the 'find_lart' and 'remove_bad' methods. The file includes
the title of the article or a link to the research paper.
