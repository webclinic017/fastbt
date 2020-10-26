import pendulum
import random
from collections import defaultdict
from typing import Optional, List, Dict, Tuple, Any
from fastbt.models.base import BaseSystem
from pydantic import BaseModel, ValidationError
from logzero import logger

class StockData(BaseModel):
    name: str
    token: Optional[int]
    can_trade: bool = True
    positions:int = 0
    ltp: float = 0
    day_high: float = -1 # Impossible value for initialization
    day_low: float = 1e10 # Almost impossible value for initialization
    order_id: Optional[str]
    stop_id: Optional[str]
    stop_loss: Optional[float]
    high: Optional[float]
    low: Optional[float]

class HighLow(BaseModel):
    symbol: str
    high: float
    low: float 

class Breakout(BaseSystem):
    """
    A simple breakout system
    Trades are taken when the given high or low is broke
    """
    
    def __init__(self, symbols:List[str],instrument_map:Dict[str,int]={}, **kwargs) -> None:
        """
        Initialize the strategy
        symbols
            list of symbols
        instrument_map
            dictionary mapping symbols to scrip code
        kwargs
            list of keyword arguments that could be passed to the 
            strategy in addition to those inherited from base system
        """
        super(Breakout, self).__init__(**kwargs)
        self._data = defaultdict(StockData)
        self._instrument_map = instrument_map
        self._rev_map= {v:k for k,v in instrument_map.items() if v is not None}
        for symbol in symbols:
            self._data[symbol] = StockData(name=symbol,
                    token=instrument_map.get(symbol))


    def update_high_low(self, high_low:List[HighLow]) -> None:
        """
        Update the high and low values for breakout
        These values are used for calculating breakouts
        """
        for hl in high_low:
            if type(hl) == dict:
                hl = HighLow(**hl)
            print(hl, hl.symbol)
            d = self._data.get(hl.symbol)
            if d:
                d.high = hl.high
                d.low = hl.low

