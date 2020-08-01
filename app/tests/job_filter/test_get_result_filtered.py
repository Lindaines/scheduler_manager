from datetime import datetime
from app.utils.filter_job_result import get_result_filtered, get_first_subset_that_satisfies_sum
import pytest
import random


def test_sublist_sum_items_is_less_than_max_allowed_value():
    jobs = []
    for i in range(0, 20):
        expexted_time = random.randint(1, 8)
        jobs.append({'_id': '5f1e498e024f993389691aa6', 'description_job': 'legacy_import',
                     'maximum_date_finish': datetime(2020, 7, random.randint(1, 31), 17, 22, 35, 181149),
                     'expexted_time_in_hours_to_finish': expexted_time,
                     'expected_time_alert_triggered': False, 'status_job': 'CREATED'})
        jobs = sorted(jobs, key=lambda x: x['maximum_date_finish'])
        jobs_filtered = get_result_filtered(jobs.copy())
        for sublist in jobs_filtered:
            assert sum([job.get('expexted_time_in_hours_to_finish') for job in sublist]) <= 8


def test_list_items_will_be_the_same_after_filter():
    jobs = []
    for i in range(0, 50):
        expexted_time = random.randint(1, 8)
        jobs.append({'_id': '5f1e498e024f993389691aa6', 'description_job': 'legacy_import',
                     'maximum_date_finish': datetime(2020, 7, random.randint(1, 31), 17, 22, 35, 181149),
                     'expexted_time_in_hours_to_finish': expexted_time,
                     'expected_time_alert_triggered': False, 'status_job': 'CREATED'})
        jobs = sorted(jobs, key=lambda x: x['maximum_date_finish'])
    jobs_filtered = get_result_filtered(jobs.copy())
    flat_jobs_filtered = [job for sublist in jobs_filtered for job in sublist]
    flat_jobs_filtered = sorted(flat_jobs_filtered, key=lambda x: x['maximum_date_finish'])
    assert all(job in jobs for job in flat_jobs_filtered)


def test_max_lengh_will_be_respected():
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
    jobs_filtered_expected = [[{'_id': '5f1e498e024f993389691aa6', 'description_job': 'legacy_import',
                                'maximum_date_finish': datetime(2020, 7, 18, 17, 22, 35, 181149),
                                'expexted_time_in_hours_to_finish': 6, 'expected_time_alert_triggered': False,
                                'status_job': 'CREATED'}], [
                                  {'_id': '5f1e498e024f993389691aa6', 'description_job': 'legacy_import',
                                   'maximum_date_finish': datetime(2020, 7, 19, 17, 22, 35, 181149),
                                   'expexted_time_in_hours_to_finish': 5, 'expected_time_alert_triggered': False,
                                   'status_job': 'CREATED'}], [
                                  {'_id': '5f1e498e024f993389691aa6', 'description_job': 'legacy_import',
                                   'maximum_date_finish': datetime(2020, 7, 20, 17, 22, 35, 181149),
                                   'expexted_time_in_hours_to_finish': 1, 'expected_time_alert_triggered': False,
                                   'status_job': 'CREATED'},
                                  {'_id': '5f1e498e024f993389691aa6', 'description_job': 'legacy_import',
                                   'maximum_date_finish': datetime(2020, 7, 24, 17, 22, 35, 181149),
                                   'expexted_time_in_hours_to_finish': 2, 'expected_time_alert_triggered': False,
                                   'status_job': 'CREATED'},
                                  {'_id': '5f1e498e024f993389691aa6', 'description_job': 'legacy_import',
                                   'maximum_date_finish': datetime(2020, 7, 25, 17, 22, 35, 181149),
                                   'expexted_time_in_hours_to_finish': 1, 'expected_time_alert_triggered': False,
                                   'status_job': 'CREATED'}], [
                                  {'_id': '5f1e498e024f993389691aa6', 'description_job': 'legacy_import',
                                   'maximum_date_finish': datetime(2020, 7, 21, 17, 22, 35, 181149),
                                   'expexted_time_in_hours_to_finish': 6, 'expected_time_alert_triggered': False,
                                   'status_job': 'CREATED'}], [
                                  {'_id': '5f1e498e024f993389691aa6', 'description_job': 'legacy_import',
                                   'maximum_date_finish': datetime(2020, 7, 22, 17, 22, 35, 181149),
                                   'expexted_time_in_hours_to_finish': 3, 'expected_time_alert_triggered': False,
                                   'status_job': 'CREATED'},
                                  {'_id': '5f1e498e024f993389691aa6', 'description_job': 'legacy_import',
                                   'maximum_date_finish': datetime(2020, 7, 26, 17, 22, 35, 181149),
                                   'expexted_time_in_hours_to_finish': 5, 'expected_time_alert_triggered': False,
                                   'status_job': 'CREATED'}], [
                                  {'_id': '5f1e498e024f993389691aa6', 'description_job': 'legacy_import',
                                   'maximum_date_finish': datetime(2020, 7, 23, 17, 22, 35, 181149),
                                   'expexted_time_in_hours_to_finish': 8, 'expected_time_alert_triggered': False,
                                   'status_job': 'CREATED'}], [
                                  {'_id': '5f1e498e024f993389691aa6', 'description_job': 'legacy_import',
                                   'maximum_date_finish': datetime(2020, 7, 27, 17, 22, 35, 181149),
                                   'expexted_time_in_hours_to_finish': 7, 'expected_time_alert_triggered': False,
                                   'status_job': 'CREATED'}]]
    jobs_filtered = get_result_filtered(jobs)
    assert str(jobs_filtered_expected) == str(jobs_filtered)


