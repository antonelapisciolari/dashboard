
def filter_dataframe(df, filters):
    for column, value in filters.items():
        if column in df.columns:
            df = df[df[column] == value]
        else:
            print(f"Column '{column}' does not exist in the DataFrame.")
    
    return df

def getColumns(df, columns):
        missing_columns = [col for col in columns if col not in df.columns]
        if missing_columns:
            raise ValueError(f"Columns not found in DataFrame: {missing_columns}")
        
        return df[columns]
