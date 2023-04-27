import streamlit as st
import pandas as pd
import plotly.graph_objs as go
from functions import *
import inspect
from sklearn.preprocessing import MinMaxScaler,LabelEncoder,StandardScaler
import os

st.set_page_config(layout="wide")

st.markdown("<h1 style='text-align: center;'>Free-Process</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>📑Preprocess Text File📑 </h3>", unsafe_allow_html=True)
st.text("")
st.text("")

col1, col2 = st.columns((1.2,1.8))

@st.cache_data
def load_data_csv(url):
    df = pd.read_csv(url)
    return df

@st.cache_data
def load_data_xlsx(url):
    df = pd.read_excel(url)
    return df

@st.cache_data
def convert_df(df):
    return df.to_csv().encode('utf-8')

def reset_session():
    if 'df' in st.session_state:
        del st.session_state['df'] 



def generate_null_plot(columns):
    null_counts = st.session_state['df'][columns].isnull().sum().sort_values(ascending=False)
    null_counts = null_counts[null_counts>0]

    fig = go.Figure(data=[go.Bar(x=null_counts.index, y=null_counts.values)])
    fig.update_layout(xaxis_title='Column Name', yaxis_title='Count')
    st.plotly_chart(fig, use_container_width=True)

def show_boxplot(columns):
    box = go.Box(y=st.session_state['df'][columns])
    layout = go.Layout(title='Box Plot Example')
    fig = go.Figure(data=[box], layout=layout)
    st.plotly_chart(fig, use_container_width=True)

def success_message(message,code):
    code = inspect.getsource(code)
    st.success(message, icon="✅")
    st.markdown("<h4>Code</h4>", unsafe_allow_html=True)
    st.code(code, language='python')


st.session_state.disabled = True
with col1:
    uploaded_file = st.file_uploader(label='',on_change=reset_session)
    if uploaded_file is not None:
        try: 
            if 'df' not in st.session_state:
                
                    file_extension = os.path.splitext(uploaded_file.name)[1]
                    if(file_extension == '.csv'):
                        st.session_state['df'] = load_data_csv(uploaded_file)
                    else:
                        st.session_state['df'] = load_data_xlsx(uploaded_file)
                


            inter_cols_pace,colInfo1, inter_cols_pace, colInfo2,inter_cols_pace = st.columns((2,2,2,2,2))
            with colInfo1:
                st.metric("Rows", st.session_state['df'].shape[0])
            with colInfo2:
                st.metric("Columns", st.session_state['df'].shape[1])
            st.write(st.session_state['df'].head())

            with st.expander("Dataframe Description"):
                st.write(st.session_state['df'].describe(include='all'))


            csv = convert_df(st.session_state['df'])
            st.download_button(
                label="Download data as CSV",
                data=csv,
                file_name='data.csv',
                mime='text/csv',
            )
            st.session_state.disabled = False
            
        except KeyError:
            st.error('Only accept CSV or XLSX files', icon="🚨")
        except ValueError:
                st.error('Only accept CSV or XLSX files', icon="🚨")
        
