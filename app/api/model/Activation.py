from enum import Enum

from pydantic import BaseModel

# from app.service.grpc.model.types import Brokerage


class StringBrokerage(Enum):
    BBAE = "BBAE"
    Chase = "Chase"
    DSPAC = "DSPAC"
    Fennel = "Fennel"
    Fidelity = "Fidelity"
    Firstrade = "Firstrade"
    Public = "Public"
    Robinhood = "Robinhood"
    Schwab = "Schwab"
    SoFi = "SoFi"
    Tornado = "Tornado"
    Tradier = "Tradier"
    Tastytrade = "Tastytrade"
    Webull = "Webull"
    Vanguard = "Vanguard"
    WellsFargo = "WellsFargo"


class ActivationRequest(BaseModel):
    group_name: str
    account_name: str
    brokerage: StringBrokerage
    cred: dict[str, str]