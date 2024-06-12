import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import json

def main()-> None:

    with open('/Users/karolinaryzka/Documents/neo4jQueries/Data/degreeCentrality500.json', 'r', encoding='utf-8-sig') as file:
        data = json.load(file)

    extractedData = [{'oa_id': item['gds.util.asNode(nodeId)']['properties']['oa_id'], 'mostCited': item['mostCited']} for item in data[:15]]
    df = pd.DataFrame(extractedData)

    plt.figure(figsize=(16, 8))

    # Plot the bar chart
    sns.set_theme()
    graph = sns.barplot(data=df, x='oa_id', y='mostCited')
    graph.set_xlabel('OPEN ALEX ID')
    graph.set_ylabel('In-Degree Centrality ')
    graph.set_title('Most Cited Papers (Top 15)')
    plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels for better readability

    # Display the plot
    plt.tight_layout()
    plt.savefig("/Users/karolinaryzka/Documents/neo4jQueries/Visualizations/degreeCentrality.png")

if __name__ == "__main__":
    main()
