import pandas as pd
import numpy as np
import requests
import re
import csv
import copy
from os import path 

file_all = open('notSubmitted.txt', 'r')
file_ggH = open('notSubmitted_ggH.txt', 'w')
file_bbH = open('notSubmitted_bbH.txt', 'w')

lines = file_all.readlines()

for i,l in enumerate(lines):
    print(i, l)
    if "ggH" in l:
        file_ggH.writelines(l)
    elif "bbH" in l:
        file_bbH.writelines(l)


