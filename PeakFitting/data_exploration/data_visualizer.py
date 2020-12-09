import matplotlib.pyplot as plt
import pandas as pd

data = pd.read_csv('../xrdData/915+Si+wafer+run+2.csv.csv', error_bad_lines=False)
print(data.keys())
plt.plot(data['Angle'], data['Intensity'])
plt.show()
