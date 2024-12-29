
# Black-Scholes Options Pricing & P&L Model

![image](https://www.investopedia.com/thmb/gXvipKIbYI--7IdNBlD4_5-PkbA=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/Black-Scholes-Model-FINAL-1-18b2378c6f894a15b5904289870aa532.jpg)

## Purpose of Model

This model simulates a Black-Scholes Options & P&L Pricer, predicting the value of an option given these 6 inputs:
1. Current Stock Price
2. Strike Price (Target Price)
3. Time to Maturity of Option (in years)
4. Risk-Free Rate (%)
5. Volatility of Stock (σ)
6. Purchase Price of the Option 

This model not only predicts the value of an option, but also incorporates the additional profit & loss (P&L) functionality to determine P&L of these options given their purchase price.

This project was built using Python, Plotly, Streamlit, and CSS, and can be found [here](https://black-scholes-options-pricing-model.streamlit.app/).

## Underlying Assumptions for the Model

The Black-Scholes Model makes the following assumptions:

1. No dividends are paid out during the life of the option.
2. Markets are random because market movements can't be predicted.
3. No transaction costs in buying the option.
4. The risk-free rate and volatility of the underlying asset are known and constant.
5. The returns of the underlying asset are normally distributed.
6. The option is European and can only be exercised at expiration.

## How does the Black-Scholes Equation work?
The mathematics involved in the formula are complicated and not necessary for the average user to understand, but this program simply finds the value of an option (call/put) using the inputs provided above, and also derives the potential P&L for each option value with different inputs used. 

To find the value of the option would first require finding the current stock price multiplied by the cumulative standard normal distribution. Thereafter, we will take this value and minus the exercise price discounted back to the present value, multiplied by the cumulative standard normal distribution again.

Now let's find *d1* and *d2* below: 

### Calculating d1:

$$
d_1 = \frac{\ln\left(\frac{S}{K}\right) + \left(r + \frac{1}{2}\sigma^2\right)T}{\sigma\sqrt{T}}
$$

### Calculating d2:
$$
d_2 = \frac{\ln\left(\frac{S}{K}\right) + \left(r - \frac{1}{2}\sigma^2\right)T}{\sigma\sqrt{T}}
$$

or, the alternate way to calculate d2 is:

$$
d_2 = d_1 - \sigma\sqrt{T}
$$

### Calculating the Call Option Price
The call option price C in the Black-Scholes-Merton model is calculated as:

$$
C = S \cdot N(d_1) - K \cdot e^{-rT} \cdot N(d_2)
$$

where S is the current stock price and K is the exercise price.

### Calculating the Put Option Price
The put option price P in the Black-Scholes-Merton model is calculated as:

$$
P = K \cdot e^{-rT} \cdot N(-d_2) - S \cdot N(-d_1)
$$

where S is the current stock price and K is the exercise price.

## How is the P&L functionality calculated?
To calculate the P&L of each option price (call/put), we take in an additional input of the purchase price of the option.

To get the P&L, we take the value of each option minus the purchase price of the option, to get the profit or loss of each option and plot it on a heatmap, with negative values being in the red and positive values in the green. 