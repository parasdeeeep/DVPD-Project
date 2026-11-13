import pandas as pd
import plotly.express as px
import streamlit as st
from analysis import load_clean

st.set_page_config(page_title='Online Retail Product Dashboard',page_icon='🛒',layout='wide')
st.title('Online Retail Product EDA Dashboard')
st.caption('Product-manager question: When, where and which products should we prioritise to grow revenue?')
df,chart_df,stats=load_clean()
with st.sidebar:
    st.header('Filters'); countries=st.multiselect('Country',sorted(df['Country'].dropna().unique()),default=[]); lo,hi=df['InvoiceDate'].min().date(),df['InvoiceDate'].max().date(); dates=st.date_input('Date range',(lo,hi),min_value=lo,max_value=hi)
if countries: chart_df=chart_df[chart_df['Country'].isin(countries)]
if isinstance(dates,tuple) and len(dates)==2: chart_df=chart_df[(chart_df['InvoiceDate'].dt.date>=dates[0])&(chart_df['InvoiceDate'].dt.date<=dates[1])]
c1,c2,c3,c4=st.columns(4); c1.metric('Revenue',f"£{chart_df['Revenue'].sum():,.0f}"); c2.metric('Orders',f"{chart_df['InvoiceNo'].nunique():,}"); c3.metric('Customers',f"{chart_df['CustomerID'].nunique():,}"); c4.metric('Products',f"{chart_df['StockCode'].nunique():,}")
monthly=chart_df.set_index('InvoiceDate').resample('MS')['Revenue'].sum().reset_index(); products=chart_df.groupby('Description',as_index=False)['Revenue'].sum().nlargest(10,'Revenue').sort_values('Revenue'); countries_df=chart_df.groupby('Country',as_index=False)['Revenue'].sum().nlargest(10,'Revenue').sort_values('Revenue'); weekday=chart_df.assign(Weekday=chart_df['InvoiceDate'].dt.day_name()).groupby('Weekday',as_index=False)['Revenue'].sum(); order=['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']; weekday['Weekday']=pd.Categorical(weekday['Weekday'],categories=order,ordered=True); weekday=weekday.sort_values('Weekday')
left,right=st.columns(2)
with left:
    st.subheader('1. Revenue trend'); st.plotly_chart(px.line(monthly,x='InvoiceDate',y='Revenue',markers=True,labels={'Revenue':'Revenue (£)','InvoiceDate':'Month'}),use_container_width=True); st.caption('Takeaway: monthly peaks and troughs support campaign and inventory planning.')
    st.subheader('3. Top markets'); st.plotly_chart(px.bar(countries_df,x='Revenue',y='Country',orientation='h',labels={'Revenue':'Revenue (£)','Country':'Country'}),use_container_width=True); st.caption('Takeaway: revenue is concentrated in the leading market.')
with right:
    st.subheader('2. Top products'); st.plotly_chart(px.bar(products,x='Revenue',y='Description',orientation='h',labels={'Revenue':'Revenue (£)','Description':'Product'}),use_container_width=True); st.caption('Takeaway: a small product group drives disproportionate revenue.')
    st.subheader('4. Weekday pattern'); st.plotly_chart(px.bar(weekday,x='Weekday',y='Revenue',labels={'Revenue':'Revenue (£)','Weekday':'Day'}),use_container_width=True); st.caption('Takeaway: operations can align staffing and promotions to weekday demand.')
st.subheader('Data quality and preprocessing'); st.write(f"Raw rows: {stats['raw_rows']:,}. Clean positive-sales rows: {stats['clean_rows']:,}. Rows used after revenue IQR filtering: {stats['chart_rows']:,}. Cancellations, invalid quantities/prices and unusable dates/descriptions were removed.")
with st.expander('Cleaned data preview'): st.dataframe(chart_df.head(100),use_container_width=True)
