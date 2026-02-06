from chimera.services.audit import AuditService


def test_audit_service_logs_event() -> None:
    service = AuditService()
    event = service.log_event(
        tenant_id="t_acme", trace_id="tr_1", event_type="test_event", payload={"foo": "bar"}
    )

    assert event.tenant_id == "t_acme"
    assert event.event_type == "test_event"
    assert event.payload == {"foo": "bar"}
    assert len(service._events) == 1
