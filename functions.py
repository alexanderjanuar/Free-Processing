import pandas as pd
import inspect
from sklearn.preprocessing import MinMaxScaler,LabelEncoder,StandardScaler

def drop_all_null(df):
    df.dropna(inplace=True)
    return df

def handle_null_median(df):
    df = df.fillna(df.median(numeric_only = True),inplace=True)
    return df

def handle_null_mean(df):
    df = df.fillna(df.mean(numeric_only = True),inplace=True)
    return df

def handle_null_mode(df):
    df.fillna(df.mode(numeric_only = True),inplace=True)
    return df

def handle_null_custom_numeric(df,custom_values):
    numeric_columns = df.select_dtypes(include=['number']).columns
    df[numeric_columns].fillna(custom_values,inplace=True)
    return df

def handle_null_mode_object(df):
    for column in df.select_dtypes(include=['object']):
        df[column].fillna(df[column].mode()[0], inplace=True)
    return df

def handle_null_custom_object(df,custom_values):
    for column in df.select_dtypes(include=['object']):
        df[column].fillna(custom_values, inplace=True)
    return df

def handle_null_custom(df,column,custom_values):
    df[column].fillna(custom_values, inplace=True)
    return df

#DUPLICATE
def drop_duplicate_columns(df):
    df.drop_duplicates(inplace=True)
    return df

#OUTLIERS
def remove_outlier(df, col_name):
    q1 = df[col_name].quantile(0.25)
    q3 = df[col_name].quantile(0.75)
    iqr = q3-q1 #Interquartile range
    fence_low  = q1-1.5*iqr
    fence_high = q3+1.5*iqr
    df = df.loc[(df[col_name] > fence_low) & (df[col_name] < fence_high)].reset_index(drop=True)
    return df

#ENCODING
def encoding_label_encoding(df):
    labelencoder = LabelEncoder()
    df = df.apply(lambda x: labelencoder.fit_transform(x))
    return df

def encoding_one_hot_encoding(df):
    df = pd.get_dummies(df)
    return df

#SCALING
def normalize_scaling(df,columns):
    # create a MinMaxScaler object
    scaler = MinMaxScaler()
    # apply normalization to the DataFrame
    df = scaler.fit_transform(df)
    df = pd.DataFrame(df, columns=columns)
    return df

def standarization_scaling(df,columns):
    # create a MinMaxScaler object
    scaler = StandardScaler()
    # apply normalization to the DataFrame
    df = scaler.fit_transform(df)
    df = pd.DataFrame(df, columns=columns)
    return df