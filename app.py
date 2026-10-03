import streamlit as st
st.image("logo.jpg")
# Cấu hình giao diện trang web
st.set_page_config(
    page_title="Ứng dụng Tính Lãi Tiết Kiệm_Phạm Hải Linh", page_icon="💰", layout="centered"
)

st.title("💰 Ứng dụng Tính Lãi Gửi Tiết Kiệm")
st.write(
    "Nhập thông tin khoản tiết kiệm của bạn bên dưới để tính toán tiền lãi chi"
    " tiết."
)

# Tạo form nhập liệu
with st.form("savings_form"):
    st.subheader("1. Thông tin khoản gửi")

    # Số tiền gửi
    principal = st.number_input(
        "Số tiền gửi (VNĐ)",
        min_value=1_000_000.0,
        value=100_000_000.0,
        step=1_000_000.0,
        format="%.0f",
        help="Nhập số tiền gốc bạn muốn gửi tiết kiệm.",
    )

    # Kỳ hạn
    col1, col2 = st.columns(2)
    with col1:
        term_value = st.number_input(
            "Kỳ hạn", min_value=1, value=12, step=1, help="Số lượng kỳ hạn"
        )
    with col2:
        term_unit = st.selectbox(
            "Đơn vị kỳ hạn", ["Tháng", "Năm"], index=0
        )

    # Lãi suất
    rate = st.number_input(
        "Lãi suất (% / năm)",
        min_value=0.0,
        max_value=100.0,
        value=6.0,
        step=0.1,
        help="Lãi suất quy đổi theo năm.",
    )

    st.subheader("2. Hình thức tính lãi")

    # Hình thức nhận lãi
    payment_method = st.selectbox(
        "Hình thức nhận lãi",
        ["Cuối kỳ", "Hàng tháng", "Hàng quý"],
        help=(
            "Nhận lãi cuối kỳ, hàng tháng hoặc hàng quý (áp dụng cho lãi đơn"
            " hoặc rút lãi định kỳ)."
        ),
    )

    # Chọn lãi đơn hay lãi kép
    interest_type = st.radio(
        "Loại lãi suất",
        ["Lãi đơn", "Lãi kép"],
        horizontal=True,
        help=(
            "Lãi đơn: Lãi không nhập gốc.\nLãi kép: Lãi nhập gốc định kỳ theo"
            " kỳ hạn ghép lãi."
        ),
    )

    # Nút tính toán
    submitted = st.form_submit_button("Tính toán")

# Xử lý tính toán khi người dùng bấm nút
if submitted:
    # Quy đổi kỳ hạn sang năm và tháng
    if term_unit == "Năm":
        total_months = term_value * 12
    else:
        total_months = term_value

    t_years = total_months / 12
    r_annual = rate / 100

    periodic_interest = 0
    total_interest = 0
    total_amount = 0

    if interest_type == "Lãi đơn":
        # Tổng tiền lãi = P * r * t (với t tính bằng năm)
        total_interest = principal * r_annual * t_years
        total_amount = principal + total_interest

        # Tiền lãi định kỳ
        if payment_method == "Hàng tháng":
            periodic_interest = principal * (r_annual / 12)
        elif payment_method == "Hàng quý":
            periodic_interest = principal * (r_annual / 4)
        else:  # Cuối kỳ
            periodic_interest = total_interest

    else:  # Lãi kép
        # Xác định tần suất ghép lãi dựa vào hình thức nhận lãi hoặc quy ước
        if payment_method == "Hàng tháng":
            n = 12
        elif payment_method == "Hàng quý":
            n = 4
        else:  # Cuối kỳ (mặc định ghép lãi hàng năm hoặc theo tháng, ở đây chuẩn hóa ghép lãi theo năm hoặc theo kỳ nhận)
            n = 12  # Thường tiết kiệm lãi kép tính ghép lãi hàng tháng

        # Công thức lãi kép: A = P * (1 + r/n)^(n * t_years)
        total_amount = principal * (1 + r_annual / n) ** (n * t_years)
        total_interest = total_amount - principal

        # Tiền lãi định kỳ (ước tính trung bình mỗi kỳ)
        if payment_method == "Hàng tháng":
            periodic_interest = total_interest / total_months
        elif payment_method == "Hàng quý":
            periodic_interest = total_interest / (total_months / 3)
        else:
            periodic_interest = total_interest

    # Hiển thị kết quả
    st.divider()
    st.subheader("📊 Kết quả tính toán")

    col_res1, col_res2, col_res3 = st.columns(3)

    with col_res1:
        if payment_method == "Cuối kỳ":
            st.metric(
                label="Tiền lãi định kỳ",
                value="N/A",
                delta="Nhận cuối kỳ",
            )
        else:
            st.metric(
                label=f"Tiền lãi ({payment_method.lower()})",
                value=f"{periodic_interest:,.0f} đ",
            )

    with col_res2:
        st.metric(
            label="Tổng tiền lãi nhận được",
            value=f"{total_interest:,.0f} đ",
            delta=f"+{rate}%/năm",
        )

    with col_res3:
        st.metric(
            label="Tổng tiền (Gốc + Lãi)",
            value=f"{total_amount:,.0f} đ",
        )

    # Hiển thị chi tiết tóm tắt dạng bảng chữ
    st.success(
        f"**Tóm tắt:** Gửi số tiền **{principal:,.0f} đ** với kỳ hạn **{term_value}"
        f" {term_unit.lower()}**, lãi suất **{rate}%/năm** ({interest_type}), hình"
        f" thức **{payment_method}**, bạn sẽ thu về tổng cộng **{total_amount:,.0f}"
        f" đ** (trong đó có **{total_interest:,.0f} đ** tiền lãi)."
    )
