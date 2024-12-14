import streamlit as st
import pandas as pd
import numpy as np
from scipy.stats import norm
import plotly.graph_objects as go
from math import exp, sqrt, log
import matplotlib.pyplot as plt
import seaborn as sns

#######################
# Page configuration
st.set_page_config(
    page_title="Black-Scholes Options Pricing Model",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded")

# Custom CSS to inject into Streamlit
st.markdown(
    """
    <style>
        footer {display: none}
        [data-testid="stHeader"] {display: none}
    </style>
    """, unsafe_allow_html = True
)

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html = True)

# Main Page for Output Display
st.markdown('<p class="bs_dashboard_title">Black-Scholes Options Pricing Model</p>', unsafe_allow_html = True)
current_price_col, strike_price_col, ttm_col, rf_rate_col, vol_col, purchase_price_col = st.columns([1,1,1,1,1,1])

# Sidebar Inputs
with st.sidebar:
    st.title("📈 Black-Scholes Options Pricing Model")
    st.write("`Created by:`")
    linkedin_url = "https://www.linkedin.com/in/joshua-foo-tse-ern/"
    st.markdown(f'<a href="{linkedin_url}" target="_blank" style="text-decoration: none; color: inherit;"><img src="https://cdn-icons-png.flaticon.com/512/174/174857.png" width="25" height="25" style="vertical-align: middle; margin-right: 10px;">`Joshua Foo Tse Ern`</a>', unsafe_allow_html=True)

    current_price = st.number_input("Current Asset Price", value=100.0)
    strike_price = st.number_input("Strike Price", value=100.0)
    time_to_maturity = st.number_input("Time to Maturity (Years)", value=1.0)
    risk_free_rate = st.number_input("Risk-Free Rate", value=0.05)
    volatility = st.number_input("Volatility (σ)", value=0.2)
    purchase_price = st.number_input("Purchase Price of Option", value=10.0)

    st.markdown("---")
    calculate_btn = st.button('Heatmap Parameters')
    spot_min = st.number_input('Min Spot Price', min_value=0.01, value=current_price*0.8, step=0.01)
    spot_max = st.number_input('Max Spot Price', min_value=0.01, value=current_price*1.2, step=0.01)
    vol_min = st.slider('Min Volatility for Heatmap', min_value=0.01, max_value=1.0, value=volatility*0.5, step=0.01)
    vol_max = st.slider('Max Volatility for Heatmap', min_value=0.01, max_value=1.0, value=volatility*1.5, step=0.01)
    
    spot_range = np.linspace(spot_min, spot_max, 10)
    vol_range = np.linspace(vol_min, vol_max, 10)

# Display Parameter Values
with current_price_col:
    st.markdown("""
        <div class="param_container">
            <p class="current_price_text">Current Price</p>
            <p class="price_details">${:.2f}</p>
        </div>
    """.format(current_price), unsafe_allow_html=True)
    
with strike_price_col:
    st.markdown("""
        <div class="param_container">
            <p class="strike_price_text">Strike Price</p>
            <p class="price_details">${:.2f}</p>
        </div>
    """.format(strike_price), unsafe_allow_html=True)

with ttm_col:
    st.markdown("""
        <div class="param_container">
            <p class="time_to_maturity_text">Time to Maturity</p>
            <p class="price_details">{:.2f} yrs</p>
        </div>
    """.format(time_to_maturity), unsafe_allow_html=True)

with rf_rate_col:
    st.markdown("""
        <div class="param_container">
            <p class="rf_rate_text">Risk-Free Rate</p>
            <p class="price_details">{:.2%}</p>
        </div>
    """.format(risk_free_rate), unsafe_allow_html=True)

with vol_col:
    st.markdown("""
        <div class="param_container">
            <p class="vol_text">Volatility (σ)</p>
            <p class="price_details">{:.2%}</p>
        </div>
    """.format(volatility), unsafe_allow_html=True)

with purchase_price_col:
    st.markdown("""
        <div class="param_container">
            <p class="purchase_price_text">Purchase Price</p>
            <p class="price_details">${:.2f}</p>
        </div>
    """.format(purchase_price), unsafe_allow_html=True)

class BlackScholes:
    def __init__(self, current_price, strike_price, time_to_maturity, risk_free_rate, volatility):
        self.current_price = current_price
        self.strike_price = strike_price
        self.time_to_maturity = time_to_maturity
        self.risk_free_rate = risk_free_rate
        self.volatility = volatility

    def calculate_prices(self):
        d1 = (log(self.current_price/self.strike_price) + (self.risk_free_rate + 0.5 * self.volatility**2)*self.time_to_maturity) / (self.volatility * sqrt(self.time_to_maturity))
        d2 = d1 - (self.volatility * sqrt(self.time_to_maturity))

        call_price = (self.current_price * norm.cdf(d1)) - (self.strike_price * exp(-self.risk_free_rate * self.time_to_maturity) * norm.cdf(d2))
        put_price = (self.strike_price * exp(-self.risk_free_rate * self.time_to_maturity) * norm.cdf(-d2)) - (self.current_price * norm.cdf(-d1))

        self.call_price = call_price
        self.put_price = put_price

        # Greeks: Delta
        self.call_delta = norm.cdf(d1)
        self.put_delta = 1 - norm.cdf(d1)

        # Greeks: Gamma
        self.call_gamma = norm.pdf(d1) / (strike_price * volatility * sqrt(time_to_maturity))
        self.put_gamma = self.call_gamma

        return call_price, put_price

