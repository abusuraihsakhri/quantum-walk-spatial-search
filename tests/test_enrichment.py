"""
Automated Pytest for quantum-walk-spatial-search Enrichment Modules.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
from enrichment import (
    SpatialSearchViaQuantumWalkWithOptimalMixingTimeEngine,
    ImplementationEngine,
    FilesToCreatemodifyEngine,
    TestingEngine,
    ContinuoustimeQuantumWalkForGraphConnectivityEngine,
    QuantumwalkspatialsearchEnrichmentSuite,
    enrichment_suite,
)

def test_enrichment_suite_execution():
    suite = QuantumwalkspatialsearchEnrichmentSuite()
    res = suite.execute_all(primary_val=0.5, secondary_val=0.2)
    assert len(res) >= 1
    for k, v in res.items():
        assert v.status in ["OPTIMAL", "WARNING", "CRITICAL_ALERT"]
        assert isinstance(v.recommendations, list)

def test_enrichment_threshold_escalation():
    suite = QuantumwalkspatialsearchEnrichmentSuite()
    res = suite.execute_all(primary_val=10.0, secondary_val=5.0)
    for k, v in res.items():
        assert v.status in ["WARNING", "CRITICAL_ALERT"]
        assert len(v.alerts) > 0

def test_enrichment_suite_has_unique_engines():
    """Verify the suite has 5 unique engine instances (no duplicates)."""
    suite = QuantumwalkspatialsearchEnrichmentSuite()
    assert len([
        suite.spatialsearchviaquan,
        suite.implementationengine,
        suite.filestocreatemodifye,
        suite.testingengine,
        suite.continuoustimequantu,
    ]) == 5

def test_enrichment_suite_returns_five_results():
    """Verify execute_all returns exactly 5 results (one per engine)."""
    suite = QuantumwalkspatialsearchEnrichmentSuite()
    res = suite.execute_all(primary_val=1.0, secondary_val=0.5)
    assert len(res) == 5
