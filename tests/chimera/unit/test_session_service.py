from chimera.services.session import SessionService, SessionState


def test_session_service_create_and_get() -> None:
    service = SessionService()
    session = service.create_session("t_acme")

    assert session.tenant_id == "t_acme"
    assert session.state == SessionState.CREATED

    retrieved = service.get_session(session.session_id)
    assert retrieved == session


def test_session_service_get_nonexistent() -> None:
    service = SessionService()
    assert service.get_session("none") is None
