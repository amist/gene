import random
import subprocess
import os

def run_python_code(code):
    filename = ''.join(random.choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUZWXYZ0123456789') for i in range(8)) + '.py'
    with open(filename, 'w') as python_file:
        python_file.write(code)
        python_file.flush()
        p = subprocess.Popen('python ' + filename, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        #print(p.stdout.read())
        for line in p.stdout.readlines():
            print(line.decode(), end='')
    os.remove(filename)
        
    
    
if __name__ == '__main__':
    a = [1,2,3,4]
    run_python_code('''
if __name__ == '__main__':
    print('print from a temporary python file')
    print('a list which has been passed as an argument = ' + repr(%s))
''' % repr(a))