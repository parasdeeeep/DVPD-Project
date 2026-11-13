from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

ROOT=Path(__file__).parent; DATA=ROOT/'data'/'Online_Retail.xlsx'; OUT=ROOT/'outputs'; OUT.mkdir(exist_ok=True)
sns.set_theme(style='whitegrid')

def load_clean():
    df=pd.read_excel(DATA); df.columns=[c.strip() for c in df.columns]
    df['InvoiceDate']=pd.to_datetime(df['InvoiceDate'],errors='coerce')
    df['Description']=df['Description'].astype('string').str.strip().str.title(); df['Country']=df['Country'].astype('string').str.strip()
    df['Revenue']=df['Quantity']*df['UnitPrice']; raw=len(df)
    df=df[~df['InvoiceNo'].astype('string').str.upper().str.startswith('C',na=False)]
    df=df[df['Quantity'].gt(0)&df['UnitPrice'].gt(0)].dropna(subset=['InvoiceDate','Description','Country'])
    q1,q3=df['Revenue'].quantile([.25,.75]); upper=q3+1.5*(q3-q1); chart=df[df['Revenue'].le(upper)].copy()
    return df,chart,{'raw_rows':raw,'clean_rows':len(df),'chart_rows':len(chart),'removed_rows':raw-len(df)}

def make_charts(df):
    monthly=df.set_index('InvoiceDate').resample('MS')['Revenue'].sum().reset_index()
    products=df.groupby('Description',as_index=False)['Revenue'].sum().nlargest(10,'Revenue').sort_values('Revenue')
    countries=df.groupby('Country',as_index=False)['Revenue'].sum().nlargest(10,'Revenue').sort_values('Revenue')
    weekday=df.assign(Weekday=df['InvoiceDate'].dt.day_name()).groupby('Weekday',as_index=False)['Revenue'].sum(); order=['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']; weekday['Weekday']=pd.Categorical(weekday['Weekday'],categories=order,ordered=True); weekday=weekday.sort_values('Weekday')
    specs=[('monthly_revenue',monthly,'InvoiceDate','Revenue','Monthly Revenue Trend','Month','Revenue (£)','Takeaway: revenue varies across the retail year.'),('top_products',products,'Revenue','Description','Top 10 Products by Revenue','Revenue (£)','Product','Takeaway: a small set of products contributes most revenue.'),('top_countries',countries,'Revenue','Country','Top 10 Countries by Revenue','Revenue (£)','Country','Takeaway: the UK is the dominant revenue market.'),('weekday_revenue',weekday,'Weekday','Revenue','Revenue by Day of Week','Day','Revenue (£)','Takeaway: demand concentration differs by weekday.')]
    for name,data,x,y,title,xlabel,ylabel,takeaway in specs:
        fig,ax=plt.subplots(figsize=(9,5)); kind='line' if name=='monthly_revenue' else 'barh' if name in ('top_products','top_countries') else 'bar'
        if kind=='line': ax.plot(data[x],data[y],marker='o',linewidth=2)
        elif kind=='barh': ax.barh(data[y],data[x],color='#386cb0')
        else: ax.bar(data[x],data[y],color='#f28e2b')
        ax.set_title(title,weight='bold'); ax.set_xlabel(xlabel); ax.set_ylabel(ylabel); fig.text(.5,.01,takeaway,ha='center',fontsize=9); fig.tight_layout(rect=(0,.04,1,1)); fig.savefig(OUT/f'{name}.png',dpi=180); plt.close(fig)

if __name__=='__main__':
    clean,chart,stats=load_clean(); clean.to_csv(OUT/'clean_transactions.csv',index=False); make_charts(chart); print(stats)
