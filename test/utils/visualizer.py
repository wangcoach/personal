import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

def plot_heatmap(df, colormap_ovlx='viridis', colormap_ovly='plasma'):
    """
    绘制热力图
    """
    # 重新整理数据为网格形式
    x_unique = sorted(df['x'].unique())
    y_unique = sorted(df['y'].unique())
    
    ovlx_grid = np.zeros((len(y_unique), len(x_unique)))
    ovly_grid = np.zeros((len(y_unique), len(x_unique)))
    
    for i, y_val in enumerate(y_unique):
        for j, x_val in enumerate(x_unique):
            mask = (df['x'] == x_val) & (df['y'] == y_val)
            if mask.any():
                ovlx_grid[i, j] = df.loc[mask, 'ovlx'].iloc[0]
                ovly_grid[i, j] = df.loc[mask, 'ovly'].iloc[0]
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    
    # OVLX热力图
    im1 = ax1.imshow(ovlx_grid, cmap=colormap_ovlx, aspect='auto', origin='lower',
                     extent=[min(x_unique), max(x_unique), min(y_unique), max(y_unique)])
    ax1.set_xlabel('X', fontsize=12)
    ax1.set_ylabel('Y', fontsize=12)
    ax1.set_title('OVLX Heat Map', fontsize=14, fontweight='bold')
    plt.colorbar(im1, ax=ax1, label='OVLX Value')
    
    # OVLY热力图
    im2 = ax2.imshow(ovly_grid, cmap=colormap_ovly, aspect='auto', origin='lower',
                     extent=[min(x_unique), max(x_unique), min(y_unique), max(y_unique)])
    ax2.set_xlabel('X', fontsize=12)
    ax2.set_ylabel('Y', fontsize=12)
    ax2.set_title('OVLY Heat Map', fontsize=14, fontweight='bold')
    plt.colorbar(im2, ax=ax2, label='OVLY Value')
    
    plt.tight_layout()
    return fig

def plot_scatter(df, colormap_ovlx='viridis', colormap_ovly='plasma'):
    """
    绘制散点图
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    
    # OVLX散点图
    scatter1 = ax1.scatter(df['x'], df['y'], c=df['ovlx'], cmap=colormap_ovlx, s=20, alpha=0.8)
    ax1.set_xlabel('X', fontsize=12)
    ax1.set_ylabel('Y', fontsize=12)
    ax1.set_title('OVLX Scatter Plot', fontsize=14, fontweight='bold')
    ax1.grid(True, alpha=0.3)
    plt.colorbar(scatter1, ax=ax1, label='OVLX Value')
    
    # OVLY散点图
    scatter2 = ax2.scatter(df['x'], df['y'], c=df['ovly'], cmap=colormap_ovly, s=20, alpha=0.8)
    ax2.set_xlabel('X', fontsize=12)
    ax2.set_ylabel('Y', fontsize=12)
    ax2.set_title('OVLY Scatter Plot', fontsize=14, fontweight='bold')
    ax2.grid(True, alpha=0.3)
    plt.colorbar(scatter2, ax=ax2, label='OVLY Value')
    
    plt.tight_layout()
    return fig

def create_summary_stats(df):
    """
    创建统计摘要
    """
    stats = {
        'OVLX': {
            'min': df['ovlx'].min(),
            'max': df['ovlx'].max(),
            'mean': df['ovlx'].mean(),
            'std': df['ovlx'].std(),
            'median': df['ovlx'].median()
        },
        'OVLY': {
            'min': df['ovly'].min(),
            'max': df['ovly'].max(),
            'mean': df['ovly'].mean(),
            'std': df['ovly'].std(),
            'median': df['ovly'].median()
        }
    }
    return stats