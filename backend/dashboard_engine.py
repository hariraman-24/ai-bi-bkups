from collections import defaultdict
import math


class DashboardEngine:

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
    # 📊 BUSINESS METRICS
    # =====================================================
    BUSINESS_COLUMNS = [
        "sales",
        "revenue",
        "profit",
        "amount",
        "cost",
        "expense",
        "income",
        "quantity",
        "price",
        "total",
        "customers"
    ]

    # =====================================================
    # 📅 TIME SERIES COLUMNS
    # =====================================================
    TIME_COLUMNS = [
        "date",
        "month",
        "year",
        "quarter",
        "time"
    ]

    # =====================================================
    # 🚀 MAIN DASHBOARD BUILDER
    # =====================================================
    def build_dashboard(self, data):

        if not data:

            return {
                "kpis": {},
                "insights": []
            }

        return {
            "kpis": self.generate_kpis(data),
            "insights": self.generate_insights(data)
        }

    # =====================================================
    # 📊 KPI ENGINE
    # =====================================================
    def generate_kpis(self, data):

        kpis = {}

        if not data:
            return kpis

        first_row = data[0]

        # -------------------------------------------------
        # TOTAL RECORDS
        # -------------------------------------------------
        kpis["Total Records"] = len(data)

        # -------------------------------------------------
        # BUSINESS NUMERIC COLUMNS ONLY
        # -------------------------------------------------
        for key, value in first_row.items():

            lower = key.lower()

            # ---------------------------------------------
            # IGNORE IDS
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

            # ---------------------------------------------
            # NUMERIC CHECK
            # ---------------------------------------------
            if not isinstance(value, (int, float)):
                continue

            values = []

            for row in data:

                try:
                    values.append(float(row[key]))
                except:
                    pass

            if not values:
                continue

            # ---------------------------------------------
            # KPI GENERATION
            # ---------------------------------------------
            total = sum(values)

            avg = total / len(values)

            max_val = max(values)

            min_val = min(values)

            metric_name = (
                key.replace("_", " ")
                .title()
            )

            # ---------------------------------------------
            # SMART KPI OUTPUT
            # ---------------------------------------------
            kpis[f"Total {metric_name}"] = round(total, 2)

            if len(values) > 1:

                kpis[f"Average {metric_name}"] = round(avg, 2)

                # Only meaningful ranges
                if max_val != min_val:

                    kpis[f"Highest {metric_name}"] = round(max_val, 2)

                    kpis[f"Lowest {metric_name}"] = round(min_val, 2)

        return kpis

    # =====================================================
    # 🧠 AI INSIGHTS ENGINE
    # =====================================================
    def generate_insights(self, data):

        insights = []

        if not data:
            return insights

        first_row = data[0]

        # -------------------------------------------------
        # DETECT BUSINESS NUMERIC COLUMNS
        # -------------------------------------------------
        numeric_keys = []

        for key, value in first_row.items():

            lower = key.lower()

            # ---------------------------------------------
            # IGNORE IDS
            # ---------------------------------------------
            if lower in self.IGNORE_COLUMNS:
                continue

            # ---------------------------------------------
            # BUSINESS ONLY
            # ---------------------------------------------
            if not any(
                word in lower
                for word in self.BUSINESS_COLUMNS
            ):
                continue

            # ---------------------------------------------
            # NUMERIC ONLY
            # ---------------------------------------------
            if isinstance(value, (int, float)):
                numeric_keys.append(key)

        # -------------------------------------------------
        # TEXT COLUMNS
        # -------------------------------------------------
        text_keys = [
            k for k, v in first_row.items()
            if isinstance(v, str)
        ]

        # -------------------------------------------------
        # TIME SERIES DETECTION
        # -------------------------------------------------
        has_time_series = any(
            any(
                t in col.lower()
                for t in self.TIME_COLUMNS
            )
            for col in first_row
        )

        # -------------------------------------------------
        # SAFETY
        # -------------------------------------------------
        if not numeric_keys:

            insights.append(
                "Business data analyzed successfully."
            )

            return insights

        # -------------------------------------------------
        # PRIMARY METRIC
        # -------------------------------------------------
        num_key = numeric_keys[0]

        metric_name = (
            num_key.replace("_", " ")
            .title()
        )

        values = []

        for row in data:

            try:
                values.append(float(row[num_key]))
            except:
                pass

        if not values:

            insights.append(
                "No meaningful business insights available."
            )

            return insights

        # -------------------------------------------------
        # BASIC STATS
        # -------------------------------------------------
        avg = sum(values) / len(values)

        variance = sum(
            (x - avg) ** 2
            for x in values
        ) / len(values)

        std = math.sqrt(variance)

        all_equal = len(set(values)) == 1

        # =================================================
        # 📊 STABILITY ANALYSIS
        # =================================================
        if all_equal:

            insights.append(
                f"{metric_name} remains consistent across the analyzed records."
            )

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
            # STABLE
            # ---------------------------------------------
            else:

                insights.append(
                    f"{metric_name} distribution appears relatively balanced across analyzed records."
                )

        # =================================================
        # 📈 TIME TREND ANALYSIS
        # =================================================
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
                        f"The observed data indicates a positive upward trend in {metric_name.lower()} over time."
                    )

                # -----------------------------------------
                # NEGATIVE TREND
                # -----------------------------------------
                elif growth < -15:

                    insights.append(
                        f"The analyzed records suggest a decline in {metric_name.lower()} over the observed period."
                    )

                # -----------------------------------------
                # STABLE TREND
                # -----------------------------------------
                else:

                    insights.append(
                        f"{metric_name} appears relatively stable throughout the analyzed timeline."
                    )

        # =================================================
        # 🏆 CONTRIBUTION ANALYSIS
        # =================================================
        if (
            text_keys
            and not all_equal
            and len(values) >= 3
        ):

            try:

                text_key = text_keys[0]

                top = max(
                    data,
                    key=lambda x: float(x.get(num_key, 0))
                )

                top_name = str(
                    top[text_key]
                )

                total = sum(values)

                contribution = (
                    float(top[num_key]) / total
                ) * 100

                if contribution > 30:

                    insights.append(
                        f"{top_name} contributes a relatively higher share of overall {metric_name.lower()} compared to other analyzed segments."
                    )

            except:
                pass

        # =================================================
        # 🛡️ OUTLIER SAFETY
        # =================================================
        if (
            not all_equal
            and std < avg * 0.10
        ):

            insights.append(
                "No major operational outliers were identified in the analyzed dataset."
            )

        # =================================================
        # LIMIT INSIGHTS
        # =================================================
        cleaned = []

        for item in insights:

            if item not in cleaned:
                cleaned.append(item)

        return cleaned[:4]