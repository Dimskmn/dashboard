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
        ['casual', 'registered']].sum().reset_index()
    return renters_df


# Menyiapkan byseason_df
def create_byseason_df(df):
    byseason_df = df.groupby(by='season')[["total_count"]].sum().reset_index()
    return byseason_df


# Menyiapkan byweather_df
def create_byweather_df(df):
    byweather_df = df.groupby(by='weather')[
        'total_count'].sum()
    return byweather_df

# Weekly Users


def create_week_avg_df(df):
    df["week"] = df["date"].dt.strftime('%Y-%U')
    week_avg_df = df.groupby("week")["total_count"].mean().mean()
    return week_avg_df


# Load Berkas all_df
all_df = pd.read_csv("https://raw.githubusercontent.com/Dimskmn/dashboard/refs/heads/main/BikeShare/day_bikeshare_clean.csv")

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
    st.logo(
        "https://cdn.lyft.com/static/bikesharefe/logo/CapitalBikeshare-main.svg", size='large')

# Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu', min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date], format="DD/MM/YYYY"
    )
# Data yang difilter disimpan dalam main_df
    main_df = all_df[(all_df["date"] >= str(start_date)) &
                     (all_df["date"] <= str(end_date))]

# Memanggil Helper Function untuk Visualisasi Data
sum_renters_df = create_sum_renters_df(main_df)
renters_df = create_renters_df(main_df)
byseason_df = create_byseason_df(main_df)
byweather_df = create_byweather_df(main_df)
week_avg_df = create_week_avg_df(main_df)

# Melengkapi Dashboard

# Menambahkan Header
st.header('BikeShare Dashboard :biking_man:')

# Menampilkan Visualisasi Jumlah Order Harian
st.subheader('Daily Performance')

col1, col2, col3 = st.columns(3)

with col1:
    total_renters = sum_renters_df.total_count.sum()
    st.metric("Total Penyewa", value=total_renters)

with col2:
    total_renters = renters_df.registered.sum()
    st.metric("Total Penyewa Terdaftar", value=total_renters)

with col3:
    total_renters = renters_df.casual.sum()
    st.metric("Total Penyewa Casual", value=total_renters)


# Membuat Line Chart Trend Penyewa Sepeda
fig, ax = plt.subplots(figsize=(20, 10))

ax.plot(
    sum_renters_df["date"],
    sum_renters_df["total_count"],
    marker='o',
    linewidth=2,
    color="#BA3B3D"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)

st.pyplot(fig)


col1, col2 = st.columns(2)
# Menampilkan Visualisasi Demografi Pelanggan by Season
with col1:
    st.subheader("Performance by Season")

    fig, ax = plt.subplots(figsize=(20, 10))
    sns.barplot(
        y="total_count",
        x="season",
        data=byseason_df.sort_values(by="total_count", ascending=False),
        palette=["#BA3B3D", "#D3D3D3",  "#D3D3D3",  "#D3D3D3"],
        ax=ax
    )
    ax.set_title("Numbers of Customer by Season (million)",
                 fontsize=40, loc="center")
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis='x', labelsize=35)
    ax.tick_params(axis='y', labelsize=30)
    st.pyplot(fig)

# Menampilkan Visualisasi Demografi Pelanggan by Weather
with col2:
    st.subheader("Performance by Weather")

    # Buat Pie Chart
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.pie(
        byweather_df,
        labels=byweather_df.index,
        autopct='%1.1f%%',
        colors=["#BA3B3D", "#fcffa4",  "#D3D3D3"],
        startangle=90,
        # wedgeprops={'edgecolor': 'black'}
    )

    ax.set_title("Numbers of Customer by Weather)", fontsize=13)

    # Tampilkan chart di Streamlit
    st.pyplot(fig)

# Menampilkan Visualisasi Perbandingan Penyewa Dalam beberapa tahun terakhir
st.subheader("User Type Comparison")

renters_df = renters_df.melt(
    id_vars='year', var_name='User Type', value_name='Count')
fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(data=renters_df, x='year', y='Count',
            hue='User Type', palette=["#fcffa4", "#BA3B3D"])

ax.set_title("Numbers of User Type (million)", fontsize=15)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis='x', labelsize=20)
ax.tick_params(axis='y', labelsize=15)
st.pyplot(fig)


# Clutering Usage Category
# Buat kategori berdasarkan quantile (binning)
all_df['usage category'] = pd.qcut(all_df['total_count'], q=3, labels=[
                                   'Casual Days', 'Occasional Days', 'Frequent Days'])

# Menampilkan Visualisasi Parameter RFM (Recency, Frequency, Monetary)
st.subheader("Clustering Based on Usage Category")

col1, col2, col3 = st.columns(3)

with col1:
    avg_registered = round(
        all_df["registered"].mean(), 1)
    st.metric("Average Registered User", value=int(avg_registered))

with col2:
    avg_casual = round(all_df["casual"].mean(), 1)
    st.metric("Average Casual User", value=int(avg_casual))

with col3:
    st.metric("Average Weekly User", value=int(week_avg_df))


# Distribusi Pelanggan Terdaftar
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(30, 10))
colors = ["#D3D3D3", "#fcffa4", "#BA3B3D"]
sns.boxplot(x='usage category', y='registered',
            data=all_df, palette=colors, ax=ax[0])
plt.tight_layout()
ax[0].set_ylabel(None)
ax[0].set_xlabel(None)
ax[0].tick_params(axis='x', labelsize=30)
ax[0].tick_params(axis='y', labelsize=30)
ax[0].set_title("Registered User Distribution by Usage Category", fontsize=30)

# Distribusi pelanggan casual
sns.boxplot(x='usage category', y='casual',
            data=all_df, palette=colors, ax=ax[1])
plt.tight_layout()
ax[1].set_ylabel(None)
ax[1].set_xlabel(None)
ax[1].invert_xaxis()
ax[1].yaxis.tick_right()
ax[1].yaxis.set_label_position('right')
ax[1].tick_params(axis='x', labelsize=30)
ax[1].tick_params(axis='y', labelsize=30)
ax[1].set_title("Casual User Distribution by Usage Category", fontsize=30)
st.pyplot(fig)

# Pola Penyewaan Customer dalam satu minggu
fig, ax = plt.subplots(figsize=(10, 5))
sns.countplot(x='weekday', hue='usage category', data=all_df,
              palette=["#fcffa4", "#ed6925", "#BA3B3D"])
ax.set_title("Customer Pattern by Usage Category in a week")
plt.tight_layout()
ax.legend(title="usage category", loc="lower right")
ax.set_xlabel(None)
ax.set_ylabel("Count")
st.pyplot(fig)
