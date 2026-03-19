"""Health-Tools — Medizinische Daten, Medikamente, klinische Studien."""

from mcp.server.fastmcp import FastMCP
from src.clients.health_apis import HealthClient

_client = HealthClient()


def register_health_tools(mcp: FastMCP):

    @mcp.tool()
    async def search_drugs(drug_name: str, limit: int = 5) -> dict:
        """Medikamenten-Informationen suchen.

        Gibt Informationen über Medikamente zurück: Wirkstoffe,
        Anwendungsgebiete, Dosierung, Warnhinweise.

        Args:
            drug_name: Name des Medikaments (z.B. "Ibuprofen", "Aspirin")
            limit: Maximale Ergebnisse
        """
        try:
            data = await _client.search_drugs(drug_name, limit)
            results = data.get("results", [])
            drugs = []
            for r in results[:limit]:
                openfda = r.get("openfda", {})
                drugs.append({
                    "brand_name": openfda.get("brand_name", [""])[0] if openfda.get("brand_name") else "",
                    "generic_name": openfda.get("generic_name", [""])[0] if openfda.get("generic_name") else "",
                    "manufacturer": openfda.get("manufacturer_name", [""])[0] if openfda.get("manufacturer_name") else "",
                    "purpose": (r.get("purpose") or [""])[0][:300] if r.get("purpose") else "",
                    "warnings": (r.get("warnings") or [""])[0][:300] if r.get("warnings") else "",
                    "dosage": (r.get("dosage_and_administration") or [""])[0][:300] if r.get("dosage_and_administration") else "",
                    "route": openfda.get("route", []),
                })
            return {"query": drug_name, "results_count": len(drugs), "drugs": drugs}
        except Exception as e:
            return {"error": str(e), "query": drug_name}

    @mcp.tool()
    async def search_adverse_events(drug_name: str, limit: int = 5) -> dict:
        """Gemeldete Nebenwirkungen eines Medikaments suchen.

        Daten aus dem FDA Adverse Event Reporting System (FAERS).

        Args:
            drug_name: Medikamenten-Name
            limit: Maximale Ergebnisse
        """
        try:
            data = await _client.search_adverse_events(drug_name, limit)
            results = data.get("results", [])
            events = []
            for r in results[:limit]:
                reactions = [rx.get("reactionmeddrapt", "") for rx in r.get("patient", {}).get("reaction", [])[:5]]
                events.append({
                    "serious": r.get("serious", ""),
                    "date": r.get("receiptdate", ""),
                    "reactions": reactions,
                    "outcome": r.get("patient", {}).get("patientonsetage", ""),
                })
            return {"drug": drug_name, "total_reports": data.get("meta", {}).get("results", {}).get("total", 0), "events": events}
        except Exception as e:
            return {"error": str(e), "drug": drug_name}

    @mcp.tool()
    async def search_clinical_trials(
        query: str, status: str = None, limit: int = 10,
    ) -> dict:
        """Klinische Studien auf ClinicalTrials.gov suchen.

        Args:
            query: Suchbegriff (Krankheit, Medikament, Therapie)
            status: Optional — "RECRUITING", "COMPLETED", "ACTIVE_NOT_RECRUITING"
            limit: Maximale Ergebnisse
        """
        try:
            data = await _client.search_trials(query, status, limit)
            studies = data.get("studies", [])
            trials = []
            for s in studies[:limit]:
                protocol = s.get("protocolSection", {})
                id_module = protocol.get("identificationModule", {})
                status_module = protocol.get("statusModule", {})
                desc_module = protocol.get("descriptionModule", {})

                trials.append({
                    "nct_id": id_module.get("nctId", ""),
                    "title": id_module.get("briefTitle", ""),
                    "status": status_module.get("overallStatus", ""),
                    "start_date": status_module.get("startDateStruct", {}).get("date", ""),
                    "summary": (desc_module.get("briefSummary", ""))[:300],
                })
            return {"query": query, "total_count": data.get("totalCount", 0), "trials": trials}
        except Exception as e:
            return {"error": str(e), "query": query}

    @mcp.tool()
    async def get_health_statistics(
        indicator: str, country: str = None, limit: int = 20,
    ) -> dict:
        """WHO Gesundheitsstatistiken abrufen.

        Daten aus dem WHO Global Health Observatory.

        Args:
            indicator: Indikator-Code (z.B. "WHOSIS_000001" für Lebenserwartung)
            country: ISO-3 Ländercode (z.B. "DEU", "USA", "JPN")
            limit: Maximale Datenpunkte
        """
        try:
            data = await _client.get_who_data(indicator, country, limit)
            values = data.get("value", [])
            results = []
            for v in values[:limit]:
                results.append({
                    "country": v.get("SpatialDim", ""),
                    "year": v.get("TimeDim", ""),
                    "value": v.get("NumericValue"),
                    "dimension": v.get("Dim1", ""),
                })
            return {"indicator": indicator, "data_points": len(results), "data": results}
        except Exception as e:
            return {"error": str(e), "indicator": indicator}

    @mcp.tool()
    async def list_health_indicators(limit: int = 20) -> dict:
        """Verfügbare WHO Gesundheitsindikatoren auflisten.

        Args:
            limit: Maximale Anzahl
        """
        try:
            data = await _client.get_who_indicators(limit)
            indicators = data.get("value", [])
            return {
                "total": len(indicators),
                "indicators": [
                    {"code": i.get("IndicatorCode", ""), "name": i.get("IndicatorName", "")}
                    for i in indicators
                ],
            }
        except Exception as e:
            return {"error": str(e)}
