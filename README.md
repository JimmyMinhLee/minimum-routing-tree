## CS 170 Project Spring 2020 (Srishti, Jimmy, CJ)

# Describe the algorithm you used. Why do you think it was a good approach?
The final algorithm is an amalgamation of a lot of different things. We found a
research paper on the Lowest Approximate Spanning/Routing Tree, and the cost
for these solutions were very good. We applied simulated annealing to these
trees to hopefully find some randomness that improved the cost of the tree,
as well as using different initial solutions, mainly the dominating set
with shortest paths between the vertices, to plug in any holes that the LAST tree
couldn't fill - i.e. if the dominating set solution was better, we'd simply pick that.

We thought that this was a good approach since the initial solution cost of the LAST
tree was already desirable; applying simulated annealing to it gave it some
randomness that in some cases made the tree even better after we repeatedly pruned
the resulting tree. It took a little bit of the work off of us since we didn't
have to explicitly think about how else we'd improve on the approximation algorithm,
and just left it up to chance. The only drawback is that it takes a lot of time
to actually run the annealer, but the tradeoff in terms of stress on our headspace
was worth it.

# What other approaches did you try? How did they perform?
Initially, we used a simulated annealing on a variety of initial solutions:
the MST, SPT and dominating set with shortest paths. The issue was that
it was mainly left up to chance, and if we wanted accurate results, we'd have to
let the algorithm explore the solution space for ~ 15 minutes beforehand, and then
run the annealer simulation - which made it almost infeasible to run it on all inputs.
It took a whole day to run it on the 1000 graphs we were given, and that amounted to
about 8/9 hours even when we split up the inputs and ran them simultaneously.

The major breakthrough that we found was the research paper mentioned above that
gave an algorithm for finding the L.A.S.T. These trees did surprisingly well even
in the face of our dominating set approach in a lot less time; although, both the
dominating set annealing approach roughly converged to the L.A.S.T solutions if we
ran it long enough. The other breakthrough was realizing we could repeatedly prune
a graph. Initially, when I (Jimmy) made the pruning function, I only ran it on the MST's,
and pruning after the initial call made the graph invalid. It also could've been because
I was working with a test graph that was very sparse, as you can see in test.py, so
we chalked it up to only being able to prune once on a solution - which was wrong!
Being able to prune multiple times on a resulting solution made our costs ridiculously better,
which was nice. We went from rank ~65 with our annealing on the dominating set, to
rank ~30 with the L.A.S.T trees, and then up to rank ~24 with the repeated pruning approach.

# What computational resources did you use?
We made the solver.py able to run on any input directory, and we batched them so that
we could run multiple instances of the solver at once. "batched_inputs" is the
folder that we duplicated and ran our solver on. We initially wanted to use AWS's EC2 instances,
but we found that it ran into a lot of issues that were difficult to solve remotely,
so we ended up just having Jimmy run the inputs on his gaming laptop. We ran 4 instances
at all times, and the resulting time it took to complete the ~1000 inputs in this way
was about 2/3 hours. We could've done better in terms of computational time if we didn't run
the annealer, but we wanted to do so just to check if the randomness could've found any
better tree that just so happened to top the cost of our L.A.S.T.