def test_sublist_sequential_by_max_date():
    jobs = [{'_id': '5f1e498e024f993389691aa6', 'description_job': 'legacy_import',
             'maximum_date_finish': datetime(2020, 7, 27, 17, 32, 2, 500705), 'expexted_time_in_hours_to_finish': 7,
             'expected_time_alert_triggered': False, 'status_job': 'CREATED'},
            {'_id': '5f1e498e024f993389691aa6', 'description_job': 'legacy_import',
             'maximum_date_finish': datetime(2020, 7, 26, 17, 32, 2, 500705), 'expexted_time_in_hours_to_finish': 5,
             'expected_time_alert_triggered': False, 'status_job': 'CREATED'},
            {'_id': '5f1e498e024f993389691aa6', 'description_job': 'legacy_import',
             'maximum_date_finish': datetime(2020, 7, 25, 17, 32, 2, 500705), 'expexted_time_in_hours_to_finish': 4,
             'expected_time_alert_triggered': False, 'status_job': 'CREATED'},
            {'_id': '5f1e498e024f993389691aa6', 'description_job': 'legacy_import',
             'maximum_date_finish': datetime(2020, 7, 24, 17, 32, 2, 500705), 'expexted_time_in_hours_to_finish': 4,
             'expected_time_alert_triggered': False, 'status_job': 'CREATED'},
            {'_id': '5f1e498e024f993389691aa6', 'description_job': 'legacy_import',
             'maximum_date_finish': datetime(2020, 7, 23, 17, 32, 2, 500705), 'expexted_time_in_hours_to_finish': 2,
             'expected_time_alert_triggered': False, 'status_job': 'CREATED'},
            {'_id': '5f1e498e024f993389691aa6', 'description_job': 'legacy_import',
             'maximum_date_finish': datetime(2020, 7, 22, 17, 32, 2, 500705), 'expexted_time_in_hours_to_finish': 7,
             'expected_time_alert_triggered': False, 'status_job': 'CREATED'},
            {'_id': '5f1e498e024f993389691aa6', 'description_job': 'legacy_import',
             'maximum_date_finish': datetime(2020, 7, 21, 17, 32, 2, 500705), 'expexted_time_in_hours_to_finish': 1,
             'expected_time_alert_triggered': False, 'status_job': 'CREATED'},
            {'_id': '5f1e498e024f993389691aa6', 'description_job': 'legacy_import',
             'maximum_date_finish': datetime(2020, 7, 20, 17, 32, 2, 500705), 'expexted_time_in_hours_to_finish': 5,
             'expected_time_alert_triggered': False, 'status_job': 'CREATED'},
            {'_id': '5f1e498e024f993389691aa6', 'description_job': 'legacy_import',
             'maximum_date_finish': datetime(2020, 7, 19, 17, 32, 2, 500705), 'expexted_time_in_hours_to_finish': 1,
             'expected_time_alert_triggered': False, 'status_job': 'CREATED'},
            {'_id': '5f1e498e024f993389691aa6', 'description_job': 'legacy_import',
             'maximum_date_finish': datetime(2020, 7, 18, 17, 32, 2, 500705), 'expexted_time_in_hours_to_finish': 2,
             'expected_time_alert_triggered': False, 'status_job': 'CREATED'},
            {'_id': '5f1e498e024f993389691aa6', 'description_job': 'legacy_import',
             'maximum_date_finish': datetime(2020, 7, 17, 17, 32, 2, 500705), 'expexted_time_in_hours_to_finish': 1,
             'expected_time_alert_triggered': False, 'status_job': 'CREATED'},
            {'_id': '5f1e498e024f993389691aa6', 'description_job': 'legacy_import',
             'maximum_date_finish': datetime(2020, 7, 16, 17, 32, 2, 500705), 'expexted_time_in_hours_to_finish': 2,
             'expected_time_alert_triggered': False, 'status_job': 'CREATED'},
            {'_id': '5f1e498e024f993389691aa6', 'description_job': 'legacy_import',
             'maximum_date_finish': datetime(2020, 7, 15, 17, 32, 2, 500705), 'expexted_time_in_hours_to_finish': 8,
             'expected_time_alert_triggered': False, 'status_job': 'CREATED'},
            {'_id': '5f1e498e024f993389691aa6', 'description_job': 'legacy_import',
             'maximum_date_finish': datetime(2020, 7, 14, 17, 32, 2, 500705), 'expexted_time_in_hours_to_finish': 1,
             'expected_time_alert_triggered': False, 'status_job': 'CREATED'},
            {'_id': '5f1e498e024f993389691aa6', 'description_job': 'legacy_import',
             'maximum_date_finish': datetime(2020, 7, 13, 17, 32, 2, 500705), 'expexted_time_in_hours_to_finish': 8,
             'expected_time_alert_triggered': False, 'status_job': 'CREATED'},
            {'_id': '5f1e498e024f993389691aa6', 'description_job': 'legacy_import',
             'maximum_date_finish': datetime(2020, 7, 12, 17, 32, 2, 500705), 'expexted_time_in_hours_to_finish': 1,
             'expected_time_alert_triggered': False, 'status_job': 'CREATED'},
            {'_id': '5f1e498e024f993389691aa6', 'description_job': 'legacy_import',
             'maximum_date_finish': datetime(2020, 7, 11, 17, 32, 2, 500705), 'expexted_time_in_hours_to_finish': 1,
             'expected_time_alert_triggered': False, 'status_job': 'CREATED'},
            {'_id': '5f1e498e024f993389691aa6', 'description_job': 'legacy_import',
             'maximum_date_finish': datetime(2020, 7, 10, 17, 32, 2, 500705), 'expexted_time_in_hours_to_finish': 1,
             'expected_time_alert_triggered': False, 'status_job': 'CREATED'},
            {'_id': '5f1e498e024f993389691aa6', 'description_job': 'legacy_import',
             'maximum_date_finish': datetime(2020, 7, 9, 17, 32, 2, 500705), 'expexted_time_in_hours_to_finish': 6,
             'expected_time_alert_triggered': False, 'status_job': 'CREATED'},
            {'_id': '5f1e498e024f993389691aa6', 'description_job': 'legacy_import',
             'maximum_date_finish': datetime(2020, 7, 8, 17, 32, 2, 500705), 'expexted_time_in_hours_to_finish': 5,
             'expected_time_alert_triggered': False, 'status_job': 'CREATED'}]
    jobs_filtered_expected = [[{'_id': '5f1e498e024f993389691aa6', 'description_job': 'legacy_import',
                                'maximum_date_finish': datetime(2020, 7, 8, 17, 32, 2, 500705),
                                'expexted_time_in_hours_to_finish': 5, 'expected_time_alert_triggered': False,
                                'status_job': 'CREATED'},
                               {'_id': '5f1e498e024f993389691aa6', 'description_job': 'legacy_import',
                                'maximum_date_finish': datetime(2020, 7, 12, 17, 32, 2, 500705),
                                'expexted_time_in_hours_to_finish': 1, 'expected_time_alert_triggered': False,
                                'status_job': 'CREATED'},
                               {'_id': '5f1e498e024f993389691aa6', 'description_job': 'legacy_import',
                                'maximum_date_finish': datetime(2020, 7, 14, 17, 32, 2, 500705),
                                'expexted_time_in_hours_to_finish': 1, 'expected_time_alert_triggered': False,
                                'status_job': 'CREATED'}], [
                                  {'_id': '5f1e498e024f993389691aa6', 'description_job': 'legacy_import',
                                   'maximum_date_finish': datetime(2020, 7, 9, 17, 32, 2, 500705),
                                   'expexted_time_in_hours_to_finish': 6, 'expected_time_alert_triggered': False,
                                   'status_job': 'CREATED'},
                                  {'_id': '5f1e498e024f993389691aa6', 'description_job': 'legacy_import',
                                   'maximum_date_finish': datetime(2020, 7, 16, 17, 32, 2, 500705),
                                   'expexted_time_in_hours_to_finish': 2, 'expected_time_alert_triggered': False,
                                   'status_job': 'CREATED'}], [
                                  {'_id': '5f1e498e024f993389691aa6', 'description_job': 'legacy_import',
                                   'maximum_date_finish': datetime(2020, 7, 10, 17, 32, 2, 500705),
                                   'expexted_time_in_hours_to_finish': 1, 'expected_time_alert_triggered': False,
                                   'status_job': 'CREATED'},
                                  {'_id': '5f1e498e024f993389691aa6', 'description_job': 'legacy_import',
                                   'maximum_date_finish': datetime(2020, 7, 11, 17, 32, 2, 500705),
                                   'expexted_time_in_hours_to_finish': 1, 'expected_time_alert_triggered': False,
                                   'status_job': 'CREATED'}], [
                                  {'_id': '5f1e498e024f993389691aa6', 'description_job': 'legacy_import',
                                   'maximum_date_finish': datetime(2020, 7, 13, 17, 32, 2, 500705),
                                   'expexted_time_in_hours_to_finish': 8, 'expected_time_alert_triggered': False,
                                   'status_job': 'CREATED'}], [
                                  {'_id': '5f1e498e024f993389691aa6', 'description_job': 'legacy_import',
                                   'maximum_date_finish': datetime(2020, 7, 15, 17, 32, 2, 500705),
                                   'expexted_time_in_hours_to_finish': 8, 'expected_time_alert_triggered': False,
                                   'status_job': 'CREATED'}], [
                                  {'_id': '5f1e498e024f993389691aa6', 'description_job': 'legacy_import',
                                   'maximum_date_finish': datetime(2020, 7, 17, 17, 32, 2, 500705),
                                   'expexted_time_in_hours_to_finish': 1, 'expected_time_alert_triggered': False,
                                   'status_job': 'CREATED'},
                                  {'_id': '5f1e498e024f993389691aa6', 'description_job': 'legacy_import',
                                   'maximum_date_finish': datetime(2020, 7, 18, 17, 32, 2, 500705),
                                   'expexted_time_in_hours_to_finish': 2, 'expected_time_alert_triggered': False,
                                   'status_job': 'CREATED'},
                                  {'_id': '5f1e498e024f993389691aa6', 'description_job': 'legacy_import',
                                   'maximum_date_finish': datetime(2020, 7, 19, 17, 32, 2, 500705),
                                   'expexted_time_in_hours_to_finish': 1, 'expected_time_alert_triggered': False,
                                   'status_job': 'CREATED'}], [
                                  {'_id': '5f1e498e024f993389691aa6', 'description_job': 'legacy_import',
                                   'maximum_date_finish': datetime(2020, 7, 20, 17, 32, 2, 500705),
                                   'expexted_time_in_hours_to_finish': 5, 'expected_time_alert_triggered': False,
                                   'status_job': 'CREATED'},
                                  {'_id': '5f1e498e024f993389691aa6', 'description_job': 'legacy_import',
                                   'maximum_date_finish': datetime(2020, 7, 21, 17, 32, 2, 500705),
                                   'expexted_time_in_hours_to_finish': 1, 'expected_time_alert_triggered': False,
                                   'status_job': 'CREATED'}], [
                                  {'_id': '5f1e498e024f993389691aa6', 'description_job': 'legacy_import',
                                   'maximum_date_finish': datetime(2020, 7, 22, 17, 32, 2, 500705),
                                   'expexted_time_in_hours_to_finish': 7, 'expected_time_alert_triggered': False,
                                   'status_job': 'CREATED'}], [
                                  {'_id': '5f1e498e024f993389691aa6', 'description_job': 'legacy_import',
                                   'maximum_date_finish': datetime(2020, 7, 23, 17, 32, 2, 500705),
                                   'expexted_time_in_hours_to_finish': 2, 'expected_time_alert_triggered': False,
                                   'status_job': 'CREATED'},
                                  {'_id': '5f1e498e024f993389691aa6', 'description_job': 'legacy_import',
                                   'maximum_date_finish': datetime(2020, 7, 26, 17, 32, 2, 500705),
                                   'expexted_time_in_hours_to_finish': 5, 'expected_time_alert_triggered': False,
                                   'status_job': 'CREATED'}], [
                                  {'_id': '5f1e498e024f993389691aa6', 'description_job': 'legacy_import',
                                   'maximum_date_finish': datetime(2020, 7, 24, 17, 32, 2, 500705),
                                   'expexted_time_in_hours_to_finish': 4, 'expected_time_alert_triggered': False,
                                   'status_job': 'CREATED'},
                                  {'_id': '5f1e498e024f993389691aa6', 'description_job': 'legacy_import',
                                   'maximum_date_finish': datetime(2020, 7, 25, 17, 32, 2, 500705),
                                   'expexted_time_in_hours_to_finish': 4, 'expected_time_alert_triggered': False,
                                   'status_job': 'CREATED'}], [
                                  {'_id': '5f1e498e024f993389691aa6', 'description_job': 'legacy_import',
                                   'maximum_date_finish': datetime(2020, 7, 27, 17, 32, 2, 500705),
                                   'expexted_time_in_hours_to_finish': 7, 'expected_time_alert_triggered': False,
                                   'status_job': 'CREATED'}]]
    jobs_filtered = get_result_filtered(jobs)
    assert str(jobs_filtered_expected) == str(jobs_filtered)


def test_get_first_subset_that_satisfies_sum():
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
    jobs_sublist_expected = [{'_id': '5f1e498e024f993389691aa6', 'description_job': 'legacy_import',
                              'maximum_date_finish': datetime(2020, 7, 23, 17, 22, 35, 181149),
                              'expexted_time_in_hours_to_finish': 8, 'expected_time_alert_triggered': False,
                              'status_job': 'CREATED'}]
    jobs_sublist_received = get_first_subset_that_satisfies_sum(jobs, 8)
    assert str(jobs_sublist_expected) == str(jobs_sublist_received)
