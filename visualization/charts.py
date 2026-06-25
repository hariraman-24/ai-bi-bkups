import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import os
import uuid
from datetime import datetime

# ======================================================
# 🌙 PROFESSIONAL DARK THEME & TYPOGRAPHY
# ======================================================
plt.style.use("dark_background")
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Segoe UI', 'Inter', 'Roboto', 'Arial']

# ======================================================
# 📅 MONTH MAP
# ======================================================
month_map = {
    "1": "Jan",
    "2": "Feb",
    "3": "Mar",
    "4": "Apr",
    "5": "May",
    "6": "Jun",
    "7": "Jul",
    "8": "Aug",
    "9": "Sep",
    "10": "Oct",
    "11": "Nov",
    "12": "Dec"
}

# ======================================================
# 🎨 POWER BI COLORS
# ======================================================
PRIMARY_COLORS = [
    "#38BDF8",
    "#06B6D4",
    "#10B981",
    "#F59E0B",
    "#EF4444",
    "#8B5CF6",
    "#EC4899",
    "#14B8A6",
    "#6366F1",
    "#F97316"
]

# ======================================================
# 🎨 UI COLORS
# ======================================================
BG_COLOR = "#0f172a"
CARD_COLOR = "#111827"
GRID_COLOR = "#334155"
TEXT_COLOR = "#f8fafc"

# ======================================================
# 🧹 CLEAN LABELS
# ======================================================
def clean_label(text):

    text = str(text)

    text = text.replace("_", " ")

    text = text.title()

    if len(text) > 25:
        text = text[:25] + "..."

    return text

# ======================================================
# 🔍 DETECT BEST NUMERIC COLUMN
# ======================================================
def detect_y_key(keys, sample_row):

    priority_words = [
        "sales",
        "revenue",
        "profit",
        "amount",
        "percentage",
        "share",
        "count",
        "total",
        "price",
        "expenses",
        "forecast"
    ]

    # ------------------------------------------
    # PRIORITY NUMERIC
    # ------------------------------------------
    for key in keys:

        if any(word in key.lower() for word in priority_words):

            try:
                float(sample_row[key])
                return key
            except:
                pass

    # ------------------------------------------
    # FALLBACK NUMERIC
    # ------------------------------------------
    for key in keys:

        try:
            float(sample_row[key])
            return key
        except:
            continue

    return None

# ======================================================
# 🏷️ GENERATE LABELS
# ======================================================
def generate_x_labels(data, x_keys):

    labels = []

    for row in data:

        # --------------------------------------
        # DATE DETECTION
        # --------------------------------------
        date_key = None

        for k in x_keys:

            if "date" in k.lower():
                date_key = k
                break

        if date_key:

            try:

                dt = datetime.strptime(
                    str(row[date_key])[:10],
                    "%Y-%m-%d"
                )

                labels.append(
                    dt.strftime("%d %b %Y")
                )

            except:

                labels.append(
                    clean_label(row[date_key])
                )

        # --------------------------------------
        # YEAR + MONTH
        # --------------------------------------
        elif (
            any("year" in k.lower() for k in x_keys)
            and any("month" in k.lower() for k in x_keys)
        ):

            year_key = None
            month_key = None

            for k in x_keys:

                if "year" in k.lower():
                    year_key = k

                if "month" in k.lower():
                    month_key = k

            year = str(row[year_key])

            month = str(row[month_key])

            month_name = month_map.get(
                month,
                f"Month {month}"
            )

            labels.append(
                f"{month_name} {year}"
            )

        # --------------------------------------
        # NORMAL LABELS
        # --------------------------------------
        else:

            label = " ".join(
                str(row[k])
                for k in x_keys
            )

            labels.append(
                clean_label(label)
            )

    return labels

