import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import json

def main()-> None:

    with open('/Users/karolinaryzka/Documents/neo4jQueries/Data/top10InDegrees.json', 'r', encoding='utf-8-sig') as file:
        data = json.load(file)

    extractedData = [{'oa_id': item['n']['properties']['oa_id'], 'degree': item['degree']} for item in data]
    df = pd.DataFrame(extractedData)

    # Plot the bar chart
    sns.set_theme()
    graph = sns.barplot(data=df, x='oa_id', y='degree')
    graph.set_xlabel('OPEN ALEX ID')
    graph.set_ylabel('Number of Citations')
    graph.set_title('Top 10 Most Cited Papers by in-Degree')
    plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels for better readability
    #label bars
    for index, value in enumerate(df['degree']):
        graph.text(index, value, str(value), ha='center', va='bottom')
    # Display the plot
    plt.tight_layout()
    plt.savefig("/Users/karolinaryzka/Documents/neo4jQueries/Visualizations/top10inDegreeNodes.png")

if __name__ == "__main__":
    main()
