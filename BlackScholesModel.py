from math import exp, sqrt, log
from scipy.stats import norm

class BlackScholesModel:
    def __init__(
            self,
            current_price: float,
            strike_price: float,
            time_to_maturity: float,
            risk_free_rate: float,
            volatility: float
    ):
        self.current_price = current_price
        self.strike_price = strike_price
        self.time_to_maturity = time_to_maturity
        self.risk_free_rate = risk_free_rate
        self.volatility = volatility
    
    def model(
            self,
    ):
        current_price = self.current_price
        strike_price = self.strike_price
        time_to_maturity = self.time_to_maturity
        risk_free_rate = self.risk_free_rate
        volatility = self.volatility

        d1 = (log(current_price/strike_price) + (risk_free_rate + 0.5 * volatility**2)*time_to_maturity) / (volatility * sqrt(time_to_maturity))
        d2 = d1 - (volatility * sqrt(time_to_maturity))

        call_price = (current_price * norm.cdf(d1)) - (strike_price * exp(-risk_free_rate * time_to_maturity) * norm.cdf(d2))
        put_price = (strike_price * exp(-risk_free_rate * time_to_maturity) * norm.cdf(-d2)) - (current_price * norm.cdf(-d1))

        self.call_price = call_price
        self.put_price = put_price

        # Greeks: Delta
        self.call_delta = norm.cdf(d1)
        self.put_delta = 1 - norm.cdf(d1)

        # Greeks: Gamma
        self.call_gamma = norm.pdf(d1) / (strike_price * volatility * sqrt(time_to_maturity))
        self.put_gamma = self.call_gamma

if __name__ == "__main__":
    current_price = 42
    strike_price = 40
    time_to_maturity = 0.5
    risk_free_rate = 0.05
    volatility = 0.2

    BlackScholes = BlackScholesModel(
        current_price=current_price,
        strike_price=strike_price,
        time_to_maturity=time_to_maturity,
        risk_free_rate=risk_free_rate,
        volatility=volatility
    )
    BlackScholes.model()