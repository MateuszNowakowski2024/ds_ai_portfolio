---
comments: true
---



Link to the App: 

<a href="https://mlrossman.streamlit.app/" class="md-button md-button--primary"> Sales Forecasting App</a>


## 🛍️ Rossman Store Sales Forecasting App


Role: Data Scientist | Tech Stack: Python, Streamlit, XGBoost, pandas, scikit-learn, AWS S3

Overview:
This project demonstrates my ability to build end-to-end data science solutions using machine learning and cloud technologies. I developed an interactive Streamlit web application that forecasts future store sales using historical time series data. The app provides actionable insights for business planning and inventory management.

Problem Solved:
Retailers often struggle with accurately predicting future sales, which can lead to either overstocking or missed revenue opportunities. My app addresses this problem by leveraging machine learning to generate accurate sales forecasts based on historical performance and temporal features.

Key Features:

📈 Time Series Forecasting using XGBoost trained on daily sales data from 2013 to 2015.

🧠 Feature Engineering with calendar variables like holidays, promotions, day-of-week, and trend decomposition.

🎛️ Interactive Streamlit Interface allowing users to select store IDs and visualize predictions.

💾 Data Storage & Persistence via local disk and AWS S3 for saving model inputs and conversation history.

🚀 Automation of ML Workflow with preprocessing, model training, and inference pipelines built in Python.

Tools & Frameworks:

Languages & Libraries: Python, pandas, NumPy, scikit-learn, XGBoost

Visualization & UI: Streamlit, Matplotlib

Cloud & Storage: AWS S3, OS file handling

Development Tools: Visual Studio Code, Git



Link to the App: 

<a href="https://mlrossman.streamlit.app/" class="md-button md-button--primary"> Sales Forecasting App</a>


### 📊 Exploratory Data Analysis (EDA)

This project explores a retail dataset containing historical sales data across multiple stores. The goal of this analysis is to understand key patterns in customer behavior, sales performance, and promotional impact. 

Using Python libraries such as `pandas`, `seaborn`, and `matplotlib`, the analysis includes:

- **Univariate Analysis**: Examining individual variables like sales distribution and store performance.
- **Bivariate Analysis**: Investigating relationships between variables, such as the impact of promotions on sales.
- **Time Series Analysis**: Identifying trends, seasonality, and anomalies in sales data over time.

Key insights from the EDA help inform feature engineering and model development, ensuring the machine learning pipeline is tailored to the dataset's characteristics.

<a href="eda.ipynb" class="md-button md-button--primary">👉 View EDA Notebook</a>

<iframe  
    id="eda"  
    src="eda.html"  
    width="100%"  
    style="border: 1px solid black; overflow: hidden; height: 600px;">  
</iframe>

---

## Store Sales Forecasting with XGBoost & Streamlit

This project demonstrates a time series forecasting pipeline using XGBoost to predict daily sales for multiple retail stores. Key steps include:

- Feature engineering with lag and rolling statistics.
- Training a regression model.
- Building an interactive Streamlit app for visualizing both historical and forecasted sales.

The app supports scenario testing (e.g., promotions, holidays) and store comparisons, making it ideal for retail analytics and demand planning use cases.

<a href="ml.ipynb" class="md-button md-button--primary">👉 View ML Training Notebook</a>

<iframe  
    id="ml"  
    src="ml.html"  
    width="100%"  
    style="border: 1px solid black; overflow: hidden; height: 600px;">  
</iframe>

---
<script>
function resizeIframeToContent(iframe) {
    iframe.onload = () => {
        const newHeight = iframe.contentWindow.document.documentElement.scrollHeight + 50;
        iframe.style.height = newHeight + 'px';
        iframe.contentDocument.body.style.overflow = 'hidden';
    };
}
window.addEventListener('load', function () {
    resizeIframeToContent(document.getElementById('eda'));
    resizeIframeToContent(document.getElementById('ml'));
});
window.addEventListener('resize', function () {
    resizeIframeToContent(document.getElementById('eda'));
    resizeIframeToContent(document.getElementById('ml'));
});
</script>