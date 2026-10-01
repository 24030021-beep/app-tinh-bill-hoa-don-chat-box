import streamlit as st
from datetime import datetime
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import unicodedata


# ==============================
# CẤU HÌNH TRANG
# ==============================
st.set_page_config(
    page_title="Tính Bill Trà Sữa",
    page_icon="🧋",
    layout="centered"
)


# ==============================
# DỮ LIỆU
# ==============================
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


# ==============================
# HÀM BỎ DẤU TIẾNG VIỆT
# Dùng cho file PDF để tránh lỗi font
# ==============================
def bo_dau(text):
    text = unicodedata.normalize("NFD", text)
    text = "".join(
        char for char in text
        if unicodedata.category(char) != "Mn"
    )
    return text.replace("đ", "d").replace("Đ", "D")


# ==============================
# CSS
# ==============================
st.markdown(
    """
    <style>
    .title {
        text-align: center;
        font-size: 40px;
        font-weight: bold;
        color: #8B4513;
    }

    .subtitle {
        text-align: center;
        color: #777777;
        margin-bottom: 30px;
    }

    .total {
        padding: 20px;
        background-color: #FFF2E2;
        border-radius: 15px;
        text-align: center;
        margin-top: 20px;
    }

    .total-text {
        font-size: 18px;
    }

    .total-money {
        font-size: 32px;
        font-weight: bold;
        color: #D35400;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# ==============================
# TIÊU ĐỀ
# ==============================
st.markdown(
    '<div class="title">🧋 TRÀ SỮA BILL</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Ứng dụng tính tiền hóa đơn trà sữa</div>',
    unsafe_allow_html=True
)


# ==============================
# THÔNG TIN KHÁCH HÀNG
# ==============================
st.header("👤 Thông tin khách hàng")

ten_khach = st.text_input(
    "Tên khách hàng",
    placeholder="Nhập tên khách hàng"
)


# ==============================
# CHỌN TRÀ SỮA
# ==============================
st.header("🧋 Chọn trà sữa")

loai_tra = st.selectbox(
    "Loại trà sữa",
    list(TRA_SUA.keys())
)

gia_tra = TRA_SUA[loai_tra]

so_luong = st.number_input(
    "Số lượng",
    min_value=1,
    max_value=20,
    value=1,
    step=1
)


# ==============================
# ĐƯỜNG + ĐÁ
# ==============================
col1, col2 = st.columns(2)

with col1:
    muc_duong = st.selectbox(
        "🍬 Mức độ đường",
        ["100%", "70%", "0%"]
    )

with col2:
    muc_da = st.selectbox(
        "🧊 Mức độ đá",
        ["100%", "70%", "0%"]
    )


# ==============================
# TOPPING
# ==============================
st.header("🍡 Topping")

topping_chon = st.multiselect(
    "Chọn topping",
    list(TOPPING.keys())
)


# ==============================
# TÍNH TIỀN
# ==============================
tong_tien_topping = 0

for topping in topping_chon:
    tong_tien_topping += TOPPING[topping]


don_gia = gia_tra + tong_tien_topping

thanh_tien = don_gia * so_luong


# ==============================
# HIỂN THỊ KẾT QUẢ
# ==============================
st.divider()

st.header("🧾 Chi tiết hóa đơn")

st.write("**Tên khách hàng:**", ten_khach if ten_khach else "Khách lẻ")
st.write("**Loại trà sữa:**", loai_tra)
st.write("**Số lượng:**", so_luong)
st.write("**Mức độ đường:**", muc_duong)
st.write("**Mức độ đá:**", muc_da)

if len(topping_chon) > 0:
    st.write("**Topping:**")
    for topping in topping_chon:
        st.write(
            f"- {topping}: {TOPPING[topping]:,} VNĐ"
        )
else:
    st.write("**Topping:** Không có")


# ==============================
# TỔNG TIỀN
# ==============================
st.markdown(
    f"""
    <div class="total">
        <div class="total-text">
            TỔNG SỐ TIỀN CẦN THANH TOÁN
        </div>
        <div class="total-money">
            {thanh_tien:,} VNĐ
        </div>
    </div>
    """,
    unsafe_allow_html=True
)


# ==============================
# TẠO FILE PDF
# ==============================
def tao_pdf():
    buffer = BytesIO()

    pdf = canvas.Canvas(buffer, pagesize=A4)

    width, height = A4

    y = height - 60

    # Tiêu đề
    pdf.setFont("Helvetica-Bold", 20)
    pdf.drawCentredString(
        width / 2,
        y,
        "HOA DON TRA SUA"
    )

    y -= 40

    pdf.setFont("Helvetica", 11)

    # Thông tin khách
    pdf.drawString(
        50,
        y,
        "Khach hang: " + bo_dau(
            ten_khach if ten_khach else "Khach le"
        )
    )

    y -= 20

    pdf.drawString(
        50,
        y,
        "Thoi gian: " +
        datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    )

    y -= 35

    # Thông tin sản phẩm
    pdf.setFont("Helvetica-Bold", 12)

    pdf.drawString(
        50,
        y,
        "THONG TIN MON"
    )

    y -= 25

    pdf.setFont("Helvetica", 11)

    pdf.drawString(
        50,
        y,
        "Tra sua: " + bo_dau(loai_tra)
    )

    y -= 20

    pdf.drawString(
        50,
        y,
        f"So luong: {so_luong}"
    )

    y -= 20

    pdf.drawString(
        50,
        y,
        f"Don gia: {gia_tra:,} VND"
    )

    y -= 20

    pdf.drawString(
        50,
        y,
        "Muc duong: " + muc_duong
    )

    y -= 20

    pdf.drawString(
        50,
        y,
        "Muc da: " + muc_da
    )

    y -= 30

    # Topping
    pdf.setFont("Helvetica-Bold", 12)

    pdf.drawString(
        50,
        y,
        "TOPPING"
    )

    y -= 20

    pdf.setFont("Helvetica", 11)

    if topping_chon:

        for topping in topping_chon:

            pdf.drawString(
                70,
                y,
                "- " +
                bo_dau(topping) +
                f": {TOPPING[topping]:,} VND"
            )

            y -= 20

    else:

        pdf.drawString(
            70,
            y,
            "- Khong co"
        )

        y -= 20

    y -= 20

    # Tổng tiền
    pdf.setFont("Helvetica-Bold", 15)

    pdf.drawString(
        50,
        y,
        f"TONG THANH TOAN: {thanh_tien:,} VND"
    )

    y -= 40

    pdf.setFont("Helvetica", 11)

    pdf.drawCentredString(
        width / 2,
        y,
        "Cam on ban da ung ho!"
    )

    pdf.save()

    buffer.seek(0)

    return buffer


# ==============================
# THANH TOÁN
# ==============================
st.divider()

if st.button(
    "💳 THANH TOÁN",
    use_container_width=True
):

    pdf_file = tao_pdf()

    st.success(
        f"Thanh toán thành công! Tổng tiền: {thanh_tien:,} VNĐ"
    )

    st.download_button(
        label="📄 Xuất hóa đơn",
        data=pdf_file,
        file_name="hoa_don_tra_sua.pdf",
        mime="application/pdf",
        use_container_width=True
    )