with col2:
    try:
        option = st.selectbox(
            "",
            ("Handle Null", "Duplicates", "Outlier","Encoding","Scaling"),
            disabled=st.session_state.disabled,
            )
        st.write(" ")
        
        if uploaded_file is not None:
            if option == "Handle Null":
                st.markdown("<h4>Null Value Counts</h4>", unsafe_allow_html=True)
                option = st.selectbox(
                    "Columns Data Type",
                    ("All", "Numeric", "Object","Others"),
                    disabled=st.session_state.disabled)

                if option=='All':
                    generate_null_plot(st.session_state['df'].columns)
                    button_drop_all_null = st.button('Drop Null')

                    if button_drop_all_null:
                        st.session_state['df'] = drop_all_null(st.session_state['df'])
                        success_message('Drop All Null Success',drop_all_null)


                #Numeric Null Imputation
                elif (option == "Numeric"):
                    numeric_columns = st.session_state['df'].select_dtypes(include=['number']).columns 
                    generate_null_plot(numeric_columns)

                    col_null_1,col_null_2,col_null_3 = st.columns((2,1,2))

                    with col_null_1:
                        option_null = st.selectbox(
                            "Imputation Method",
                            ("Median", "Mean", "Modus","Custom Value"),
                            disabled=st.session_state.disabled)
                    
                    with col_null_2:
                        st.write("")
                        st.write("")
                        button_null = st.button("Submit")

                    if(option_null=="Custom Value"):
                        number_null = st.number_input('Insert a number')

                    if button_null:
                        if(option_null == "Median"):
                            handle_null_median(st.session_state['df'])
                            success_message(' Imputation Success',handle_null_median)

                        elif(option_null == "Mean"):
                            handle_null_median(st.session_state['df'])
                            success_message(' Imputation Success',handle_null_median)
                        
                        elif(option_null == "Median"):
                            handle_null_mode(st.session_state['df'])
                            success_message(' Imputation Success',handle_null_mode)
                        
                        elif(option_null == "Custom Value"):
                            handle_null_custom_numeric(st.session_state['df'])
                            success_message(' Imputation Success',handle_null_custom_numeric)
                    

                #Object Null Imputation
                elif (option == "Object"):
                    object_columns = st.session_state['df'].select_dtypes(include=['object']).columns 
                    generate_null_plot(object_columns)

                    col_null_1,col_null_2,col_null_3 = st.columns((2,1,2))

                    with col_null_1:
                        option_null = st.selectbox(
                            "Imputation Method",
                            ("Mode","Custom Value"),
                            disabled=st.session_state.disabled)
                    
                    with col_null_2:
                        st.write("")
                        st.write("")
                        button_null = st.button("Submit")

                    if(option_null=="Custom Value"):
                        text_null = st.text_input('Insert a text', 'Unknown')
                    
                    if button_null:
                        if(option_null == "Mode"):
                            handle_null_mode_object(st.session_state['df'])
                            success_message(' Imputation Success',handle_null_mode_object)

                        elif(option_null == "Custom Value"):
                            handle_null_custom_object(st.session_state['df'],text_null)
                            success_message(' Imputation Success',handle_null_custom_object)
                
                #Custom Values Null Imputation
                elif (option == "Others"):
                    try:
                        null_cols = st.session_state['df'].columns[st.session_state['df'].isnull().any()]

                        option_null = st.selectbox(
                                "Select Columns",
                                null_cols)
                        fig = go.Figure(data=[go.Bar(x=[option_null], y=[st.session_state['df'][option_null].isna().sum()])])
                        fig.update_layout(xaxis_title='Column Name', yaxis_title='Count')
                        st.plotly_chart(fig, use_container_width=True)

                        col_null_1,col_null_2 = st.columns((2,2))

                        with col_null_2:
                            st.write("")
                            st.write("")   
                            button_custom_null = st.button('Submit')

                        with col_null_1:
                            if(st.session_state['df'][option_null].dtypes=='object'):
                                text_custom_null = st.text_input('Insert a text', 'Unknown')
                                if button_custom_null:
                                    handle_null_custom(st.session_state['df'],option_null,text_null)
                                    success_message('Imputation Success',handle_null_custom)

                            
                            elif(st.session_state['df'][option_null].dtypes=='float' or st.session_state['df'][option_null].dtypes=='int'):
                                number_custom_null = st.number_input('Insert a number')
                                if button_custom_null:
                                    handle_null_custom(st.session_state['df'],option_null,number_custom_null)
                                    success_message(' Imputation Success',handle_null_custom)

                    except :
                        st.error('No Null Columns', icon="🚨")
                with st.expander("More Information"):
                    st.write(f"""
                    In computer programming and database management, a null value is a special value that represents the absence of a value or an unknown value.

                    Null values can appear in various contexts, such as when a data field has not been filled in, when a query does not return any results, or when a calculation cannot be performed due to missing information.

                    Whether or not to remove null values depends on the specific use case and the type of data analysis being performed. In some cases, null values may be critical to the analysis and removing them could lead to incorrect results. In other cases, null values may be irrelevant or unwanted and removing them may simplify the analysis.

                    For example, in machine learning models, null values can be handled by imputation methods, such as replacing them with the mean or median of the data, or by dropping the rows or columns containing null values. However, in some cases, null values may represent a meaningful pattern in the data, and dropping them could result in a biased model.

                    Ultimately, the decision to remove null values should be made carefully and with a clear understanding of the potential implications for the analysis or modeling.
                    
                    Here some function that we can use to handle null values:
                    """)
                    st.write(st.session_state['df'].fillna)
                    st.write(st.session_state['df'].dropna)

                
            elif option == "Duplicates":
                sum_duplicates = st.session_state['df'].duplicated().sum()
                
                st.markdown(f"<h4>Duplicate Values</h4>", unsafe_allow_html=True)
                st.markdown(f"<h5>Total Values : {sum_duplicates}</h5>", unsafe_allow_html=True)
                st.write(st.session_state['df'][st.session_state['df'].duplicated()])

                if(sum_duplicates==0):
                    buttom_duplicate = st.button('Drop Duplicates',disabled=True)
                else:
                    buttom_duplicate = st.button('Drop Duplicates',disabled=False)
                    if(buttom_duplicate):
                        drop_duplicate_columns(st.session_state['df'])
                        success_message('Drop Duplicate Success',drop_duplicate_columns)
                
                with st.expander("More Information"):
                    st.write(f"""
                    In computer programming and database management, duplicate values refer to the occurrence of the same data value more than once in a dataset or database table.

                    Whether or not to remove duplicate values depends on the specific use case and the type of data analysis being performed. In some cases, duplicate values may be critical to the analysis and removing them could lead to incorrect results. In other cases, duplicate values may be irrelevant or unwanted and removing them may simplify the analysis.

                    For example, in data analysis or machine learning models, duplicate values can skew the results or accuracy of the analysis by over-representing certain data points. In such cases, it may be necessary to remove duplicate values to ensure the analysis is accurate and unbiased.

                    On the other hand, in some cases, duplicate values may be meaningful and removing them could result in a loss of information. For example, in a database of customer orders, duplicate values for a particular product might represent multiple orders of the same product by different customers.

                    Therefore, it is important to carefully evaluate the potential implications of removing duplicate values before making a decision to do so. In many cases, it may be necessary to weigh the benefits and drawbacks of removing duplicate values against the impact it may have on the accuracy and completeness of the data analysis.
                    
                    Here some function that we can use to handle duplicate values:
                    """)
                    st.write(st.session_state['df'].drop_duplicates)


            elif option=='Outlier':
                # create an empty list to store box traces
                numeric_dataframe = st.session_state['df'].select_dtypes(include=['number'])
                data = []
                checkbox_outlier = st.checkbox('Custom Columns')

                if(checkbox_outlier):
                    option_outlier = st.selectbox(
                            "Select Columns",
                            numeric_dataframe.columns,
                            disabled=st.session_state.disabled)
                    show_boxplot(option_outlier)

                    if(st.button('Drop Outliers')):
                        st.session_state['df'] = remove_outlier(st.session_state['df'],option_outlier)
                        success_message('Drop Outlier Success',remove_outlier)

                else:
                    # iterate through each column in the dataframe and create a box trace
                    for col in numeric_dataframe.columns[1:]:
                        box = go.Box(y=numeric_dataframe[col], name=col)
                        data.append(box)
                    # create a layout
                    layout = go.Layout(title='Box Plot Example', yaxis_title='Value', xaxis_title='Column Names')
                    # create a figure object
                    fig = go.Figure(data=data, layout=layout)
                    st.plotly_chart(fig, use_container_width=True)

                    if(st.button('Drop Outliers')):
                        for col in numeric_dataframe.columns[1:]:
                            st.session_state['df'] = remove_outlier(st.session_state['df'],col)
                        success_message('Drop Outlier Success',remove_outlier)

                with st.expander("More Information"):
                    st.write(f"""
                    In statistics and data analysis, an outlier is a data point that differs significantly from other observations in a dataset. Outliers can occur due to measurement errors, data entry errors, or other factors, and can have a significant impact on statistical analysis and modeling.

                    Whether or not to remove outliers depends on the specific use case and the type of analysis being performed. In some cases, outliers may be valid data points that represent an unusual or rare occurrence, and removing them could result in a loss of important information. In other cases, outliers may represent errors or noise in the data, and removing them could improve the accuracy and reliability of the analysis.

                    For example, in some machine learning models, outliers can have a significant impact on the accuracy of the model, and removing them can lead to better results. However, in other cases, outliers may represent important information, such as in a medical study where an outlier might indicate a rare disease or treatment outcome.

                    Therefore, it is important to carefully evaluate the potential impact of outliers on the analysis before making a decision to remove them. In many cases, it may be necessary to use statistical methods or modeling techniques that are robust to outliers, or to conduct sensitivity analyses to evaluate the impact of outliers on the results.
                    
                    Here some function that we can use to handle Outliers values:
                    """)
                    code = inspect.getsource(remove_outlier)
                    st.code(code, language='python')
            

            #ENCODING
            elif(option=='Encoding'):
                option_encoding = st.selectbox(
                                "Select Methods",
                                ("One-Hot Encoding","Label Encoding"))

                st.write(st.session_state['df'].select_dtypes(include='object').head())

                if(st.button("Encode Data")):
                    if(option_encoding=='Label Encoding'):
                        st.session_state['df'] = encoding_label_encoding(st.session_state['df'])
                        success_message('Label Encoding Success',encoding_label_encoding)
                    elif(option_encoding=='One-Hot Encoding'):
                        st.session_state['df'] = encoding_one_hot_encoding(st.session_state['df'])
                        success_message('One-Hot Encoding Success',encoding_one_hot_encoding)
                
                with st.expander("More Information"):
                    st.write(f"""
                    Label encoding and one-hot encoding are two techniques used in machine learning to transform categorical data into numerical data that can be used in models. The main difference between the two techniques is that label encoding assigns a unique integer to each category, while one-hot encoding creates a binary vector for each category.

                    In label encoding, each category is assigned a unique integer value based on its order or frequency in the dataset. For example, in a dataset of colors (red, green, blue), red may be assigned the value 1, green the value 2, and blue the value 3. Label encoding can be useful for datasets with a large number of categories, as it can reduce the number of features in the dataset and simplify the modeling process.

                    However, label encoding can lead to problems in some cases, as it can imply an ordinal relationship between categories that may not exist. For example, if red is assigned the value 1 and green is assigned the value 2, a model may interpret this as green being "better" than red. This can lead to biased or incorrect results in some cases.

                    In one-hot encoding, each category is represented by a binary vector of 0s and 1s, with a 1 in the position corresponding to the category and 0s in all other positions. For example, in a dataset of colors, red may be represented by the vector [1, 0, 0], green by [0, 1, 0], and blue by [0, 0, 1]. One-hot encoding can be useful for datasets where there is no inherent ordering between categories.

                    However, one-hot encoding can lead to a large number of features in the dataset, particularly if there are many categories. This can make modeling more difficult and can lead to the "curse of dimensionality", where the model becomes less effective as the number of features increases.

                    In general, the choice between label encoding and one-hot encoding depends on the specific dataset and the modeling task. If there is no inherent ordering between categories, one-hot encoding is generally preferred. However, if there is an ordinal relationship between categories, label encoding may be more appropriate. Additionally, it is sometimes useful to try both techniques and compare the results to determine which is more effective in a particular case.
                    
                    Here some function that we can use to encode values:
                    """)
                    st.write("Label Encoding :")
                    st.write(LabelEncoder)
                    st.write("One-Hot Encoding :")
                    st.write(pd.get_dummies)



            #SCALING
            elif(option=='Scaling'):
                option_scaling = st.selectbox(
                                "Select Methods",
                                ("Standarization","Normalization"))
                
                st.write(st.session_state['df'].head())
                
                try:
                    if(st.button("Scale Data")):
                        if(option_scaling=='Normalization'):
                            st.session_state['df'] = normalize_scaling(st.session_state['df'],st.session_state['df'].columns)
                            success_message('Normalization Success',normalize_scaling)
                        elif(option_scaling=='Standarization'):
                            st.session_state['df'] = standarization_scaling(st.session_state['df'],st.session_state['df'].columns)
                            success_message('Standarization Success',standarization_scaling)
                
                except ValueError:
                    st.error('Scaling error, Make sure all columns is numeric', icon="🚨")
                    st.error('Remove categorical feature or do encoding first', icon="🚨")
                
                if(st.session_state['df'].isna().any().any()):
                    st.warning('There were still null values in the data, We recommend to drop or replace the null values first',icon="⚠️")
                
                with st.expander("More Information"):
                    st.write(f"""
                    Standardization and normalization are two common techniques used to preprocess data in data analysis and machine learning.

                    Standardization scales the data to have a mean of 0 and a standard deviation of 1. This means that after standardization, the data will have a normal distribution with mean 0 and standard deviation 1. Standardization is useful when the data has a wide range of values and different units of measurement, as it allows for better comparison of different variables.

                    Normalization, on the other hand, scales the data to a range between 0 and 1. This technique is useful when the absolute values of the data are not as important as their relative values. Normalization can be helpful when dealing with data that has a bounded range or when working with neural networks.

                    In summary, standardization and normalization are used to preprocess data for different purposes. Standardization is helpful when comparing different variables, while normalization is helpful when dealing with data that has a bounded range or when working with neural networks. The choice of which technique to use depends on the specific requirements of the data analysis or machine learning task at hand.
                    
                    Here some function that we can use to encode values:
                    """)
                    st.write("Normalization :")
                    st.write(MinMaxScaler)
                    st.write("Standarization :")
                    st.write(StandardScaler)
    except KeyError:
            st.error('Only accept CSV or XLSX files', icon="🚨")
    except ValueError:
            st.error('Only accept CSV or XLSX files', icon="🚨")






            

    
     
    
