import streamlit as st

# ============================================================
# CẤU HÌNH TRANG
# ============================================================
st.set_page_config(
    page_title="Dự Đoán Phản Ứng Hóa Học",
    page_icon="🧪",
    layout="centered"
)

# ============================================================
# INJECT CSS — LÀM ĐẸP GIAO DIỆN
# ============================================================
st.markdown("""
<style>
    /* Nền gradient toàn trang */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 100vh;
    }

    /* Ẩn header/footer mặc định của Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Container chính - card trắng */
    .block-container {
        background: #ffffff;
        padding: 2.5rem 2.5rem 2rem 2.5rem !important;
        border-radius: 20px;
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.3);
        max-width: 720px !important;
        margin-top: 2rem !important;
        margin-bottom: 2rem !important;
    }

    /* Tiêu đề */
    h1 {
        color: #2d3561 !important;
        text-align: center !important;
        font-size: 26px !important;
        font-weight: 800 !important;
        margin-bottom: 6px !important;
    }

    /* Subtitle */
    .subtitle {
        text-align: center;
        color: #777;
        font-size: 14px;
        margin-bottom: 24px;
        font-style: italic;
    }

    /* Box dãy hoạt động */
    .activity-box {
        background: #f5f7ff;
        border-left: 5px solid #667eea;
        padding: 16px 18px;
        border-radius: 10px;
        margin-bottom: 24px;
    }
    .activity-box h4 {
        color: #444;
        font-size: 15px;
        margin: 0 0 10px 0;
    }
    .series {
        display: flex;
        flex-wrap: wrap;
        gap: 6px;
        margin-bottom: 8px;
    }
    .series span {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: #fff;
        padding: 5px 11px;
        border-radius: 6px;
        font-weight: bold;
        font-size: 13px;
    }
    .series span.h {
        background: linear-gradient(135deg, #e74c3c, #c0392b);
    }
    .activity-note {
        font-size: 12px;
        color: #666;
        font-style: italic;
        margin: 6px 0 0 0;
    }

    /* Selectbox đẹp hơn */
    .stSelectbox label {
        font-weight: 600 !important;
        color: #444 !important;
        font-size: 14px !important;
    }
    .stSelectbox div[data-baseweb="select"] > div {
        border: 2px solid #e0e4f5 !important;
        border-radius: 10px !important;
        transition: 0.2s !important;
    }
    .stSelectbox div[data-baseweb="select"] > div:hover {
        border-color: #667eea !important;
    }

    /* Button */
    .stButton > button {
        background: linear-gradient(135deg, #667eea, #764ba2) !important;
        color: #fff !important;
        border: none !important;
        padding: 12px 24px !important;
        border-radius: 10px !important;
        font-size: 16px !important;
        font-weight: 700 !important;
        width: 100% !important;
        transition: 0.25s !important;
        margin-top: 10px !important;
    }
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 10px 22px rgba(102, 126, 234, 0.45) !important;
        color: #fff !important;
    }

    /* Alert đẹp hơn */
    div[data-testid="stAlert"] {
        border-radius: 10px !important;
        border-left-width: 5px !important;
        font-size: 15px !important;
        line-height: 1.6 !important;
    }

    /* Phương trình hóa học */
    .equation {
        font-family: 'Courier New', monospace;
        font-size: 18px;
        font-weight: bold;
        background: #f0f3ff;
        color: #2d3561;
        padding: 12px 18px;
        border-radius: 8px;
        display: inline-block;
        margin-top: 10px;
        border: 1px dashed #667eea;
    }

    /* Subheader kết quả */
    h3 {
        color: #2d3561 !important;
        margin-top: 16px !important;
        font-size: 18px !important;
    }
</style>
""", unsafe_allow_html=True)


# ============================================================
# DỮ LIỆU HÓA HỌC
# ============================================================
DAY_HOAT_DONG = ['K', 'Na', 'Ba', 'Ca', 'Mg', 'Al', 'Zn', 'Fe', 'Ni',
                 'Sn', 'Pb', 'H', 'Cu', 'Hg', 'Ag', 'Pt', 'Au']

# Kim loại phản ứng với nước ở nhiệt độ thường
PU_NUOC_THUONG = ['K', 'Na', 'Ba', 'Ca']

# Hóa trị khi tạo muối (đơn giản hóa)
HOA_TRI = {
    'K': 1, 'Na': 1, 'Ba': 2, 'Ca': 2,
    'Mg': 2, 'Al': 3, 'Zn': 2, 'Fe': 2,
    'Ni': 2, 'Sn': 2, 'Pb': 2,
    'Cu': 2, 'Hg': 2, 'Ag': 1
}
HOA_TRI_LA_MA = {1: 'I', 2: 'II', 3: 'III'}


