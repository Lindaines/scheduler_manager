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


from datetime import datetime, timedelta
import random

jobs = []
base = datetime.today()
date_list = [base - timedelta(days=x) for x in range(20)]

# for date in date_list:
#     job = {
#         "_id": "5f1e498e024f993389691aa6",
#         "description_job": "legacy_import",
#         "maximum_date_finish": "2020-07-28T00:18:15",
#         "expexted_time_in_hours_to_finish": 4,
#         "expected_time_alert_triggered": False,
#         "status_job": "CREATED"
#     }
#     job['maximum_date_finish'] = date
#     job['expexted_time_in_hours_to_finish'] = random.randint(1, 8)
#     jobs.append(job)
print(jobs)

jobs = [{'_id': '5f1e498e024f993389691aa6', 'description_job': 'legacy_import',
             'maximum_date_finish': datetime(2020, 7, 27, 17, 22, 35, 181149), 'expexted_time_in_hours_to_finish': 7,
             'expected_time_alert_triggered': False, 'status_job': 'CREATED'},
            {'_id': '5f1e498e024f993389691aa6', 'description_job': 'legacy_import',
             'maximum_date_finish': datetime(2020, 7, 26, 17, 22, 35, 181149), 'expexted_time_in_hours_to_finish': 5,
             'expected_time_alert_triggered': False, 'status_job': 'CREATED'},
            {'_id': '5f1e498e024f993389691aa6', 'description_job': 'legacy_import',
             'maximum_date_finish': datetime(2020, 7, 25, 17, 22, 35, 181149), 'expexted_time_in_hours_to_finish': 1,
             'expected_time_alert_triggered': False, 'status_job': 'CREATED'},
            {'_id': '5f1e498e024f993389691aa6', 'description_job': 'legacy_import',
             'maximum_date_finish': datetime(2020, 7, 24, 17, 22, 35, 181149), 'expexted_time_in_hours_to_finish': 2,
             'expected_time_alert_triggered': False, 'status_job': 'CREATED'},
            {'_id': '5f1e498e024f993389691aa6', 'description_job': 'legacy_import',
             'maximum_date_finish': datetime(2020, 7, 23, 17, 22, 35, 181149), 'expexted_time_in_hours_to_finish': 8,
             'expected_time_alert_triggered': False, 'status_job': 'CREATED'},
            {'_id': '5f1e498e024f993389691aa6', 'description_job': 'legacy_import',
             'maximum_date_finish': datetime(2020, 7, 22, 17, 22, 35, 181149), 'expexted_time_in_hours_to_finish': 3,
             'expected_time_alert_triggered': False, 'status_job': 'CREATED'},
            {'_id': '5f1e498e024f993389691aa6', 'description_job': 'legacy_import',
             'maximum_date_finish': datetime(2020, 7, 21, 17, 22, 35, 181149), 'expexted_time_in_hours_to_finish': 6,
             'expected_time_alert_triggered': False, 'status_job': 'CREATED'},
            {'_id': '5f1e498e024f993389691aa6', 'description_job': 'legacy_import',
             'maximum_date_finish': datetime(2020, 7, 20, 17, 22, 35, 181149), 'expexted_time_in_hours_to_finish': 1,
             'expected_time_alert_triggered': False, 'status_job': 'CREATED'},
            {'_id': '5f1e498e024f993389691aa6', 'description_job': 'legacy_import',
             'maximum_date_finish': datetime(2020, 7, 19, 17, 22, 35, 181149), 'expexted_time_in_hours_to_finish': 5,
             'expected_time_alert_triggered': False, 'status_job': 'CREATED'},
            {'_id': '5f1e498e024f993389691aa6', 'description_job': 'legacy_import',
             'maximum_date_finish': datetime(2020, 7, 18, 17, 22, 35, 181149), 'expexted_time_in_hours_to_finish': 6,
             'expected_time_alert_triggered': False, 'status_job': 'CREATED'}]
a = get_first_subset_that_satisfies_sum(jobs,8)
print(a)