def plot_heatmap_with_pnl(bs_model, spot_range, vol_range, strike_price, purchase_price):
    call_prices = np.zeros((len(vol_range), len(spot_range)))
    put_prices = np.zeros((len(vol_range), len(spot_range)))
    call_pnl = np.zeros((len(vol_range), len(spot_range)))
    put_pnl = np.zeros((len(vol_range), len(spot_range)))
    
    for i, vol in enumerate(vol_range):
        for j, spot in enumerate(spot_range):
            bs_temp = BlackScholes(
                current_price=spot,
                strike_price=strike_price,
                time_to_maturity=bs_model.time_to_maturity,
                risk_free_rate=bs_model.risk_free_rate,
                volatility=vol,
            )
            bs_temp.calculate_prices()
            call_prices[i, j] = bs_temp.call_price
            put_prices[i, j] = bs_temp.put_price
            call_pnl[i, j] = bs_temp.call_price - purchase_price
            put_pnl[i, j] = bs_temp.put_price - purchase_price
    
    # Plotting Call Price Heatmap
    fig_call, ax_call = plt.subplots(figsize=(10, 8))
    sns.heatmap(call_prices, xticklabels=np.round(spot_range, 2), yticklabels=np.round(vol_range, 2),
                annot=True, fmt=".2f", cmap="RdYlGn", ax=ax_call)
    ax_call.set_title('CALL PRICE')
    ax_call.set_xlabel('Spot Price')
    ax_call.set_ylabel('Volatility')
    
    # Plotting Put Price Heatmap
    fig_put, ax_put = plt.subplots(figsize=(10, 8))
    sns.heatmap(put_prices, xticklabels=np.round(spot_range, 2), yticklabels=np.round(vol_range, 2),
                annot=True, fmt=".2f", cmap="RdYlGn", ax=ax_put)
    ax_put.set_title('PUT PRICE')
    ax_put.set_xlabel('Spot Price')
    ax_put.set_ylabel('Volatility')
    
    # Plotting Call P&L Heatmap
    fig_call_pnl, ax_call_pnl = plt.subplots(figsize=(10, 8))
    sns.heatmap(call_pnl, xticklabels=np.round(spot_range, 2), yticklabels=np.round(vol_range, 2),
                annot=True, fmt=".2f", cmap="RdYlGn", ax=ax_call_pnl)
    ax_call_pnl.set_title('CALL P&L')
    ax_call_pnl.set_xlabel('Spot Price')
    ax_call_pnl.set_ylabel('Volatility')
    
    # Plotting Put P&L Heatmap
    fig_put_pnl, ax_put_pnl = plt.subplots(figsize=(10, 8))
    sns.heatmap(put_pnl, xticklabels=np.round(spot_range, 2), yticklabels=np.round(vol_range, 2),
                annot=True, fmt=".2f", cmap="RdYlGn", ax=ax_put_pnl)
    ax_put_pnl.set_title('PUT P&L')
    ax_put_pnl.set_xlabel('Spot Price')
    ax_put_pnl.set_ylabel('Volatility')
    
    return fig_call, fig_put, fig_call_pnl, fig_put_pnl

# Calculate Call and Put values
bs_model = BlackScholes(current_price, strike_price, time_to_maturity, risk_free_rate, volatility)
call_price, put_price = bs_model.calculate_prices()

# Display Call and Put Values in colored tables
col1, col2 = st.columns([1,1], gap="small")

with col1:
    st.markdown(f"""
        <div class="metric-container metric-call">
            <div>
                <div class="metric-label">CALL Value</div>
                <div class="metric-value">${call_price:.2f}</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
        <div class="metric-container metric-put">
            <div>
                <div class="metric-label">PUT Value</div>
                <div class="metric-value">${put_price:.2f}</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("")
st.title("Interactive Heatmaps for Option Prices and P&L")

# Interactive Heatmaps
col1, col2 = st.columns([1, 1], gap="small")

with col1:
    st.subheader("Call Option Price Heatmap")
    heatmap_fig_call, heatmap_fig_put, heatmap_fig_call_pnl, heatmap_fig_put_pnl = plot_heatmap_with_pnl(
        bs_model, spot_range, vol_range, strike_price, purchase_price)
    st.pyplot(heatmap_fig_call)

with col2:
    st.subheader("Put Option Price Heatmap")
    st.pyplot(heatmap_fig_put)

# P&L Heatmaps
col1, col2 = st.columns([1, 1], gap="small")

with col1:
    st.subheader("Call Option P&L Heatmap")
    st.pyplot(heatmap_fig_call_pnl)

with col2:
    st.subheader("Put Option P&L Heatmap")
    st.pyplot(heatmap_fig_put_pnl)