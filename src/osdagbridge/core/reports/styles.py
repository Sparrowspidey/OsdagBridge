"""Single source of truth for report styling (LaTeX values)."""

OSDAG_GREEN_HEX = "91B014"
PAGE_MARGIN = "1in"
FOOTER_LEFT = r"Osdag $|$ FOSSEE $|$ Indian Institute of Technology Bombay"

TAB_COL_SEP = "6pt"
ARRAY_STRETCH = "1.12"
LT_PRE = "0pt"
LT_POST = "6pt"
RULE_WIDTH = "0.5pt"
EXTRA_ROW_HEIGHT = "0.6pt"
NEEDSPACE_LINES = 5


def table_layout_block():
    return (
        r"\setlength{\tabcolsep}{" + TAB_COL_SEP + "}\n"
        r"\renewcommand{\arraystretch}{" + ARRAY_STRETCH + "}\n"
        r"\setlength{\LTpre}{" + LT_PRE + "}\n"
        r"\setlength{\LTpost}{" + LT_POST + "}\n"
        r"\setlength{\arrayrulewidth}{" + RULE_WIDTH + "}\n"
        r"\setlength{\extrarowheight}{" + EXTRA_ROW_HEIGHT + "}\n"
        r"\BeforeBeginEnvironment{table}{\needspace{" + str(NEEDSPACE_LINES) + r"\baselineskip}}" + "\n"
        r"\BeforeBeginEnvironment{longtable}{\needspace{" + str(NEEDSPACE_LINES) + r"\baselineskip}}" + "\n"
    )