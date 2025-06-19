# Customer Segmentation & Intelligent Product Recommendation System

This project presents an end-to-end solution for **e-commerce customer segmentation** and **smart product recommendations**. It combines **Power BI dashboards**, **machine learning models**, and an **LLM-powered chatbot interface** to deliver strategic insights and actionable suggestions for marketing and sales operations.

> ![Main Page](https://i.ibb.co/0jtD0Y8B/Screenshot-8-kopya.png)


---
## Project Overview

The system is designed to:
- **Segment customers** based on Recency, Frequency, and Monetary (RFM) analysis
- Visualize customer behavior and value clusters in an **interactive Power BI dashboard**
- Recommend **cross-sell** and **up-sell** products based on historical purchase patterns using hybrid machine learning models
- Enable natural language Q&A over the dataset through a **LangChain-based chatbot**

---

## Components

### 1. Power BI Dashboard
- Interactive customer segmentation view based on RFM metrics
- Cluster visualizations with demographic and behavioral filters
- Time-based purchase trends, segment heatmaps, and churn risk indicators

### 2. ML-based Recommendation Engine
- **Cross-sell** and **Up-sell** logic trained on e-commerce invoices
- Uses:
  - `LightFM` for collaborative filtering (matrix factorization)
  - `LightGBM` for re-ranking predictions based on price, product type, and frequency
- Outputs personalized suggestions with product metadata (name, type, price)

### 3. Natural Language Chatbot
- Built using **LangChain + OpenAI**
- Allows querying of transactional CSV using free-form questions (e.g. "Which customer segment buys most frequently on weekends?")
- Integrated conversation memory and CSV agent with data validation
- Responses are also stored in SQLite via custom backend

---

## Tech Stack

| Component          | Technology                     |
|-------------------|--------------------------------|
| Visualization      | Power BI                       |
| Machine Learning   | Python, LightGBM, LightFM      |
| Chatbot Framework  | LangChain, OpenAI API          |
| Backend            | FastAPI                        |
| Data Source        | CSV-based e-commerce invoices  |
| Storage            | SQLite                         |
| Dev Tools          | Git, Streamlit (for demos)     |

---

## 🗂️ Folder Structure

app/

├── asistantservice.py # LangChain-based chatbot

├── suggestservice.py # LightFM + LightGBM hybrid model

├── main.py # FastAPI entry point

├── model/ # Pickled ML models & encoders

├── data/ # Transactional CSV and assets

└── static/ # UI elements (optional)

---

## Sample Use Cases

- Identify your highest-value segment and what they tend to buy
- Ask the chatbot:  
  > _"What do customers in Segment A buy during winter?"_  
- Get product recommendations for a given invoice number (hybrid prediction)

---

## How to Run

1. **Clone the repository**
2. **Install dependencies**
   
```bash
   pip install -r requirements.txt
   ```
Start the FastAPI backend

   ```bash
    uvicorn main:app --reload
```
---

## Power BI Setup

- Open the `Customer_Segmentation.pbix` file with Power BI Desktop.
- The dashboard is fully interactive and filterable by:
    - Day of Week / Time of Day

    - Customer Segments

    - Product Type
> ![Main Page](https://i.ibb.co/7x9tkQQp/Screenshot-9-kopya.png)

---
