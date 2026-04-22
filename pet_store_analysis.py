"""
Pet Store Records 2020 - Data Analysis
======================================
Course: ACC102 - Python Data Product
Data Source: Kaggle - Pet Store Records 2020
URL: https://www.kaggle.com/datasets/ippudkiippude/pet-store-records-2020
Date Accessed: April 17, 2026

Analytical Problem: Analyze pet store sales performance and identify key factors 
affecting product success to provide actionable business insights.
Target Audience: Pet store management and marketing team
"""

# ============================================================
# PART 1: IMPORT LIBRARIES
# ============================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# Set style for better visualizations
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("husl")

# ============================================================
# PART 2: DATA LOADING AND INITIAL EXPLORATION
# ============================================================

def load_and_explore_data(file_path):
    """
    Load the dataset and perform initial exploration
    """
    print("="*60)
    print("PET STORE RECORDS 2020 - DATA ANALYSIS")
    print("="*60)
    
    # Load data
    df = pd.read_csv(file_path)
    
    print("\n1. DATASET OVERVIEW")
    print("-"*40)
    print(f"Dataset Shape: {df.shape[0]} rows × {df.shape[1]} columns")
    print(f"\nColumn Names:\n{list(df.columns)}")
    
    print("\n2. DATA TYPES")
    print("-"*40)
    print(df.dtypes)
    
    print("\n3. MISSING VALUES")
    print("-"*40)
    missing = df.isnull().sum()
    print(missing if missing.sum() > 0 else "No missing values found ✓")
    
    print("\n4. DUPLICATE ROWS")
    print("-"*40)
    duplicates = df.duplicated().sum()
    print(f"Number of duplicate rows: {duplicates}")
    
    print("\n5. FIRST 5 ROWS")
    print("-"*40)
    print(df.head())
    
    return df


# ============================================================
# PART 3: DESCRIPTIVE STATISTICS
# ============================================================

def descriptive_statistics(df):
    """
    Generate comprehensive descriptive statistics
    """
    print("\n" + "="*60)
    print("DESCRIPTIVE STATISTICS")
    print("="*60)
    
    # Numeric columns statistics
    numeric_cols = ['sales', 'price', 'rating']
    print("\n1. NUMERIC VARIABLES SUMMARY")
    print("-"*40)
    print(df[numeric_cols].describe().round(2))
    
    # Categorical columns distribution
    print("\n2. CATEGORICAL VARIABLES DISTRIBUTION")
    print("-"*40)
    
    categorical_cols = ['product_category', 'pet_type', 'pet_size', 'country', 'VAP', 're_buy']
    
    for col in categorical_cols:
        print(f"\n{col.upper()}:")
        print(df[col].value_counts().head(10))
    
    # Key business metrics
    print("\n3. KEY BUSINESS METRICS")
    print("-"*40)
    print(f"Total Sales Volume: {df['sales'].sum():,} units")
    print(f"Average Product Price: ₹{df['price'].mean():,.2f}")
    print(f"Total Revenue (Est.): ₹{(df['sales'] * df['price']).sum():,.2f}")
    print(f"Average Customer Rating: {df['rating'].mean():.2f}/10")
    print(f"Repeat Purchase Rate: {(df['re_buy'].mean() * 100):.1f}%")
    print(f"Products Requiring Vet Approval: {(df['VAP'].mean() * 100):.1f}%")


# ============================================================
# PART 4: DATA VISUALIZATION
# ============================================================

