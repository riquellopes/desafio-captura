# from handlers import MonkRegister
#
#
# def main():
#     for register in MonkRegister():
#         register.start()
#
# if __name__ == "__main__":
#     main()

# import itertools
# import threading
# import time
# import sys
#
# done = False
#
# # Snippet credit
# # http://stackoverflow.com/questions/22029562/python-how-to-make-simple-animated-loading-while-process-is-running?answertab=active#tab-top
#
#
# def animate():
#     for c in itertools.cycle(['|', '/', '-', '\\']):
#         if done:
#             break
#         sys.stdout.write('\rloading ' + c)
#         sys.stdout.flush()
#         time.sleep(0.1)
#     sys.stdout.write('\rDone!     \n')
#
# t = threading.Thread(target=animate)
# t.start()


# time.sleep(10)
# done = True

from monk.csv import MonkMonitorCSV

monitor = MonkMonitorCSV()
monitor.run()
