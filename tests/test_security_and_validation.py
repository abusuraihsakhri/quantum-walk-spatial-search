"""
Security and input validation tests for quantum-walk-spatial-search.
"""
import sys
import math
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
import warnings
from agents.base import AuditTrail, PHIGuard, SecurityException
from agents.models import SystemTaskPayload


class TestAuditTrailSecurity:
    """Test audit trail security defaults."""

    def test_audit_trail_generates_ephemeral_key_without_env(self):
        """Without AUDIT_SECRET_KEY, an ephemeral key should be generated with a warning."""
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            trail = AuditTrail()
            assert len(w) == 1
            assert "AUDIT_SECRET_KEY not set" in str(w[0].message)
            assert issubclass(w[0].category, RuntimeWarning)

    def test_audit_trail_uses_provided_key(self):
        """When a key is provided, no warning should be issued."""
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            trail = AuditTrail(secret_key="test-key-12345")
            assert len(w) == 0

    def test_audit_trail_uses_env_key(self, monkeypatch):
        """When AUDIT_SECRET_KEY env var is set, it should be used."""
        monkeypatch.setenv("AUDIT_SECRET_KEY", "env-key-12345")
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            trail = AuditTrail()
            assert len(w) == 0

    def test_audit_trail_logs_and_verifies(self):
        """Audit trail should log entries and verify integrity."""
        trail = AuditTrail(secret_key="test-key")
        trail.log("test_actor", "tier1", "TEST_EVENT", {"data": "value"})
        assert len(trail.get_trail()) == 1
        assert trail.verify_integrity() is True

    def test_audit_trail_detects_tampering(self):
        """Tampered entries should fail integrity verification."""
        trail = AuditTrail(secret_key="test-key")
        trail.log("actor", "tier", "EVENT", {"data": "original"})
        # Tamper with the entry
        trail.logs[0]["payload_hash"] = "tampered_hash"
        assert trail.verify_integrity() is False


class TestInputValidation:
    """Test metric value validation."""

    def test_nan_primary_metric_rejected(self):
        """NaN primary metric should raise ValueError."""
        with pytest.raises(ValueError, match="must be finite"):
            SystemTaskPayload(task_id="T1", target_identifier="K1", primary_metric=math.nan)

    def test_inf_primary_metric_rejected(self):
        """Infinity primary metric should raise ValueError."""
        with pytest.raises(ValueError, match="must be finite"):
            SystemTaskPayload(task_id="T1", target_identifier="K1", primary_metric=math.inf)

    def test_negative_inf_secondary_metric_rejected(self):
        """Negative infinity secondary metric should raise ValueError."""
        with pytest.raises(ValueError, match="must be finite"):
            SystemTaskPayload(task_id="T1", target_identifier="K1", primary_metric=1.0, secondary_metric=-math.inf)

    def test_valid_finite_metrics_accepted(self):
        """Normal finite values should be accepted."""
        payload = SystemTaskPayload(task_id="T1", target_identifier="K1", primary_metric=25.0, secondary_metric=10.0)
        assert payload.primary_metric == 25.0
        assert payload.secondary_metric == 10.0

    def test_zero_metrics_accepted(self):
        """Zero values should be accepted."""
        payload = SystemTaskPayload(task_id="T1", target_identifier="K1", primary_metric=0.0, secondary_metric=0.0)
        assert payload.primary_metric == 0.0

    def test_negative_finite_metrics_accepted(self):
        """Negative finite values should be accepted."""
        payload = SystemTaskPayload(task_id="T1", target_identifier="K1", primary_metric=-5.0, secondary_metric=-3.0)
        assert payload.primary_metric == -5.0


class TestPHIGuard:
    """Test PHI outbound guard patterns."""

    def test_mrn_pattern_detected(self):
        with pytest.raises(SecurityException):
            PHIGuard.assert_no_phi("Patient MRN-12345678")

    def test_ssn_pattern_detected(self):
        with pytest.raises(SecurityException):
            PHIGuard.assert_no_phi("SSN: 123-45-6789")

    def test_phone_pattern_detected(self):
        with pytest.raises(SecurityException):
            PHIGuard.assert_no_phi("Call 555-123-4567")

    def test_email_pattern_detected(self):
        with pytest.raises(SecurityException):
            PHIGuard.assert_no_phi("Email: patient@example.com")

    def test_clean_text_passes(self):
        PHIGuard.assert_no_phi("Analytical specimen KEY-001 optimal status")

    def test_redact_phi(self):
        result = PHIGuard.redact_phi("Contact patient@example.com for MRN-12345")
        assert "[REDACTED_IDENTIFIER]" in result
        assert "patient@example.com" not in result
        assert "MRN-12345" not in result