# ======================================================
# 🎯 MAIN CHART ENGINE
# ======================================================
def generate_chart(data, question=""):

    # ==================================================
    # SAFETY
    # ==================================================
    if not data or len(data) == 0:
        return None, None

    keys = list(data[0].keys())

    # ==================================================
    # DETECT AXIS
    # ==================================================
    y_key = detect_y_key(
        keys,
        data[0]
    )

    if y_key is None:
        return None, None

    x_keys = [
        k for k in keys
        if k != y_key
    ]

    x = generate_x_labels(
        data,
        x_keys
    )

    # ==================================================
    # Y VALUES
    # ==================================================
    y = []

    for row in data:

        try:
            y.append(float(row[y_key]))
        except:
            y.append(0)

    # ==================================================
    # CLEAN INVALID VALUES
    # ==================================================
    filtered = [
        (a, b)
        for a, b in zip(x, y)
        if b is not None
    ]

    # ==================================================
    # AGGREGATE DUPLICATES (PREVENT OVERLAPPING)
    # ==================================================
    agg_dict = {}
    for lx, ly in filtered:
        if lx not in agg_dict:
            agg_dict[lx] = 0
        agg_dict[lx] += ly
        
    x = []
    y = []
    for lx, ly in filtered:
        if lx not in x:
            x.append(lx)
            y.append(agg_dict[lx])

    # ==================================================
    # LIMIT HUGE DATA
    # ==================================================
    if len(x) > 12:

        x = x[:12]
        y = y[:12]

    if len(x) == 0:
        return None, None

    # ==================================================
    # FIGURE
    # ==================================================
    fig, ax = plt.subplots(
        figsize=(14, 7)
    )

    fig.patch.set_facecolor(BG_COLOR)

    ax.set_facecolor(CARD_COLOR)

    q = question.lower()

    colors = PRIMARY_COLORS * 10

    chart_type = "bar"

    # ==================================================
    # 📈 TREND / FORECAST
    # ==================================================
    if any(word in q for word in [
        "trend",
        "forecast",
        "growth",
        "monthly",
        "yearly",
        "time",
        "over time"
    ]):

        ax.plot(
            x,
            y,
            marker='o',
            linewidth=3,
            markersize=8,
            color="#38BDF8"
        )

        ax.fill_between(
            range(len(y)),
            y,
            alpha=0.20,
            color="#38BDF8"
        )

        # VALUE LABELS
        for i, value in enumerate(y):

            ax.text(
                i,
                value,
                f"{value:,.0f}",
                fontsize=9,
                ha='center',
                color="white"
            )

        chart_type = "line"

    # ==================================================
    # 🥧 PROFESSIONAL DONUT CHART
    # ==================================================
    elif any(word in q for word in [
        "distribution",
        "share",
        "contribution",
        "percentage"
    ]):

        # ----------------------------------------------
        # SORT & LIMIT TOP VALUES
        # ----------------------------------------------
        donut_data = sorted(
            zip(x, y),
            key=lambda z: z[1],
            reverse=True
        )[:6]

        x = [i[0] for i in donut_data]
        y = [i[1] for i in donut_data]

        # ----------------------------------------------
        # CONVERT TO PERCENTAGES
        # ----------------------------------------------
        total = sum(y)

        if total > 0:

            y = [
                (v / total) * 100
                for v in y
            ]

        # ----------------------------------------------
        # CLEAN LABELS
        # ----------------------------------------------
        short_labels = []

        for label in x:

            words = label.split()

            short = words[0]

            if len(words) > 1:
                short += f" {words[-1]}"

            if len(short) > 18:
                short = short[:18] + "..."

            short_labels.append(short)

        # ----------------------------------------------
        # DONUT CHART
        # ----------------------------------------------
        wedges, texts, autotexts = ax.pie(
            y,
            labels=short_labels,
            colors=colors[:len(x)],
            autopct='%1.1f%%',
            startangle=90,
            pctdistance=0.78,
            labeldistance=1.08,
            wedgeprops={
                'linewidth': 2,
                'edgecolor': BG_COLOR,
                'width': 0.42
            }
        )

        # ----------------------------------------------
        # LABEL STYLING
        # ----------------------------------------------
        for text in texts:

            text.set_color(TEXT_COLOR)
            text.set_fontsize(10)
            text.set_fontweight("bold")

        for autotext in autotexts:

            autotext.set_color("white")
            autotext.set_fontsize(10)
            autotext.set_fontweight("bold")

        chart_type = "donut"

    # ==================================================
    # 📊 HORIZONTAL BAR
    # ==================================================
    elif any(word in q for word in [
        "top",
        "best",
        "compare",
        "highest",
        "employee",
        "product",
        "region",
        "category",
        "department",
        "performance"
    ]):

        sorted_data = sorted(
            zip(x, y),
            key=lambda z: z[1],
            reverse=True
        )

        x = [i[0] for i in sorted_data]
        y = [i[1] for i in sorted_data]

        bars = ax.barh(
            x,
            y,
            color=colors[:len(x)],
            height=0.60
        )

        ax.invert_yaxis()

        # VALUE LABELS
        for bar in bars:

            width = bar.get_width()

            ax.text(
                width,
                bar.get_y() + bar.get_height()/2,
                f"{width:,.0f}",
                va='center',
                fontsize=10,
                color="white",
                fontweight='bold'
            )

        chart_type = "barh"

    # ==================================================
    # 📦 PROFESSIONAL KPI CARD
    # ==================================================
    elif len(x) == 1:

        # ----------------------------------------------
        # REMOVE AXES
        # ----------------------------------------------
        ax.axis('off')

        # ----------------------------------------------
        # MAIN KPI VALUE
        # ----------------------------------------------
        ax.text(
            0.5,
            0.58,
            f"{y[0]:,.0f}",
            fontsize=42,
            fontweight='bold',
            ha='center',
            color="#38BDF8",
            transform=ax.transAxes
        )

        # ----------------------------------------------
        # KPI TITLE
        # ----------------------------------------------
        ax.text(
            0.5,
            0.42,
            clean_label(question),
            fontsize=16,
            ha='center',
            color="white",
            transform=ax.transAxes
        )

        # ----------------------------------------------
        # SUBTITLE
        # ----------------------------------------------
        ax.text(
            0.5,
            0.30,
            "Executive KPI Summary",
            fontsize=11,
            ha='center',
            color="#94A3B8",
            transform=ax.transAxes
        )

        chart_type = "single"

    # ==================================================
    # 📊 DEFAULT BAR
    # ==================================================
    else:

        bars = ax.bar(
            x,
            y,
            color=colors[:len(x)],
            width=0.65
        )

        for bar in bars:

            height = bar.get_height()

            ax.text(
                bar.get_x() + bar.get_width()/2,
                height,
                f"{height:,.0f}",
                ha='center',
                va='bottom',
                fontsize=9,
                color="white"
            )

        chart_type = "bar"

    # ==================================================
    # 🎨 STYLING
    # ==================================================
    title = (
        question.title()
        if question
        else "Business Analytics"
    )

    ax.set_title(
        title,
        fontsize=18,
        fontweight='bold',
        color="white",
        pad=20
    )

    # ==================================================
    # REMOVE MEANINGLESS AXIS LABELS
    # ==================================================
    if chart_type not in ["donut", "barh", "single"]:

        ax.set_ylabel(
            clean_label(y_key),
            fontsize=12,
            color=TEXT_COLOR
        )

    # ==================================================
    # GRID
    # ==================================================
    if chart_type not in ["single", "donut"]:

        ax.grid(
            alpha=0.12,
            linestyle='--',
            color=GRID_COLOR
        )

    ax.tick_params(
        colors=TEXT_COLOR
    )

    # ==================================================
    # X TICKS
    # ==================================================
    if chart_type not in ["barh", "single"]:

        plt.xticks(
            rotation=15,
            fontsize=10
        )

    if chart_type != "single":

        plt.yticks(
            fontsize=10
        )

    # ==================================================
    # REMOVE EXTRA BORDERS
    # ==================================================
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    # ==================================================
    # TIGHT LAYOUT
    # ==================================================
    plt.tight_layout()

    # ==================================================
    # SAVE
    # ==================================================
    if not os.path.exists("static"):
        os.makedirs("static")

    filename = f"{uuid.uuid4().hex}.png"

    path = os.path.join(
        "static",
        filename
    )

    plt.savefig(
        path,
        bbox_inches='tight',
        dpi=300,
        facecolor=fig.get_facecolor()
    )

    plt.close()

    return path, chart_type