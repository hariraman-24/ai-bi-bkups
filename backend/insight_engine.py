import pandas as pd
import math


class InsightEngine:

    # =====================================================
    # 🚫 IGNORE NON-BUSINESS COLUMNS
    # =====================================================
    IGNORE_COLUMNS = [
        "id",
        "customer_id",
        "employee_id",
        "product_id",
        "sale_id",
        "transaction_id",
        "invoice_id",
        "order_id",
        "serial_no",
        "index"
    ]

    # =====================================================
    # 📊 BUSINESS METRIC KEYWORDS
    # =====================================================
    BUSINESS_COLUMNS = [
        "sales",
        "revenue",
        "profit",
        "amount",
        "growth",
        "forecast",
        "performance",
        "expenses",
        "income",
        "quantity",
        "price",
        "total",
        "cost",
        "customers"
    ]

    # =====================================================
    # 📅 TIME SERIES KEYWORDS
    # =====================================================
    TIME_COLUMNS = [
        "date",
        "month",
        "year",
        "time",
        "quarter"
    ]

    # =====================================================
    # 🎯 MAIN INSIGHT ENGINE
    # =====================================================
    def generate_insight(self, result):

        # -------------------------------------------------
        # SAFETY
        # -------------------------------------------------
        if not result:
            return "No meaningful business data found."

        if isinstance(result, dict):
            result = [result]

        # -------------------------------------------------
        # DETECT NUMERIC BUSINESS COLUMNS
        # -------------------------------------------------
        numeric_keys = []

        for key in result[0]:

            lower = key.lower()

            # ---------------------------------------------
            # IGNORE TECHNICAL IDS
            # ---------------------------------------------
            if lower in self.IGNORE_COLUMNS:
                continue

            # ---------------------------------------------
            # ONLY BUSINESS METRICS
            # ---------------------------------------------
            if not any(
                word in lower
                for word in self.BUSINESS_COLUMNS
            ):
                continue

            try:

                float(result[0][key])

                numeric_keys.append(key)

            except:
                pass

        # -------------------------------------------------
        # TEXT COLUMNS
        # -------------------------------------------------
        text_keys = [
            k for k in result[0]
            if isinstance(result[0][k], str)
        ]

        # -------------------------------------------------
        # TIME SERIES DETECTION
        # -------------------------------------------------
        has_time_series = any(
            any(
                word in col.lower()
                for word in self.TIME_COLUMNS
            )
            for col in result[0]
        )

        # -------------------------------------------------
        # FALLBACK
        # -------------------------------------------------
        if not numeric_keys:

            return (
                "Business data analyzed successfully."
            )

        # -------------------------------------------------
        # PRIMARY METRIC
        # -------------------------------------------------
        num_key = numeric_keys[0]

        metric_name = (
            num_key
            .replace("_", " ")
            .title()
        )

        # -------------------------------------------------
        # NUMERIC VALUES
        # -------------------------------------------------
        values = []

        for row in result:

            try:

                values.append(
                    float(row[num_key])
                )

            except:
                continue

        if not values:

            return (
                "No meaningful business insights available."
            )

        # -------------------------------------------------
        # BASIC CALCULATIONS
        # -------------------------------------------------
        total = sum(values)

        avg = total / len(values)

        variance = sum(
            (x - avg) ** 2
            for x in values
        ) / len(values)

        std = math.sqrt(variance)

        all_equal = len(set(values)) == 1

        insights = []

        recommendations = []

        # =================================================
        # 🚀 BUSINESS INSIGHTS TITLE
        # =================================================
        insights.append(
            "🚀 Business Insights"
        )

        # =================================================
        # 📊 SMALL DATASET SAFETY
        # =================================================
        if len(values) < 3:

            insights.append(
                "Limited records are available for deeper business analysis."
            )

        # =================================================
        # 📊 STABLE PERFORMANCE
        # =================================================
        elif all_equal:

            insights.append(
                f"{metric_name} appears consistent across the analyzed records."
            )

            insights.append(
                "No major operational variations were identified in the dataset."
            )

        # =================================================
        # 📈 VARIATION ANALYSIS
        # =================================================
        else:

            # ---------------------------------------------
            # HIGH VARIATION
            # ---------------------------------------------
            if std > avg * 0.50:

                insights.append(
                    f"The dataset shows noticeable variation in {metric_name.lower()} across different business segments."
                )

            # ---------------------------------------------
            # MODERATE VARIATION
            # ---------------------------------------------
            elif std > avg * 0.20:

                insights.append(
                    f"Moderate variation is observed in {metric_name.lower()} across analyzed records."
                )

            # ---------------------------------------------
            # LOW VARIATION
            # ---------------------------------------------
            else:

                insights.append(
                    f"{metric_name} distribution appears relatively balanced across analyzed records."
                )

            # ---------------------------------------------
            # TOP CONTRIBUTOR
            # ---------------------------------------------
            if text_keys and len(values) >= 3:

                try:

                    text_key = text_keys[0]

                    top = max(
                        result,
                        key=lambda x: float(x[num_key])
                    )

                    top_name = str(
                        top[text_key]
                    )

                    contribution = (
                        float(top[num_key]) / total
                    ) * 100

                    # ONLY IF SIGNIFICANT
                    if contribution > 30:

                        insights.append(
                            f"{top_name} contributes a relatively higher share of overall {metric_name.lower()} compared to other analyzed segments."
                        )

                except:
                    pass

        # =================================================
        # 📈 TIME SERIES / TREND ANALYSIS
        # =================================================
        growth = 0

        if (
            has_time_series
            and len(values) >= 3
            and not all_equal
        ):

            first = values[0]

            last = values[-1]

            if first != 0:

                growth = (
                    (last - first) / first
                ) * 100

                # -----------------------------------------
                # POSITIVE TREND
                # -----------------------------------------
                if growth > 15:

                    insights.append(
                        f"The observed data suggests an upward trend in {metric_name.lower()} over the analyzed period."
                    )

                # -----------------------------------------
                # DECLINING TREND
                # -----------------------------------------
                elif growth < -15:

                    insights.append(
                        f"The dataset indicates a downward trend in {metric_name.lower()} over time."
                    )

                # -----------------------------------------
                # STABLE TREND
                # -----------------------------------------
                else:

                    insights.append(
                        f"{metric_name} appears relatively stable over the observed timeline."
                    )

        # =================================================
        # 📉 OUTLIER SAFETY
        # =================================================
        if (
            not all_equal
            and std < avg * 0.10
        ):

            insights.append(
                "No major performance outliers were identified in the analyzed dataset."
            )

        # =================================================
        # 🎯 RECOMMENDATIONS
        # =================================================
        recommendations.append(
            "Regular monitoring of business KPIs may help support better strategic planning and operational decision-making."
        )

        # -------------------------------------------------
        # HIGH VARIATION
        # -------------------------------------------------
        if (
            len(values) >= 3
            and std > avg * 0.50
        ):

            recommendations.append(
                "Certain business segments may benefit from additional operational attention to improve overall consistency."
            )

        # -------------------------------------------------
        # GROWTH OPPORTUNITY
        # -------------------------------------------------
        if growth > 15:

            recommendations.append(
                "Current business patterns may indicate potential opportunities for strategic expansion."
            )

        # -------------------------------------------------
        # DECLINING TREND
        # -------------------------------------------------
        elif growth < -15:

            recommendations.append(
                "Further investigation into declining trends may help identify operational or market-related challenges."
            )

        # -------------------------------------------------
        # TOP SEGMENT ANALYSIS
        # -------------------------------------------------
        if (
            text_keys
            and not all_equal
            and std > avg * 0.20
        ):

            try:

                recommendations.append(
                    f"Further analysis of high-performing segments such as {top_name} may provide useful strategic insights."
                )

            except:
                pass

        # =================================================
        # LIMIT INSIGHTS
        # =================================================
        insights = insights[:5]

        recommendations = recommendations[:3]

        # =================================================
        # APPEND RECOMMENDATIONS
        # =================================================
        insights.append("\n🎯 Recommendations")

        for rec in recommendations:

            insights.append(rec)

        # =================================================
        # FINAL OUTPUT
        # =================================================
        return "\n".join(insights)

    # =====================================================
    # 📄 CSV INSIGHT
    # =====================================================
    def csv_insight(self, file_path):

        df = pd.read_csv(file_path)

        return {
            "total_rows": len(df),
            "columns": list(df.columns),
            "sample_rows": df.head(5).to_dict(
                orient="records"
            )
        }

    # =====================================================
    # 📄 EXCEL INSIGHT
    # =====================================================
    def excel_insight(self, file_path):

        df = pd.read_excel(
            file_path,
            engine="openpyxl"
        )

        return {
            "total_rows": len(df),
            "columns": list(df.columns),
            "sample_rows": df.head(5).to_dict(
                orient="records"
            )
        }

    # =====================================================
    # 📄 PDF INSIGHT
    # =====================================================
    def pdf_insight(self, text):

        words = text.split()

        return {
            "total_words": len(words),
            "preview_text": text[:500]
        }