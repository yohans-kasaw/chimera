from typing import Annotated

from pydantic import StringConstraints

# Tenant ID format: t followed by underscore and alphanumeric
TenantId = Annotated[str, StringConstraints(pattern=r"^t_[a-z0-9_]+$")]
TraceId = Annotated[str, StringConstraints(min_length=1)]
TaskId = Annotated[str, StringConstraints(min_length=1)]
SessionId = Annotated[str, StringConstraints(min_length=1)]
