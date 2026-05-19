# InsightOps AI: Customer Risk & Growth Decision Platform

InsightOps AI is an interactive analytics dashboard that turns public customer reviews into product risk alerts, issue trends, and business action recommendations.

The project uses NLP, sentiment analysis, issue classification, risk scoring, and trend detection to help product, quality, and customer support teams identify which customer issues need attention first.

## Business Problem

Companies receive thousands of customer reviews, but important product risks are often hidden inside unstructured text. This project answers:

- Which reviews are high risk?
- What are customers complaining about?
- Which issue categories have the highest risk scores?
- Which products need attention?
- Which complaints are growing over time?
- What business actions should teams take next?

## Dataset

This project uses a public sample of Amazon Reviews 2023 data from the All Beauty category.

The dashboard was built using approximately 20,000 customer reviews. The data is used for portfolio and educational purposes only.

## Key Features

- Customer review cleaning and preprocessing
- Risk label creation using review ratings
- NLP-based sentiment scoring
- Rule-based customer issue classification
- Product-level risk scoring
- Emerging issue trend detection
- Interactive Streamlit dashboard
- AI-style executive summary
- Business action recommendations

## Dashboard Sections

- Executive Overview
- Review Risk Distribution
- Highest-Risk Customer Issue Categories
- Product Risk Radar
- Issue Trend Detection
- Emerging Issue Alerts
- Top Risky Customer Reviews
- AI Executive Summary
- Recommended Business Actions

## Key Insights

- Analysed 19,962 customer reviews.
- Identified 15.54% of reviews as high risk.
- General negative complaints and product quality/effectiveness issues showed the highest average risk scores.
- Emerging issue detection highlighted fast-growing complaint themes such as price/value concerns, scent/fragrance issues, and skin reaction concerns.

## Tech Stack

- Python
- Pandas
- NumPy
- NLTK VADER Sentiment Analysis
- Streamlit
- Plotly
- GitHub
- Streamlit Community Cloud

## How to Run Locally

Install the required packages:

```bash
pip install -r requirements.txt