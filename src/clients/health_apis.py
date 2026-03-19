"""Health API Clients — WHO, OpenFDA, ClinicalTrials.gov."""

import httpx


class HealthClient:
    """Async-Client für öffentliche Gesundheits-APIs."""

    def __init__(self):
        self._client = httpx.AsyncClient(timeout=30.0)

    # --- OpenFDA (Medikamente, Nebenwirkungen) ---

    async def search_drugs(self, query: str, limit: int = 10) -> dict:
        """Medikamente über OpenFDA suchen."""
        url = "https://api.fda.gov/drug/label.json"
        params = {"search": f'openfda.brand_name:"{query}"+openfda.generic_name:"{query}"', "limit": limit}
        resp = await self._client.get(url, params=params)
        resp.raise_for_status()
        return resp.json()

    async def search_adverse_events(self, drug: str, limit: int = 10) -> dict:
        """Nebenwirkungen eines Medikaments suchen."""
        url = "https://api.fda.gov/drug/event.json"
        params = {"search": f'patient.drug.openfda.brand_name:"{drug}"', "limit": limit}
        resp = await self._client.get(url, params=params)
        resp.raise_for_status()
        return resp.json()

    # --- ClinicalTrials.gov v2 ---

    async def search_trials(self, query: str, status: str = None, limit: int = 10) -> dict:
        """Klinische Studien suchen."""
        url = "https://clinicaltrials.gov/api/v2/studies"
        params = {"query.term": query, "pageSize": min(limit, 50), "format": "json"}
        if status:
            params["filter.overallStatus"] = status
        resp = await self._client.get(url, params=params)
        resp.raise_for_status()
        return resp.json()

    # --- WHO GHO (Global Health Observatory) ---

    async def get_who_indicators(self, limit: int = 20) -> dict:
        """WHO Gesundheitsindikatoren auflisten."""
        url = "https://ghoapi.azureedge.net/api/Indicator"
        params = {"$top": limit}
        resp = await self._client.get(url, params=params)
        resp.raise_for_status()
        return resp.json()

    async def get_who_data(self, indicator_code: str, country: str = None, limit: int = 20) -> dict:
        """WHO Gesundheitsdaten für einen Indikator abrufen."""
        url = f"https://ghoapi.azureedge.net/api/{indicator_code}"
        params = {"$top": limit}
        if country:
            params["$filter"] = f"SpatialDim eq '{country}'"
        resp = await self._client.get(url, params=params)
        resp.raise_for_status()
        return resp.json()

    async def close(self):
        await self._client.aclose()
