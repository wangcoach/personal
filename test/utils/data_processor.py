import pandas as pd
import re

def parse_df_to_res(df):
    """
    解析DataFrame，将列数据重新组织为嵌套字典结构
    """
    res = {}
    
    for row_idx, row in df.iterrows():
        for col in df.columns:
            if '(' in col and ')' in col:
                equation_part = col.split('(')[0]
                variable = col.split('(')[1].rstrip(')')
                
                if equation_part in ['X', 'Y']:
                    equation = equation_part + '1'
                else:
                    equation = equation_part
                
                if equation not in res:
                    res[equation] = {}
                res[equation][variable] = row[col]
                
            else:
                if col[0] in ['X', 'Y']:
                    equation_prefix = col[0]
                    order = col[1:]
                    
                    if len(order) >= 2:
                        first_digit = int(order[0])
                        remaining = order[1:]
                        
                        if first_digit >= 1:
                            equation = equation_prefix + str(first_digit)
                            actual_order = remaining
                        else:
                            equation = equation_prefix + '1'
                            actual_order = order
                    else:
                        equation = equation_prefix + '1'
                        actual_order = order
                    
                    if equation not in res:
                        res[equation] = {}
                    res[equation][actual_order] = row[col]
    
    return res

def validate_dataframe(df):
    """
    验证DataFrame格式是否正确
    """
    try:
        if df.empty:
            return {"is_valid": False, "error": "数据为空"}
        
        # 检查列名格式
        valid_patterns = [
            r'^[XY]\d*$',  # X1, Y2, X, Y等
            r'^[XY]\d*\([xy]\)$'  # X1(y), Y2(x)等
        ]
        
        invalid_cols = []
        for col in df.columns:
            if not any(re.match(pattern, col) for pattern in valid_patterns):
                invalid_cols.append(col)
        
        if invalid_cols:
            return {
                "is_valid": False, 
                "error": f"列名格式不正确: {invalid_cols}"
            }
        
        return {"is_valid": True, "error": None}
        
    except Exception as e:
        return {"is_valid": False, "error": str(e)}