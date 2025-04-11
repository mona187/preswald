from preswald import connect, get_df, table, text, slider, text_input, plotly,image
import plotly.express as px

connect()

df = get_df("sample_csv")

if df.empty:
    text("⚠️ Dataset is empty.")
else:
    text("# 🌍 Welcome, Detective!")
    text("Explore global air quality monitoring across all countries. Uncover hidden pollution patterns using interactive dashboards and visual clues.")

    text("### Full AQI Dataset from All Countries")
    table(df, title="🔍 Full AQI Dataset Overview")

    threshold = slider("🎚️ Adjust AQI Threshold", min_val=0, max_val=500, default=100)
    filtered_df = df[df["aqi_value"] > threshold]

    text("### ⚙️ Filtered Cities Based on AQI Threshold")
    table(filtered_df, title=f"🌫️ Cities with AQI > {threshold}")

    if threshold > 300:
        text("🚨 Extreme pollution detected in these cities.")
    elif threshold < 50:
        text("🌱 Air quality looks clean — but are clues hiding here?")
    else:
        text("🕵️ Moderate zones — potential hidden patterns.")

    try:
        text("### 🗺️ Global Pollution Overview")
        agg_df = df.groupby("country_name")["aqi_value"].mean().reset_index()
        agg_df.rename(columns={"aqi_value": "avg_aqi"}, inplace=True)

        fig_map = px.choropleth(
            agg_df,
            locations="country_name",
            locationmode="country names",
            color="avg_aqi",
            color_continuous_scale="Reds",
            title="Average AQI by Country",
            labels={"country_name": "Country", "avg_aqi": "Avg AQI"},
        )
        plotly(fig_map)
        text(" This map reveals national averages. Use it to focus your investigation.")
    except Exception as e:
        text("Map error: " + str(e))

    try:
        text("### AQI vs PM2.5 Concentration")

        required_columns = ["pm2.5_aqi_value", "aqi_value", "aqi_category"]
        if all(col in df.columns for col in required_columns):
            df_clean = df[required_columns].dropna()

            fig_scatter = px.scatter(
                df_clean,
                x="pm2.5_aqi_value",
                y="aqi_value",
                color="aqi_category",
                title="AQI vs PM2.5",
                labels={
                    "pm2.5_aqi_value": "PM2.5 AQI Value",
                    "aqi_value": "Overall AQI",
                    "aqi_category": "AQI Category"
                },
            )
            plotly(fig_scatter)
            text(" This scatter plot shows how PM2.5 concentration relates to AQI, colored by category.")
        else:
            missing = [col for col in required_columns if col not in df.columns]
            text(f"⚠️ Missing column(s): {', '.join(missing)} — cannot render scatter plot.")
    except Exception as e:
        text(" Scatter plot error: " + str(e))

    text("### 🧠 Clue Challenge: What's Driving the AQI Spikes?")
    text("A) Rainfall levels")  
    text("B) Carbon Dioxide Emissions")  
    text("C) City Population Size")  
    text("D) Building Height")

    correct_letter = "B"

    guess_1 = text_input("🔍 Attempt 1 (A/B/C/D):").strip().upper()
    guess_2 = text_input("🔍 Attempt 2 (A/B/C/D):").strip().upper()
    guess_3 = text_input("🔍 Attempt 3 (A/B/C/D):").strip().upper()

    guesses = [guess_1, guess_2, guess_3]
    used = 0
    success = False

    for g in guesses:
        if g in ["A", "B", "C", "D"]:
            used += 1
            if g == correct_letter:
                success = True
                break

    if success:
        text(f"✅ Correct! You solved it in {used} guess{'es' if used > 1 else ''}. The culprit is Carbon Dioxide Emissions.")
    elif used == 3:
        text(f"❌ You’ve used all 3 guesses. The answer was **{correct_letter}) Carbon Dioxide Emissions**.")
    elif used > 0:
        text(f"🔁 You’ve used {used}/3 guesses. Keep going!")

    text(" Great work, detective. You’ve explored data, uncovered insights, and cracked the clue.")
