# Implementation Plan: Dashboard Journalistique Olympique

**Branch**: `001-journalistic-dashboard` | **Date**: 2025-12-16 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-journalistic-dashboard/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Transform the existing Olympic MVP dashboard into a comprehensive journalistic tool by adding: (1) interactive choropleth world map showing medal density by country, (2) Top 10 athletes section with ranked table display, (3) two-country comparison timeline chart, (4) CSV export functionality for filtered data, and (5) tabbed navigation interface using Streamlit's `st.tabs()`. All features must respect established teal/blue-green theme, maintain <3s load times via `@st.cache_data`, and handle edge cases (zero medals, empty filters, duplicate country selection) gracefully.

## Technical Context

**Language/Version**: Python 3.10+  
**Primary Dependencies**: Streamlit 1.52.0+, Pandas 2.3.3+, Plotly Express 6.5.0+  
**Storage**: CSV file (`raw_data/olympics_1896_2004.csv`, loaded with `skiprows=5` due to header format)  
**Testing**: Manual acceptance testing against user story scenarios (automated testing framework NEEDS CLARIFICATION)  
**Target Platform**: Web browser via Streamlit server (cross-platform: Windows/macOS/Linux)  
**Project Type**: Single web application (Streamlit dashboard)  
**Performance Goals**: Initial load <3s for full dataset, filter interactions <500ms, chart rendering <1s per visualization  
**Constraints**: Offline-capable (no external APIs), dataset ends at 2004 (no post-2004 data), theme colors fixed in `.streamlit/config.toml`, NOC codes used as-is without historical country fusion  
**Scale/Scope**: ~30k rows in dataset (1896-2004 Olympics), 4 main tabs, 6+ visualizations, 14 functional requirements, single-user local deployment

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### I. Data-Centric Development ✅ PASS

**Evaluation**: All 5 user stories trace back to dataset transformations:
- World map: Aggregates medals by NOC code
- Top athletes: Aggregates medals by athlete name with Olympic tiebreaker
- Country comparison: Time-series aggregation by year and NOC
- CSV export: Direct filtered dataset extraction
- Tab navigation: UI wrapper (no data transformation, compliant)

**Data Handling**: FR-013 requires informative messages for empty filter results. Edge cases document handling of zero-medal countries, missing athletes, and empty exports.

**Testability**: Each user story includes independent test criteria with sample data scenarios.

**Verdict**: Feature is fundamentally data-driven. All visualizations explicitly reference dataset columns (NOC, Athlete Name, Year, Medal, Sport). No violations.

---

### II. Performance-First Caching ✅ PASS

**Evaluation**: 
- FR-012 mandates `@st.cache_data` for all heavy data operations
- SC-001 through SC-004 define explicit performance targets (<5s map, <2s athletes, <3s comparison, <2s export)
- SC-006 requires maintaining <3s initial load despite feature additions

**Implementation Plan**: 
- Cached functions will include: `load_data()`, `aggregate_medals_by_country()`, `get_top_athletes()`, `get_country_comparison_data()`
- Cache keys will use filter parameters (year_range, sport, noc) as inputs

**Verdict**: Performance requirements align with constitution's <3s load, <500ms interaction goals. Explicit caching mandate in FR-012. No violations.

---

### III. Type Safety & Documentation ✅ PASS

**Evaluation**: Constitution requires type hints and Google-style docstrings for all functions. Spec does not explicitly mention this, but it's a code-level requirement enforced during implementation.

**Implementation Commitment**: All new functions added to `app.py` will include:
- Type hints using Python 3.10+ syntax (`list[dict[str, Any]]`, `pd.DataFrame`, etc.)
- Google-style docstrings with Args, Returns, Raises sections
- Example usage in docstrings for complex aggregations (e.g., Olympic tiebreaker logic)

**Verdict**: No specification-level conflict. Constitution enforces this at code review stage. Compliant.

---

### IV. Specification-Driven Development ✅ PASS

**Evaluation**: This plan follows Speckit workflow:
1. ✅ Specification created (`spec.md` with 5 user stories, 14 FRs, 8 success criteria)
2. ✅ Clarification session completed (5 Q&A pairs resolving display formats, tiebreakers, naming)
3. 🔄 Planning phase (this document) in progress
4. ⏳ Research phase (Phase 0) next
5. ⏳ Design phase (Phase 1) after research
6. ⏳ Implementation phase (Phase 2) after design approval

