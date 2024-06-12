import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter, MaxNLocator


def main() -> None:
    #JSON to DF
    df = pd.read_json('/Users/karolinaryzka/Documents/neo4jQueries/Data/outDegreeFrequency.json', encoding='utf-8-sig')

    
    def plotRange(minFreq, maxFreq, title, ylabel_formatter, y_major_locator):
        rangeDf = df[(df['frequency'] >= minFreq) & (df['frequency'] <= maxFreq) & (df['frequency'] >= 25)]
        #rangeDf = df[(df['frequency'] >= minFreq) & (df['frequency'] <= maxFreq)]
        plt.figure(figsize=(12, 6))
        sns.set_theme()
        graph = sns.barplot(data=rangeDf, x='degree', y = 'frequency' )
        graph.set_ylabel('Frequency')
        graph.set_xlabel('Number of References')
        graph.set_title(f'Reference Frequency in Papers ({int(minFreq)}-{int(maxFreq)})')

        graph.yaxis.set_major_formatter(FuncFormatter(ylabel_formatter))
        graph.yaxis.set_major_locator(MaxNLocator(y_major_locator))
        
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(f"/Users/karolinaryzka/Documents/neo4jQueries/Visualizations/outDegreeDistributions/outDegreeDistr_{int(minFreq)}_{int(maxFreq)}.png")

    def customFormatter(x, pos):
        if x >= 1e6:
            return f'{x / 1e6:.1f}M'
        else:
            return f'{x / 1e3:.1f}K'
        
    plotRange(0, 1.5e6, 'Frequency (all data)', customFormatter, 10)     
    plotRange(1e5, 1.5e6, 'Frequency (100k and above)', customFormatter, 10)
    plotRange(1e4, 99999, 'Frequency (10K - 99K)', lambda x, pos: f'{int(x/1e3)}K', 10)
    plotRange(1e3, 9999, 'Frequency (1K - 9,999)', lambda x, pos: f'{int(x/1e3)}K', 10)
    plotRange(200, 999, 'Frequency (0 - 999)', lambda x, pos: f'{int(x)}', 10)
    plotRange(0, 199, 'Frequency (0 - 999)', lambda x, pos: f'{int(x)}', 10)
        


if __name__ == "__main__":
    main()