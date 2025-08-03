import pandas as pd

# 创建示例数据
sample_data = {
    'X22': [2], 
    'X21': [1], 
    'X20': [1.0], 
    'X2(y)': ['4*y + 1'],
    'X32': [2.0], 
    'X31': [1], 
    'X30': [1], 
    'X3(y)': ['y**2 + 4*y + 1'],
    'X2': [2], 
    'X1': [1], 
    'X0': [1.0], 
    'X(y)': ['y**2 + 2*y + 1'],
    'Y6': [1.0], 
    'Y5': [0.8], 
    'Y4': [0.6], 
    'Y(x)': ['3*x + 3']
}

df = pd.DataFrame(sample_data)

# 保存为Excel文件
df.to_excel('sample_data.xlsx', index=False)
print("示例数据已保存到 sample_data.xlsx")
