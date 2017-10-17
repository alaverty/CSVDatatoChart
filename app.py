import pandas as pd
import numpy as np
import matplotlib as mpl
from matplotlib.dates import DateFormatter, WeekdayLocator, MonthLocator

mpl.use('TkAgg')
import matplotlib.pyplot as plt
from cycler import cycler

mpl.rcParams['axes.prop_cycle'] = cycler(color='grbcmyk')

df = pd.read_csv("CSVData.csv", names=["date", "credit", "description", "balance", "category"])

df['income'] = df.apply(lambda row: (row['credit']
                                     if row['credit'] > 0
                                     else 0),
                        axis=1)

df['expense'] = df.apply(lambda row: (row['credit'] * -1
                                      if row['credit'] < 0
                                      else 0),
                         axis=1)

df['total'] = df.apply(lambda row: (row['income'] - row['expense']),
                         axis=1)

df.index = pd.to_datetime(df['date'], dayfirst=True)

groupData = df.groupby(pd.Grouper(freq='M')).aggregate({
    'income': np.sum,
    'expense': np.sum,
    'balance': np.max,
    'total': np.sum

})

monthsFmt = DateFormatter("%b '%y")

ax = groupData[['income', 'expense']].plot.bar(grid="on", fontsize=6, rot=0)

ax.xaxis.set_major_formatter(plt.FixedFormatter(groupData.index.to_series().dt.strftime("%b %y")))
plt.title('Income vs Expense')
plt.savefig('CSVData-IncomeVSExpense.png')

ax = groupData[['balance']].plot.line(grid="on", fontsize=6, rot=0)

ax.xaxis.set_major_formatter(plt.FixedFormatter(groupData.index.to_series().dt.strftime("%b %y")))
plt.title('Balance')
plt.savefig('CSVData-Balance.png')

ax = groupData[['total']].plot.bar(grid="on", fontsize=6, rot=0)

ax.xaxis.set_major_formatter(plt.FixedFormatter(groupData.index.to_series().dt.strftime("%b %y")))
plt.title('Total $ Saved Per Month')
plt.savefig('CSVData-TotalSaved.png')

plt.show()
