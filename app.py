import streamlit as st
import numpy as np
import plotly.graph_objects as go

# ==============================================================================
# 1. CẤU HÌNH HỆ THỐNG & ĐỊNH NỀN KỸ THUẬT (SYSTEM & THEME OVERRIDE)
# ==============================================================================
st.set_page_config(
    page_title="Hệ thống mô phỏng khảo sát Cell-Free Massive MIMO cho 6G| Nhóm 08",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Khóa chặt theme sáng, triệt tiêu lỗi nút đen, nhúng font công nghệ
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@500;600&family=Space+Grotesk:wght@600;700;800&display=swap');

    /* Nền Technical Dot-Grid Blueprint */
    .stApp {
        background-color: #f8fafc !important;
        background-image: radial-gradient(#94a3b8 1.1px, transparent 1.1px) !important;
        background-size: 22px 22px !important;
        color: #0f172a !important;
        font-family: 'Inter', sans-serif !important;
    }

    h1, h2, h3 {
        font-family: 'Space Grotesk', sans-serif !important;
        color: #0f172a !important;
        letter-spacing: -0.02em !important;
    }

    /* Telemetry Header */
    .telemetry-bar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background: #ffffff !important;
        border: 1px solid #cbd5e1 !important;
        padding: 6px 16px !important;
        border-radius: 20px !important;
        font-size: 0.8rem !important;
        color: #334155 !important;
        font-family: 'JetBrains Mono', monospace !important;
        margin-bottom: 12px !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.03) !important;
    }
    .status-dot {
        display: inline-block;
        width: 8px;
        height: 8px;
        background-color: #10b981;
        border-radius: 50%;
        margin-right: 6px;
        box-shadow: 0 0 6px #10b981;
    }

    /* Ép buộc màu nút bấm: Nền trắng, viền rõ, chữ than chì tương phản cao */
    .stButton>button {
        background-color: #ffffff !important;
        color: #0f172a !important;
        border: 1.5px solid #cbd5e1 !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        font-family: 'Space Grotesk', sans-serif !important;
        font-size: 0.9rem !important;
        padding: 8px 16px !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.03) !important;
        transition: all 0.2s ease-in-out !important;
    }
    .stButton>button:hover {
        background-color: #f0f9ff !important;
        border-color: #0284c7 !important;
        color: #0284c7 !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 10px rgba(2, 132, 199, 0.15) !important;
    }

    /* Nút chính / Active: Gradient Xanh Lam Viễn Thông */
    .stButton>button[kind="primary"] {
        background: linear-gradient(135deg, #0284c7 0%, #2563eb 100%) !important;
        color: #ffffff !important;
        border: none !important;
        box-shadow: 0 4px 12px rgba(2, 132, 199, 0.3) !important;
    }
    .stButton>button[kind="primary"]:hover {
        background: linear-gradient(135deg, #0369a1 0%, #1d4ed8 100%) !important;
        color: #ffffff !important;
        box-shadow: 0 6px 16px rgba(2, 132, 199, 0.45) !important;
    }

    /* Khung Selectbox & Input */
    div[data-baseweb="select"] > div,
    div[data-baseweb="input"] > div {
        background-color: #ffffff !important;
        border: 1.5px solid #cbd5e1 !important;
        border-radius: 8px !important;
        color: #0f172a !important;
    }
    div[data-baseweb="select"] * {
        color: #0f172a !important;
        font-family: 'JetBrains Mono', monospace !important;
    }

    /* Thẻ Insight học thuật dạng gạch đầu dòng */
    .insight-card {
        background: #ffffff !important;
        border: 1px solid #e2e8f0 !important;
        border-left: 4px solid #0284c7 !important;
        border-radius: 10px !important;
        padding: 10px 16px !important;
        margin-top: 10px !important;
        color: #334155 !important;
        font-size: 0.9rem !important;
        box-shadow: 0 2px 5px rgba(0,0,0,0.03) !important;
    }

    /* Thẻ Preset */
    .preset-container {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 10px 14px;
        margin-bottom: 12px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02);
    }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 2. KHỞI TẠO BIẾN TRẠNG THÁI (SESSION STATE)
# ==============================================================================
if 'page' not in st.session_state: st.session_state.page = 'home'
if 'M' not in st.session_state: st.session_state.M = 100
if 'K' not in st.session_state: st.session_state.K = 20
if 'L' not in st.session_state: st.session_state.L = 1000
if 'Pt' not in st.session_state: st.session_state.Pt = 23
if 'sim_seed' not in st.session_state: st.session_state.sim_seed = 42
if 'view_mode' not in st.session_state: st.session_state.view_mode = 'map'
if 'selected_ue' not in st.session_state: st.session_state.selected_ue = 0

def switch_page(target):
    st.session_state.page = target

# ==============================================================================
# 3. LÕI TÍNH TOÁN TOÁN HỌC & JAIN'S FAIRNESS INDEX
# ==============================================================================
@st.cache_data(show_spinner=False)
def run_cf_simulation(M, K, L, Pt_dBm, seed):
    np.random.seed(seed)
    ap_c = np.random.uniform(0, L, (M, 2))
    ue_c = np.random.uniform(0, L, (K, 2))
    ap_cell = np.full((M, 2), [L/2, L/2])
    
    def compute_fading(aps):
        d = np.zeros((M, K))
        for m in range(M):
            for k in range(K):
                d[m, k] = max(np.linalg.norm(aps[m] - ue_c[k]), 10.0)
        PL = 128.1 + 37.6 * np.log10(d / 1000.0)
        shadowing = np.random.normal(0, 8.0, (M, K))
        return 10.0 ** ((-PL + shadowing) / 10.0), d

    beta_cf, dist_cf = compute_fading(ap_c)
    beta_cell, _ = compute_fading(ap_cell)
    
    Pt_w = (10.0 ** (Pt_dBm / 10.0)) / 1000.0
    noise_w = (10.0 ** (-100.0 / 10.0)) / 1000.0
    
    def calculate_metrics(beta):
        rates = np.zeros(K)
        sinr_arr = np.zeros(K)
        for k in range(K):
            sig = (np.sum(beta[:, k])) ** 2
            intf = sum(np.sum(beta[:, k] * beta[:, i]) for i in range(K) if i != k)
            n_pwr = (noise_w / Pt_w) * np.sum(beta[:, k])
            sinr = sig / (intf + n_pwr + 1e-15)
            sinr_arr[k] = sinr
            rates[k] = np.log2(1.0 + sinr)
        
        jain_index = (np.sum(rates) ** 2) / (K * np.sum(rates ** 2) + 1e-15)
        return rates, sinr_arr, jain_index

    rates_cf, sinr_cf, jain_cf = calculate_metrics(beta_cf)
    rates_cell, sinr_cell, jain_cell = calculate_metrics(beta_cell)
    
    return ap_c, ue_c, beta_cf, dist_cf, rates_cf, rates_cell, sinr_cf, sinr_cell, jain_cf, jain_cell

# ==============================================================================
# 4. SIDEBAR CẨM NĂNG & MÃ QR MOBILE
# ==============================================================================
with st.sidebar:
    st.markdown("<h2 style='text-align: center; color: #0284c7; margin-bottom: 0;'>📡 NHÓM 08 </h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 0.82rem; color: #64748b; margin-top: 2px;'>BAN CÔNG NGHỆ - CHIẾN LƯỢC</p>", unsafe_allow_html=True)
    st.markdown("---")
    
    st.markdown("##### 👥 Kỹ Sư Thực Hiện:")
    st.markdown("  **Đặng Đình Khôi**  \n  **Trần Quốc Lãm**  \n  **Trần Tuấn Kiệt**  \n  **Nguyễn Phương Nhi**  \n  **Nguyễn Thị Nhiều**")
    
    st.markdown("---")
    st.markdown("##### 🎯 Đề Tài: Khảo sát Cell-Free Massive MIMO cho 6G")
    st.caption("Khảo sát kiến trúc Cell-Free Massive MIMO: Distributed AP, User-Centric Serving, Macro-Diversity & Fairness.")
    
    st.markdown("##### 📱 Quét QR để trải nghiệm trên Mobile")
    web_url = "https://n8thongtindidonggk-jtfw3us2u2uv6mqukunczo.streamlit.app/"  # Dán link Cloud của bạn vào đây
    qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=200x200&data={web_url}"
    st.image(qr_url, caption=web_url, use_container_width=True)

# Telemetry Tag cố định ở đầu trang
st.markdown("""
<div class="telemetry-bar">
    <div><span class="status-dot"></span><b>ONLINE</b> | HỆ THỐNG MÔ PHỎNG MẠNG 6G CELL-FREE MASSIVE MIMO</div>
    <div>SÓNG MANG: <b>3.5 GHz (TDD)</b> | NHÓM THỰC HIỆN: <b>08</b></div>
</div>
""", unsafe_allow_html=True)

# ==============================================================================
# TRANG 1: MÀN HÌNH CHÍNH (HERO LANDING PAGE)
# ==============================================================================
if st.session_state.page == 'home':
    st.markdown("<br>", unsafe_allow_html=True)
    _, col_hero, _ = st.columns([1, 8, 1])
    with col_hero:
        st.markdown("<h1 style='text-align: center; font-size: 3.1rem; font-weight: 800; line-height: 1.15;'>HỆ THỐNG MÔ PHỎNG MẠNG<br><span style='color: #0284c7;'>6G CELL-FREE MASSIVE MIMO</span></h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; font-size: 1.15rem; color: #64748b; margin-top: 15px; margin-bottom: 35px;'>Phân tích kiến trúc phục vụ lấy người dùng làm trung tâm và hiệu ứng phân tập vĩ mô</p>", unsafe_allow_html=True)
        
        _, col_btn, _ = st.columns([1, 1.3, 1])
        with col_btn:
            if st.button("🚀 BẮT ĐẦU CẤU HÌNH HỆ THỐNG", type="primary", use_container_width=True):
                switch_page('settings')
                st.rerun()

# ==============================================================================
# TRANG 2: BÀN ĐIỀU KHIỂN THAM SỐ (SETTINGS DESK)
# ==============================================================================
elif st.session_state.page == 'settings':
    st.markdown("<h2 style='text-align: center; margin-bottom: 2px;'>⚙️ Bàn Điều Khiển Tham Số Mạng</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #64748b; margin-bottom: 15px; font-size: 0.95rem;'>Tùy chọn kịch bản dựng sẵn hoặc tinh chỉnh cấu hình kiểm thử</p>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class="preset-container">
        <p style="font-size: 0.85rem; font-weight: 700; color: #475569; margin-bottom: 8px; letter-spacing: 0.03em;">
            ⚡ KỊCH BẢN THỬ NGHIỆM NHANH (PRESET SCENARIOS):
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    p1, p2, p3 = st.columns(3)
    with p1:
        if st.button("📌 Tiêu Chuẩn Giữa Kỳ\n(M=100, K=20)", use_container_width=True):
            st.session_state.M, st.session_state.K, st.session_state.L, st.session_state.Pt = 100, 20, 1000, 23
            st.rerun()
    with p2:
        if st.button("🏙️ Tải Cao Đô Thị\n(M=150, K=40)", use_container_width=True):
            st.session_state.M, st.session_state.K, st.session_state.L, st.session_state.Pt = 150, 40, 800, 23
            st.rerun()
    with p3:
        if st.button("🌾 Thưa Thớt Ngoại Ô\n(M=40, K=10)", use_container_width=True):
            st.session_state.M, st.session_state.K, st.session_state.L, st.session_state.Pt = 40, 10, 1500, 30
            st.rerun()

    c_ap, _, c_ue = st.columns([1, 0.06, 1])
    with c_ap:
        st.markdown("#### 📡 Hạ tầng Điểm truy cập (AP)")
        st.session_state.M = st.slider("Mật độ AP phân tán (M)", 20, 200, value=st.session_state.M, step=10)
        st.session_state.L = st.number_input("Kích thước bản đồ (mét)", 500, 2000, value=st.session_state.L, step=100)
    with c_ue:
        st.markdown("#### 📱 Thiết bị Người dùng (UE)")
        st.session_state.K = st.slider("Số lượng người dùng đồng thời (K)", 5, 50, value=st.session_state.K, step=1)
        st.session_state.Pt = st.number_input("Công suất phát AP (dBm)", 10, 40, value=st.session_state.Pt, step=1)

    st.markdown("<br>", unsafe_allow_html=True)
    _, col_run, _ = st.columns([1, 1.4, 1])
    with col_run:
        if st.button("⚡ KHỞI CHẠY GIẢI TÍCH & XUẤT KẾT QUẢ", type="primary", use_container_width=True):
            switch_page('results')
            st.rerun()

# ==============================================================================
# TRANG 3: BÁO CÁO KẾT QUẢ & PHÂN TÍCH (ZERO SCROLL RESULTS LAB)
# ==============================================================================
elif st.session_state.page == 'results':
    
    ap_c, ue_c, beta_cf, dist_cf, rates_cf, rates_cell, sinr_cf, sinr_cell, jain_cf, jain_cell = run_cf_simulation(
        st.session_state.M, st.session_state.K, st.session_state.L, st.session_state.Pt, st.session_state.sim_seed
    )
    
    nav1, nav2, nav_reroll = st.columns([1, 1, 0.8])
    with nav1:
        if st.button("📍 XEM BẢN ĐỒ & BÚP SÓNG", type="primary" if st.session_state.view_mode == 'map' else "secondary", use_container_width=True):
            st.session_state.view_mode = 'map'
            st.rerun()
    with nav2:
        if st.button("📈 XEM ĐỒ THỊ TỐC ĐỘ (CDF)", type="primary" if st.session_state.view_mode == 'chart' else "secondary", use_container_width=True):
            st.session_state.view_mode = 'chart'
            st.rerun()
    with nav_reroll:
        if st.button("🎲 Sinh Tọa Độ Mới (Re-roll)", use_container_width=True):
            st.session_state.sim_seed = int(np.random.randint(1, 999999))
            st.rerun()

    # --------------------------------------------------------------------------
    # CHẾ ĐỘ 1: BẢN ĐỒ KHÔNG GIAN & BEAMFORMING ĐỘNG
    # --------------------------------------------------------------------------
    if st.session_state.view_mode == 'map':
        head_col, select_col = st.columns([2.2, 1])
        with head_col:
            st.markdown(f"<h3 style='margin-bottom:0;'>📍 Bản Đồ Vùng Phủ Không Gian ({st.session_state.M} APs / {st.session_state.K} UEs)</h3>", unsafe_allow_html=True)
        with select_col:
            ue_opts = [f"UE #{i+1}" for i in range(st.session_state.K)]
            selected_str = st.selectbox("Chọn UE khảo sát:", ue_opts, index=st.session_state.selected_ue, label_visibility="collapsed")
            st.session_state.selected_ue = int(selected_str.split('#')[1]) - 1

        k_idx = st.session_state.selected_ue
        top_serving_aps = np.argsort(beta_cf[:, k_idx])[-3:]
        min_dist = np.min(dist_cf[:, k_idx])
        ue_sinr_db = 10 * np.log10(sinr_cf[k_idx] + 1e-15)

        fig_map = go.Figure()

        # Tia Beamforming nét đứt
        for ap_idx in top_serving_aps:
            fig_map.add_trace(go.Scatter(
                x=[ap_c[ap_idx, 0], ue_c[k_idx, 0]],
                y=[ap_c[ap_idx, 1], ue_c[k_idx, 1]],
                mode='lines',
                line=dict(color='#0284c7', width=2, dash='dash'),
                hoverinfo='skip',
                showlegend=False
            ))

        # AP thông thường
        other_aps = [i for i in range(st.session_state.M) if i not in top_serving_aps]
        fig_map.add_trace(go.Scatter(
            x=ap_c[other_aps, 0], y=ap_c[other_aps, 1],
            mode='markers',
            marker=dict(symbol='triangle-up', size=9, color='#f87171', opacity=0.45),
            name='AP Phân tán',
            hovertemplate='<b>AP #%{text}</b><br>Tọa độ: (%{x:.1f}m, %{y:.1f}m)<extra></extra>',
            text=[str(i+1) for i in other_aps]
        ))

        # Cụm AP phục vụ (Màu vàng hổ phách)
        fig_map.add_trace(go.Scatter(
            x=ap_c[top_serving_aps, 0], y=ap_c[top_serving_aps, 1],
            mode='markers+text',
            marker=dict(symbol='triangle-up', size=15, color='#eab308', line=dict(color='#0f172a', width=1.5)),
            name='Cụm AP Phục Vụ (Serving)',
            text=[f"AP #{i+1}" for i in top_serving_aps],
            textposition="bottom center",
            textfont=dict(size=10, color='#b45309'),
            hovertemplate='<b>AP Phục vụ #%{text}</b><extra></extra>'
        ))

        # UE thông thường
        other_ues = [i for i in range(st.session_state.K) if i != k_idx]
        fig_map.add_trace(go.Scatter(
            x=ue_c[other_ues, 0], y=ue_c[other_ues, 1],
            mode='markers',
            marker=dict(symbol='circle', size=8, color='#94a3b8', opacity=0.6),
            name='UE Khác',
            hovertemplate='<b>UE #%{text}</b><br>Tốc độ: %{customdata:.2f} bps/Hz<extra></extra>',
            text=[str(i+1) for i in other_ues],
            customdata=rates_cf[other_ues]
        ))

        # UE khảo sát
        fig_map.add_trace(go.Scatter(
            x=[ue_c[k_idx, 0]], y=[ue_c[k_idx, 1]],
            mode='markers+text',
            marker=dict(symbol='circle', size=16, color='#0284c7', line=dict(color='#ffffff', width=2.5)),
            name=f'UE #{k_idx+1}',
            text=[f"UE #{k_idx+1}"],
            textposition="top center",
            textfont=dict(size=11, color='#0284c7'),
            hovertemplate=f'<b>UE #{k_idx+1}</b><br>Tốc độ: {rates_cf[k_idx]:.2f} bps/Hz<extra></extra>'
        ))

        # Cấu hình chuẩn cho Plotly mới (tránh lỗi titlefont)
        fig_map.update_layout(
            template='plotly_white',
            paper_bgcolor='white',
            plot_bgcolor='white',
            height=390,
            margin=dict(l=15, r=15, t=15, b=15),
            xaxis=dict(
                title=dict(text="Tọa độ X (mét)", font=dict(color="#0f172a")),
                showgrid=True,
                gridcolor='#f1f5f9',
                zeroline=False,
                linecolor='#cbd5e1',
                mirror=True,
                range=[-15, st.session_state.L + 15]
            ),
            yaxis=dict(
                title=dict(text="Tọa độ Y (mét)", font=dict(color="#0f172a")),
                showgrid=True,
                gridcolor='#f1f5f9',
                zeroline=False,
                linecolor='#cbd5e1',
                mirror=True,
                range=[-15, st.session_state.L + 15]
            ),
            legend=dict(
                yanchor="top",
                y=0.99,
                xanchor="left",
                x=0.01,
                bgcolor="rgba(255, 255, 255, 0.95)",
                bordercolor="#cbd5e1",
                borderwidth=1,
                font=dict(color="#0f172a")
            )
        )
        st.plotly_chart(fig_map, use_container_width=True, theme=None)

        srv_list = ", ".join([f"AP #{idx+1}" for idx in top_serving_aps])
        st.markdown(f"""
        <div class="insight-card">
            <p style="margin: 0 0 6px 0; font-weight: 700; color: #0284c7;">📡 ĐÁNH GIÁ CỤM PHỤC VỤ (USER-CENTRIC SERVING) - UE #{k_idx+1}:</p>
            <ul style="margin: 0; padding-left: 20px; line-height: 1.6;">
                <li><b>Vị trí & Cự ly:</b> Tọa độ <code>({ue_c[k_idx, 0]:.1f}m, {ue_c[k_idx, 1]:.1f}m)</code> | Khoảng cách tới AP gần nhất: <b>{min_dist:.1f} m</b>.</li>
                <li><b>Cụm phục vụ:</b> Cụm <b>{srv_list}</b> tự động phối hợp phát sóng đồng pha (Conjugate Beamforming), triệt tiêu biên ô.</li>
                <li><b>Phân tập vĩ mô:</b> Bù đắp suy hao chắn vật cản (Shadowing 8 dB), loại bỏ điểm chết sóng.</li>
                <li><b>Chất lượng thu:</b> SINR = <b>{ue_sinr_db:.2f} dB</b> | Tốc độ phổ = <b>{rates_cf[k_idx]:.3f} bps/Hz</b>.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    # --------------------------------------------------------------------------
    # CHẾ ĐỘ 2: ĐỒ THỊ CDF & ĐÁNH GIÁ TÍNH CÔNG BẰNG
    # --------------------------------------------------------------------------
    elif st.session_state.view_mode == 'chart':
        st.markdown("<h3 style='margin-bottom:6px;'>📈 Báo Cáo Hiệu Năng Phổ Tần & Tính Công Bằng Hệ Thống (Fairness)</h3>", unsafe_allow_html=True)

        rate_5_cf = float(np.percentile(rates_cf, 5))
        rate_5_cell = float(np.percentile(rates_cell, 5))
        mean_sinr_cf_db = 10 * np.log10(np.mean(sinr_cf))
        mean_rate_cf = float(np.mean(rates_cf))

        # 4 Thẻ KPI HUD
        st.markdown(f"""
        <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; margin-bottom: 12px; font-family: 'Space Grotesk', sans-serif;">
            <div style="background: white; border: 1.5px solid #e2e8f0; border-radius: 10px; padding: 10px 14px;">
                <div style="font-size: 0.72rem; color: #64748b; font-weight: 600;">5%-USER RATE (CELL-FREE)</div>
                <div style="font-size: 1.6rem; font-weight: 700; color: #10b981;">{rate_5_cf:.3f} <span style="font-size: 0.75rem; color: #64748b;">bps/Hz</span></div>
                <div style="font-size: 0.72rem; color: #059669; font-weight: 600;">Cellular: {rate_5_cell:.3f} bps/Hz</div>
            </div>
            <div style="background: white; border: 1.5px solid #e2e8f0; border-radius: 10px; padding: 10px 14px;">
                <div style="font-size: 0.72rem; color: #64748b; font-weight: 600;">JAIN'S FAIRNESS INDEX (J)</div>
                <div style="font-size: 1.6rem; font-weight: 700; color: #0284c7;">{jain_cf:.3f} <span style="font-size: 0.75rem; color: #64748b;">/ 1.000</span></div>
                <div style="font-size: 0.72rem; color: #0369a1; font-weight: 600;">Cellular: {jain_cell:.3f}</div>
            </div>
            <div style="background: white; border: 1.5px solid #e2e8f0; border-radius: 10px; padding: 10px 14px;">
                <div style="font-size: 0.72rem; color: #64748b; font-weight: 600;">SINR TRUNG BÌNH HỆ THỐNG</div>
                <div style="font-size: 1.6rem; font-weight: 700; color: #8b5cf6;">{mean_sinr_cf_db:.1f} <span style="font-size: 0.75rem; color: #64748b;">dB</span></div>
                <div style="font-size: 0.72rem; color: #7c3aed; font-weight: 600;">Chất lượng thu phân tán</div>
            </div>
            <div style="background: white; border: 1.5px solid #e2e8f0; border-radius: 10px; padding: 10px 14px;">
                <div style="font-size: 0.72rem; color: #64748b; font-weight: 600;">TỐC ĐỘ PHỔ TRUNG BÌNH</div>
                <div style="font-size: 1.6rem; font-weight: 700; color: #0f172a;">{mean_rate_cf:.3f} <span style="font-size: 0.75rem; color: #64748b;">bps/Hz</span></div>
                <div style="font-size: 0.72rem; color: #475569; font-weight: 600;">Tổng thông lượng phổ</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        fig_cdf = go.Figure()
        cdf_y = np.arange(1, st.session_state.K + 1) / st.session_state.K

        fig_cdf.add_trace(go.Scatter(
            x=np.sort(rates_cf), y=cdf_y, mode='lines+markers',
            name='Cell-Free 6G (Distributed)', line=dict(color='#10b981', width=3), marker=dict(size=5, color='#10b981')
        ))
        fig_cdf.add_trace(go.Scatter(
            x=np.sort(rates_cell), y=cdf_y, mode='lines+markers',
            name='Cellular Cổ Điển (Centralized)', line=dict(color='#f59e0b', width=2.5, dash='dot'), marker=dict(size=5, color='#f59e0b')
        ))
        fig_cdf.add_hline(y=0.05, line_dash="dash", line_color="#94a3b8", annotation_text="Mốc 5% Outage Threshold", annotation_position="top right")

        fig_cdf.update_layout(
            template='plotly_white',
            paper_bgcolor='white',
            plot_bgcolor='white',
            height=350,
            margin=dict(l=15, r=15, t=15, b=15),
            xaxis=dict(
                title=dict(text="Tốc độ phổ người dùng - Spectral Efficiency (bps/Hz)", font=dict(color="#0f172a")),
                showgrid=True,
                gridcolor='#f1f5f9',
                zeroline=False,
                linecolor='#cbd5e1',
                mirror=True
            ),
            yaxis=dict(
                title=dict(text="Xác suất tích lũy CDF: P(Rate ≤ x)", font=dict(color="#0f172a")),
                showgrid=True,
                gridcolor='#f1f5f9',
                zeroline=False,
                linecolor='#cbd5e1',
                mirror=True,
                range=[0, 1.05]
            ),
            legend=dict(
                yanchor="bottom",
                y=0.08,
                xanchor="right",
                x=0.98,
                bgcolor="rgba(255, 255, 255, 0.95)",
                bordercolor="#cbd5e1",
                borderwidth=1,
                font=dict(color="#0f172a")
            )
        )
        st.plotly_chart(fig_cdf, use_container_width=True, theme=None)

        st.markdown(f"""
        <div class="insight-card">
            <p style="margin: 0 0 6px 0; font-weight: 700; color: #0284c7;">⚖️ ĐÁNH GIÁ HIỆU NĂNG & TÍNH CÔNG BẰNG (FAIRNESS BENCHMARK):</p>
            <ul style="margin: 0; padding-left: 20px; line-height: 1.6;">
                <li><b>5%-User Rate:</b> Đạt <b>{rate_5_cf:.3f} bps/Hz</b> trên Cell-Free (Cellular cũ chỉ đạt <b>{rate_5_cell:.3f} bps/Hz</b>).</li>
                <li><b>Jain's Fairness Index:</b> Đạt <b>J = {jain_cf:.3f} / 1.0</b> (Cellular cũ đạt <b>{jain_cell:.3f}</b>), khẳng định tài nguyên được chia đều.</li>
                <li><b>Độ dốc đường CDF:</b> Đường cong Cell-Free dốc đứng về bên phải, chứng minh sự đồng nhất về chất lượng dịch vụ.</li>
                <li><b>Tổng thể mạng:</b> Tốc độ phổ trung bình đạt <b>{mean_rate_cf:.3f} bps/Hz</b> | Mức thu trung bình: <b>{mean_sinr_cf_db:.1f} dB</b>.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
    _, col_back, _ = st.columns([1, 1.3, 1])
    with col_back:
        if st.button("⬅️ QUAY LẠI CẤU HÌNH THAM SỐ", use_container_width=True):
            switch_page('settings')
            st.rerun()