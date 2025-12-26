# Decisions: Streamlit Deprecation Fixes

## Decision Log

### 2025-12-26 - Parameter Mapping

**Context**: Streamlit is deprecating `use_container_width`.

**Options**:
1. Follow Streamlit's official recommendation.
2. Ignore until it breaks.

**Decision**: Option 1

**Reasoning**: Proactive maintenance prevents future breakage as the feature will be removed after 2025-12-31.

**Consequences**: The code will use the modern API.
