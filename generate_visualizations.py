import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Load the dataset (updated to match your file name)
df = pd.read_csv('nasa_cneos_cleaned.csv')

# Set aesthetic styling
sns.set_theme(style="whitegrid")
plt.rcParams.update({'font.sans-serif': 'Arial', 'font.size': 11})

# ---------------------------------------------------------
# Chart 1: Distribution of Asteroid Risk Scores
# ---------------------------------------------------------
if 'risk_score' in df.columns:
    plt.figure(figsize=(8, 5))
    sns.histplot(df['risk_score'], bins=20, kde=True, color='#1f77b4')
    plt.title('Distribution of Asteroid Risk Scores', fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('Risk Score')
    plt.ylabel('Asteroid Count')
    plt.tight_layout()
    plt.savefig('chart1_risk_distribution.png', dpi=300)
    plt.close()

# ---------------------------------------------------------
# Chart 2: Size Class vs. Average Miss Distance (LD)
# ---------------------------------------------------------
if 'size_class' in df.columns and 'miss_distance_ld' in df.columns:
    plt.figure(figsize=(8, 5))
    avg_miss = df.groupby('size_class')['miss_distance_ld'].mean().reset_index()
    sns.barplot(data=avg_miss, x='size_class', y='miss_distance_ld', palette='Blues_d')
    plt.title('Average Miss Distance by Size Class', fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('Size Class')
    plt.ylabel('Avg Miss Distance (Lunar Distances)')
    plt.tight_layout()
    plt.savefig('chart2_miss_distance_by_size.png', dpi=300)
    plt.close()

# ---------------------------------------------------------
# Chart 3: Velocity vs. Risk Score Scatter Plot
# ---------------------------------------------------------
if 'v_inf' in df.columns and 'risk_score' in df.columns:
    plt.figure(figsize=(8, 5))
    hue_param = 'risk_level' if 'risk_level' in df.columns else None
    sns.scatterplot(data=df, x='v_inf', y='risk_score', hue=hue_param, palette='Set1', alpha=0.7)
    plt.title('Velocity (v_inf) vs. Risk Score', fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('Velocity at Infinity (km/s)')
    plt.ylabel('Risk Score')
    if hue_param:
        plt.legend(title='Threat Level')
    plt.tight_layout()
    plt.savefig('chart3_velocity_vs_risk.png', dpi=300)
    plt.close()

print("All 3 Matplotlib charts generated and saved successfully as PNG images!")