def create_visualizations(df, output_dir='/mnt/okcomputer/output/'):
    """
    Create comprehensive visualizations for the analysis
    """
    print("\n" + "="*60)
    print("CREATING VISUALIZATIONS")
    print("="*60)
    
    # 1. Sales Distribution by Product Category
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    
    # Plot 1: Sales by Product Category
    category_sales = df.groupby('product_category')['sales'].sum().sort_values(ascending=False)
    axes[0, 0].bar(category_sales.index, category_sales.values, color='steelblue')
    axes[0, 0].set_title('Total Sales by Product Category', fontsize=14, fontweight='bold')
    axes[0, 0].set_xlabel('Product Category')
    axes[0, 0].set_ylabel('Total Sales (Units)')
    axes[0, 0].tick_params(axis='x', rotation=45)
    
    # Plot 2: Price Distribution
    axes[0, 1].hist(df['price'], bins=30, color='coral', edgecolor='black', alpha=0.7)
    axes[0, 1].set_title('Price Distribution', fontsize=14, fontweight='bold')
    axes[0, 1].set_xlabel('Price (INR)')
    axes[0, 1].set_ylabel('Frequency')
    axes[0, 1].axvline(df['price'].mean(), color='red', linestyle='--', 
                       label=f'Mean: ₹{df["price"].mean():.0f}')
    axes[0, 1].legend()
    
    # Plot 3: Sales by Pet Type
    pet_sales = df.groupby('pet_type')['sales'].sum().sort_values(ascending=False)
    axes[1, 0].bar(pet_sales.index, pet_sales.values, color='lightgreen')
    axes[1, 0].set_title('Total Sales by Pet Type', fontsize=14, fontweight='bold')
    axes[1, 0].set_xlabel('Pet Type')
    axes[1, 0].set_ylabel('Total Sales (Units)')
    
    # Plot 4: Rating Distribution
    rating_counts = df['rating'].value_counts().sort_index()
    axes[1, 1].bar(rating_counts.index, rating_counts.values, color='gold', edgecolor='black')
    axes[1, 1].set_title('Customer Rating Distribution', fontsize=14, fontweight='bold')
    axes[1, 1].set_xlabel('Rating (1-10)')
    axes[1, 1].set_ylabel('Number of Products')
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}figure1_overview_analysis.png', dpi=300, bbox_inches='tight')
    print("✓ Figure 1 saved: Overview Analysis")
    plt.close()
    
    # 2. Advanced Analysis - Correlation and Relationships
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    
    # Plot 1: Price vs Sales Scatter Plot
    scatter = axes[0, 0].scatter(df['price'], df['sales'], 
                                  c=df['rating'], cmap='viridis', alpha=0.6, s=50)
    axes[0, 0].set_title('Price vs Sales (Colored by Rating)', fontsize=14, fontweight='bold')
    axes[0, 0].set_xlabel('Price (INR)')
    axes[0, 0].set_ylabel('Sales (Units)')
    plt.colorbar(scatter, ax=axes[0, 0], label='Rating')
    
    # Plot 2: Repeat Purchase Analysis
    rebuy_analysis = df.groupby('product_category')['re_buy'].mean().sort_values(ascending=False)
    axes[0, 1].barh(rebuy_analysis.index, rebuy_analysis.values * 100, color='mediumpurple')
    axes[0, 1].set_title('Repeat Purchase Rate by Category', fontsize=14, fontweight='bold')
    axes[0, 1].set_xlabel('Repeat Purchase Rate (%)')
    
    # Plot 3: Sales by Country (Top 5)
    country_sales = df.groupby('country')['sales'].sum().sort_values(ascending=False).head(5)
    axes[1, 0].pie(country_sales.values, labels=country_sales.index, autopct='%1.1f%%',
                   startangle=90, colors=plt.cm.Set3.colors)
    axes[1, 0].set_title('Sales Distribution by Country (Top 5)', fontsize=14, fontweight='bold')
    
    # Plot 4: Average Rating by Product Category
    avg_rating = df.groupby('product_category')['rating'].mean().sort_values(ascending=False)
    axes[1, 1].bar(range(len(avg_rating)), avg_rating.values, color='teal')
    axes[1, 1].set_title('Average Rating by Product Category', fontsize=14, fontweight='bold')
    axes[1, 1].set_xlabel('Product Category')
    axes[1, 1].set_ylabel('Average Rating')
    axes[1, 1].set_xticks(range(len(avg_rating)))
    axes[1, 1].set_xticklabels(avg_rating.index, rotation=45, ha='right')
    axes[1, 1].set_ylim(0, 10)
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}figure2_advanced_analysis.png', dpi=300, bbox_inches='tight')
    print("✓ Figure 2 saved: Advanced Analysis")
    plt.close()
    
    # 3. Business Insights Visualization
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    
    # Plot 1: Revenue by Category (Sales × Price)
    df['revenue'] = df['sales'] * df['price']
    revenue_by_category = df.groupby('product_category')['revenue'].sum().sort_values(ascending=False)
    axes[0, 0].bar(revenue_by_category.index, revenue_by_category.values / 1000000, color='darkorange')
    axes[0, 0].set_title('Total Revenue by Product Category', fontsize=14, fontweight='bold')
    axes[0, 0].set_xlabel('Product Category')
    axes[0, 0].set_ylabel('Revenue (Million INR)')
    axes[0, 0].tick_params(axis='x', rotation=45)
    
    # Plot 2: VAP Impact on Sales
    vap_sales = df.groupby('VAP')['sales'].mean()
    vap_labels = ['No VAP Required', 'VAP Required']
    axes[0, 1].bar(vap_labels, vap_sales.values, color=['lightcoral', 'lightblue'])
    axes[0, 1].set_title('Average Sales: VAP vs Non-VAP Products', fontsize=14, fontweight='bold')
    axes[0, 1].set_ylabel('Average Sales (Units)')
    for i, v in enumerate(vap_sales.values):
        axes[0, 1].text(i, v + 2, f'{v:.1f}', ha='center', fontweight='bold')
    
    # Plot 3: Pet Size vs Sales
    size_sales = df.groupby('pet_size')['sales'].sum().sort_values(ascending=False)
    axes[1, 0].bar(size_sales.index, size_sales.values, color='seagreen')
    axes[1, 0].set_title('Total Sales by Pet Size', fontsize=14, fontweight='bold')
    axes[1, 0].set_xlabel('Pet Size')
    axes[1, 0].set_ylabel('Total Sales (Units)')
    
    # Plot 4: Rating vs Repeat Purchase
    rating_rebuy = df.groupby('rating')['re_buy'].mean() * 100
    axes[1, 1].plot(rating_rebuy.index, rating_rebuy.values, marker='o', 
                    linewidth=2, markersize=8, color='navy')
    axes[1, 1].set_title('Repeat Purchase Rate by Rating', fontsize=14, fontweight='bold')
    axes[1, 1].set_xlabel('Customer Rating')
    axes[1, 1].set_ylabel('Repeat Purchase Rate (%)')
    axes[1, 1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}figure3_business_insights.png', dpi=300, bbox_inches='tight')
    print("✓ Figure 3 saved: Business Insights")
    plt.close()


