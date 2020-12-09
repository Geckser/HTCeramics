from os import listdir
from os.path import isfile, join
import pandas as pd
from collections import Counter
from collections import defaultdict

data_sets_dir = '../xrdData'
all_data_sets = [join(data_sets_dir, f) for f in listdir(data_sets_dir) if isfile(join(data_sets_dir, f))]

# find repeated values in dataset

repeating_data_sets = defaultdict(lambda: 0)

print(pd.read_csv('../xrdData/915+glass.csv'))

# for file in all_data_sets:
#     print(file)
#     data_set = pd.read_csv(file)
#     angle, intensity = data_set['Angle'], data_set['Intensity']
#     angle_counts = Counter(angle)
#     for count in angle_counts.values():
#         if count > 1:
#             repeating_data_sets[file] += 1
#
# print(repeating_data_sets)