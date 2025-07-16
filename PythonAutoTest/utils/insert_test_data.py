import pandas as pd
from datetime import datetime

def generate_insert_statements(excel_path):
    xls = pd.ExcelFile(excel_path)
    sql_statements = []
    
    for sheet_name in xls.sheet_names:
        df = pd.read_excel(xls, sheet_name=sheet_name)
        columns = df.columns.tolist()
        
        sql = f"INSERT INTO {sheet_name} ({', '.join(columns)}) VALUES"
        
        for _, row in df.iterrows():
            values = []
            for col in columns:
                value = row[col]
                if isinstance(value, datetime):
                    values.append(f"'{value.strftime('%Y-%m-%d %H:%M:%S')}'")
                elif pd.isna(value):
                    values.append("NULL")
                elif isinstance(value, (int, float)):
                    values.append(str(value))
                else:
                    strVal = str(value).replace("'", "''")
                    values.append(f"'{strVal}'")  # 修正引号转义
            sql += f" ({', '.join(values)})"
        
        sql_statements.append(sql.replace(") (", "),("))
    return ''.join(sql_statements)