# ============================================================
# PART 5: STATISTICAL ANALYSIS
# ============================================================

def statistical_analysis(df):
    """
    Perform statistical tests and correlation analysis
    """
    print("\n" + "="*60)
    print("STATISTICAL ANALYSIS")
    print("="*60)
    
    # 1. Correlation Analysis
    print("\n1. CORRELATION MATRIX (Numeric Variables)")
    print("-"*40)
    numeric_df = df[['sales', 'price', 'rating', 're_buy', 'VAP']]
    correlation = numeric_df.corr()
    print(correlation.round(3))
    
    # 2. T-test: VAP vs Non-VAP Products
    print("\n2. T-TEST: VAP vs Non-VAP Products (Sales)")
    print("-"*40)
    vap_sales = df[df['VAP'] == 1]['sales']
    non_vap_sales = df[df['VAP'] == 0]['sales']
    
    t_stat, p_value = stats.ttest_ind(vap_sales, non_vap_sales)
    print(f"VAP Products - Mean Sales: {vap_sales.mean():.2f}, Std: {vap_sales.std():.2f}")
    print(f"Non-VAP Products - Mean Sales: {non_vap_sales.mean():.2f}, Std: {non_vap_sales.std():.2f}")
    print(f"T-statistic: {t_stat:.4f}")
    print(f"P-value: {p_value:.4f}")
    print(f"Result: {'Significant' if p_value < 0.05 else 'Not Significant'} difference")
    
    # 3. T-test: Repeat Purchase vs Non-Repeat
    print("\n3. T-TEST: Repeat vs Non-Repeat Products (Rating)")
    print("-"*40)
    repeat_rating = df[df['re_buy'] == 1]['rating']
    non_repeat_rating = df[df['re_buy'] == 0]['rating']
    
    t_stat2, p_value2 = stats.ttest_ind(repeat_rating, non_repeat_rating)
    print(f"Repeat Products - Mean Rating: {repeat_rating.mean():.2f}")
    print(f"Non-Repeat Products - Mean Rating: {non_repeat_rating.mean():.2f}")
    print(f"T-statistic: {t_stat2:.4f}")
    print(f"P-value: {p_value2:.4f}")
    print(f"Result: {'Significant' if p_value2 < 0.05 else 'Not Significant'} difference")
    
    # 4. ANOVA: Sales across Pet Types
    print("\n4. ANOVA: Sales across Different Pet Types")
    print("-"*40)
    pet_groups = [df[df['pet_type'] == pet]['sales'] for pet in df['pet_type'].unique()]
    f_stat, p_value3 = stats.f_oneway(*pet_groups)
    print(f"F-statistic: {f_stat:.4f}")
    print(f"P-value: {p_value3:.4f}")
    print(f"Result: {'Significant' if p_value3 < 0.05 else 'Not Significant'} difference across pet types")
    
    return correlation


