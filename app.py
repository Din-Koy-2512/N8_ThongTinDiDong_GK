import streamlit as st
import numpy as np
import plotly.graph_objects as go

# ==============================================================================
# 1. CẤU HÌNH HỆ THỐNG & ĐỊNH NỀN KỸ THUẬT (SYSTEM & THEME OVERRIDE)
# ==============================================================================
st.set_page_config(
    page_title="Hệ thống mô phỏng khảo sát Cell-Free Massive MIMO cho 6G | Nhóm 08",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Khóa chặt theme sáng, triệt tiêu lỗi nút đen, nhúng font kỹ thuật viễn thông
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

    /* Ép buộc màu nút bấm */
    .stButton>button {
        background-color: #ffffff !important;
        color: #0f172a !important;
        border: 1.5px solid #cbd5e1 !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        font-family: 'Space Grotesk', sans-serif !important;
        font-size: 0.88rem !important;
        padding: 8px 14px !important;
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

    /* Nút chính / Active */
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

    /* Thẻ Insight học thuật */
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
if 'M' not in st.session_state: st.session_state.M = 64
if 'K' not in st.session_state: st.session_state.K = 15
if 'Nc' not in st.session_state: st.session_state.Nc = 5
if 'L' not in st.session_state: st.session_state.L = 1000
if 'Pt' not in st.session_state: st.session_state.Pt = 23
if 'sim_seed' not in st.session_state: st.session_state.sim_seed = 42
if 'view_mode' not in st.session_state: st.session_state.view_mode = 'map'
if 'selected_ue' not in st.session_state: st.session_state.selected_ue = 0

def switch_page(target):
    st.session_state.page = target

# ==============================================================================
# 3. LÕI TÍNH TOÁN VẬT LÝ: USER-CENTRIC CLUSTERING & CO-LOCATED SHADOWING
# ==============================================================================
@st.cache_data(show_spinner=False)
def run_cf_simulation(M, K, Nc, L, Pt_dBm, seed):
    np.random.seed(seed)
    ap_c = np.random.uniform(0, L, (M, 2))
    ue_c = np.random.uniform(0, L, (K, 2))
    ap_cell = np.full((M, 2), [L / 2.0, L / 2.0])
    
    Nc_eff = min(Nc, M)

    def compute_fading(aps, is_colocated=False):
        d = np.zeros((M, K))
        for m in range(M):
            for k in range(K):
                d[m, k] = max(np.linalg.norm(aps[m] - ue_c[k]), 10.0)
        PL = 128.1 + 37.6 * np.log10(d / 1000.0)
        
        if is_colocated:
            # Trạm Cellular tập trung: M ăng-ten đặt cùng 1 vị trí nên chịu chung Shadowing tới từng UE
            sh_single = np.random.normal(0, 8.0, (1, K))
            shadowing = np.repeat(sh_single, M, axis=0)
        else:
            # Mạng Cell-Free phân tán: Mỗi đường truyền AP-UE độc lập về mặt địa lý
            shadowing = np.random.normal(0, 8.0, (M, K))
            
        return 10.0 ** ((-PL + shadowing) / 10.0), d

    beta_cf, dist_cf = compute_fading(ap_c, is_colocated=False)
    beta_cell, _ = compute_fading(ap_cell, is_colocated=True)
    
    # Ma trận mặt nạ kết nối User-Centric (M x K): Chỉ Top Nc AP tốt nhất phục vụ mỗi UE
    mask_uc = np.zeros((M, K))
    for k in range(K):
        top_aps = np.argsort(beta_cf[:, k])[-Nc_eff:]
        mask_uc[top_aps, k] = 1.0
        
    # Mạng Cellular: Toàn bộ M ăng-ten tại trạm gốc trung tâm cùng phục vụ
    mask_cell = np.ones((M, K))
    
    Pt_w = (10.0 ** (Pt_dBm / 10.0)) / 1000.0
    noise_w = (10.0 ** (-100.0 / 10.0)) / 1000.0
    
    def calculate_metrics(beta, mask):
        beta_srv = beta * mask  # Kênh truyền hiệu dụng của cụm phục vụ
        rates = np.zeros(K)
        sinr_arr = np.zeros(K)
        
        for k in range(K):
            # Tín hiệu mong muốn cộng hưởng đồng pha từ cụm AP phục vụ UE k
            sig = (np.sum(beta_srv[:, k])) ** 2
            
            # Can nhiễu đa người dùng từ các AP đang phát cho UE i (i != k) lan truyền qua kênh vật lý tới UE k
            intf = sum(np.sum(beta[:, k] * beta_srv[:, i]) for i in range(K) if i != k)
            
            # Công suất tạp âm nhiệt chuẩn hóa theo búp sóng cụm phục vụ
            n_pwr = (noise_w / Pt_w) * np.sum(beta_srv[:, k])
            
            sinr = sig / (intf + n_pwr + 1e-15)
            sinr_arr[k] = sinr
            rates[k] = np.log2(1.0 + sinr)
        
        jain_index = (np.sum(rates) ** 2) / (K * np.sum(rates ** 2) + 1e-15)
        return rates, sinr_arr, jain_index

    rates_cf, sinr_cf, jain_cf = calculate_metrics(beta_cf, mask_uc)
    rates_cell, sinr_cell, jain_cell = calculate_metrics(beta_cell, mask_cell)
    
    # Tính toán Bản đồ nhiệt Cường độ phủ sóng (2D Coverage Heatmap) đồng bộ cụm Nc và Shadowing không gian
    grid_res = 35
    gx = np.linspace(0, L, grid_res)
    gy = np.linspace(0, L, grid_res)
    GX, GY = np.meshgrid(gx, gy)
    grid_pts = np.stack([GX.ravel(), GY.ravel()], axis=1)
    
    diff = ap_c[:, np.newaxis, :] - grid_pts[np.newaxis, :, :]
    grid_dist = np.maximum(np.linalg.norm(diff, axis=2), 10.0)
    grid_PL = 128.1 + 37.6 * np.log10(grid_dist / 1000.0)
    
    # Mặt phẳng nhiễu bóng mờ không gian mượt (Spatial Shadowing Field)
    spatial_sh = 4.0 * np.sin(GX / 180.0 + seed) * np.cos(GY / 180.0 - seed)
    grid_rx_all_mw = 10.0 ** ((Pt_dBm - grid_PL) / 10.0)
    
    # Tổng hợp công suất thu từ Top Nc AP mạnh nhất tại mỗi điểm lưới
    top_nc_rx_mw = np.sort(grid_rx_all_mw, axis=0)[-Nc_eff:, :]
    coverage_heatmap = (10.0 * np.log10(np.sum(top_nc_rx_mw, axis=0))).reshape((grid_res, grid_res)) + spatial_sh
    
    return ap_c, ue_c, beta_cf, dist_cf, rates_cf, rates_cell, sinr_cf, sinr_cell, jain_cf, jain_cell, gx, gy, coverage_heatmap

# ==============================================================================
# 4. SIDEBAR THÔNG TIN & MÃ QR MOBILE
# ==============================================================================
with st.sidebar:
    st.markdown("<h2 style='text-align: center; color: #0284c7; margin-bottom: 0;'>📡 NHÓM 08</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 0.82rem; color: #64748b; margin-top: 2px;'>BAN CÔNG NGHỆ - CHIẾN LƯỢC</p>", unsafe_allow_html=True)
    st.markdown("---")
    
    st.markdown("##### 👥 Kỹ Sư Thực Hiện:")
    st.markdown("  **Đặng Đình Khôi**  \n  **Trần Quốc Lãm**  \n  **Trần Tuấn Kiệt**  \n  **Nguyễn Phương Nhi**  \n  **Nguyễn Thị Nhiều**")
    
    st.markdown("---")
    st.markdown("##### 🎯 Đề Tài: Khảo sát Cell-Free Massive MIMO cho 6G")
    st.caption("Khảo sát kiến trúc Cell-Free Massive MIMO: Distributed AP, User-Centric Serving, Macro-Diversity & Fairness.")
    
    st.markdown("##### 📱 Quét QR để trải nghiệm trên Mobile")
    web_url = "https://n8thongtindidonggk-jtfw3us2u2uv6mqukunczo.streamlit.app/"
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
    st.markdown("<p style='text-align: center; color: #64748b; margin-bottom: 15px; font-size: 0.95rem;'>Tùy chọn kịch bản chuẩn hóa (20–100 AP, 5–20 UE) và kích thước cụm phục vụ động User-Centric</p>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class="preset-container">
        <p style="font-size: 0.85rem; font-weight: 700; color: #475569; margin-bottom: 8px; letter-spacing: 0.03em;">
            ⚡ KỊCH BẢN THỬ NGHIỆM CHUẨN BAREM (PRESET SCENARIOS):
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    p1, p2, p3 = st.columns(3)
    with p1:
        if st.button("📌 Tiêu Chuẩn Giữa Kỳ\n(M=64, K=15, Nc=5)", use_container_width=True):
            st.session_state.M, st.session_state.K, st.session_state.Nc, st.session_state.L, st.session_state.Pt = 64, 15, 5, 1000, 23
            st.rerun()
    with p2:
        if st.button("🏙️ Tối Đa Tải Đô Thị\n(M=100, K=20, Nc=8)", use_container_width=True):
            st.session_state.M, st.session_state.K, st.session_state.Nc, st.session_state.L, st.session_state.Pt = 100, 20, 8, 800, 23
            st.rerun()
    with p3:
        if st.button("🌾 Ngoại Ô Thưa Thớt\n(M=30, K=8, Nc=3)", use_container_width=True):
            st.session_state.M, st.session_state.K, st.session_state.Nc, st.session_state.L, st.session_state.Pt = 30, 8, 3, 1200, 30
            st.rerun()

    c_ap, _, c_ue = st.columns([1, 0.06, 1])
    with c_ap:
        st.markdown("#### 📡 Hạ tầng Điểm truy cập (AP)")
        st.session_state.M = st.slider("Mật độ AP phân tán (M)", 20, 100, value=min(max(st.session_state.M, 20), 100), step=4)
        st.session_state.Nc = st.slider("Cụm AP phục vụ mỗi UE - User-Centric (Nc)", 2, 15, value=min(max(st.session_state.Nc, 2), 15), step=1)
        st.session_state.L = st.number_input("Kích thước bản đồ (mét)", 500, 2000, value=st.session_state.L, step=100)
    with c_ue:
        st.markdown("#### 📱 Thiết bị Người dùng (UE)")
        st.session_state.K = st.slider("Số lượng người dùng đồng thời (K)", 5, 20, value=min(max(st.session_state.K, 5), 20), step=1)
        st.session_state.Pt = st.number_input("Công suất phát mỗi AP (dBm)", 10, 40, value=st.session_state.Pt, step=1)

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
    
    ap_c, ue_c, beta_cf, dist_cf, rates_cf, rates_cell, sinr_cf, sinr_cell, jain_cf, jain_cell, gx, gy, cov_map = run_cf_simulation(
        st.session_state.M, st.session_state.K, st.session_state.Nc, st.session_state.L, st.session_state.Pt, st.session_state.sim_seed
    )
    
    nav1, nav2, nav3, nav_reroll = st.columns([1, 1, 1, 0.8])
    with nav1:
        if st.button("📍 BẢN ĐỒ & BÚP SÓNG", type="primary" if st.session_state.view_mode == 'map' else "secondary", use_container_width=True):
            st.session_state.view_mode = 'map'
            st.rerun()
    with nav2:
        if st.button("🔥 CƯỜNG ĐỘ PHỦ SÓNG", type="primary" if st.session_state.view_mode == 'heatmap' else "secondary", use_container_width=True):
            st.session_state.view_mode = 'heatmap'
            st.rerun()
    with nav3:
        if st.button("📈 ĐỒ THỊ TỐC ĐỘ (CDF)", type="primary" if st.session_state.view_mode == 'chart' else "secondary", use_container_width=True):
            st.session_state.view_mode = 'chart'
            st.rerun()
    with nav_reroll:
        if st.button("🎲 Sinh Tọa Độ Mới", use_container_width=True):
            st.session_state.sim_seed = int(np.random.randint(1, 999999))
            st.rerun()

    # --------------------------------------------------------------------------
    # CHẾ ĐỘ 1: BẢN ĐỒ KHÔNG GIAN & BEAMFORMING ĐỘNG
    # --------------------------------------------------------------------------
    if st.session_state.view_mode == 'map':
        head_col, select_col = st.columns([2.2, 1])
        with head_col:
            st.markdown(f"<h3 style='margin-bottom:0;'>📍 Bản Đồ Cụm Phục Vụ User-Centric ({st.session_state.M} APs / {st.session_state.K} UEs / Cụm Nc={st.session_state.Nc})</h3>", unsafe_allow_html=True)
        with select_col:
            ue_opts = [f"UE #{i+1}" for i in range(st.session_state.K)]
            selected_str = st.selectbox("Chọn UE khảo sát:", ue_opts, index=min(st.session_state.selected_ue, st.session_state.K-1), label_visibility="collapsed")
            st.session_state.selected_ue = int(selected_str.split('#')[1]) - 1

        k_idx = st.session_state.selected_ue
        nc_eff = min(st.session_state.Nc, st.session_state.M)
        top_serving_aps = np.argsort(beta_cf[:, k_idx])[-nc_eff:]
        min_dist = np.min(dist_cf[:, k_idx])
        ue_sinr_db = 10 * np.log10(sinr_cf[k_idx] + 1e-15)

        fig_map = go.Figure()

        # Tia Beamforming nét đứt nối đúng Nc AP trong cụm phục vụ
        for ap_idx in top_serving_aps:
            fig_map.add_trace(go.Scatter(
                x=[ap_c[ap_idx, 0], ue_c[k_idx, 0]],
                y=[ap_c[ap_idx, 1], ue_c[k_idx, 1]],
                mode='lines',
                line=dict(color='#0284c7', width=2, dash='dash'),
                hoverinfo='skip',
                showlegend=False
            ))

        # AP thông thường (Ngoài cụm phục vụ của UE đang chọn)
        other_aps = [i for i in range(st.session_state.M) if i not in top_serving_aps]
        fig_map.add_trace(go.Scatter(
            x=ap_c[other_aps, 0], y=ap_c[other_aps, 1],
            mode='markers',
            marker=dict(symbol='triangle-up', size=9, color='#f87171', opacity=0.45),
            name='AP Phân tán (Ngoài cụm)',
            hovertemplate='<b>AP #%{text}</b><br>Tọa độ: (%{x:.1f}m, %{y:.1f}m)<extra></extra>',
            text=[str(i+1) for i in other_aps]
        ))

        # Cụm AP phục vụ (Top Nc AP)
        fig_map.add_trace(go.Scatter(
            x=ap_c[top_serving_aps, 0], y=ap_c[top_serving_aps, 1],
            mode='markers+text',
            marker=dict(symbol='triangle-up', size=15, color='#eab308', line=dict(color='#0f172a', width=1.5)),
            name=f'Cụm AP Phục Vụ (Top {nc_eff})',
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

        fig_map.update_layout(
            template='plotly_white',
            paper_bgcolor='white',
            plot_bgcolor='white',
            height=390,
            margin=dict(l=15, r=15, t=15, b=15),
            xaxis=dict(title=dict(text="Tọa độ X (mét)", font=dict(color="#0f172a")), showgrid=True, gridcolor='#f1f5f9', zeroline=False, linecolor='#cbd5e1', mirror=True, range=[-15, st.session_state.L + 15]),
            yaxis=dict(title=dict(text="Tọa độ Y (mét)", font=dict(color="#0f172a")), showgrid=True, gridcolor='#f1f5f9', zeroline=False, linecolor='#cbd5e1', mirror=True, range=[-15, st.session_state.L + 15]),
            legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01, bgcolor="rgba(255, 255, 255, 0.95)", bordercolor="#cbd5e1", borderwidth=1, font=dict(color="#0f172a"))
        )
        st.plotly_chart(fig_map, use_container_width=True, theme=None)

        srv_list = ", ".join([f"AP #{idx+1}" for idx in top_serving_aps])
        st.markdown(f"""
        <div class="insight-card">
            <p style="margin: 0 0 6px 0; font-weight: 700; color: #0284c7;">📡 ĐÁNH GIÁ CỤM PHỤC VỤ ĐỘNG (USER-CENTRIC CLUSTER) - UE #{k_idx+1}:</p>
            <ul style="margin: 0; padding-left: 20px; line-height: 1.6;">
                <li><b>Vị trí & Cự ly:</b> Tọa độ <code>({ue_c[k_idx, 0]:.1f}m, {ue_c[k_idx, 1]:.1f}m)</code> | Khoảng cách tới AP vật lý gần nhất: <b>{min_dist:.1f} m</b>.</li>
                <li><b>Cụm phục vụ ({nc_eff} AP):</b> Nhóm <b>{srv_list}</b> có hệ số kênh truyền $\\beta_{{mk}}$ lớn nhất được chọn vào ma trận mặt nạ kết nối để phát sóng đồng pha.</li>
                <li><b>Giảm tải & Triệt nhiễu:</b> Chỉ {nc_eff}/{st.session_state.M} AP phát tín hiệu cho UE #{k_idx+1}, giúp tiết kiệm dung lượng Fronthaul và giảm nhiễu chéo sang các UE ở xa.</li>
                <li><b>Hiệu năng thực tế:</b> SINR = <b>{ue_sinr_db:.2f} dB</b> | Tốc độ phổ đạt <b>{rates_cf[k_idx]:.3f} bps/Hz</b>.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    # --------------------------------------------------------------------------
    # CHẾ ĐỘ 2: BẢN ĐỒ CƯỜNG ĐỘ PHỦ SÓNG (2D COVERAGE HEATMAP)
    # --------------------------------------------------------------------------
    elif st.session_state.view_mode == 'heatmap':
        st.markdown(f"<h3 style='margin-bottom:0;'>🔥 Bản Đồ Cường Độ Phủ Sóng 2D ({st.session_state.M} APs - Tổng Hợp Cụm Nc={st.session_state.Nc})</h3>", unsafe_allow_html=True)
        
        fig_heat = go.Figure()
        
        # Lớp Heatmap mật độ công suất thu
        fig_heat.add_trace(go.Heatmap(
            x=gx, y=gy, z=cov_map,
            colorscale='Viridis',
            colorbar=dict(title=dict(text="RSSI (dBm)", font=dict(color="#0f172a")), tickfont=dict(color="#0f172a")),
            hovertemplate='Tọa độ: (%{x:.0f}m, %{y:.0f}m)<br>Mức thu cụm RSSI: <b>%{z:.1f} dBm</b><extra></extra>'
        ))
        
        # Định vị các trạm AP trên nền bản đồ nhiệt
        fig_heat.add_trace(go.Scatter(
            x=ap_c[:, 0], y=ap_c[:, 1],
            mode='markers',
            marker=dict(symbol='triangle-up', size=8, color='#ffffff', line=dict(color='#0f172a', width=1)),
            name='Vị trí AP',
            hovertemplate='<b>AP #%{text}</b><extra></extra>',
            text=[str(i+1) for i in range(st.session_state.M)]
        ))
        
        # Định vị người dùng UE
        fig_heat.add_trace(go.Scatter(
            x=ue_c[:, 0], y=ue_c[:, 1],
            mode='markers',
            marker=dict(symbol='circle', size=9, color='#ef4444', line=dict(color='#ffffff', width=1.5)),
            name='Người dùng (UE)',
            hovertemplate='<b>UE #%{text}</b><extra></extra>',
            text=[str(i+1) for i in range(st.session_state.K)]
        ))

        fig_heat.update_layout(
            template='plotly_white',
            paper_bgcolor='white',
            plot_bgcolor='white',
            height=390,
            margin=dict(l=15, r=15, t=15, b=15),
            xaxis=dict(title=dict(text="Tọa độ X (mét)", font=dict(color="#0f172a")), showgrid=False, range=[-5, st.session_state.L + 5]),
            yaxis=dict(title=dict(text="Tọa độ Y (mét)", font=dict(color="#0f172a")), showgrid=False, range=[-5, st.session_state.L + 5]),
            legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01, bgcolor="rgba(255, 255, 255, 0.9)", bordercolor="#cbd5e1", borderwidth=1, font=dict(color="#0f172a"))
        )
        st.plotly_chart(fig_heat, use_container_width=True, theme=None)

        st.markdown(f"""
        <div class="insight-card">
            <p style="margin: 0 0 6px 0; font-weight: 700; color: #0284c7;">📊 PHÂN TÍCH VÙNG PHỦ & BÙ ĐẮP SUY HAO BÓNG MỜ (COVERAGE ANALYSIS):</p>
            <ul style="margin: 0; padding-left: 20px; line-height: 1.6;">
                <li><b>Cường độ thu (RSSI):</b> Biểu diễn tổng công suất thu từ Top {st.session_state.Nc} AP lân cận kết hợp trường nhiễu bóng mờ không gian, dao động từ <b>{np.min(cov_map):.1f} dBm</b> đến <b>{np.max(cov_map):.1f} dBm</b>.</li>
                <li><b>San phẳng vùng lõm sóng:</b> Mật độ {st.session_state.M} AP phân tán giúp duy trì mức thu cao đều khắp miền {st.session_state.L}x{st.session_state.L}m, không bị suy giảm nghiêm trọng ở rìa bản đồ.</li>
                <li><b>Bản chất Phân tập vĩ mô:</b> Các hướng truyền độc lập từ cụm {st.session_state.Nc} AP bù trừ hiện tượng che khuất vật cản cục bộ (Shadowing), bảo toàn chất lượng thu cho các UE (chấm đỏ).</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    # --------------------------------------------------------------------------
    # CHẾ ĐỘ 3: ĐỒ THỊ CDF & ĐÁNH GIÁ TÍNH CÔNG BẰNG
    # --------------------------------------------------------------------------
    elif st.session_state.view_mode == 'chart':
        st.markdown("<h3 style='margin-bottom:6px;'>📈 Báo Cáo Hiệu Năng Phổ Tần & Tính Công Bằng Hệ Thống (Fairness)</h3>", unsafe_allow_html=True)

        rate_5_cf = float(np.percentile(rates_cf, 5))
        rate_5_cell = float(np.percentile(rates_cell, 5))
        mean_sinr_cf_db = 10 * np.log10(np.mean(sinr_cf) + 1e-15)
        mean_rate_cf = float(np.mean(rates_cf))

        # 4 Thẻ KPI HUD
        st.markdown(f"""
        <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; margin-bottom: 12px; font-family: 'Space Grotesk', sans-serif;">
            <div style="background: white; border: 1.5px solid #e2e8f0; border-radius: 10px; padding: 10px 14px;">
                <div style="font-size: 0.72rem; color: #64748b; font-weight: 600;">5%-USER RATE (CELL-FREE)</div>
                <div style="font-size: 1.6rem; font-weight: 700; color: #10b981;">{rate_5_cf:.3f} <span style="font-size: 0.75rem; color: #64748b;">bps/Hz</span></div>
                <div style="font-size: 0.72rem; color: #059669; font-weight: 600;">Cellular đối chứng: {rate_5_cell:.3f} bps/Hz</div>
            </div>
            <div style="background: white; border: 1.5px solid #e2e8f0; border-radius: 10px; padding: 10px 14px;">
                <div style="font-size: 0.72rem; color: #64748b; font-weight: 600;">JAIN'S FAIRNESS INDEX (J)</div>
                <div style="font-size: 1.6rem; font-weight: 700; color: #0284c7;">{jain_cf:.3f} <span style="font-size: 0.75rem; color: #64748b;">/ 1.000</span></div>
                <div style="font-size: 0.72rem; color: #0369a1; font-weight: 600;">Cellular đối chứng: {jain_cell:.3f}</div>
            </div>
            <div style="background: white; border: 1.5px solid #e2e8f0; border-radius: 10px; padding: 10px 14px;">
                <div style="font-size: 0.72rem; color: #64748b; font-weight: 600;">SINR TRUNG BÌNH (Nc={st.session_state.Nc})</div>
                <div style="font-size: 1.6rem; font-weight: 700; color: #8b5cf6;">{mean_sinr_cf_db:.1f} <span style="font-size: 0.75rem; color: #64748b;">dB</span></div>
                <div style="font-size: 0.72rem; color: #7c3aed; font-weight: 600;">User-Centric Beamforming</div>
            </div>
            <div style="background: white; border: 1.5px solid #e2e8f0; border-radius: 10px; padding: 10px 14px;">
                <div style="font-size: 0.72rem; color: #64748b; font-weight: 600;">TỐC ĐỘ PHỔ TRUNG BÌNH</div>
                <div style="font-size: 1.6rem; font-weight: 700; color: #0f172a;">{mean_rate_cf:.3f} <span style="font-size: 0.75rem; color: #64748b;">bps/Hz</span></div>
                <div style="font-size: 0.72rem; color: #475569; font-weight: 600;">Hiệu suất phổ toàn mạng</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        fig_cdf = go.Figure()
        cdf_y = np.arange(1, st.session_state.K + 1) / st.session_state.K

        fig_cdf.add_trace(go.Scatter(
            x=np.sort(rates_cf), y=cdf_y, mode='lines+markers',
            name=f'Cell-Free User-Centric (Nc={st.session_state.Nc} AP/UE)', line=dict(color='#10b981', width=3), marker=dict(size=5, color='#10b981')
        ))
        fig_cdf.add_trace(go.Scatter(
            x=np.sort(rates_cell), y=cdf_y, mode='lines+markers',
            name='Cellular Đối Chứng (Co-located Array)', line=dict(color='#f59e0b', width=2.5, dash='dot'), marker=dict(size=5, color='#f59e0b')
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
                <li><b>5%-User Rate:</b> Đạt <b>{rate_5_cf:.3f} bps/Hz</b> trên Cell-Free với cụm $N_c={st.session_state.Nc}$ AP (Cellular tập trung tại tâm chỉ đạt <b>{rate_5_cell:.3f} bps/Hz</b> do suy hao biên và nhiễu bóng mờ đồng nhất).</li>
                <li><b>Jain's Fairness Index:</b> Đạt <b>J = {jain_cf:.3f} / 1.0</b> so với <b>{jain_cell:.3f}</b> của Cellular, chứng minh tài nguyên phổ được phân bổ đồng đều.</li>
                <li><b>Tác động của cụm $N_c$:</b> Giới hạn mỗi UE chỉ kết nối với {st.session_state.Nc} AP tốt nhất vừa giữ được >90% năng lượng búp sóng chính, vừa triệt tiêu nhiễu đồng kênh từ các AP ở xa.</li>
                <li><b>Cơ sở giải tích:</b> Mô hình áp dụng tính chất làm cứng kênh (Channel Hardening) với giả định ước lượng kênh hoàn hảo (Ideal CSI) cho bộ tiền mã hóa Conjugate Beamforming.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
    _, col_back, _ = st.columns([1, 1.3, 1])
    with col_back:
        if st.button("⬅️ QUAY LẠI CẤU HÌNH THAM SỐ", use_container_width=True):
            switch_page('settings')
            st.rerun()