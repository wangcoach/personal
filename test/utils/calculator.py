import numpy as np
import pandas as pd
from sympy import symbols, sympify

def cal(res, x_val, y_val):
    """
    计算ovlx和ovly
    """
    x, y = symbols('x y')
    
    ovlx = 0
    ovly = 0
    
    # 处理X方程
    x_equations = {k: v for k, v in res.items() if k.startswith('X')}
    for equation_name, equation_data in x_equations.items():
        polynomial = 0
        for key, coeff in equation_data.items():
            if key.isdigit():
                power = int(key)
                polynomial += coeff * (x ** power)
        
        y_function = 1
        if 'y' in equation_data:
            try:
                y_function = sympify(equation_data['y'])
            except:
                y_function = float(equation_data['y'])
        
        equation_result = polynomial * y_function
        try:
            if hasattr(equation_result, 'subs'):
                numerical_result = float(equation_result.subs([(x, x_val), (y, y_val)]))
            else:
                numerical_result = float(equation_result)
            ovlx += numerical_result
        except:
            pass
    
    # 处理Y方程
    y_equations = {k: v for k, v in res.items() if k.startswith('Y')}
    for equation_name, equation_data in y_equations.items():
        polynomial = 0
        for key, coeff in equation_data.items():
            if key.isdigit():
                power = int(key)
                polynomial += coeff * (y ** power)
        
        x_function = 1
        if 'x' in equation_data:
            try:
                x_function = sympify(equation_data['x'])
            except:
                x_function = float(equation_data['x'])
        
        equation_result = polynomial * x_function
        try:
            if hasattr(equation_result, 'subs'):
                numerical_result = float(equation_result.subs([(x, x_val), (y, y_val)]))
            else:
                numerical_result = float(equation_result)
            ovly += numerical_result
        except:
            pass
    
    return ovlx, ovly

def generate_grid_and_calculate(res, x_range, y_range, x_count=50, y_count=50, progress_callback=None):
    """
    生成网格坐标点并计算每个点的ovlx和ovly值
    """
    x_min, x_max = x_range
    y_min, y_max = y_range
    
    x_edges = np.linspace(x_min, x_max, x_count + 1)
    y_edges = np.linspace(y_min, y_max, y_count + 1)
    
    x_centers = (x_edges[:-1] + x_edges[1:]) / 2
    y_centers = (y_edges[:-1] + y_edges[1:]) / 2
    
    x_grid, y_grid = np.meshgrid(x_centers, y_centers)
    
    x_coords = x_grid.flatten()
    y_coords = y_grid.flatten()
    
    ovlx_values = []
    ovly_values = []
    
    total_points = len(x_coords)
    
    for i, (x_val, y_val) in enumerate(zip(x_coords, y_coords)):
        try:
            ovlx, ovly = cal(res, x_val, y_val)
            ovlx_values.append(ovlx)
            ovly_values.append(ovly)
        except Exception:
            ovlx_values.append(np.nan)
            ovly_values.append(np.nan)
        
        # 更新进度
        if progress_callback and i % 100 == 0:
            progress_callback((i + 1) / total_points)
    
    if progress_callback:
        progress_callback(1.0)
    
    result_df = pd.DataFrame({
        'x': x_coords,
        'y': y_coords,
        'ovlx': ovlx_values,
        'ovly': ovly_values
    })
    
    return result_df