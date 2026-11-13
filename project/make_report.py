from pathlib import Path
from docx import Document
from docx.shared import Pt

root=Path(__file__).parent; doc=Document(); doc.styles['Normal'].font.size=Pt(12)
doc.add_heading('Part E — Product EDA Dashboard',0)
doc.add_paragraph('Product question: When, where and which products should a product manager prioritise to grow revenue?')
sections=[
('Dataset and source','I used the public Online Retail dataset from the UCI Machine Learning Repository. It contains transactions from a UK-based non-store online retailer between 1 December 2010 and 9 December 2011. The local copy is data/Online_Retail.xlsx. Source: Daqing Chen, Online Retail, UCI Machine Learning Repository, DOI 10.24432/C5BW33, https://archive.ics.uci.edu/dataset/352/online-retail.'),
('Data types and profiling','InvoiceNo, StockCode, CustomerID and Country are categorical identifiers or labels. Description is categorical text. Quantity is discrete quantitative data, UnitPrice is continuous quantitative data, and InvoiceDate is temporal data. Revenue is derived as Quantity × UnitPrice in pounds sterling.'),
('Preprocessing','InvoiceDate was parsed as datetime and text fields were trimmed. Cancellation invoices beginning with C, non-positive quantities/prices, and rows missing date, description or country were removed. Revenue was calculated as Quantity × UnitPrice. For visual summaries, transaction-revenue outliers above Q3 + 1.5×IQR were excluded so extreme invoices did not distort the charts.'),
('Dashboard charts and takeaways','1. Monthly revenue trend: a line chart reveals peaks and troughs for campaign and inventory planning. 2. Top products by revenue: a sorted horizontal bar chart shows product concentration. 3. Top markets by revenue: a sorted bar chart supports geographic prioritisation. 4. Revenue by weekday: a bar chart compares operational demand across weekdays. KPI cards show revenue, orders, customers and products.'),
('Insight and limitation','Revenue is concentrated in a small number of products and markets, making stock availability and market-specific retention important management questions. This is descriptive analysis, not proof of causation. The dataset is historical and represents one retailer, so current decisions should be validated with newer internal data and experiments.'),
('Reproducibility','Run python analysis.py to regenerate outputs/clean_transactions.csv and static PNG charts. Run streamlit run app.py to open the interactive dashboard.')]
for title,body in sections: doc.add_heading(title,1); doc.add_paragraph(body)
doc.save(root/'Part_E_Product_EDA_Report.docx')
