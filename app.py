import streamlit as st
from datetime import datetime
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


# =========================
# CẤU HÌNH TRANG
# =========================
st.set_page_config(
    page_title="Trà Sữa Bill",
    page_icon="🧋",
    layout="centered"
)


# =========================
# DỮ LIỆU SẢN PHẨM
# =========================
TRA_SUA = {
    "Trà sữa truyền thống": 30000,
    "Trà sữa matcha": 35000,
    "Trà sữa socola": 35000,
    "Trà sữa khoai môn": 38000,
    "Trà sữa dâu": 35000,
    "Trà sữa caramel": 38000
}

TOPPING = {
    "Trân châu đen": 7000,
    "Trân châu trắng": 7000,
    "Thạch trái cây": 6000,
    "Thạch phô mai": 8000,
    "Pudding trứng": 8000,
    "Kem cheese": 10000
}

MUC_DUONG = ["100%", "70%", "0%"]
MUC_DA = ["100%", "70%", "0%"]


# =========================
# CSS GIAO DIỆN
# =========================
st.markdown("""
<style>
    .main-title {
        text-align: center;
        font-size: 40px;
        font-weight: bold;
        color: #8B4513;
        margin-bottom: 5px;
    }

    .sub-title {
        text-align: center;
        color: #777;
        margin-bottom: 30px;
    }

    .total-box {
        background-color: #FFF3E6;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        margin-top: 20px;
        margin-bottom: 20px;
    }

    .total-price {
        font-size: 32px;
        font-weight: bold;
        color: #D35400;
    }

    .bill-title {
        font-size: 25px;
        font-weight: bold;
        color: #8B4513;
    }
</style>
""", unsafe_allow_html=True)


# =========================
# TIÊU ĐỀ
# =========================
st.markdown(
    '<div class="main-title">🧋 TRÀ SỮA BILL</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-title">Chọn món yêu thích và tạo hóa đơn của bạn</div>',
    unsafe_allow_html=True
)


# =========================
# NHẬP THÔNG TIN KHÁCH HÀNG
# =========================
st.subheader("👤 Thông tin khách hàng")

ten_khach = st.text_input(
    "Tên khách hàng",
    placeholder="Nhập tên khách hàng..."
)


# =========================
# CHỌN TRÀ SỮA
# =========================
st.subheader("🧋 Chọn trà sữa")

loai_tra = st.selectbox(
    "
