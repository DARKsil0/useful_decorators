import time
from functools import wraps


class ExecutionTime:
    results = {}

    def __init__(self, group_name):
        self.group_name = group_name
        self.func_name = None
        self.start_time = None
        self.end_time = None
        self.execution_time = None

    def __call__(self, func):
        def wrapped_func(*args, **kwargs):
            self.func_name = func.__name__
            self.start_time = time.time()
            result = func(*args, **kwargs)
            self.end_time = time.time()
            self.execution_time = self.end_time - self.start_time
            if self.group_name not in ExecutionTime.results:
                ExecutionTime.results[self.group_name] = []
            ExecutionTime.results[self.group_name].append((self.func_name, self.execution_time))
            return result

        return wrapped_func

    @staticmethod
    def report():
        for group_name, results in sorted(ExecutionTime.results.items()):
            print(f"Group name {group_name}")
            print("No.\tFunction Name\t\tExecution Time")
            results = sorted(results, key=lambda x: x[1])
            for i, (func_name, execution_time) in enumerate(results):
                print(f"{i + 1}\t{func_name}\t\t{execution_time:.6f}")
            print()


@ExecutionTime(group_name=1)
def reverse_string_1(s):
    return s[::-1]


@ExecutionTime(group_name=1)
def reverse_string_2(s):
    return "".join(reversed(s))


@ExecutionTime(group_name=1)
def reverse_string_3(s):
    return "".join(s[i] for i in range(len(s) - 1, -1, -1))


@ExecutionTime(group_name=1)
def reverse_string_4(s):
    return "".join(s[i] for i in reversed(range(len(s))))


@ExecutionTime(group_name=1)
def reverse_string_5(s):
    return "".join(s[i] for i in range(len(s) - 1, -1, -1))


if __name__ == '__main__':
    s = 'qwerty'
    reverse_string_1(s)
    reverse_string_2(s)
    reverse_string_3(s)
    reverse_string_4(s)
    reverse_string_5(s)
    ExecutionTime.report()
    #output
    """Group name 1
No.	Function Name		Execution Time
1	reverse_string_1		0.000001
2	reverse_string_5		0.000001
3	reverse_string_3		0.000002
4	reverse_string_4		0.000002
5	reverse_string_2		0.000002"""