# ============================================================
# HÀM TẠO PHƯƠNG TRÌNH HÓA HỌC
# ============================================================
def tao_phuong_trinh_axit(kl):
    """KL + HCl → Muối clorua + H2"""
    v = HOA_TRI.get(kl, 2)
    if v == 1:
        return f"{kl} + HCl → {kl}Cl + H₂↑"
    elif v == 2:
        return f"{kl} + 2HCl → {kl}Cl₂ + H₂↑"
    elif v == 3:
        return f"2{kl} + 6HCl → 2{kl}Cl₃ + 3H₂↑"


def tao_phuong_trinh_muoi(A, B):
    """A + B(NO3)n → A(NO3)m + B"""
    vA = HOA_TRI.get(A, 2)
    vB = HOA_TRI.get(B, 2)

    # Tạo công thức muối
    def muoi(kl, v):
        if v == 1:
            return f"{kl}NO₃"
        return f"{kl}(NO₃){v}"

    muoiA = muoi(A, vA)
    muoiB = muoi(B, vB)

    # Cân bằng: bội số chung
    coefA = vB
    coefB = vA

    left_A = f"{coefA}{A}" if coefA > 1 else A
    left_B = f"{coefB}{muoiB}" if coefB > 1 else muoiB
    right_A = f"{coefA}{muoiA}" if coefA > 1 else muoiA
    right_B = f"{coefB}{B}" if coefB > 1 else B

    return f"{left_A} + {left_B} → {right_A} + {right_B}↓"


def tao_phuong_trinh_nuoc(kl):
    """KL kiềm/kiềm thổ + H2O → Bazơ + H2"""
    v = HOA_TRI.get(kl, 1)
    if v == 1:
        return f"2{kl} + 2H₂O → 2{kl}OH + H₂↑"
    elif v == 2:
        return f"{kl} + 2H₂O → {kl}(OH)₂ + H₂↑"


# ============================================================
# GIAO DIỆN
# ============================================================
st.markdown('<h1>🧪 Công Cụ Dự Đoán Phản Ứng Kim Loại</h1>', unsafe_allow_html=True)
st.markdown(
    '<p class="subtitle">Dựa trên dãy hoạt động hóa học — Chương trình phổ thông</p>',
    unsafe_allow_html=True
)

# Hiển thị dãy hoạt động dạng badge đẹp
badges = "".join(
    f'<span class="h">{kl}</span>' if kl == 'H' else f'<span>{kl}</span>'
    for kl in DAY_HOAT_DONG
)
st.markdown(f"""
<div class="activity-box">
    <h4>📌 Dãy hoạt động hóa học của kim loại:</h4>
    <div class="series">{badges}</div>
    <p class="activity-note">
        Kim loại đứng trước (trừ K, Na, Ba, Ca) đẩy được kim loại đứng sau ra khỏi dung dịch muối.
        Kim loại đứng trước H đẩy được H ra khỏi axit loãng.
    </p>
</div>
""", unsafe_allow_html=True)


# ============================================================
# FORM NHẬP LIỆU
# ============================================================
col1, col2 = st.columns(2)

with col1:
    kim_loai_A = st.selectbox(
        "🔹 Chọn Kim loại (A):",
        DAY_HOAT_DONG[:-1],
        index=None,
        placeholder="-- Chọn kim loại --"
    )

with col2:
    loai_phan_ung = st.selectbox(
        "🔹 Chọn chất phản ứng cùng:",
        ["Nước (H₂O)", "Axit loãng (HCl, H₂SO₄ loãng)", "Dung dịch Muối"]
    )

kim_loai_trong_muoi = None
if loai_phan_ung == "Dung dịch Muối":
    danh_sach_muoi = [kl for kl in DAY_HOAT_DONG if kl != kim_loai_A and kl != 'H']
    kim_loai_trong_muoi = st.selectbox(
        "🔹 Chọn kim loại có trong dung dịch Muối (B):",
        danh_sach_muoi,
        index=None,
        placeholder="-- Chọn kim loại trong muối --"
    )


