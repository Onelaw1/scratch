from typing import Dict, Any

class GlobalService:
    """
    Service for Global Localization & Currency Management.
    """
    
    # Mock Exchange Rates (Base: KRW)
    EXCHANGE_RATES = {
        "KRW": 1.0,
        "USD": 1300.0,
        "EUR": 1450.0,
        "JPY": 9.0
    }
    
    CURRENCY_SYMBOLS = {
        "KRW": "₩",
        "USD": "$",
        "EUR": "€",
        "JPY": "¥"
    }

    def get_supported_currencies(self) -> Dict[str, Any]:
        return {
            "rates": self.EXCHANGE_RATES,
            "symbols": self.CURRENCY_SYMBOLS,
            "default": "KRW"
        }

    def convert_currency(self, amount_krw: float, target_currency: str) -> float:
        """
        Converts KRW amount to target currency.
        """
        rate = self.EXCHANGE_RATES.get(target_currency, 1.0)
        if rate == 0: return amount_krw
        return round(amount_krw / rate, 2)
