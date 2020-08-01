def get_first_subset_that_satisfies_sum(jobs, max_value):
    aggregated = 0
    sub_jobs = []
    while aggregated < 8:
        try:
            value = next((job for job in jobs if
                          job.get('expexted_time_in_hours_to_finish') + aggregated == max_value),
                         next(job for job in jobs if
                              job.get('expexted_time_in_hours_to_finish') + aggregated < max_value))
            sub_jobs.append(value)
            jobs.remove(value)
            aggregated += sum([job.get('expexted_time_in_hours_to_finish') for job in sub_jobs])
        except:
            break
    return sub_jobs


def get_result_filtered(jobs: list):
    grouped_jobs_by_window_time = []
    while jobs:
        subset = get_first_subset_that_satisfies_sum(jobs, 8)
        if subset:
            grouped_jobs_by_window_time.append(sorted(subset, key=lambda k: k['maximum_date_finish']))
        else:
            grouped_jobs_by_window_time.append(jobs.copy())
            for job in jobs.copy():
                jobs.remove(job)
    return sorted(grouped_jobs_by_window_time, key=lambda x: x[0].get('maximum_date_finish'))
