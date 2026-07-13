import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Create reports directory if it doesn't exist
os.makedirs("reports", exist_ok=True)

# Load data
df = pd.read_csv("ai_image_eval_results.csv")

# Clean model names for display
df['Model'] = df['Model Name'].str.split('/').str[-1]

# 1. Overall Score Comparison
plt.figure(figsize=(10, 6))
sns.barplot(data=df, x='Model', y='Overall Score', errorbar='ci', capsize=0.1)
plt.title('Average Overall Score by Model')
plt.ylim(1, 5)
plt.ylabel('Score (1-5)')
plt.savefig('reports/overall_score.png', dpi=300, bbox_inches='tight')
plt.close()

# 2. Product Focus vs Realism
# We use "Product Focus" vs "Visual Quality" / "Fabric Realism"
plt.figure(figsize=(10, 6))
metrics = ['Product Focus', 'Fabric Realism', 'Anatomical Correctness']
melted_df = df.melt(id_vars=['Model'], value_vars=metrics, var_name='Metric', value_name='Score')
sns.barplot(data=melted_df, x='Metric', y='Score', hue='Model', errorbar='ci')
plt.title('Product Focus vs Realism Metrics')
plt.ylim(1, 5)
plt.ylabel('Score (1-5)')
plt.savefig('reports/focus_vs_realism.png', dpi=300, bbox_inches='tight')
plt.close()

print("Charts generated successfully in reports/ directory.")
