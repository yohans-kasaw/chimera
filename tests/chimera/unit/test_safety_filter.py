import pytest
import uuid
from datetime import datetime
from chimera.models.result import Result
from chimera.services.safety import SafetyService

@pytest.fixture
def safety_service():
    return SafetyService(confidence_threshold=0.7)

def test_safety_filter_flags_low_confidence(safety_service):
    """US2: Results with confidence < 0.7 should be flagged."""
    # This is expected to fail because check_result is NotImplemented
    result = Result(
        tenant_id="t_tenant1",
        trace_id=str(uuid.uuid4()),
        task_id=str(uuid.uuid4()),
        result_id=str(uuid.uuid4()),
        status="succeeded",
        output={"content": "safe output"},
        confidence=0.6,
        created_at=datetime.utcnow(),
        completed_at=datetime.utcnow()
    )
    assert safety_service.check_result(result) is False

def test_safety_filter_flags_sensitive_keywords(safety_service):
    """US2: Results with sensitive keywords should be flagged."""
    # This is expected to fail because check_result is NotImplemented
    result = Result(
        tenant_id="t_tenant1",
        trace_id=str(uuid.uuid4()),
        task_id=str(uuid.uuid4()),
        result_id=str(uuid.uuid4()),
        status="succeeded",
        output={"content": "My password is 'secret123'"},
        confidence=0.95,
        created_at=datetime.utcnow(),
        completed_at=datetime.utcnow()
    )
    assert safety_service.check_result(result) is False

def test_safety_filter_allows_safe_result(safety_service):
    """US2: Safe results should pass."""
    # This is expected to fail because check_result is NotImplemented
    result = Result(
        tenant_id="t_tenant1",
        trace_id=str(uuid.uuid4()),
        task_id=str(uuid.uuid4()),
        result_id=str(uuid.uuid4()),
        status="succeeded",
        output={"content": "This is a safe message about weather."},
        confidence=0.9,
        created_at=datetime.utcnow(),
        completed_at=datetime.utcnow()
    )
    assert safety_service.check_result(result) is True