**Verdict**: Textbook adherence to specification-driven approach. No violations.

---

### V. Visual Consistency ✅ PASS

**Evaluation**:
- FR-011 mandates all graphics respect `.streamlit/config.toml` theme (teal/blue-green)
- SC-007 requires 0 visual regressions
- Constitution prohibits theme changes without user approval
- Spec explicitly states theme is "not to be changed" (Out of Scope section)

**Color Preservation**: All new Plotly charts (choropleth, line charts, styled tables) will use:
- `color_continuous_scale` with teal gradient for choropleth
- `color_discrete_sequence` with theme colors for comparison lines
- Streamlit's native table styling (inherits theme automatically)

**Verdict**: Feature spec reinforces constitution's visual consistency mandate. No violations.

---

## Overall Constitution Compliance: ✅ PASS

**Summary**: All 5 core principles are satisfied by the feature specification. No violations require justification in Complexity Tracking table.

**Gate Status**: **CLEARED** - Proceed to Phase 0 (Research)

---

## Post-Phase 1 Constitution Re-Check

*Re-evaluation after research.md, data-model.md, contracts/, and quickstart.md completed*

### Design Artifacts Review

**research.md**:
- ✅ Principle I (Data-Centric): All 8 research tasks resolve data transformation questions
- ✅ Principle II (Performance): Research #8 defines caching strategy to meet <500ms target
- ✅ Principle III (Type Safety): No violations (code-level enforcement in Phase 2)
- ✅ Principle IV (Spec-Driven): Follows Speckit workflow (Phase 0 complete)
- ✅ Principle V (Visual Consistency): Research #5 documents color constant strategy

**data-model.md**:
- ✅ Principle I (Data-Centric): 4 derived models with explicit transformation logic
- ✅ Principle II (Performance): Caching strategy marked for each aggregation function
- ✅ Principle III (Type Safety): Schema definitions include types for all fields
- ✅ Principle IV (Spec-Driven): Entities map directly to functional requirements
- ✅ Principle V (Visual Consistency): No design-level conflicts

**contracts/functions.md**:
- ✅ Principle I (Data-Centric): 14 function contracts define input/output schemas
- ✅ Principle II (Performance): Cache decorators specified for 4 functions
- ✅ Principle III (Type Safety): All signatures include type hints (Python 3.10+)
- ✅ Principle IV (Spec-Driven): Contracts reference spec FRs and success criteria
- ✅ Principle V (Visual Consistency): Color constants referenced in rendering functions

**quickstart.md**:
- ✅ Principle I (Data-Centric): Implementation phases prioritize data transformations
- ✅ Principle II (Performance): Performance testing checklist includes timing targets
- ✅ Principle III (Type Safety): Code samples include type hints and docstrings
- ✅ Principle IV (Spec-Driven): Testing checklist uses acceptance scenarios from spec
- ✅ Principle V (Visual Consistency): Visual consistency testing section included

### Verdict: ✅ NO NEW VIOLATIONS

**Phase 1 design artifacts maintain full compliance with all 5 constitution principles.**

**Gate Status**: **RE-CLEARED** - Ready for Phase 2 (Implementation via `/speckit.tasks`)

## Project Structure

### Documentation (this feature)

```text
specs/[###-feature]/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)

```text
app.py                          # Main Streamlit application (current MVP + new features)
raw_data/
└── olympics_1896_2004.csv      # Source dataset
.streamlit/
└── config.toml                 # Theme configuration (teal/blue-green)
requirements.txt                # Python dependencies
README.md                       # Project documentation
specs/
└── 001-journalistic-dashboard/ # This feature's documentation
    ├── spec.md
    ├── plan.md                 # This file
    ├── research.md             # Phase 0 output (to be created)
    ├── data-model.md           # Phase 1 output (to be created)
    ├── quickstart.md           # Phase 1 output (to be created)
    └── contracts/              # Phase 1 output (to be created)
```

**Structure Decision**: Single-file Streamlit application architecture. All feature code will be added to `app.py` using modular functions. No separate `src/` directory needed for this scale (single dashboard with ~500-800 LOC after feature additions). Testing will be manual via acceptance scenarios in spec.md until automated test framework is established.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |
