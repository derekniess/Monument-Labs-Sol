
from subprocess import Popen
import time
import threading

commands = [
	'uptime',
    'sleep 3',
    'ls -l /',
    'find /',    
    'sleep 4',
    'find /usr',
    'date',
    'sleep 5'
]

# reports total elapsed time, avg/min/max runtimes among commands
def print_report(runtimes, elapsed_time):

	print("\nReport (in seconds)")
	print("Minimum runtime   : ", min(runtimes))
	print("Maximum runtime   : ", max(runtimes))
	print("Average runtime   : ", sum(runtimes)/len(runtimes))
	print("Total elapsed time: ", elapsed_time)

# wrapper to time execution of a command handled by a subprocess
def execute(command, runtimes, index):
	start_time = time.time()
	process = Popen(command.split())
	process.wait()
	runtimes[index] = time.time() - start_time
	return runtimes


num_cmds = len(commands)
runtimes = [0 for i in range(num_cmds)]
processes = [None] * num_cmds

# spawn one thread per subprocess to time its corresponding command's execution independently
for i, command in enumerate(commands):
	processes[i] = threading.Thread(target=execute, kwargs={'command':command, 'runtimes':runtimes, 'index':i})

start_time = time.time()

# run all subprocesses at once
for process in processes:
	process.start()

# wait for all subprocesses to finish
for process in processes:
	process.join()

elapsed_time = time.time() - start_time

print_report(runtimes, elapsed_time)


