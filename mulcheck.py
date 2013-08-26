#!/usr/bin/env python

import numpy as np
import sys
import getopt
from random import randint
import time

from randomized_algorithm import randomized_algorithm

options = {}


def ndim_random_array(ndim):

    global options

    _min = options['min_value'] or 0
    _max = options['max_value'] or 1
    return np.reshape([randint(_min, _max) for i in [1]*(ndim*ndim)],
                      (ndim, ndim))


def corrupt(C):

    global options

    corruptions = options['corruptions']
    R = C.copy()

    corrupted = []
    for i in range(0, corruptions):

        _i = randint(0,C.shape[0]-1)
        _j = randint(0,C.shape[1]-1)
        while (_i, _j) in corrupted:
            _i = randint(0,C.shape[0]-1)
            _j = randint(0,C.shape[1]-1)

        R[_i][_j] += 1
        corrupted.append((_i, _j))

    return R


def usage():

    print """\
Usage: %s -n # [-i # | -c # | -k # ] [options]
Options:
   -n, --ndim : array size
   -i, --iter : number of iterations (default is 10)
   -k         : number of randomized algorithm iterations (default is 1)
   -c, --corruptions : number of corruptions (default is 1)
       --min         : minimum value (default is 0)
       --max         : maximal value (default is 1)
""" % sys.argv[0]


def main():

    global options

    try:
        opts, args = getopt.getopt(sys.argv[1:],
                                   "ho:vn:i:c:k:",
                                   ["help", "output=", "ndim=", "--iter=", "--corruptions"])
    except getopt.GetoptError as err:
        # print help information and exit:
        print str(err)  # will print something like "option -a not recognized"
        usage()
        sys.exit(2)

    output = None
    verbose = False
    ndim = None
    k = 1 # randomized algorithm iterations

    corruptions = 1
    iterations = 10  # 10
    min_value = 0
    max_value = 1

    for o, a in opts:
        if o == "-v":
            verbose = True
        elif o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-o", "--output"):
            output = a
        elif o in ("-n", "--ndim"):
            ndim = int(a)
        elif o in ("-i", "--iter"):
            iterations = int(a)
        elif o in ("-c", "--corruptions"):
            corruptions = int(a)
        elif o in ("-k",):
            k = int(a)
        else:
            assert False, "unhandled option"

    if not ndim:
        usage()
        sys.exit(2)

    options['corruptions'] = corruptions
    options['min_value'] = min_value
    options['max_value'] = max_value
    options['verbose'] = verbose
    options['iterations'] = iterations
    options['ndim'] = ndim
    options['output'] = output
    options['k'] = k

    fail_counter = 0
    check_all_time = 0.0
    check_rand_time = 0.0
    for i in range(1, iterations+1):

        A = ndim_random_array(ndim)
        B = ndim_random_array(ndim)
        C = A.dot(B)

        t0 = time.time()
        (A.dot(B) == C)
        dt = time.time()-t0
        check_all_time += dt

        _C = corrupt(C)  # small changes to C

        t0 = time.time()
        r = randomized_algorithm(A, B, _C, k)
        dt = time.time()-t0
        check_rand_time += dt

        if r is True:
            fail_counter += 1

    check_all_time /= i
    check_rand_time /= i
    print "Summary"
    print "======="
    print
    print "Parameters:"
    print "\t [*] Array Shape: %dx%d" % (ndim,ndim)
    print "\t [*] Iterations: %d" % iterations
    print "\t [*] Randomize Algorithm Iterations: %d" % k
    print "\t [*] Corruptions: %d" % corruptions
    print "\t [*] Arrays minimum value: %d" % min_value
    print "\t [*] Arrays maximal value: %d" % max_value
    print
    print "Results:"
    print "\t [*] Check All Time Average: %f" % check_all_time
    print "\t [*] Check Rand Time Average: %f" % check_rand_time
    print
    print "The random algorithm was %d times of %d wrong (%2f %%)." % (fail_counter, i, 1.0*fail_counter/i*100)


if __name__ == "__main__":
    main()
