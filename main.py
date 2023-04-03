import time
from collections import defaultdict
import logging


def time_it(make_report=False, group=None):
    timing_data = defaultdict(list)

    def decorator(func):
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            elapsed_time = end_time - start_time
            timing_data[func.__name__].append(elapsed_time)
            return result
        return wrapper

    def report():
        nonlocal make_report
        make_report = True

    def report_groups():
        nonlocal make_report, group
        make_report = True
        group_data = defaultdict(list)
        for name, times in timing_data.items():
            group_data[name.split(group, 1)[0]].extend(times)
        for name, times in group_data.items():
            print(f"{name} group: Function {group}{name} took {min(times)} seconds to execute.")

    if make_report:
        if group is None:
            return decorator
        else:
            return report_groups
    else:
        return report


def log_it(log_file):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    def decorator(func):
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            logger.info(f"Function {func.__name__} was called with arguments {args}, {kwargs}, and returned {result}.")
            return result
        return wrapper

    return decorator
