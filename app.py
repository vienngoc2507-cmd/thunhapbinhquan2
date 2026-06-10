import streamlit as st
import wbdata
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

st.set_page_config(
    page_title="GDP Bình Quân Đầu Người",
    page_icon="🌍"
)

st.title("🌍 GDP Bình Quân Đầu Người")

# Danh sách quốc gia
countries = {
    "Việt Nam": "VN",
    "Hoa Kỳ": "US",
    "Nhật Bản": "JP",
    "Trung Quốc": "CN",
    "Hàn Quốc": "KR",
    "Thái Lan": "TH",
    "Singapore": "SG",
    "Indonesia": "ID"
}

country_name = st.selectbox(
    "Chọn quốc gia",
    list(countries.keys())
)

country_code = countries[country_name]

indicator = {
    "NY.GDP.PCAP.CD": "GDP_PER_CAPITA"
}

try:
    df = wbdata.get_dataframe(
        indicator,
        country=country_code,
        date=(
            datetime(2000, 1, 1),
            datetime(2024, 12, 31)
        )
    )

    df = df.sort_index()

    if df.empty:
        st.warning("Không có dữ liệu cho quốc gia này.")
    else:

        st.subheader("📊 Bảng dữ liệu")
        st.dataframe(df)

        latest_value = df["GDP_PER_CAPITA"].dropna().iloc[-1]

        st.metric(
            label="GDP bình quân đầu người mới nhất",
            value=f"${latest_value:,.0f}"
        )

        fig, ax = plt.subplots(figsize=(10, 5))

        ax.plot(
            df.index,
            df["GDP_PER_CAPITA"],
            marker="o"
        )

        ax.set_title(
            f"GDP bình quân đầu người - {country_name}"
        )

        ax.set_xlabel("Năm")
        ax.set_ylabel("USD/người")

        ax.grid(True)

        plt.xticks(rotation=45)

        st.pyplot(fig)

except Exception as e:
    st.error(f"Lỗi: {e}")
