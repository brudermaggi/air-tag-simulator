from pydantic import BaseModel



class Airtag(BaseModel):
    id : int
    name : str | None = None
    lon : float | None = None
    lat: float | None = None

    