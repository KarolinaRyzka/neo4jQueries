import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd 
import numpy as np
from scipy.stats import expon

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

fitDist = expon(scale=meanValue)
fitData = np.linspace(0, np.max(expandedDf['degree']), 1000)
fitPdf = fitDist.pdf(fitData)

plt.figure(figsize=(12, 6))

sns.histplot(data=expandedDf['degree'], kde=False, stat='density')

plt.xlim(0, 100)
plt.ylim(0,0.7)
# Overlay the fitted distribution onto the plot
plt.plot(fitData, fitPdf, color='red', label='Exponential Fit')

plt.axvline(meanValue, color='orange', linestyle='--', label=f'Mean: {meanValue:.2f}')
plt.axvline(medianValue, color='green', linestyle='-.', label=f'Median: {medianValue:.2f}')
plt.axvline(modeValue, color='blue', linestyle=':', label=f'Mode: {modeValue:.2f}')

plt.text(meanValue + stdDevValue, plt.ylim()[1]*0.05, f'Std Dev: {stdDevValue:.2f}', color='purple')
plt.legend()
plt.title('Exponential Distribution of Node Degrees')
plt.xlabel('Degree')
plt.ylabel('Probability Density')
plt.savefig('/Users/karolinaryzka/Documents/neo4jQueries/Visualizations/expDistrAllDegrees.png')