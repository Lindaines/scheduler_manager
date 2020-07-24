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
    final_list = []
    while len(jobs) > 1:
        b = get_first_subset_that_satisfies_sum(jobs, 8)
        if b:
            sorted_sub_list = sorted(b, key=lambda k: k['maximum_date_finish'])
            final_list.append(sorted_sub_list)
            for item in sorted_sub_list:
                jobs.remove(item)
        else:
            for item in jobs:
                final_list.append([item])
            break
    return final_list

# print(get_result_filtered([1, 1, 2, 3, 4, 5, 6, 8, 7, 2, 1, 5, 6, 4]))

# import datetime
# import random
#
#
# def random_date():
#     start = datetime.datetime(year=2020, month=7, day=24)
#     end = datetime.datetime(year=2020, month=8, day=24)
#     return start + datetime.timedelta(
#         seconds=random.randint(0, int((end - start).total_seconds())),
#     )
#
#
# jobs = []
# for i in range(10):
#     jobs.append({
#         "maximum_date_finish": random_date(),
#         "expexted_time_in_hours_to_finish": random.randint(1, 8)
#     })
#
# r = get_result_filtered(jobs)
# for item in r:
#     print(item)