# ============================================================
# PART 6: BUSINESS INSIGHTS AND RECOMMENDATIONS
# ============================================================

def generate_insights(df):
    """
    Generate key business insights and recommendations
    """
    print("\n" + "="*60)
    print("KEY BUSINESS INSIGHTS & RECOMMENDATIONS")
    print("="*60)
    
    # Calculate derived metrics
    df['revenue'] = df['sales'] * df['price']
    
    print("\n1. TOP PERFORMING CATEGORIES (By Revenue)")
    print("-"*40)
    revenue_by_category = df.groupby('product_category').agg({
        'revenue': 'sum',
        'sales': 'sum',
        'rating': 'mean'
    }).round(2)
    revenue_by_category = revenue_by_category.sort_values('revenue', ascending=False)
    print(revenue_by_category.head())
    
    print("\n2. MOST REPEAT-PURCHASED CATEGORIES")
    print("-"*40)
    repeat_rate = df.groupby('product_category')['re_buy'].mean().sort_values(ascending=False) * 100
    print(repeat_rate.round(1))
    
    print("\n3. PRICE-SALES RELATIONSHIP INSIGHTS")
    print("-"*40)
    # Create price segments
    df['price_segment'] = pd.cut(df['price'], 
                                  bins=[0, 5000, 10000, 15000, float('inf')],
                                  labels=['Low (<₹5K)', 'Medium (₹5K-10K)', 
                                         'High (₹10K-15K)', 'Premium (>₹15K)'])
    
    price_analysis = df.groupby('price_segment').agg({
        'sales': 'mean',
        'rating': 'mean',
        're_buy': 'mean'
    }).round(2)
    print(price_analysis)
    
    print("\n4. COUNTRY-WISE PERFORMANCE")
    print("-"*40)
    country_performance = df.groupby('country').agg({
        'revenue': 'sum',
        'sales': 'sum',
        'rating': 'mean'
    }).round(2)
    country_performance = country_performance.sort_values('revenue', ascending=False)
    print(country_performance.head(8))
    
    print("\n5. KEY RECOMMENDATIONS")
    print("-"*40)
    
    # Find highest revenue category
    top_revenue_cat = revenue_by_category.index[0]
    
    # Find highest repeat rate category
    top_repeat_cat = repeat_rate.index[0]
    
    # Find best rated category
    best_rated = df.groupby('product_category')['rating'].mean().sort_values(ascending=False)
    best_rated_cat = best_rated.index[0]
    
    print(f"✓ Focus on '{top_revenue_cat}' category - generates highest revenue")
    print(f"✓ Promote '{top_repeat_cat}' category - highest customer loyalty")
    print(f"✓ Maintain quality in '{best_rated_cat}' category - best customer satisfaction")
    
    # VAP insight
    vap_impact = df.groupby('VAP')['sales'].mean()
    if vap_impact[1] > vap_impact[0]:
        print(f"✓ VAP-approved products sell {((vap_impact[1]/vap_impact[0]-1)*100):.1f}% better - expand vet-approved range")
    
    # Rating insight
    high_rating = df[df['rating'] >= 8]['re_buy'].mean()
    low_rating = df[df['rating'] <= 5]['re_buy'].mean()
    print(f"✓ High-rated products (≥8) have {(high_rating/low_rating-1)*100:.1f}% higher repeat purchase rate")
    
    print("\n" + "="*60)
    print("ANALYSIS COMPLETED SUCCESSFULLY")
    print("="*60)


# ============================================================
# PART 7: MAIN EXECUTION
# ============================================================

def main():
    """
    Main function to run the complete analysis
    """
    # File path - update this to your local path
    file_path = 'pet_store_records_2020.csv'
    
    # Run all analysis steps
    df = load_and_explore_data(file_path)
    descriptive_statistics(df)
    create_visualizations(df)
    correlation = statistical_analysis(df)
    generate_insights(df)
    
    # Save processed data
    output_path = '/mnt/okcomputer/output/processed_pet_store_data.csv'
    df.to_csv(output_path, index=False)
    print(f"\n✓ Processed data saved to: {output_path}")
    
    return df


# Execute main function
if __name__ == "__main__":
    df = main()
