import streamlit as st
import plotly.express as px
import pandas as pd



# Title of the app
st.title("Data Visualization App")

# Add a sidebar
st.sidebar.subheader("Visualization Settings")

# Setup file upload
uploaded_file = st.sidebar.file_uploader(
    label="Upload your CSV or Excel file. (200MB max)",
    type=['csv', 'xlsx']
)

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
    except Exception as e:
        print(e)
        df = pd.read_excel(uploaded_file)

    try:
        st.write(df)
        numeric_columns = list(df.select_dtypes(['float', 'int']).columns)
        non_numeric_columns = list(df.select_dtypes(['object']).columns)
        non_numeric_columns.append(None)
    except Exception as e:
        print(e)
        st.write("Please upload a valid file to the application.")
else:
    st.write("Please upload a file to the application and Select Chart.")

if uploaded_file is not None:
    # Add a select widget to the sidebar
    chart_select = st.sidebar.selectbox(
        label="Select the chart type",
        options=['Scatterplots', 'Lineplots', 'Histogram', 'Boxplot']
    )

    if chart_select == 'Scatterplots':
        st.sidebar.subheader("Scatterplot Settings")
        try:
            x_values = st.sidebar.selectbox('X axis', options=numeric_columns)
            y_values = st.sidebar.selectbox('Y axis', options=numeric_columns)
            color_value = st.sidebar.selectbox("Color", options=non_numeric_columns)
            plot = px.scatter(data_frame=df, x=x_values, y=y_values, color=color_value)
            # Display the chart
            st.plotly_chart(plot)
        except Exception as e:
            print(e)

    if chart_select == 'Lineplots':
        st.sidebar.subheader("Line Plot Settings")
        try:
            x_values = st.sidebar.selectbox('X axis', options=numeric_columns)
            y_values = st.sidebar.selectbox('Y axis', options=numeric_columns)
            color_value = st.sidebar.selectbox("Color", options=non_numeric_columns)
            plot = px.line(data_frame=df, x=x_values, y=y_values, color=color_value)
            st.plotly_chart(plot)
        except Exception as e:
            print(e)

    if chart_select == 'Histogram':
        st.sidebar.subheader("Histogram Settings")
        try:
            x = st.sidebar.selectbox('Feature', options=numeric_columns)
            bin_size = st.sidebar.slider("Number of Bins", min_value=10, max_value=100, value=40)
            color_value = st.sidebar.selectbox("Color", options=non_numeric_columns)
            plot = px.histogram(data_frame=df, x=x, nbins=bin_size, color=color_value)
            st.plotly_chart(plot)
        except Exception as e:
            print(e)

    if chart_select == 'Boxplot':
        st.sidebar.subheader("Boxplot Settings")
        try:
            y = st.sidebar.selectbox("Y axis", options=numeric_columns)
            x = st.sidebar.selectbox("X axis", options=non_numeric_columns)
            color_value = st.sidebar.selectbox("Color", options=non_numeric_columns)
            plot = px.box(data_frame=df, y=y, x=x, color=color_value)
            st.plotly_chart(plot)
        except Exception as e:
            print(e)

