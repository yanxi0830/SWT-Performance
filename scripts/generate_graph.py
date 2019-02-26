"""
Generate comparison log and graph (last 30 days) for performance tests.
"""
import argparse
import os
import numpy
import matplotlib.pyplot as plt

END = 84
BASE = "2018_12_06__07_00_01.log"


# UNITS
# Time: (ms)
# Memory: (K)
def str_to_number(data):
    if data.endswith('ms'):
        return float(data[:-2])
    if data.endswith('s'):
        return float(data[:-1]) * 1000
    if data.endswith('K'):
        return float(data[:-1])
    if data.endswith('M'):
        return float(data[:-1]) * 1024
    return float(data)


def parse_log(logfile):
    with open(logfile, "r") as f:
        lines = f.readlines()

    res = {}

    for i in range(0, END, 12):
        line = lines[i]
        test_name = line[32:][:line[32:].find("'")]
        new_entry = {}
        for k in range(1, 11):
            relevant_info = lines[i + k][:lines[i + k].find('(')]
            datalog = [w.strip() for w in relevant_info.split(":")]
            new_entry[datalog[0]] = str_to_number(datalog[1])

        res[test_name] = new_entry

    return res


def date(file):
    return file[:10]


def get_unit(metric):
    if "time" in metric.lower():
        return 'ms'
    else:
        return 'K'


def compare_to_base(logfile, metric):
    baselog = parse_log("../logs/{}".format(BASE))
    currlog = parse_log("../logs/{}".format(logfile))

    res = []
    for test_type in currlog.keys():
        base_metric = baselog[test_type][metric]
        curr_metric = currlog[test_type][metric]
        change = base_metric - curr_metric
        res.append(test_type)
        res.append("\t{}: {:.2f}{}".format(date(BASE), base_metric, get_unit(metric)))
        res.append("\t{}: {:.2f}{}".format(date(logfile), curr_metric, get_unit(metric)))
        res.append("\tDelta: {:.1f}{} ({:.1f}%)\n".format(change, get_unit(metric), (change / base_metric) * 100))

    print('\n'.join(res))
    with open('../result/compare/{}.txt'.format(date(logfile)), 'w') as f:
        f.write('\n'.join(res))

    return '\n'.join(res)


def graph_metric(file_list, use_metric):

    dates = []
    values = {}

    for i, file in enumerate(file_list):
        file_log = parse_log("../logs/{}".format(file))
        dates.append(date(file))
        for test_type in file_log.keys():
            v = file_log[test_type][use_metric]
            if test_type not in values:
                values[test_type] = []
            values[test_type].append(v)

    for test_type in values.keys():
        f, axe = plt.subplots()
        plt.plot(dates, values[test_type], label=use_metric)
        plt.title(test_type)
        plt.xlabel('Date')
        plt.xticks([dates[0], dates[-1]], [dates[0], dates[-1]])
        # annotate with yesterday's delta
        delta = ((values[test_type][-2] - values[test_type][-1]) / values[test_type][-2]) * 100
        axe.annotate('Delta: {:.1f}%'.format(delta), (dates[-2], values[test_type][-2]))
        plt.ylabel('{} ({})'.format(use_metric, get_unit(use_metric)))
        plt.legend()
        plt.savefig('../result/{}.png'.format(test_type.replace(' ', '-')))
        # plt.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='generate CPU Time graph for last 30 days, and comparison stats with base log'
    )
    baselog = parse_log("../logs/{}".format(BASE))
    metrics = baselog.keys()
    parser.add_argument('--metric', type=str, help='one of {}'.format(metrics))
    parser.add_argument('--base', type=str, help='base file to compare to')
    parser.add_argument('--current', type=str, help='current file to compare with base')
    args = parser.parse_args()

    files = os.listdir("../logs/")
    files.sort()
    # remove logs before base
    files = files[files.index(BASE)+1:]
    files.remove('error')

    # latest log file
    current = files[-1]
    metric = 'CPU Time'
    if args.metric is not None:
        metric = args.metric
    if args.base is not None:
        BASE = args.base
    if args.current is not None:
        current = args.current

    # Comparison log
    compare_to_base(current, metric)

    # Graph
    last_month = files
    if len(last_month) > 30:
        last_month = files[-30:]

    graph_metric(last_month, metric)
