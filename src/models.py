"""
Intermediate data transmission objects (DTO) for bundling data transmitted 
between xlwings scripts and QBHandler object
"""

from dataclasses import dataclass


@dataclass
class LineItemDTO:
    item_id: str
    quantity: float
    unit_price: float
    description: str | None = None

@dataclass
class EstimateDTO:
    customer_id: str
    lines: list[LineItemDTO]
    estimate_number: str | None = None
    total_amount: float | None = None

