import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Menyiapkan sum_renters


def create_sum_renters_df(df):
    sum_renters_df = df.groupby(["date", "month"]).agg({
        "total_count": "sum"
    }).reset_index()
    return sum_renters_df


# Menyiapkan renters
def create_renters_df(df):
    renters_df = df.groupby(by='year')[
        ['registered', 'casual']].sum().reset_index()
    return renters_df


# Menyiapkan byseason_df
def create_byseason_df(df):
    byseason_df = df.groupby(by='season')[["total_count"]].sum().reset_index()
    return byseason_df


# Menyiapkan byweather_df
def create_byweather_df(df):
    byweather_df = df.groupby(by='weather')[
        ["total_count"]].sum().reset_index()
    return byweather_df


# Load Berkas all_df
all_df = pd.read_csv("/day_bikeshare_clean.csv")

# Mengurutkan DataFrame berdasarkan order_date
datetime_columns = ["date"]
all_df.sort_values(by="date", inplace=True)
all_df.reset_index(inplace=True)

for column in datetime_columns:
    all_df[column] = pd.to_datetime(all_df[column])


# Membuat Komponen Filter
min_date = all_df["date"].min()
max_date = all_df["date"].max()

with st.sidebar:
    # Menambahkan logo perusahaan
    st.image(
        "https://raw.githubusercontent.com/Dimskmn/dashboard/refs/heads/main/BikeShare.png")

# Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu', min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )
# Data yang difilter disimpan dalam main_df
main_df = all_df[(all_df["date"] >= str(start_date)) &
                 (all_df["date"] <= str(end_date))]

# Memanggil Helper Function untuk Visualisasi Data
sum_renters_df = create_sum_renters_df(main_df)
renters_df = create_renters_df(main_df)
byseason_df = create_byseason_df(main_df)
byweather_df = create_byweather_df(main_df)

# Melengkapi Dashboard

# Menambahkan Header
st.header('BikeShare Dashboard :bike:')

# Menampilkan Visualisasi Jumlah Order Harian
st.subheader('Jumlah Penyewa')

col1, col2, col3 = st.columns(3)

with col1:
    total_renters = sum_renters_df.total_count.sum()
    st.metric("Total Penyewa", value=total_renters)

with col2:
    total_registered = renters_df.registered.sum()
    st.metric("Penyewa Terdaftar", value=total_registered)

with col3:
    total_casual = renters_df.casual.sum()
    st.metric("Penyewa Casual", value=total_casual)


# Membuat Line Chart Trend Penyewa Sepeda
fig, ax = plt.subplots(figsize=(20, 10))
ax.plot(
    sum_renters_df["date"],
    sum_renters_df["total_count"],
    marker='o',
    linewidth=2,
    color="#6086e6"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)

st.pyplot(fig)


# Menampilkan Visualisasi Demografi Pelanggan by Season, Weaather
st.subheader("Customer Demographics")

col1, col2 = st.columns(2)

with col1:
    fig, ax = plt.subplots(figsize=(20, 10))

    sns.barplot(
        y="total_count",
        x="season",
        data=byseason_df.sort_values(by="total_count", ascending=False),
        palette="viridis",
        ax=ax
    )
    ax.set_title("Jumlah Penyewa Berdasarkan Musim", loc="center", fontsize=50)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis='x', labelsize=35)
    ax.tick_params(axis='y', labelsize=30)
    st.pyplot(fig)

with col2:
    fig, ax = plt.subplots(figsize=(20, 10))

    sns.barplot(
        y="total_count",
        x="weather",
        data=byweather_df.sort_values(by="weather", ascending=False),
        palette="viridis",
        ax=ax
    )
    ax.set_title("Jumlah Penyewa Berdasarkan Keadaan Cuaca",
                 loc="center", fontsize=50)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis='x', labelsize=35)
    ax.tick_params(axis='y', labelsize=30)
    st.pyplot(fig)
