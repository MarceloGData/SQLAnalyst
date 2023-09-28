import os
os.system('color')
from termcolor import colored, COLORS

print(COLORS)

var = colored('hello', 'red') + colored(' world', 'green') + 'bn'
print(var)


