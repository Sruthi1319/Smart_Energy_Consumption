# Smart Energy Consumption Dashboard

# 1. Import all the required libraries
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 2. Streamlit page setup
st.set_page_config(page_title="Smart Energy Dashboard", layout="wide")

# 3. Custom CSS for UI
st.markdown("""
<style>
    body {
        background-color: #f5f5f5;
    }
    .main {
        background-color: #ffffff;
        padding: 2rem;
        border-radius: 10px;
    }
    div[data-testid="metric-container"] {
        background-color: #E8F6F3;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0px;
        box-shadow: 0 0 10px rgba(0,0,0,0.05);
    }
    section[data-testid="stSidebar"] {
        background-color: #D6EAF8;
    }
</style>
""", unsafe_allow_html=True)

# 4. Load Dataset
df = pd.read_csv("energy_data_india_coYOUOMGWA.csv")

# 5. Title
st.title("⚡ Smart Energy Consumption Dashboard")

# 6. Sidebar Filters
st.sidebar.header("🔍 Filter Options")
region = st.sidebar.selectbox("Select Region", ["All"] + sorted(df["Region"].unique().tolist()))
if region != "All":
    df = df[df["Region"] == region]

# 7. Show Data
st.subheader("📋 Household Energy Consumption Overview")
st.write(df.head())

# 8. Key Metrics
avg_energy = df["Monthly_Energy_Consumption_kWh"].mean()
total_energy = df["Monthly_Energy_Consumption_kWh"].sum()

col1, col2 = st.columns(2)
col1.metric("Average Monthly Consumption (kWh)", f"{avg_energy:.2f}")
col2.metric("Total Energy Consumption (kWh)", f"{total_energy:.0f}")

# 9. Scatter Plot: Income vs Energy Consumption
st.subheader("📈 Income vs Energy Consumption")
fig1, ax1 = plt.subplots()
sns.scatterplot(data=df, x="Monthly_Income_INR", y="Monthly_Energy_Consumption_kWh", hue="Region", ax=ax1)
st.pyplot(fig1)

# 10. Bar Chart: Appliance vs Energy Consumption
st.subheader("🔌 Appliance Count vs Energy Consumption")
appliances = ["Appliance_AC", "Appliance_Fan", "Appliance_Light", "Fridge", "Washing_Machine", "EV_Charging"]
selected_appliance = st.selectbox("Select Appliance", appliances)
fig2, ax2 = plt.subplots()
sns.barplot(x=df[selected_appliance], y=df["Monthly_Energy_Consumption_kWh"], ax=ax2)
ax2.set_xlabel(f"No. of {selected_appliance.replace('_', ' ')}")
ax2.set_ylabel("Energy Consumption (kWh)")
st.pyplot(fig2)

# 11. Pie Chart: Region-wise household distribution
st.subheader("📊 Household Distribution by Region")
region_counts = df["Region"].value_counts()
fig3, ax3 = plt.subplots()
ax3.pie(region_counts, labels=region_counts.index, autopct='%1.1f%%', startangle=90)
ax3.axis("equal")
st.pyplot(fig3)

# 12. Bar Chart: Average consumption by region
st.subheader("🌍 Average Energy Consumption by Region")
region_avg = df.groupby("Region")["Monthly_Energy_Consumption_kWh"].mean().sort_values(ascending=False)
fig4, ax4 = plt.subplots()
region_avg.plot(kind='bar', color='teal', ax=ax4)
ax4.set_ylabel("Avg Monthly Consumption (kWh)")
st.pyplot(fig4)

# 13. Recommendations
st.subheader("💡 Smart Recommendations")
recommendations = []

for _, row in df.iterrows():
    if row["Monthly_Energy_Consumption_kWh"] > 250:
        message = f"Household ID {row['Household_ID']} - ⚠️ High usage! Recommend switching to solar and LED bulbs."
        recommendations.append(message)
        st.warning(message)
    elif row["EV_Charging"] == 1:
        message = f"Household ID {row['Household_ID']} - 🚗 Consider installing a separate EV meter for optimal billing."
        recommendations.append(message)
        st.info(message)

# 14. Download Recommendations
if recommendations:
    st.download_button(
        label="📥 Download Recommendations",
        data="\n".join(recommendations),
        file_name="recommendations.txt",
        mime="text/plain"
    )

# 15. Footer
st.markdown("---")
st.markdown("<p style='text-align:center;'>🚀 Built with ❤️ using Streamlit | <a href='https://github.com/yourusername/your-repo' target='_blank'>GitHub Repo</a></p>", unsafe_allow_html=True)
