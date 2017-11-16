import random
import os
import os.path
import subprocess
import shlex
import re
import threading

class Command(object):
    def __init__(self, cmd):
        self.cmd = cmd
        self.process = None

    def run(self, timeout):
        proc = subprocess.Popen(shlex.split(self.cmd), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # kill_proc = lambda p: p.kill()
        # timer = threading.Timer(timeout, kill_proc, [proc])
        stdout = None
 
        time.sleep(timeout)
        # timer.start()
        if proc.poll() is None:
            proc.kill()
        else:
            stdout, stderr = proc.communicate()
            pass

        return stdout
     
def run(n):
    DIRECTORY = r'C:\tmp\ggnfs\example' 
    
    r = '%s-%s' % (str(n)[:20], str(n)[-20:])
    
    with open(os.path.join(DIRECTORY, 'task_%s.n' % r), 'w') as f:
        f.write('n: %d' % n)
    
    current_dir = os.getcwd()
    os.chdir(os.path.join(DIRECTORY))

    # stdout = subprocess.check_output(["python", "factmsieve.py", "task_%s" % r], timeout=30)
    stdout = subprocess.check_output("python factmsieve.py task_%s" % r, timeout=30)
    # stdout = p.stdout

    # p = Command("python factmsieve.py task_%s" % r)
    # stdout = p.run(timeout=30)    

    if stdout is None:
        return None

    answer = []
    for line in stdout.decode().split('\n'):
        line = line.strip()
        m = re.match('p\d+ factor: (\d+)', line)
        if m:
            answer.append(int(m.groups()[0]))

    os.chdir(current_dir)
    return answer
    

if __name__ == '__main__':
    # print(list(run(8958978968711216842229769107799765957769401415157946420165008908439654777086360344756881068328073822208)))
    print(list(run(8958978968711216842229769107799765957769401415157946420165008908439654777086360344756881068328073822208123412341234123412341234123412341234123412341234)))