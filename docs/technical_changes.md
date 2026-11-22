# OsdagBridge Report Generator: Technical Changes

Branch: `report-enhancements` (fork: Sparrowspidey/OsdagBridge)

## 0. Note on architecture
The report is built from raw LaTeX strings assembled in `src/osdagbridge/core/reports/chap*.py`
and compiled with pdflatex (twice, in a temporary directory). It does not use PyLaTeX. The
requirements were therefore implemented as LaTeX `longtable` constructs and string helpers,
not PyLaTeX objects. No engineering calculation was changed; all edits concern
presentation, structure and visualisation.

## 1. Files altered (all under src/osdagbridge/core/reports/)
| File | Change |
|---|---|
| styles.py (new) | Central style module (see section 4) |
| charts.py (new) | Matplotlib charts (UR and quantity charts), Agg backend |
| report_utils.py | Added `lt_head()` and `keep_rows_together()` helpers |
| report_generator.py | Preamble reads styles; passes the temp image directory to chapters |
| chap2.py, chap3.py, chap4.py, chap5.py, chap7.py | Repeated headers; live-load tables; charts |
| .gitignore | Ignore `*.bak` |

## 2. Requirement-by-requirement
**R1 Repeated headers.** `lt_head(caption, header_row)` emits `\caption`, header row and
`\endfirsthead`, then a `\caption*{... (continued)}`, the header row and `\endhead`. It was
applied to 44 longtables (apply_lt_head.py preview/convert script) plus the BOM table in
chapter 7. `\BeforeBeginEnvironment{longtable}{\Needspace{10\baselineskip}}` (in
styles.table_layout_block) prevents tables starting with too little room.

**R2 Footer overlap.** Cause: the girder label (G1..G4) was a tall `\multirow{N}` cell; when a
page break fell inside a group, the label was drawn over the footer. Fix:
`keep_rows_together()` makes rows inside a group non-breaking (`\\*`) and reduces the
label cell to `\multirow{1}`, so the label sits on the first row and cannot overlap the footer.
Verified on the Report_After pages with girder tables.

**R3 Live loads (Chapter 3).** The merged table was replaced by three tables:
vehicular (Vehicle Class, Total Load kN, Impact Factor, Reference), associated loads
(braking, centrifugal), and footway load (only when a footpath exists). Vehicles come from the
Additional Inputs > Loading selection (verified with only Class A and 70R Wheeled ticked).
Impact factors use IRC6_2017.cl_208_2 (Class A) and cl_208_3 (AA/70R). Total loads are read from
existing IRC6_2017 vehicle functions. The old footway row was blank because the computed value
was never used; this is fixed (4.905 kN/m2 per IRC 6 Cl. 206.1).

**R4 UR charts.** `charts.build_ur_charts_tex` takes the UR values collected while Table 5.29
is built, so the charts always match the table. Four bar charts (girders, deck slab, cross
bracing, end diaphragms) with a red dashed line at UR = 1.0; failing bars are red. They are
embedded after Table 5.29 in Section 5.5. PNGs are written to the temporary `images/` folder.

**R5 Quantity charts.** `charts.build_quantity_charts_tex` reads the same dictionary that prints
Table 7.1: steel tonnage (girders, cross bracing, end diaphragms) and concrete volume (m3) vs
reinforcement weight (MT, separate panels because units differ).

**R6 Central style module.** See section 4.

## 3. Rationale
- Helper functions and a style module keep each chapter free of repeated LaTeX boilerplate and
  allow global changes in one place.
- Charts use the Agg backend because the report is generated in a background thread.
- Chart data is taken from the same values as the tables to prevent inconsistencies.
- No engineering logic was modified.

## 4. styles.py structure
- `OSDAG_GREEN_HEX`, `PAGE_MARGIN`, `FOOTER_LEFT`: colour, geometry, footer text.
- Table layout constants and `table_layout_block()`: column separation, longtable
  alignment, needspace rule.
- Chart constants: `CHART_PASS_COLOR`, `CHART_FAIL_COLOR`, `CHART_LIMIT_COLOR`, `CHART_DPI`.
- `report_generator.preamble()` consumes these values.

## 5. Known gaps (not completed)
- R3: per-vehicle braking columns (Considered/Value/Eccentricity) and Total Load for Class AA,
  70R Bogie and Fatigue are not shown; the library has no per-vehicle values for them.
  `IRC6_2017.cl_211_2_braking_force(2)` raises UnboundLocalError (`braking_force_2` unset),
  so braking load shows "not available". Centrifugal force is not implemented in the
  library, so it is shown as not applicable (straight bridge).
- R5: end diaphragm steel quantity is not computed by the take-off (shown as N.A.).
  End diaphragm UR values are the cross-bracing results copied by the existing pipeline.
- R6: column widths, row spacing and some paddings are still in chapter files.

## 6. Additional findings (reported, not fixed)
- Table 2.7 units wrong (1.67 mm should be 1670 mm).
- Table 2.4 overall width prints 12.149999999999999 with a footpath.
- Table 4.1 row order changes between runs.
- Many "[ PLACEHOLDER ]" figures (headless CAD export).
- Blank cells in Tables 3.5, 4.2, 5.7.
- Executive summary says "pass" while overall status is Fail (fatigue, deflection).
- Table 2.9 says IS 100x100x10 bracing while Table 5.23 shows 40x40x3.
- Steel density 76.4 vs 78.5 kN/m3 in assumptions text.