import pandas as pd
from prophet import Prophet


def forecast_sales(data):

    if not data or len(data) < 2:
        return {}

    df = pd.DataFrame(data)

    # ==============================
    # 🔥 SMALL DATA → SIMPLE TREND
    # ==============================
    if len(df) < 6:

        last = df.iloc[-1]["total_sales"]
        prev = df.iloc[-2]["total_sales"]

        growth = last - prev

        forecast_output = []

        last_month = int(df.iloc[-1]["month"])
        last_year = int(df.iloc[-1]["year"])

        for i in range(1, 4):
            next_val = last + (growth * i)

            month = last_month + i
            year = last_year

            # Handle year overflow
            if month > 12:
                month -= 12
                year += 1

            forecast_output.append({
                "year": year,
                "month": month,
                "forecast_sales": max(0, float(next_val))
            })

    else:
        # ==============================
        # 🔥 LARGE DATA → PROPHET
        # ==============================
        df["ds"] = pd.to_datetime(
            df["year"].astype(str) + "-" + df["month"].astype(str) + "-01"
        )

        df["y"] = df["total_sales"].astype(float)

        model = Prophet()
        model.fit(df[["ds", "y"]])

        # 🔥 FIX: Use Month Start for stability
        future = model.make_future_dataframe(periods=3, freq='MS')

        forecast = model.predict(future)

        # 🔥 FIX: REMOVE DUPLICATE LAST MONTH
        last_date = df["ds"].max()

        future_only = forecast[forecast["ds"] > last_date]

        result = future_only[["ds", "yhat"]].head(3)

        forecast_output = []

        last_actual = df["y"].iloc[-1]

        for _, row in result.iterrows():

            val = max(0, float(row["yhat"]))

            # ✅ Stability control
            if val < last_actual * 0.6:
                val = last_actual * 0.6
            if val > last_actual * 1.6:
                val = last_actual * 1.6

            forecast_output.append({
                "year": int(row["ds"].year),
                "month": int(row["ds"].month),
                "forecast_sales": round(val, 2)
            })

            last_actual = val

    # ==============================
    # 📉 INSIGHT CALCULATION
    # ==============================
    last_actual = data[-1]["total_sales"]
    first_forecast = forecast_output[0]["forecast_sales"]

    change = first_forecast - last_actual
    percent = (change / last_actual) * 100 if last_actual else 0

    trend = "increase" if percent > 0 else "decrease"
    abs_percent = abs(percent)

    # Risk / Stability message
    if abs_percent < 5:
        risk_msg = "This indicates a stable trend."
    elif abs_percent < 15:
        risk_msg = "This shows moderate variation. Monitoring is recommended."
    else:
        risk_msg = "This indicates high volatility. Growth may not be consistent."

    insight = f"""
Sales are expected to {trend} by {abs_percent:.2f}%.
Estimated change in revenue: {round(change, 2)}.
{risk_msg}
""".strip()

    return {
        "historical": data,
        "forecast": forecast_output,
        "insight": insight
    }