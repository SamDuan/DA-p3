# initiation
import pandas as pd
# data import
titanic_df = pd.read_csv('titanic-data.csv')

# calculate numbers of rows and columns
titanic_df.shape
# (891, 12)

# have a peek view of data
titanic_df.head()
summary = titanic_df.describe()
nullsum = titanic_df.isnull().sum()

# mosaic plots
tb1 = pd.crosstab(titanic_df['Pclass'], titanic_df['Survived'])
tb2 = pd.crosstab(titanic_df['Sex'], titanic_df['Survived'])

from statsmodels.graphics.mosaicplot import mosaic
import matplotlib.pyplot as plt

fig1, ax1 = plt.subplots()
m11 = mosaic(tb1.stack(), ax=ax1, 
             labelizer=lambda x: tb1.loc[int(x[0]), int(x[1])])
ax1.set_yticklabels(['Deceased', 'Survived'])
ax1.set_title("Ticket Class and Survivability")

fig2, ax2 = plt.subplots()
m22 = mosaic(tb2.stack(), ax=ax2, labelizer=lambda y: tb2.loc[y[0], int(y[1])])
ax2.set_yticklabels(['Deceased', 'Survived'])
ax2.set_title("Gender and Survivability")

# box plots
bp1 = titanic_df.boxplot(column='Age', by='Survived')
bp1.set_ylabel("Age")
bp1.set_xlabel("Survival")