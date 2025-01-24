import io
import base64
import pandas as pd
import streamlit as st
import math

from utilities.statistical_calculations import calculate_sample_size, ab_test_calculations, ab_test_calculations_overall
from utilities.data_loader import load_default_data
from utilities.download_utils import get_excel_download_link

from plotly.subplots import make_subplots
import plotly.graph_objects as go

st.set_page_config(
    page_title="A/B Testing App",
    page_icon="📊",
    initial_sidebar_state="expanded",
    layout="wide"
)

st.sidebar.image("assets/ab_test_app.png", width=150, height = 150) # or use_container_width=True

# Add a title to the sidebar
st.sidebar.title("A/B Testing App")

# Add helpful information or links
st.sidebar.markdown("""
Welcome to the **A/B Testing App**! Use this tool to:
- Calculate the required sample size for an A/B test.
- Analyze daily or overall A/B test results.
""")

# Add links to relevant resources
st.sidebar.markdown("""
**Quick Links:**
- [What is A/B Testing?](https://azizesultanpalali.com/category/articles/)
- [Streamlit Documentation](https://docs.streamlit.io)
""")

app_mode = st.sidebar.selectbox('Select Page', ['Sample Size Calculator', 'A/B Test Result'])

default_df = load_default_data()

if app_mode == "Sample Size Calculator":
    st.title("Sample Size Calculator :rocket:")

    st.write("---")
    st.write("""
            Question: How many subjects are needed for an A/B test?
            - Check out this [link](https://signalvnoise.com/posts/3004-ab-testing-tech-note-determining-sample-size) for more detail
    """)
    st.write("---")

    beta = st.slider(label='Statistical power 1−β:',
                     min_value=60,
                     max_value=95,
                     step=5,
                     value=80,
                     help="Statistical power is the probability of observing a statistically significant result at level alpha (α) if a true effect of a certain magnitude is present.") / 100
    alpha = st.slider(label='Significance level α:',
                      min_value=1,
                      max_value=10,
                      step=1,
                      value=5,
                      help='Percent of the time a difference will be detected, assuming one does NOT exist') / 100

    baseline_conversion_rate = float(st.text_input(label='Baseline Kpi: %',
                                                   value="18.55",
                                                   help="Kpi that you want to improve with A/B testing.")) / 100
    minimum_detectable_effect = float(st.text_input(label='Minimum Detectable Effect: %',
                                                    value="0.1",
                                                    help='The Minimum Detectable Effect is the effect size which, if it truly exists, can be detected with a given probability with a statistical test of a certain significance level.')) / 100

    traffic_ratio = float(st.text_input(label='Traffic Ratio: %',
                                        value="10",
                                        help='Percent of traffic that in A/B test')) / 100

    sample_size = calculate_sample_size(alpha=alpha,
                                        power_level=beta,
                                        p=baseline_conversion_rate,
                                        delta=minimum_detectable_effect)

    st.header(f'Sample size: {int(sample_size)}')

    average_daily_view = float(st.text_input('Average Daily View:', value="520501"))
    needed_sample_view = sample_size
    needed_total_view = needed_sample_view * 2
    needed_days = needed_total_view / (average_daily_view * traffic_ratio)

    lift = minimum_detectable_effect / baseline_conversion_rate

    st.table(pd.DataFrame({
        "Needed Sample View": needed_sample_view,
        "Needed Total View": needed_total_view,
        "Needed Days": needed_days,
        "Relative Lift %": round(lift * 100, 2)
    }, index=[0]))

else:
    st.title("A/B Test Result :rocket:")
    st.write("---")
    uploaded_file = st.file_uploader("Upload your A/B test CSV file", type="csv")

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.write("### Uploaded Data Preview")
        st.write(df.head())
    else:
        st.write("### Default Data Preview")
        st.write(default_df.head())
        df = default_df

    clicked_calculate_daily, clicked_calculate_overall = st.columns(2)
    clicked_calculate_daily = clicked_calculate_daily.button('Calculate A/B Test Daily 🗓')
    clicked_calculate_overall = clicked_calculate_overall.button('Calculate A/B Test Overall 🔍')

    if clicked_calculate_daily:
        df = ab_test_calculations(df)
        st.markdown("### Key Metrics")
        distinct_dy = df["dy"].nunique()
        treatment_ctr_yes = len(df[(df['experiments'] == 'treatment') & (df['significant_ctr'] == 'Yes')])
        treatment_cr_yes = len(df[(df['experiments'] == 'treatment') & (df['significant_cr'] == 'Yes')])

        kpi1, kpi2, kpi3, kpi4 = st.columns(4)

        kpi1.metric(label="Run Day 🏃🏻", value=distinct_dy)
        kpi2.metric(label="CTR Significant Count 📈", value=treatment_ctr_yes)
        kpi3.metric(label="CR Significant Count 🛫", value=treatment_cr_yes)
        
        # Total number of views
        srm_n = df["view_user_cnt"].sum()
        
        # Proportion of views in the treatment group
        srm_p = df.loc[df["experiments"] == "treatment", "view_user_cnt"].sum() / srm_n
        srm_pvalue = srm_p * math.sqrt(srm_p*(1-srm_p)/srm_n) 
        
        if srm_pvalue < 0.001:
            value = "No"
        else:
            value = "Yes"
            
        kpi4.metric(label = "Split Issue 📣",value = value)

        cols = ["view_user_cnt", "ctr", "cr"]
        fig = make_subplots(rows=1, cols=len(cols), subplot_titles=cols)

        for index, col in enumerate(cols):
            for bucket, sub_df in df.groupby('experiments'):
                trace = go.Scatter(x=sub_df["dy"],
                                   y=sub_df[col],
                                   name=col + "_" + bucket,
                                   mode='lines')

                fig.add_trace(trace, row=1, col=index + 1)

        fig.update_layout(title_text="The expected distributions of variation A and B")
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("### Daily Detail of A and B")
        st.table(df)

        download_link = get_excel_download_link(df)
        st.markdown(download_link, unsafe_allow_html=True)

    elif clicked_calculate_overall:
        df = ab_test_calculations_overall(df)
        st.markdown("### Overall Key Metrics")
        st.table(df)

        download_link = get_excel_download_link(df)
        st.markdown(download_link, unsafe_allow_html=True)
