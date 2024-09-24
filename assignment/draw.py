import matplotlib.pyplot as plt
import seaborn as sns

def draw_scatter(norads, alts):
    plt.scatter(norads, alts, s=15)
    plt.title('Starlink Altitude distribution of satellites')
    plt.xlabel('Norad')
    plt.ylabel('Alt(km)')
    plt.show()

def draw_bar(norads, alts):
    plt.bar(norads, alts)
    plt.title('Starlink Altitude distribution of satellites')
    plt.xlabel('Norad')
    plt.ylabel('Alt(km)')
    plt.show()
    
def draw_scatter2(norads, alts):
    sns.set()
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x=norads, y=alts)
    plt.title('Starlink卫星的高度分布')
    plt.xlabel('Norad')
    plt.ylabel('高度(km)')
    plt.show()