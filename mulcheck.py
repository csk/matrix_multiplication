#!/usr/bin/env python

import numpy as np
import sys
import getopt
from random import randint

from randomized_algorithm import randomized_algorithm


def ndim_random_array(ndim):
    return np.reshape([randint(0, 2**8) for i in [1]*(ndim*ndim)],
                      (ndim, ndim))


def usage():

    print """\
    %s --ndim dimension
Options:
   -n, --ndim : number of dimensions for arrays
   -i, --iter : number of iterations
""" % sys.argv[0]


def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:],
                                   "ho:vn:i:",
                                   ["help", "output=", "ndim=", "--iter="])
    except getopt.GetoptError as err:
        # print help information and exit:
        print str(err)  # will print something like "option -a not recognized"
        usage()
        sys.exit(2)
    output = None
    verbose = False
    ndim = None
    iterations = 10  # 10

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
        else:
            assert False, "unhandled option"

    if not ndim:
        usage()
        sys.exit(2)

    fail_counter = 0
    for i in range(0, iterations):

        A = ndim_random_array(ndim)
        B = ndim_random_array(ndim)
        C = A.dot(B)

        r = randomized_algorithm(A, B, C)

        if r is False:
            fail_counter += 1

        print "[ %d / %d ] " % (fail_counter, i+1)


if __name__ == "__main__":
    main()
