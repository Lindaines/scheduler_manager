def get_first_subset_that_satisfies_sum(jobs, max_value, sub_jobs=[]):
    if sum(sub_jobs) == max_value:
        return sub_jobs
    if sum(sub_jobs) >= max_value:
        return

    for index, value in enumerate(jobs):
        remaining = jobs[index + 1:]
        result = get_first_subset_that_satisfies_sum(remaining, max_value, sub_jobs + [value])
        if result:
            return result


def get_result_filtered(jobs: list):
    final_list = []
    while len(jobs) > 1:
        b = get_first_subset_that_satisfies_sum(jobs, 8)
        if b:
            final_list.append(b)
            for item in b:
                jobs.remove(item)
        else:
            for item in jobs:
                final_list.append([item])
            break
    return final_list


print(get_result_filtered([1, 1, 2, 3, 4, 5, 6, 8, 7, 2, 1, 5, 6, 4]))
