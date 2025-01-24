# **A/B Testing App**

## **Overview**
The **A/B Testing App** is an interactive Streamlit application designed to help users conduct and analyze A/B tests. This tool provides two main functionalities:
1. **Sample Size Calculator**: Determine the minimum sample size needed for an A/B test based on key parameters like statistical power, significance level, and baseline conversion rates.
2. **A/B Test Results Analysis**: Upload your test results to calculate key metrics, visualize trends, and evaluate statistical significance.
---
https://ab-test-app.streamlit.app/

## **Features**

### **1. Sample Size Calculator**
- **Input parameters:**
  - Statistical Power (1-β)
  - Significance Level (α)
  - Baseline KPI (Conversion Rate)
  - Minimum Detectable Effect (MDE)
  - Traffic Ratio
- **Outputs:**
  - Required sample size for each group (control and treatment)
  - Estimated number of days needed based on daily traffic.
  - Relative lift percentage.

### **2. A/B Test Results Analysis**
- **Upload CSV file** containing the following columns:
  - `dy`: Date of the test (e.g., 2023-01-01).
  - `experiments`: Experiment group (`control_group` or `treatment`).
  - `view_user_cnt`: Number of users who viewed.
  - `click_user_cnt`: Number of users who clicked.
  - `order_user_cnt`: Number of users who converted.
- **Key Metrics:**
  - Daily CTR and CR significance.
  - Aggregated metrics for the control and treatment groups.
  - Statistical significance (p-values).
- **Visualization:**
  - Time-series graphs for key metrics (View Count, CTR, CR).

---

## **How to Use**

### **1. Installation**
Make sure you have Python installed on your system.

Install the required dependencies using the following command:
```bash
pip install -r requirements.txt
```

### **2. Running the App**
Run the Streamlit app using the command:

```bash
streamlit run streamlit_app.py
```
### **3. File Upload Format**
Ensure your uploaded CSV file adheres to the following structure: csv

```bash
dy,experiments,view_user_cnt,click_user_cnt,order_user_cnt
2023-01-01,control_group,1000,200,50
2023-01-01,treatment,1100,250,60
```

### **Requirements**
- Python 3.7 or above
- Libraries:
  - streamlit
  - pandas
  - numpy
  - scipy
  - plotly
  - openpyxl

### **Project Structure**
```plaintext
project/
├── streamlit_app.py        # Main Streamlit application
├── calculations.py         # Statistical calculations for A/B tests
├── utilities/
│   ├── data_loader.py      # Load default or uploaded data
│   ├── download_utils.py   # Utility to create download links
├── data/
│   └── default_ab_data.csv # Default A/B test data
├── requirements.txt        # Python dependencies
└── README.md               # Project documentation
```

### **Future Enhancements**
Add support for Bayesian A/B testing.
Include confidence intervals in visualizations.
Allow users to export graphs as images.

### **Contact**
For questions or support, please contact:
  - 👩🏻‍💻 Azize Sultan Palalı
  - 📧 azizepalali@gmail.com
  - 🌍 https://www.linkedin.com/in/azize-sultan/

Let me know if further adjustments or refinements are needed! 😊






