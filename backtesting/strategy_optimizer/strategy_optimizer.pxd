# cython: language_level=3
#  Drakkar-Software OctoBot
#  Copyright (c) Drakkar-Software, All rights reserved.
#
#  This library is free software; you can redistribute it and/or
#  modify it under the terms of the GNU Lesser General Public
#  License as published by the Free Software Foundation; either
#  version 3.0 of the License, or (at your option) any later version.
#
#  This library is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#  Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public
#  License along with this library.

cdef class StrategyOptimizer:
    cdef bint is_properly_initialized
    cdef object logger
    cdef dict config
    cdef object trading_mode
    cdef object strategy_class
    cdef list run_results
    cdef dict sorted_results_by_time_frame
    cdef dict sorted_results_through_all_time_frame
    cdef list all_time_frames
    cdef list all_TAs
    cdef list risks
    cdef object current_test_suite
    cdef set errors
    cdef bint is_computing
    cdef int run_id
    cdef int total_nb_runs

    cpdef void find_optimal_configuration(self, list TAs=*, list time_frames=*, list risks=*)
    cpdef void print_report(self)
    cpdef int get_overall_progress(self)
    cpdef bint is_in_progress(self)
    cpdef int get_current_test_suite_progress(self)
    cpdef list get_report(self)
    cpdef list get_results(self)
    cpdef tuple get_current_progress(self)
    cpdef bint get_is_computing(self)
    cpdef object get_errors_description(self)

    cdef void _run_test_suite(self, dict config)
    cdef void _find_optimal_configuration_using_results(self)
