def classify_query(question):

    q = question.lower()

    # -------- CHART KEYWORDS (STRONG DETECTION) --------
    chart_keywords = [
        "trend",
        "compare",
        "growth",
        "distribution",
        "by region",
        "by category",
        "monthly",
        "top",
        "analysis",
        "breakdown"
    ]

    # -------- TEXT KEYWORDS --------
    text_keywords = [
        "count",
        "total",
        "sum",
        "average",
        "list",
        "show all"
    ]

    # -------- PRIORITY: CHART --------
    if any(word in q for word in chart_keywords):
        return "chart"

    # -------- TEXT --------
    if any(word in q for word in text_keywords):
        return "text"

    # -------- DEFAULT --------
    return "text"