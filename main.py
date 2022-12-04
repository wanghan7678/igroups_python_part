# coding=utf-8
# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import sys
import os
import retrievedata.operation_daily_data as op

sys.path.append(os.path.dirname(sys.path[0]))


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print("Hi, {0}".format(name))  # Press ⌘F8 to toggle the breakpoint.


def main(arg):
    op.update_stock_basic()
    date = arg[1]
    op.load_stock_day_lines_oneday(date)
    op.load_ta_signals_oneday(date)
    op.load_chart_signals_oneday(date)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main(sys.argv)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
