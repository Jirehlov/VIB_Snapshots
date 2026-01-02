import pandas as pd
from scipy.stats import mannwhitneyu, kruskal, wilcoxon, spearmanr
from scipy.stats import ks_2samp, shapiro, bartlett, levene, kendalltau
file_path = 'sorted1.csv'
df = pd.read_csv(file_path)
first_group = df.iloc[:, 7:17]
second_group = df.iloc[:, 20:30]
mannwhitney_pvalues = []
kruskal_pvalues = []
wilcoxon_pvalues = []
spearman_pvalues = []
ks_pvalues = []
shapiro_pvalues = []
bartlett_pvalues = []
levene_pvalues = []
kendalltau_pvalues = []
for i in range(len(df)):
    _, mannwhitney_pvalue = mannwhitneyu(first_group.iloc[i], second_group.iloc[i], alternative='two-sided')
    mannwhitney_pvalues.append(mannwhitney_pvalue)
    _, kruskal_pvalue = kruskal(first_group.iloc[i], second_group.iloc[i])
    kruskal_pvalues.append(kruskal_pvalue)
    try:
        _, wilcoxon_pvalue = wilcoxon(first_group.iloc[i], second_group.iloc[i])
    except ValueError:
        wilcoxon_pvalue = None
    wilcoxon_pvalues.append(wilcoxon_pvalue)
    _, spearman_pvalue = spearmanr(first_group.iloc[i], second_group.iloc[i])
    spearman_pvalues.append(spearman_pvalue)
    _, ks_pvalue = ks_2samp(first_group.iloc[i], second_group.iloc[i])
    ks_pvalues.append(ks_pvalue)
    try:
        _, shapiro_pvalue = shapiro(first_group.iloc[i])
    except ValueError:
        shapiro_pvalue = None
    shapiro_pvalues.append(shapiro_pvalue)
    try:
        _, bartlett_pvalue = bartlett(first_group.iloc[i], second_group.iloc[i])
    except ValueError:
        bartlett_pvalue = None
    bartlett_pvalues.append(bartlett_pvalue)
    _, levene_pvalue = levene(first_group.iloc[i], second_group.iloc[i])
    levene_pvalues.append(levene_pvalue)
    _, kendalltau_pvalue = kendalltau(first_group.iloc[i], second_group.iloc[i])
    kendalltau_pvalues.append(kendalltau_pvalue)
df['Mann-Whitney p-value'] = mannwhitney_pvalues
df['Kruskal-Wallis p-value'] = kruskal_pvalues
df['Wilcoxon p-value'] = wilcoxon_pvalues
df['Spearman p-value'] = spearman_pvalues
df['Kolmogorov-Smirnov p-value'] = ks_pvalues
df['Shapiro-Wilk p-value'] = shapiro_pvalues
df['Bartlett p-value'] = bartlett_pvalues
df['Levene p-value'] = levene_pvalues
df['Kendall’s Tau p-value'] = kendalltau_pvalues
output_file_path = 'sorted1_with_tests.csv'
df.to_csv(output_file_path, index=False, encoding='utf-8-sig')
