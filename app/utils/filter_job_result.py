def get_first_subset_that_satisfies_sum(jobs, max_value, sub_jobs=[]):
    expexted_time_in_hours_to_finish_summed = sum(int(job.get('expexted_time_in_hours_to_finish')) for job in sub_jobs)
    if expexted_time_in_hours_to_finish_summed == max_value:
        return sub_jobs
    if expexted_time_in_hours_to_finish_summed >= max_value:
        return

    for index, value in enumerate(jobs):
        remaining = jobs[index + 1:]
        result = get_first_subset_that_satisfies_sum(remaining, max_value, sub_jobs + [value])
        if result:
            return result


def get_result_filtered(jobs: list):
    # Returns a list of sublists that the sum of its elements is less or equal 8.

    # Parameters:
    #    jobs (list): A list of jobs

    # Returns:
    #    grouped_jobs_by_window_time(list):The expected list asked in the test project.
    grouped_jobs_by_window_time = []
    while len(jobs) > 1:
        subset = get_first_subset_that_satisfies_sum(jobs, 8)
        if subset:
            sorted_sub_list = sorted(subset, key=lambda k: k['maximum_date_finish'])
            grouped_jobs_by_window_time.append(sorted_sub_list)
            for item in sorted_sub_list:
                jobs.remove(item)
        else:
            for item in jobs:
                grouped_jobs_by_window_time.append([item])
            break
    return sorted(grouped_jobs_by_window_time, key=lambda x: x[0].get('maximum_date_finish'))

