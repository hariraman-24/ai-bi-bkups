import re


def detect_intent(question):

    q = question.lower().strip()

    # =============================
    # 📄 DOCUMENT QUERIES
    # =============================
    if any(x in q for x in [
        "pdf",
        "document",
        "uploaded file",
        "uploaded pdf",
        "summarize page",
        "word count",
        "overview of file",
        "what is this pdf about",
        "explain this document",
        "page "
    ]):
        return "document_query"

    # =============================
    # 🔢 TOP N (HIGHEST PRIORITY)
    # =============================
    if re.search(r"\btop\s+\d+\b", q):
        return "top_n"

    # =============================
    # 🔮 FORECAST / PREDICTION
    # =============================
    if any(x in q for x in [
        "forecast",
        "predict",
        "prediction",
        "future",
        "projection",
        "future growth",
        "future sales"
    ]):
        return "forecast"

    # =============================
    # 📌 KPI / EXECUTIVE METRICS
    # =============================
    if any(x in q for x in [
        "kpi",
        "dashboard",
        "executive summary",
        "business summary",
        "company overview",
        "overall performance",
        "overall sales",
        "overall revenue",
        "overall profit",
        "total sales",
        "total revenue",
        "total profit",
        "total customers",
        "total amount"
    ]):
        return "kpi"

    # =============================
    # 📈 TREND / TIME SERIES
    # =============================
    if any(x in q for x in [
        "trend",
        "growth",
        "over time",
        "monthly",
        "yearly",
        "time series",
        "sales trend",
        "revenue trend"
    ]):
        return "trend"

    # =============================
    # 🥧 DISTRIBUTION / SHARE
    # =============================
    if any(x in q for x in [
        "distribution",
        "share",
        "contribution",
        "percentage",
        "market share",
        "split"
    ]):
        return "distribution"

    # =============================
    # 📊 VISUALIZATION
    # =============================
    if any(x in q for x in [
        "visualize",
        "analytics",
        "chart",
        "graph",
        "dashboard visualization"
    ]):
        return "visualization"

    # =============================
    # 🧠 BUSINESS ANALYSIS
    # =============================
    if any(x in q for x in [
        "business insights",
        "analyze business",
        "business analysis",
        "executive insights",
        "strategic insights",
        "business performance",
        "performance analysis"
    ]):
        return "business_analysis"

    # =============================
    # 📊 TOTAL / SUM
    # =============================
    if any(x in q for x in [
        "total",
        "sum",
        "overall",
        "how much",
        "sales did we make"
    ]):
        return "sum"

    # =============================
    # 🔢 COUNT
    # =============================
    if any(x in q for x in [
        "count",
        "how many",
        "number of"
    ]):
        return "count"

    # =============================
    # 📉 AVERAGE
    # =============================
    if any(x in q for x in [
        "average",
        "mean",
        "avg"
    ]):
        return "average"

    # =============================
    # 🔝 RANGE / MAX / MIN
    # =============================
    if any(x in q for x in [
        "range",
        "between",
        "highest",
        "lowest",
        "maximum",
        "minimum",
        "max",
        "min",
        "biggest",
        "smallest"
    ]):
        return "range_query"

    # =============================
    # 🔝 RANKING TOP
    # =============================
    if any(x in q for x in [
        "top",
        "best",
        "most",
        "leading",
        "top performing",
        "best selling"
    ]):
        return "ranking_top"

    # =============================
    # 🔻 RANKING LOW
    # =============================
    if any(x in q for x in [
        "worst",
        "least",
        "bottom",
        "poor performance",
        "low performing"
    ]):
        return "ranking_low"

    # =============================
    # 📅 MONTH FILTER
    # =============================
    if any(month in q for month in [
        "january",
        "february",
        "march",
        "april",
        "may",
        "june",
        "july",
        "august",
        "september",
        "october",
        "november",
        "december",
        "jan",
        "feb",
        "mar",
        "apr",
        "jun",
        "jul",
        "aug",
        "sep",
        "oct",
        "nov",
        "dec"
    ]):
        return "month_filter"

    # =============================
    # 📅 YEAR FILTER
    # =============================
    if re.search(r"\b20\d{2}\b", q):
        return "year_filter"

    # =============================
    # 📊 GROUPING
    # =============================
    if any(x in q for x in [
        "by region",
        "group by",
        "per region",
        "category wise",
        "by category",
        "by product",
        "product wise",
        "by employee",
        "employee wise",
        "department wise"
    ]):
        return "group"

    # =============================
    # 🔃 SORTING
    # =============================
    if any(x in q for x in [
        "ascending",
        "low to high"
    ]):
        return "sort_asc"

    if any(x in q for x in [
        "descending",
        "high to low"
    ]):
        return "sort_desc"

    if any(x in q for x in [
        "alphabetical",
        "a to z"
    ]):
        return "sort_alpha"

    # =============================
    # ⚖️ COMPARISON
    # =============================
    if any(x in q for x in [
        "compare",
        "difference",
        "vs",
        "versus"
    ]):
        return "compare"

    # =============================
    # 📄 SUMMARY / REPORT
    # =============================
    if any(x in q for x in [
        "summary",
        "overview",
        "insight",
        "analysis",
        "report",
        "how are we doing"
    ]):
        return "analysis"

    # =============================
    # 💰 PROFIT
    # =============================
    if any(x in q for x in [
        "profit",
        "profitability",
        "making profit",
        "making money"
    ]):
        return "profit"

    # =============================
    # ❓ GENERAL
    # =============================
    return "general"