# ============================================================
# XỬ LÝ DỰ ĐOÁN
# ============================================================
if st.button("🔮 Dự đoán kết quả", use_container_width=True):

    # Kiểm tra đầu vào
    if not kim_loai_A:
        st.warning("⚠️ Vui lòng chọn kim loại A.")
        st.stop()
    if loai_phan_ung == "Dung dịch Muối" and not kim_loai_trong_muoi:
        st.warning("⚠️ Vui lòng chọn kim loại trong dung dịch muối B.")
        st.stop()

    idx_A = DAY_HOAT_DONG.index(kim_loai_A)
    idx_H = DAY_HOAT_DONG.index('H')

    st.markdown("### 🎯 Kết quả dự đoán:")

    # ---------- TRƯỜNG HỢP 1: NƯỚC ----------
    if loai_phan_ung == "Nước (H₂O)":
        if kim_loai_A in PU_NUOC_THUONG:
            pt = tao_phuong_trinh_nuoc(kim_loai_A)
            st.success(
                f"✅ **PHẢN ỨNG XẢY RA!**\n\n"
                f"**{kim_loai_A}** tan mạnh trong nước ở nhiệt độ thường, "
                f"tạo dung dịch kiềm và giải phóng khí H₂."
            )
            st.markdown(f'<div class="equation">{pt}</div>', unsafe_allow_html=True)

        elif kim_loai_A == 'Mg':
            st.warning(
                f"⚠️ **CHỈ PHẢN ỨNG VỚI NƯỚC NÓNG / HƠI NƯỚC**\n\n"
                f"**{kim_loai_A}** không phản ứng với nước ở nhiệt độ thường, "
                f"nhưng phản ứng khi đun nóng."
            )
        else:
            st.error(
                f"❌ **KHÔNG PHẢN ỨNG!**\n\n"
                f"**{kim_loai_A}** không phản ứng với nước ở nhiệt độ thường."
            )

    # ---------- TRƯỜNG HỢP 2: AXIT LOÃNG ----------
    elif loai_phan_ung == "Axit loãng (HCl, H₂SO₄ loãng)":
        if idx_A < idx_H:
            v = HOA_TRI.get(kim_loai_A, 2)
            hoa_tri_la_ma = HOA_TRI_LA_MA.get(v, '?')
            pt = tao_phuong_trinh_axit(kim_loai_A)

            canh_bao = ""
            if kim_loai_A == 'Pb':
                canh_bao = (
                    "\n\n⚠️ **Lưu ý:** Pb phản ứng **rất chậm** với HCl/H₂SO₄ loãng "
                    "vì muối tạo thành ít tan, bám lên bề mặt kim loại."
                )

            st.success(
                f"✅ **PHẢN ỨNG XẢY RA!**\n\n"
                f"**{kim_loai_A}** đứng trước H trong dãy hoạt động, "
                f"đẩy được H ra khỏi axit loãng.\n\n"
                f"**Sản phẩm:** Muối {kim_loai_A} (hóa trị **{hoa_tri_la_ma}**) + khí H₂↑"
                f"{canh_bao}"
            )
            st.markdown(f'<div class="equation">{pt}</div>', unsafe_allow_html=True)
        else:
            st.error(
                f"❌ **KHÔNG PHẢN ỨNG!**\n\n"
                f"**{kim_loai_A}** đứng sau H trong dãy hoạt động "
                f"nên không tác dụng với axit loãng."
            )

    # ---------- TRƯỜNG HỢP 3: DUNG DỊCH MUỐI ----------
    elif loai_phan_ung == "Dung dịch Muối":
        idx_B = DAY_HOAT_DONG.index(kim_loai_trong_muoi)

        if kim_loai_A in PU_NUOC_THUONG:
            st.warning(
                f"⚠️ **PHẢN ỨNG PHỨC TẠP — KHÔNG ĐƠN GIẢN!**\n\n"
                f"**{kim_loai_A}** là kim loại kiềm/kiềm thổ hoạt động rất mạnh. "
                f"Khi cho vào dung dịch muối, nó sẽ **phản ứng với NƯỚC trong dung dịch trước** "
                f"để tạo bazơ, chứ không đẩy trực tiếp **{kim_loai_trong_muoi}** ra ngoài."
            )

        elif idx_A < idx_B:
            pt = tao_phuong_trinh_muoi(kim_loai_A, kim_loai_trong_muoi)
            vA = HOA_TRI.get(kim_loai_A, 2)
            vB = HOA_TRI.get(kim_loai_trong_muoi, 2)

            st.success(
                f"✅ **PHẢN ỨNG XẢY RA!**\n\n"
                f"**{kim_loai_A}** đứng trước **{kim_loai_trong_muoi}** trong dãy hoạt động, "
                f"đủ mạnh để đẩy **{kim_loai_trong_muoi}** ra khỏi dung dịch muối.\n\n"
                f"**Sản phẩm:** Muối {kim_loai_A} (hóa trị {HOA_TRI_LA_MA.get(vA,'?')}) "
                f"+ kim loại {kim_loai_trong_muoi}↓ (hóa trị {HOA_TRI_LA_MA.get(vB,'?')})."
            )
            st.markdown(f'<div class="equation">{pt}</div>', unsafe_allow_html=True)
            st.caption("💡 Phương trình minh họa với gốc NO₃⁻. Với gốc khác (Cl⁻, SO₄²⁻...) sản phẩm tương tự.")

        else:
            st.error(
                f"❌ **KHÔNG PHẢN ỨNG!**\n\n"
                f"**{kim_loai_A}** hoạt động yếu hơn **{kim_loai_trong_muoi}** "
                f"nên không thể đẩy **{kim_loai_trong_muoi}** ra khỏi dung dịch muối."
            )


# ============================================================
# FOOTER
# ============================================================
st.markdown(
    '<p style="text-align:center;color:#aaa;font-size:12px;margin-top:30px;">'
    'Made with ❤️ — Nhóm 6'
    '</p>',
    unsafe_allow_html=True
)
