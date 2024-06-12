import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd 
import numpy as np

dfValues = pd.read_json('/Users/karolinaryzka/Documents/neo4jQueries/BaseMetricFiles/allDegreeFrequencies.json', encoding='utf-8-sig')

#expand degrees based on frequency to pass as vals
expandedValues = dfValues.apply(lambda row: [row['degree']] * row['frequency'], axis=1)
expandedValues = [item for sublist in expandedValues for item in sublist]
expandedDf = pd.DataFrame(expandedValues, columns=['degree'])

#mean stat
meanDf = pd.read_json('/Users/karolinaryzka/Documents/neo4jQueries/StatMetrics/avgAllDegrees.json', encoding='utf-8-sig')
meanValue = meanDf['mean'][0]  

#median stat
medianDf = pd.read_json('/Users/karolinaryzka/Documents/neo4jQueries/StatMetrics/medianAllDegrees.json', encoding='utf-8-sig')
medianValue = medianDf['median'][0]  

#mode stat
modeDf = pd.read_json('/Users/karolinaryzka/Documents/neo4jQueries/StatMetrics/modeAllDegrees.json', encoding='utf-8-sig')
modeValue = modeDf['mode'][0]  

#standard deviation stat
stdDevDf = pd.read_json('/Users/karolinaryzka/Documents/neo4jQueries/StatMetrics/stDevAllDegrees.json', encoding='utf-8-sig')
stdDevValue = stdDevDf['stDev'][0]  

#normal distribution plot
plt.figure(figsize=(12, 6))
sns.histplot(expandedDf['degree'], kde=True, bins=30, color='skyblue', stat='density', label='Data Distribution')
plt.ylim(0, 0.25)
#plot lines for mean, median, mode
plt.axvline(meanValue, color='red', linestyle='--', label=f'Mean: {meanValue:.2f}')
plt.axvline(medianValue, color='green', linestyle='-.', label=f'Median: {medianValue:.2f}')
plt.axvline(modeValue, color='blue', linestyle=':', label=f'Mode: {modeValue:.2f}')

plt.text(meanValue + stdDevValue, plt.ylim()[1]*0.05, f'Std Dev: {stdDevValue:.2f}', color='purple')
plt.legend()
plt.title('Normal Distribution of Node Degrees (All)')
plt.xlabel('Degree')
plt.ylabel('Probability Density')
plt.savefig('/Users/karolinaryzka/Documents/neo4jQueries/Visualizations/normDistrAllDegrees.png')
