---
comments: true
---

Link to the App: 

<a href="https://creditpredictor2025.streamlit.app/" class="md-button md-button--primary"> Credit Aproval</a>

## 🧠 Credit Risk Prediction Machine Learning Project


In this credit risk classification project, I performed a comprehensive exploratory data analysis (EDA) to uncover key patterns, address data quality issues, and engineer features that directly impacted model performance. The dataset, derived from loan application records, included a range of categorical, numerical, and duration-based features, many of which required domain-informed preprocessing.

I began by reducing categorical noise through frequency-based grouping—collapsing rare levels in features like OCCUPATION_TYPE and NAME_INCOME_TYPE into an "Other" category. Boolean flags such as car and real estate ownership were transformed into binary values to meet model requirements. I converted day-based duration fields like DAYS_BIRTH into more intuitive YEARS_BIRTH, ensuring consistent and interpretable time-based metrics.

To handle missing values in categorical features, I implemented a targeted imputation strategy using group-level modes based on education level, increasing the semantic quality of replacements. I then applied smoothed target encoding to multiple categorical variables, replacing categories with a weighted mean of the target (STATUS) using both the category-specific mean and the global average. This approach preserved the predictive signal without overfitting, especially for categories with few observations.

I further enhanced the dataset by engineering income-related features such as INCOME_PER_PERSON, INCOME_PER_CHILD, and INCOME_PER_YEAR_EMPLOYED, and introduced a LOW_INCOME_FLAG to highlight economically vulnerable applicants. To address the severe class imbalance—where default cases made up less than 2% of the data—I used SMOTE to synthetically balance the dataset and applied custom sample weights to prioritize vulnerable applicants in both training and evaluation.

Despite the initial imbalance, I trained three high-performing ensemble models—Random Forest, LightGBM, and XGBoost—with the best model achieving 98.7% accuracy on the test set. My feature engineering pipeline, combined with thoughtful target encoding and resampling techniques, demonstrated the power of combining domain knowledge with statistical rigor to build robust, real-world-ready machine learning systems.


Link to the App: 

<a href="https://creditpredictor2025.streamlit.app/" class="md-button md-button--primary"> Credit Aproval</a>

---

### 📊 Exploratory Data Analysis (EDA)

Take a visual tour through the credit application dataset. I explore patterns in income, housing, family structure, and socio-economic indicators, while preparing the ground for model training through data cleaning and transformation.

<a href="credit_card_eda.ipynb" class="md-button md-button--primary">👉 View EDA Notebook</a>

<iframe  
    id="eda"  
    src="credit_card_eda.html"  
    width="100%"  
    style="border: 1px solid black; overflow: hidden; height: 600px;">  
</iframe>


---

### 🤖 Machine Learning Pipeline

This notebook walks through the entire machine learning process—from preprocessing, target encoding with smoothing, and SMOTE balancing, to training and evaluating ensemble models with adjusted sample weights.

<a href="ml_training.ipynb" class="md-button md-button--primary">👉 View ML Training Notebook</a>

<iframe  
    id="ml"  
    src="ml_training.html"  
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