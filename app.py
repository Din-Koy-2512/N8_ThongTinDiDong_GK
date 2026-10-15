import streamlit as st
import streamlit.components.v1 as components
import numpy as np
import plotly.graph_objects as go

# ==============================================================================
# 1. CẤU HÌNH HỆ THỐNG & GIAO DIỆN CINEMATIC + ĐỒ THỊ NỀN TRẮNG RÕ NÉT
# ==============================================================================
st.set_page_config(
    page_title="Hệ thống mô phỏng khảo sát Cell-Free Massive MIMO cho 6G | Nhóm 08",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Giao diện Cinematic Midnight + Đồ thị nền trắng tương phản cao
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Playfair+Display:ital,wght@0,600;1,500;1,600&family=JetBrains+Mono:wght@500;600;700&display=swap');

    :root {
        --lime: #84cc16;
        --lime-bright: #a3e635;
        --cyan: #38bdf8;
        --bg-deep: #070b16;
        --bg-navy: #0f172a;
        --text-white: #ffffff;
        --text-silver: #cbd5e1;
    }

    /* ================= KEYFRAME ANIMATIONS SINH ĐỘNG ================= */
    @keyframes fadeSlideUp {
        0% { opacity: 0; transform: translateY(22px) scale(0.985); }
        100% { opacity: 1; transform: translateY(0) scale(1); }
    }
    @keyframes floatOrbSlow {
        0%, 100% { transform: translate(0px, 0px) scale(1); }
        50% { transform: translate(28px, -22px) scale(1.08); }
    }
    @keyframes floatOrbReverse {
        0%, 100% { transform: translate(0px, 0px) scale(1); }
        50% { transform: translate(-25px, 20px) scale(1.06); }
    }
    @keyframes pulseNeon {
        0%, 100% { box-shadow: 0 0 0 0 rgba(163, 230, 53, 0.55), 0 10px 28px rgba(132, 204, 22, 0.42); }
        50% { box-shadow: 0 0 0 10px rgba(163, 230, 53, 0), 0 14px 36px rgba(163, 230, 53, 0.65); }
    }
    @keyframes shimmerSweep {
        0% { transform: translateX(-120%) skewX(-18deg); }
        100% { transform: translateX(220%) skewX(-18deg); }
    }
    @keyframes iconPulse {
        0%, 100% { transform: translateY(0px) scale(1); }
        50% { transform: translateY(-5px) scale(1.06); }
    }
    @keyframes radarPing {
        0% { transform: scale(1); opacity: 0.9; }
        100% { transform: scale(2.6); opacity: 0; }
    }

    /* Nền trang web sống động với hiệu ứng ánh sáng Bokeh & dải sóng 6G */
    .stApp, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
        background-color: #070b16 !important;
        background-image:
            radial-gradient(circle at 18% 28%, rgba(56, 189, 248, 0.16) 0%, transparent 38%),
            radial-gradient(circle at 82% 24%, rgba(99, 102, 241, 0.18) 0%, transparent 42%),
            radial-gradient(circle at 50% 75%, rgba(132, 204, 22, 0.12) 0%, transparent 45%),
            linear-gradient(180deg, #060913 0%, #0d1527 50%, #070b16 100%) !important;
        background-attachment: fixed !important;
        color: #ffffff !important;
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }

    header[data-testid="stHeader"] {
        background: rgba(6, 9, 19, 0.75) !important;
        backdrop-filter: blur(12px) !important;
        border-bottom: 1px solid rgba(255, 255, 255, 0.07) !important;
    }
    header[data-testid="stHeader"] * {
        color: #ffffff !important;
    }

    .block-container {
        padding-top: 1.5rem !important;
        padding-bottom: 2.2rem !important;
        max-width: 1280px !important;
        animation: fadeSlideUp 0.45s cubic-bezier(0.16, 1, 0.3, 1);
    }

    h1, h2, h3, h4, h5, h6 {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        color: #ffffff !important;
        letter-spacing: -0.02em !important;
    }
    p, li, span, label, [data-testid="stWidgetLabel"] p, [data-testid="stMarkdownContainer"] p {
        color: #e2e8f0 !important;
    }

    /* ================= SIDEBAR (THANH BÊN TRÁI) ================= */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #090e1c 0%, #0f172a 100%) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.1) !important;
    }
    .brand-logo-box {
        border: 2px solid rgba(255, 255, 255, 0.85);
        padding: 4px;
        display: inline-block;
        margin-bottom: 14px;
        transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
    }
    .brand-logo-box:hover {
        border-color: #a3e635;
        transform: scale(1.04) rotate(-1deg);
        box-shadow: 0 0 22px rgba(163, 230, 53, 0.35);
    }
    .brand-logo-inner {
        border: 1px solid rgba(255, 255, 255, 0.45);
        padding: 10px 18px;
        text-align: center;
    }
    .brand-logo-title {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-weight: 800;
        font-size: 1.05rem;
        letter-spacing: 0.16em;
        color: #ffffff !important;
        line-height: 1.2;
    }
    .brand-logo-sub {
        font-size: 0.65rem;
        letter-spacing: 0.22em;
        color: #a3e635 !important;
        font-weight: 700;
        margin-top: 3px;
    }
    .sidebar-member-list {
        background: rgba(255, 255, 255, 0.04);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 14px;
        padding: 8px 12px;
        margin-bottom: 16px;
    }
    .sidebar-member-row {
        display: flex;
        align-items: center;
        gap: 10px;
        padding: 7px 8px;
        border-radius: 8px;
        font-size: 0.88rem;
        font-weight: 600;
        color: #f8fafc !important;
        border-bottom: 1px solid rgba(255, 255, 255, 0.06);
        transition: all 0.22s ease;
    }
    .sidebar-member-row:last-child {
        border-bottom: none;
    }
    .sidebar-member-row:hover {
        background: rgba(132, 204, 22, 0.15);
        transform: translateX(6px);
        color: #bef264 !important;
    }
    .lime-dot {
        position: relative;
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: #a3e635;
        box-shadow: 0 0 8px #84cc16;
        display: inline-block;
    }
    .lime-dot::after {
        content: "";
        position: absolute;
        inset: -2px;
        border-radius: 50%;
        border: 1.5px solid #a3e635;
        animation: radarPing 2s infinite ease-out;
    }
    .sidebar-topic-card {
        background: rgba(132, 204, 22, 0.08);
        border: 1px solid rgba(163, 230, 53, 0.3);
        border-left: 4px solid #84cc16;
        border-radius: 12px;
        padding: 12px 14px;
        margin-bottom: 16px;
        font-size: 0.84rem;
        line-height: 1.55;
        color: #ecfccb !important;
        transition: all 0.25s ease;
    }
    .sidebar-topic-card:hover {
        background: rgba(132, 204, 22, 0.15);
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(132, 204, 22, 0.18);
    }

    /* ================= TOP NAVIGATION BAR ================= */
    .top-navbar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 14px;
        padding: 12px 24px;
        background: rgba(15, 23, 42, 0.68);
        backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.12);
        border-radius: 16px;
        margin-bottom: 20px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.35);
        transition: border-color 0.3s ease;
    }
    .top-navbar:hover {
        border-color: rgba(163, 230, 53, 0.35);
    }
    .nav-logo-frame {
        border: 1.5px solid rgba(255, 255, 255, 0.85);
        padding: 3px;
        display: inline-block;
        transition: all 0.25s ease;
    }
    .nav-logo-inner {
        border: 1px solid rgba(255, 255, 255, 0.35);
        padding: 5px 14px;
        text-align: center;
    }
    .nav-logo-text {
        font-weight: 800;
        font-size: 0.85rem;
        letter-spacing: 0.18em;
        color: #ffffff !important;
    }
    .nav-logo-sub {
        font-size: 0.58rem;
        letter-spacing: 0.22em;
        color: #a3e635 !important;
        font-weight: 700;
    }
    .nav-links {
        display: flex;
        align-items: center;
        gap: 24px;
        flex-wrap: wrap;
    }
    .nav-item {
        font-size: 0.76rem;
        font-weight: 700;
        letter-spacing: 0.16em;
        text-transform: uppercase;
        color: #94a3b8 !important;
        padding-bottom: 5px;
        border-bottom: 2px solid transparent;
        transition: all 0.22s ease;
    }
    .nav-item.active {
        color: #ffffff !important;
        border-bottom: 2px solid #84cc16;
        text-shadow: 0 0 12px rgba(163, 230, 53, 0.5);
    }
    .nav-pill {
        background: rgba(132, 204, 22, 0.15);
        border: 1px solid rgba(163, 230, 53, 0.45);
        color: #d9f99d !important;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.75rem;
        font-weight: 600;
        padding: 5px 12px;
        border-radius: 999px;
    }

    /* ================= HERO SHOWCASE ================= */
    .hero-showcase {
        position: relative;
        overflow: hidden;
        border-radius: 26px;
        border: 1px solid rgba(255, 255, 255, 0.15);
        background:
            radial-gradient(circle at 26% 38%, rgba(30, 64, 175, 0.48) 0%, rgba(15, 23, 42, 0.2) 42%, transparent 70%),
            radial-gradient(circle at 75% 32%, rgba(56, 189, 248, 0.32) 0%, rgba(30, 58, 138, 0.25) 45%, transparent 72%),
            radial-gradient(circle at 52% 85%, rgba(132, 204, 22, 0.18) 0%, transparent 55%),
            linear-gradient(135deg, #070b16 0%, #111c38 48%, #090d1a 100%);
        padding: 54px 40px 42px 40px;
        text-align: center;
        box-shadow: 0 25px 60px rgba(0, 0, 0, 0.55);
        margin-bottom: 24px;
        animation: fadeSlideUp 0.55s cubic-bezier(0.16, 1, 0.3, 1);
    }
    .hero-orb-left {
        position: absolute;
        width: 340px;
        height: 340px;
        border-radius: 50%;
        left: -60px;
        top: 20px;
        background: radial-gradient(circle at 35% 35%, rgba(96, 165, 250, 0.38), rgba(30, 58, 138, 0.12) 60%, transparent 75%);
        filter: blur(8px);
        pointer-events: none;
        animation: floatOrbSlow 9s infinite ease-in-out;
    }
    .hero-orb-right {
        position: absolute;
        width: 400px;
        height: 400px;
        border-radius: 50%;
        right: -70px;
        top: -20px;
        background: radial-gradient(circle at 40% 40%, rgba(56, 189, 248, 0.32), rgba(15, 23, 42, 0.15) 65%, transparent 80%);
        filter: blur(10px);
        pointer-events: none;
        animation: floatOrbReverse 11s infinite ease-in-out;
    }
    .hero-main-title {
        position: relative;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-size: 4.3rem !important;
        font-weight: 800 !important;
        letter-spacing: -0.03em !important;
        color: #ffffff !important;
        margin: 0 0 8px 0 !important;
        line-height: 1.08 !important;
        text-shadow: 0 8px 30px rgba(0, 0, 0, 0.6);
        transition: transform 0.3s ease, text-shadow 0.3s ease;
    }
    .hero-main-title:hover {
        transform: scale(1.02);
        text-shadow: 0 0 32px rgba(56, 189, 248, 0.45), 0 8px 30px rgba(0, 0, 0, 0.6);
    }
    .hero-script-sub {
        position: relative;
        font-family: 'Playfair Display', Georgia, serif !important;
        font-style: italic !important;
        font-weight: 500 !important;
        font-size: 1.55rem !important;
        color: #e2e8f0 !important;
        margin: 0 0 18px 0 !important;
        letter-spacing: 0.01em;
    }
    .hero-desc {
        position: relative;
        max-width: 680px;
        margin: 0 auto 28px auto !important;
        font-size: 0.95rem !important;
        line-height: 1.68 !important;
        color: #cbd5e1 !important;
    }

    /* 4 Cột Icon Viền Xanh Neon */
    .hero-icon-grid {
        position: relative;
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 20px;
        margin-top: 40px;
        padding-top: 28px;
        border-top: 1px solid rgba(255, 255, 255, 0.12);
    }
    .hero-icon-item {
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align: center;
        padding: 16px 12px;
        border-radius: 18px;
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid transparent;
        transition: all 0.28s cubic-bezier(0.34, 1.56, 0.64, 1);
    }
    .hero-icon-item:hover {
        background: rgba(132, 204, 22, 0.1);
        border-color: rgba(163, 230, 53, 0.45);
        transform: translateY(-6px) scale(1.02);
        box-shadow: 0 14px 30px rgba(0, 0, 0, 0.4), 0 0 20px rgba(132, 204, 22, 0.2);
    }
    .hero-icon-svg {
        width: 48px;
        height: 48px;
        margin-bottom: 12px;
        filter: drop-shadow(0 0 10px rgba(132, 204, 22, 0.4));
        animation: iconPulse 3.6s infinite ease-in-out;
        transition: transform 0.3s ease;
    }
    .hero-icon-item:hover .hero-icon-svg {
        transform: scale(1.15) rotate(5deg);
        filter: drop-shadow(0 0 16px rgba(163, 230, 53, 0.85));
    }
    .hero-icon-title {
        font-weight: 700;
        font-size: 0.92rem;
        color: #ffffff !important;
        margin-bottom: 4px;
    }
    .hero-icon-caption {
        font-family: 'Playfair Display', Georgia, serif;
        font-style: italic;
        font-size: 0.88rem;
        color: #cbd5e1 !important;
        line-height: 1.45;
    }

    /* ================= NÚT BẤM VIÊN THUỐC + HIỆU ỨNG SÁNG ================= */
    .stButton > button,
    button[data-testid="stBaseButton-secondary"] {
        position: relative !important;
        overflow: hidden !important;
        width: 100% !important;
        background: rgba(30, 41, 59, 0.82) !important;
        color: #ffffff !important;
        border: 1.5px solid rgba(148, 163, 184, 0.38) !important;
        border-radius: 999px !important;
        font-weight: 700 !important;
        font-size: 0.84rem !important;
        letter-spacing: 0.05em !important;
        text-transform: uppercase !important;
        padding: 0.7rem 1.2rem !important;
        min-height: 48px !important;
        backdrop-filter: blur(10px) !important;
        box-shadow: 0 6px 18px rgba(0, 0, 0, 0.3) !important;
        transition: all 0.24s cubic-bezier(0.34, 1.56, 0.64, 1) !important;
    }
    .stButton > button::before {
        content: "";
        position: absolute;
        top: 0;
        left: -100%;
        width: 60%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.28), transparent);
        transform: skewX(-20deg);
        transition: none;
        pointer-events: none;
    }
    .stButton > button:hover::before {
        animation: shimmerSweep 0.75s ease-out;
    }
    .stButton > button *,
    button[data-testid="stBaseButton-secondary"] * {
        color: #ffffff !important;
        font-weight: 700 !important;
    }
    .stButton > button:hover,
    button[data-testid="stBaseButton-secondary"]:hover {
        background: rgba(132, 204, 22, 0.22) !important;
        border-color: #a3e635 !important;
        transform: translateY(-3px) scale(1.02) !important;
        box-shadow: 0 12px 26px rgba(132, 204, 22, 0.3), 0 0 16px rgba(163, 230, 53, 0.35) !important;
    }
    .stButton > button:active,
    button[data-testid="stBaseButton-secondary"]:active {
        transform: translateY(1px) scale(0.95) !important;
    }

    /* Nút Chính: Viên thuốc Xanh Lá mạ Neon */
    .stButton > button[kind="primary"],
    button[data-testid="stBaseButton-primary"] {
        width: 100% !important;
        background: linear-gradient(135deg, #84cc16 0%, #65a30d 100%) !important;
        color: #ffffff !important;
        border: 1.5px solid #bef264 !important;
        border-radius: 999px !important;
        font-weight: 800 !important;
        letter-spacing: 0.08em !important;
        text-transform: uppercase !important;
        min-height: 50px !important;
        animation: pulseNeon 2.8s infinite;
    }
    .stButton > button[kind="primary"] *,
    button[data-testid="stBaseButton-primary"] * {
        color: #ffffff !important;
        font-weight: 800 !important;
    }
    .stButton > button[kind="primary"]:hover,
    button[data-testid="stBaseButton-primary"]:hover {
        background: linear-gradient(135deg, #a3e635 0%, #84cc16 100%) !important;
        transform: translateY(-4px) scale(1.03) !important;
        box-shadow: 0 16px 36px rgba(163, 230, 53, 0.65), 0 0 24px rgba(190, 242, 100, 0.6) !important;
    }

    /* ================= KHUNG KÍNH MỜ & Ô CHỌN UE RÕ CHỮ ================= */
    [data-testid="stVerticalBlockBorderWrapper"] {
        background: rgba(15, 23, 42, 0.72) !important;
        backdrop-filter: blur(16px) !important;
        border: 1px solid rgba(148, 163, 184, 0.22) !important;
        border-radius: 20px !important;
        padding: 20px !important;
        box-shadow: 0 12px 32px rgba(0, 0, 0, 0.35) !important;
        transition: border-color 0.3s ease, box-shadow 0.3s ease !important;
    }
    [data-testid="stVerticalBlockBorderWrapper"]:hover {
        border-color: rgba(163, 230, 53, 0.38) !important;
    }

    [data-testid="stWidgetLabel"] p {
        font-size: 0.94rem !important;
        font-weight: 700 !important;
        color: #f8fafc !important;
    }

    /* Ô Selectbox chọn UE & ô Input: Nền trắng chữ xanh đen đậm cực rõ */
    div[data-baseweb="select"] > div,
    div[data-baseweb="input"] > div,
    div[data-baseweb="base-input"] {
        background-color: #ffffff !important;
        border: 2px solid #84cc16 !important;
        border-radius: 12px !important;
        color: #0f172a !important;
        transition: all 0.22s ease !important;
    }
    div[data-baseweb="select"] > div:hover,
    div[data-baseweb="input"] > div:hover {
        border-color: #38bdf8 !important;
        box-shadow: 0 0 14px rgba(56, 189, 248, 0.35) !important;
    }
    div[data-baseweb="input"] input {
        color: #0f172a !important;
        -webkit-text-fill-color: #0f172a !important;
        font-family: 'JetBrains Mono', monospace !important;
        font-weight: 700 !important;
        font-size: 0.98rem !important;
    }
    [data-testid="stNumberInputStepDown"],
    [data-testid="stNumberInputStepUp"] {
        background-color: #f1f5f9 !important;
        color: #0f172a !important;
    }
    [data-testid="stNumberInputStepDown"] svg,
    [data-testid="stNumberInputStepUp"] svg {
        fill: #0f172a !important;
    }
    div[data-baseweb="select"] *,
    div[data-baseweb="select"] span,
    div[data-baseweb="select"] div {
        color: #0f172a !important;
        -webkit-text-fill-color: #0f172a !important;
        font-family: 'JetBrains Mono', monospace !important;
        font-weight: 700 !important;
    }
    div[data-baseweb="select"] svg {
        fill: #0f172a !important;
    }
    ul[data-baseweb="menu"],
    div[data-baseweb="popover"] {
        background-color: #ffffff !important;
        border: 1.5px solid #84cc16 !important;
    }
    li[role="option"] {
        background-color: #ffffff !important;
        color: #0f172a !important;
        font-weight: 600 !important;
    }
    li[role="option"] * {
        color: #0f172a !important;
    }
    li[role="option"]:hover {
        background-color: #ecfccb !important;
        color: #365314 !important;
        padding-left: 18px !important;
    }

    /* ================= KHUNG ĐỒ THỊ NỀN TRẮNG NỔI BẬT ================= */
    [data-testid="stPlotlyChart"] {
        background-color: #ffffff !important;
        border-radius: 16px !important;
        padding: 10px 12px 6px 12px !important;
        border: 2px solid rgba(163, 230, 53, 0.55) !important;
        box-shadow: 0 12px 32px rgba(0, 0, 0, 0.45) !important;
        margin-top: 6px !important;
        transition: transform 0.25s ease, box-shadow 0.25s ease !important;
    }
    [data-testid="stPlotlyChart"]:hover {
        box-shadow: 0 16px 40px rgba(0, 0, 0, 0.55), 0 0 22px rgba(163, 230, 53, 0.25) !important;
    }

    /* ================= THẺ KPI & INSIGHT ================= */
    .kpi-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 16px;
        margin-bottom: 16px;
    }
    .kpi-card {
        background: rgba(15, 23, 42, 0.78);
        backdrop-filter: blur(14px);
        border: 1px solid rgba(148, 163, 184, 0.22);
        border-radius: 16px;
        padding: 16px 18px;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);
        transition: all 0.26s cubic-bezier(0.34, 1.56, 0.64, 1);
    }
    .kpi-card:hover {
        transform: translateY(-5px);
        border-color: rgba(163, 230, 53, 0.55);
        box-shadow: 0 14px 32px rgba(0, 0, 0, 0.45), 0 0 22px rgba(132, 204, 22, 0.22);
    }
    .kpi-label {
        font-size: 0.72rem;
        font-weight: 700;
        color: #94a3b8 !important;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        margin-bottom: 6px;
    }
    .kpi-value {
        font-family: 'JetBrains Mono', monospace;
        font-size: 1.7rem;
        font-weight: 800;
        line-height: 1.2;
        margin-bottom: 5px;
    }
    .kpi-sub {
        font-size: 0.8rem;
        font-weight: 600;
        color: #cbd5e1 !important;
    }

    .insight-card {
        background: rgba(15, 23, 42, 0.78) !important;
        backdrop-filter: blur(16px) !important;
        border: 1px solid rgba(163, 230, 53, 0.3) !important;
        border-left: 5px solid #84cc16 !important;
        border-radius: 16px !important;
        padding: 18px 24px !important;
        margin-top: 14px !important;
        color: #f1f5f9 !important;
        font-size: 0.94rem !important;
        box-shadow: 0 10px 28px rgba(0, 0, 0, 0.35) !important;
    }
    .insight-card code {
        background: rgba(132, 204, 22, 0.18) !important;
        color: #bef264 !important;
        padding: 2px 8px !important;
        border-radius: 6px !important;
        font-family: 'JetBrains Mono', monospace !important;
        font-weight: 700 !important;
    }
    .stat-banner {
        background: rgba(132, 204, 22, 0.1);
        border: 1px solid rgba(163, 230, 53, 0.35);
        border-radius: 12px;
        padding: 10px 14px;
        margin-top: 8px;
        font-size: 0.88rem;
        color: #ecfccb !important;
    }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# NHÚNG HIỆU ỨNG SÓNG RADAR 6G KHI CLICK CHUỘT
# ==============================================================================
components.html("""
<script>
(function() {
    const parentDoc = window.parent.document;
    if (parentDoc.getElementById('cf6g-interactive-fx')) return;

    const styleEl = parentDoc.createElement('style');
    styleEl.id = 'cf6g-interactive-fx';
    styleEl.innerHTML = `
        .cf6g-click-ring {
            position: fixed;
            border-radius: 50%;
            pointer-events: none;
            z-index: 999999;
            transform: translate(-50%, -50%) scale(0.1);
            border: 2px solid #a3e635;
            box-shadow: 0 0 18px #84cc16, inset 0 0 12px #38bdf8;
            animation: cf6gRingExpand 0.65s cubic-bezier(0.16, 1, 0.3, 1) forwards;
        }
        .cf6g-cursor-glow {
            position: fixed;
            width: 320px;
            height: 320px;
            border-radius: 50%;
            pointer-events: none;
            z-index: 1;
            background: radial-gradient(circle, rgba(163, 230, 53, 0.07) 0%, rgba(56, 189, 248, 0.04) 40%, transparent 70%);
            transform: translate(-50%, -50%);
            transition: left 0.08s linear, top 0.08s linear;
        }
        @keyframes cf6gRingExpand {
            0% { width: 12px; height: 12px; opacity: 0.95; transform: translate(-50%, -50%) scale(0.3); }
            100% { width: 95px; height: 95px; opacity: 0; transform: translate(-50%, -50%) scale(1.2); }
        }
    `;
    parentDoc.head.appendChild(styleEl);

    const glow = parentDoc.createElement('div');
    glow.className = 'cf6g-cursor-glow';
    parentDoc.body.appendChild(glow);

    parentDoc.addEventListener('mousemove', function(e) {
        glow.style.left = e.clientX + 'px';
        glow.style.top = e.clientY + 'px';
    }, { passive: true });

    parentDoc.addEventListener('mousedown', function(e) {
        const ring = parentDoc.createElement('div');
        ring.className = 'cf6g-click-ring';
        ring.style.left = e.clientX + 'px';
        ring.style.top = e.clientY + 'px';
        parentDoc.body.appendChild(ring);
        setTimeout(() => ring.remove(), 680);
    });
})();
</script>
""", height=0)

# ==============================================================================
# 2. KHỞI TẠO BIẾN TRẠNG THÁI (SESSION STATE CHUẨN BAREM GIẢNG VIÊN)
# ==============================================================================
if 'page' not in st.session_state: st.session_state.page = 'home'
if 'M' not in st.session_state: st.session_state.M = 64
if 'K' not in st.session_state: st.session_state.K = 15
if 'Nc' not in st.session_state: st.session_state.Nc = 5
if 'L' not in st.session_state: st.session_state.L = 1000
if 'Pt' not in st.session_state: st.session_state.Pt = 23
if 'sim_seed' not in st.session_state: st.session_state.sim_seed = 42
if 'view_mode' not in st.session_state: st.session_state.view_mode = 'map'
if 'cov_style' not in st.session_state: st.session_state.cov_style = 'contour'
if 'selected_ue' not in st.session_state: st.session_state.selected_ue = 0

def switch_page(target):
    st.session_state.page = target

# ==============================================================================
# 3. LÕI TÍNH TOÁN VẬT LÝ & ĐỒ HỌA TRƯỜNG SÓNG ĐẲNG THẾ (ISO-CONTOUR / 3D)
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
            sh_single = np.random.normal(0, 8.0, (1, K))
            shadowing = np.repeat(sh_single, M, axis=0)
        else:
            shadowing = np.random.normal(0, 8.0, (M, K))
            
        return 10.0 ** ((-PL + shadowing) / 10.0), d

    beta_cf, dist_cf = compute_fading(ap_c, is_colocated=False)
    beta_cell, _ = compute_fading(ap_cell, is_colocated=True)
    
    # Ma trận mặt nạ kết nối User-Centric (Top Nc AP phục vụ mỗi UE)
    mask_uc = np.zeros((M, K))
    for k in range(K):
        top_aps = np.argsort(beta_cf[:, k])[-Nc_eff:]
        mask_uc[top_aps, k] = 1.0
        
    mask_cell = np.ones((M, K))
    
    Pt_w = (10.0 ** (Pt_dBm / 10.0)) / 1000.0
    noise_w = (10.0 ** (-100.0 / 10.0)) / 1000.0
    
    def calculate_metrics(beta, mask):
        beta_srv = beta * mask
        rates = np.zeros(K)
        sinr_arr = np.zeros(K)
        for k in range(K):
            sig = (np.sum(beta_srv[:, k])) ** 2
            intf = sum(np.sum(beta[:, k] * beta_srv[:, i]) for i in range(K) if i != k)
            n_pwr = (noise_w / Pt_w) * np.sum(beta_srv[:, k])
            sinr = sig / (intf + n_pwr + 1e-15)
            sinr_arr[k] = sinr
            rates[k] = np.log2(1.0 + sinr)
        
        jain_index = (np.sum(rates) ** 2) / (K * np.sum(rates ** 2) + 1e-15)
        return rates, sinr_arr, jain_index

    rates_cf, sinr_cf, jain_cf = calculate_metrics(beta_cf, mask_uc)
    rates_cell, sinr_cell, jain_cell = calculate_metrics(beta_cell, mask_cell)
    
    # Lưới phân giải cao (80x80) để nội suy mặt đẳng thế mượt tuyệt đối (không bị pixel)
    grid_res = 80
    gx = np.linspace(0, L, grid_res)
    gy = np.linspace(0, L, grid_res)
    GX, GY = np.meshgrid(gx, gy)
    grid_pts = np.stack([GX.ravel(), GY.ravel()], axis=1)
    
    # 1. Trường công suất Cell-Free (Tổng hợp đồng pha từ cụm Nc AP lân cận)
    diff_cf = ap_c[:, np.newaxis, :] - grid_pts[np.newaxis, :, :]
    dist_grid_cf = np.maximum(np.linalg.norm(diff_cf, axis=2), 12.0)
    pl_grid_cf = 128.1 + 37.6 * np.log10(dist_grid_cf / 1000.0)
    rx_all_mw = 10.0 ** ((Pt_dBm - pl_grid_cf) / 10.0)
    top_nc_mw = np.sort(rx_all_mw, axis=0)[-Nc_eff:, :]
    
    # Trường fading bóng mờ không gian tương quan mượt (Correlated Spatial Shadowing)
    spatial_sh = (
        3.2 * np.sin(2.2 * np.pi * GX / L + seed) * np.cos(2.2 * np.pi * GY / L - seed)
        + 1.8 * np.cos(4.0 * np.pi * (GX + GY) / L)
    )
    field_cf_dbm = (10.0 * np.log10(np.sum(top_nc_mw, axis=0))).reshape((grid_res, grid_res)) + spatial_sh

    # 2. Trường công suất Cellular đối chứng (Trạm phát tập trung tại tâm L/2, L/2)
    dist_grid_cell = np.maximum(np.sqrt((GX - L/2.0)**2 + (GY - L/2.0)**2), 12.0)
    pl_grid_cell = 128.1 + 37.6 * np.log10(dist_grid_cell / 1000.0)
    field_cell_dbm = (Pt_dBm + 10.0 * np.log10(Nc_eff) - pl_grid_cell) + spatial_sh
    
    return (
        ap_c, ue_c, beta_cf, dist_cf,
        rates_cf, rates_cell, sinr_cf, sinr_cell,
        jain_cf, jain_cell, gx, gy, field_cf_dbm, field_cell_dbm
    )

# ==============================================================================
# 4. SIDEBAR CẨM NĂNG & MÃ QR MOBILE
# ==============================================================================
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding-top: 6px;">
        <div class="brand-logo-box">
            <div class="brand-logo-inner">
                <div class="brand-logo-title">NHÓM 08</div>
                <div class="brand-logo-sub">6G WIRELESS LAB</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("##### 👥 Kỹ Sư Thực Hiện")
    st.markdown("""
    <div class="sidebar-member-list">
        <div class="sidebar-member-row"><span class="lime-dot"></span>Đặng Đình Khôi</div>
        <div class="sidebar-member-row"><span class="lime-dot"></span>Trần Quốc Lãm</div>
        <div class="sidebar-member-row"><span class="lime-dot"></span>Trần Tuấn Kiệt</div>
        <div class="sidebar-member-row"><span class="lime-dot"></span>Nguyễn Phương Nhi</div>
        <div class="sidebar-member-row"><span class="lime-dot"></span>Nguyễn Thị Nhiều</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("##### 🎯 Đề Tài Nghiên Cứu")
    st.markdown("""
    <div class="sidebar-topic-card">
        <b>Khảo sát Cell-Free Massive MIMO cho 6G</b><br>
        Kiến trúc AP phân tán, phục vụ lấy người dùng làm trung tâm (User-Centric), phân tập vĩ mô & chỉ số công bằng Jain.
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("##### 📱 Trải Nghiệm Trên Mobile")
    web_url = "https://n8thongtindidonggk-jtfw3us2u2uv6mqukunczo.streamlit.app/"
    qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=200x200&data={web_url}"
    st.image(qr_url, caption="Quét QR mở trên điện thoại")

# ==============================================================================
# THANH ĐIỀU HƯỚNG ĐẦU TRANG (TOP NAVBAR)
# ==============================================================================
active_home = "active" if st.session_state.page == 'home' else ""
active_set = "active" if st.session_state.page == 'settings' else ""
active_res = "active" if st.session_state.page == 'results' else ""

st.markdown(f"""
<div class="top-navbar">
    <div class="nav-logo-frame">
        <div class="nav-logo-inner">
            <div class="nav-logo-text">CELL-FREE 6G</div>
            <div class="nav-logo-sub">NHÓM 08 • TELECOM</div>
        </div>
    </div>
    <div class="nav-links">
        <span class="nav-item {active_home}">TRANG CHỦ</span>
        <span class="nav-item {active_set}">CẤU HÌNH THAM SỐ</span>
        <span class="nav-item {active_res}">PHÂN TÍCH & ĐỒ THỊ</span>
    </div>
    <div style="display: flex; gap: 8px; flex-wrap: wrap;">
        <span class="nav-pill">3.5 GHz TDD</span>
        <span class="nav-pill">M={st.session_state.M} | K={st.session_state.K} | Nc={st.session_state.Nc} | {st.session_state.Pt}dBm</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ==============================================================================
# TRANG 1: MÀN HÌNH CHÍNH (HERO LANDING PAGE)
# ==============================================================================
if st.session_state.page == 'home':
    st.markdown("""
    <div class="hero-showcase">
        <div class="hero-orb-left"></div>
        <div class="hero-orb-right"></div>
        <h1 class="hero-main-title">Cell-Free 6G</h1>
        <div class="hero-script-sub">Kiến tạo mạng không dây đồng nhất, xóa bỏ mọi ranh giới ô mạng.</div>
        <p class="hero-desc">
            Hệ thống mô phỏng chuyên sâu kiến trúc <b>Cell-Free Massive MIMO</b> cho thế hệ mạng 6G —
            nơi các điểm truy cập (AP) phân tán phối hợp phát sóng đồng pha theo cụm phục vụ lấy người dùng làm trung tâm (User-Centric),
            loại bỏ nhiễu biên ô và mang lại tốc độ phổ công bằng vượt trội so với mạng Cellular tập trung.
        </p>
        <div class="hero-icon-grid">
            <div class="hero-icon-item">
                <svg class="hero-icon-svg" viewBox="0 0 24 24" fill="none" stroke="#a3e635" stroke-width="1.6">
                    <circle cx="12" cy="12" r="9"/>
                    <ellipse cx="12" cy="12" rx="4.2" ry="9"/>
                    <line x1="3.5" y1="9" x2="20.5" y2="9"/>
                    <line x1="3.5" y1="15" x2="20.5" y2="15"/>
                </svg>
                <div class="hero-icon-title">Distributed APs</div>
                <div class="hero-icon-caption">Trải đều 20–100 điểm truy cập<br>trên toàn vùng phủ sóng</div>
            </div>
            <div class="hero-icon-item">
                <svg class="hero-icon-svg" viewBox="0 0 24 24" fill="none" stroke="#a3e635" stroke-width="1.6">
                    <path d="M4.9 19.1C1 15.2 1 8.8 4.9 4.9"/>
                    <path d="M7.8 16.2c-2.3-2.3-2.3-6.1 0-8.5"/>
                    <circle cx="12" cy="12" r="2"/>
                    <path d="M16.2 7.8c2.3 2.3 2.3 6.1 0 8.5"/>
                    <path d="M19.1 4.9C23 8.8 23 15.1 19.1 19"/>
                </svg>
                <div class="hero-icon-title">User-Centric Serving</div>
                <div class="hero-icon-caption">Phối hợp búp sóng đồng pha<br>theo cụm AP tối ưu (Nc)</div>
            </div>
            <div class="hero-icon-item">
                <svg class="hero-icon-svg" viewBox="0 0 24 24" fill="none" stroke="#a3e635" stroke-width="1.6">
                    <path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/>
                    <polyline points="3.27 6.96 12 12.01 20.73 6.96"/>
                    <line x1="12" y1="22.08" x2="12" y2="12"/>
                </svg>
                <div class="hero-icon-title">Iso-Contour & 3D Field</div>
                <div class="hero-icon-caption">Quy hoạch trường đẳng thế sóng<br>& địa hình năng lượng 3D</div>
            </div>
            <div class="hero-icon-item">
                <svg class="hero-icon-svg" viewBox="0 0 24 24" fill="none" stroke="#a3e635" stroke-width="1.6">
                    <path d="M12 20V10"/>
                    <path d="M18 20V4"/>
                    <path d="M6 20v-6"/>
                    <circle cx="18" cy="4" r="1.5"/>
                    <circle cx="12" cy="10" r="1.5"/>
                    <circle cx="6" cy="14" r="1.5"/>
                </svg>
                <div class="hero-icon-title">Jain's Fairness</div>
                <div class="hero-icon-caption">Tối ưu tốc độ biên 5%-Rate<br>và độ công bằng phổ tần</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    _, col_btn, _ = st.columns([1.1, 1.1, 1.1])
    with col_btn:
        if st.button("🚀 BẮT ĐẦU CẤU HÌNH HỆ THỐNG", type="primary"):
            st.toast("⚙️ Đang mở Bàn Điều Khiển Tham Số Mạng 6G...", icon="📡")
            switch_page('settings')
            st.rerun()

# ==============================================================================
# TRANG 2: BÀN ĐIỀU KHIỂN THAM SỐ (CHUẨN HÓA 20–100 AP & 5–20 UE)
# ==============================================================================
elif st.session_state.page == 'settings':
    st.markdown("<h2 style='text-align: center; margin-bottom: 4px; font-size: 2rem;'>⚙️ Bàn Điều Khiển Tham Số Mạng 6G</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #cbd5e1; margin-bottom: 20px; font-family: Playfair Display, serif; font-style: italic; font-size: 1.15rem;'>Tuân thủ phạm vi chuẩn (20–100 AP, 5–20 UE) và tùy biến cụm phục vụ User-Centric</p>", unsafe_allow_html=True)
    
    with st.container(border=True):
        st.markdown("##### ⚡ Kịch Bản Thử Nghiệm Nhanh (Preset Scenarios)")
        p1, p2, p3 = st.columns(3)
        with p1:
            if st.button("📌 Tiêu Chuẩn Giữa Kỳ (M=64, K=15)"):
                st.session_state.M, st.session_state.K, st.session_state.Nc, st.session_state.L, st.session_state.Pt = 64, 15, 5, 1000, 23
                st.toast("📌 Đã nạp cấu hình Tiêu Chuẩn Giữa Kỳ (M=64, K=15, Nc=5)!", icon="✅")
                st.rerun()
            st.caption("Vùng phủ 1000m × 1000m • Cụm Nc=5 AP • Công suất 23 dBm")
        with p2:
            if st.button("🏙️ Tải Cao Đô Thị (M=100, K=20)"):
                st.session_state.M, st.session_state.K, st.session_state.Nc, st.session_state.L, st.session_state.Pt = 100, 20, 8, 800, 23
                st.toast("🏙️ Đã nạp cấu hình Tải Cao Đô Thị (M=100, K=20, Nc=8)!", icon="⚡")
                st.rerun()
            st.caption("Vùng phủ 800m × 800m • Cụm Nc=8 AP • Mật độ cực đại")
        with p3:
            if st.button("🌾 Thưa Thớt Ngoại Ô (M=32, K=8)"):
                st.session_state.M, st.session_state.K, st.session_state.Nc, st.session_state.L, st.session_state.Pt = 32, 8, 3, 1400, 30
                st.toast("🌾 Đã nạp cấu hình Thưa Thớt Ngoại Ô (M=32, K=8, Nc=3)!", icon="📡")
                st.rerun()
            st.caption("Vùng phủ 1400m × 1400m • Cụm Nc=3 AP • Công suất 30 dBm")

    c_ap, c_ue = st.columns(2)
    with c_ap:
        with st.container(border=True):
            st.markdown("#### 📡 Hạ Tầng Điểm Truy Cập (AP)")
            st.session_state.M = st.slider("Mật độ AP phân tán (M: 20–100)", 20, 100, value=min(max(st.session_state.M, 20), 100), step=4)
            st.session_state.Nc = st.slider("Kích thước cụm phục vụ User-Centric (Nc)", 2, 12, value=min(max(st.session_state.Nc, 2), 12), step=1)
            st.session_state.L = st.number_input("Kích thước vùng phủ L × L (mét)", 500, 2000, value=st.session_state.L, step=100)
            area_km2 = (st.session_state.L / 1000.0) ** 2
            st.markdown(f"<div class='stat-banner'>📐 Diện tích: <b>{area_km2:.2f} km²</b> • Mật độ: <b>{st.session_state.M / area_km2:.0f} APs/km²</b> • Cụm phục vụ: <b>{st.session_state.Nc} AP/UE</b></div>", unsafe_allow_html=True)

    with c_ue:
        with st.container(border=True):
            st.markdown("#### 📱 Thiết Bị Người Dùng (UE)")
            st.session_state.K = st.slider("Số lượng người dùng đồng thời (K: 5–20)", 5, 20, value=min(max(st.session_state.K, 5), 20), step=1)
            st.session_state.Pt = st.number_input("Công suất phát mỗi AP (dBm)", 10, 40, value=st.session_state.Pt, step=1)
            pt_mw = 10.0 ** (st.session_state.Pt / 10.0)
            st.markdown(f"<div class='stat-banner'>⚡ Tỷ lệ Massive MIMO: <b>{st.session_state.M / st.session_state.K:.1f} AP / UE</b> • Công suất bức xạ: <b>{pt_mw:.0f} mW</b></div>", unsafe_allow_html=True)

    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
    col_b1, col_run, col_b2 = st.columns([0.8, 1.4, 0.8])
    with col_b1:
        if st.button("🏠 Về Trang Chủ"):
            switch_page('home')
            st.rerun()
    with col_run:
        if st.button("⚡ KHỞI CHẠY GIẢI TÍCH & XUẤT KẾT QUẢ", type="primary"):
            st.toast("🚀 Đang tổng hợp búp sóng & nội suy trường đẳng thế 6G!", icon="⚡")
            switch_page('results')
            st.rerun()

# ==============================================================================
# TRANG 3: BÁO CÁO KẾT QUẢ & PHÂN TÍCH (3 CHẾ ĐỘ CHUYÊN SÂU)
# ==============================================================================
elif st.session_state.page == 'results':
    
    (
        ap_c, ue_c, beta_cf, dist_cf,
        rates_cf, rates_cell, sinr_cf, sinr_cell,
        jain_cf, jain_cell, gx, gy, field_cf_dbm, field_cell_dbm
    ) = run_cf_simulation(
        st.session_state.M, st.session_state.K, st.session_state.Nc,
        st.session_state.L, st.session_state.Pt, st.session_state.sim_seed
    )

    if st.session_state.selected_ue >= st.session_state.K:
        st.session_state.selected_ue = 0
    
    nav1, nav2, nav3, nav_reroll, nav_back = st.columns([1.05, 1.15, 1.05, 0.85, 0.75])
    with nav1:
        if st.button("📍 VỊ TRÍ & BÚP SÓNG", type="primary" if st.session_state.view_mode == 'map' else "secondary"):
            st.session_state.view_mode = 'map'
            st.rerun()
    with nav2:
        if st.button("🌊 TRƯỜNG PHỦ SÓNG", type="primary" if st.session_state.view_mode == 'coverage' else "secondary"):
            st.session_state.view_mode = 'coverage'
            st.rerun()
    with nav3:
        if st.button("📈 ĐỒ THỊ TỐC ĐỘ (CDF)", type="primary" if st.session_state.view_mode == 'chart' else "secondary"):
            st.session_state.view_mode = 'chart'
            st.rerun()
    with nav_reroll:
        if st.button("🎲 Sinh Tọa Độ Mới"):
            st.session_state.sim_seed = int(np.random.randint(1, 999999))
            st.toast(f"🎲 Đã sinh ngẫu nhiên ma trận tọa độ mới (Seed #{st.session_state.sim_seed})!", icon="✨")
            st.rerun()
    with nav_back:
        if st.button("⚙️ Tham Số"):
            switch_page('settings')
            st.rerun()

    # --------------------------------------------------------------------------
    # CHẾ ĐỘ 1: BẢN ĐỒ KHÔNG GIAN & BEAMFORMING ĐỘNG (KẾT HỢP ĐƯỜNG ĐẲNG THẾ MỜ)
    # --------------------------------------------------------------------------
    if st.session_state.view_mode == 'map':
        with st.container(border=True):
            head_col, select_col = st.columns([2.2, 1])
            with head_col:
                st.markdown(f"<h3 style='margin:0;'>📍 Bản Đồ Cụm Phục Vụ User-Centric ({st.session_state.M} APs / {st.session_state.K} UEs / Cụm Nc={st.session_state.Nc})</h3>", unsafe_allow_html=True)
                st.caption("Chọn thiết bị người dùng (UE) ở ô bên phải để quan sát cụm AP mạnh nhất hợp tác phát sóng đồng pha.")
            with select_col:
                ue_opts = [f"Đang khảo sát: UE #{i+1}" for i in range(st.session_state.K)]
                selected_str = st.selectbox("Chọn UE khảo sát:", ue_opts, index=st.session_state.selected_ue, label_visibility="collapsed")
                st.session_state.selected_ue = int(selected_str.split('#')[1]) - 1

            k_idx = st.session_state.selected_ue
            nc_eff = min(st.session_state.Nc, st.session_state.M)
            top_serving_aps = np.argsort(beta_cf[:, k_idx])[-nc_eff:]
            min_dist = np.min(dist_cf[:, k_idx])
            ue_sinr_db = 10 * np.log10(sinr_cf[k_idx] + 1e-15)
            srv_list = ", ".join([f"AP #{idx+1}" for idx in top_serving_aps])

            st.markdown(f"""
            <div class="kpi-grid" style="margin-top: 10px;">
                <div class="kpi-card" style="border-top: 3px solid #38bdf8;">
                    <div class="kpi-label">THIẾT BỊ ĐANG KHẢO SÁT</div>
                    <div class="kpi-value" style="color: #38bdf8;">UE #{k_idx+1}</div>
                    <div class="kpi-sub">Tọa độ: ({ue_c[k_idx, 0]:.1f}m, {ue_c[k_idx, 1]:.1f}m)</div>
                </div>
                <div class="kpi-card" style="border-top: 3px solid #a3e635;">
                    <div class="kpi-label">CỤM {nc_eff} AP PHỤC VỤ MẠNH NHẤT</div>
                    <div class="kpi-value" style="color: #a3e635; font-size: 1.12rem; padding-top: 5px;">{srv_list}</div>
                    <div class="kpi-sub">AP vật lý gần nhất: {min_dist:.1f} m</div>
                </div>
                <div class="kpi-card" style="border-top: 3px solid #c084fc;">
                    <div class="kpi-label">SINR THU TẠI UE #{k_idx+1}</div>
                    <div class="kpi-value" style="color: #c084fc;">{ue_sinr_db:.2f} <span style="font-size: 0.85rem;">dB</span></div>
                    <div class="kpi-sub">Conjugate Beamforming ({nc_eff} APs)</div>
                </div>
                <div class="kpi-card" style="border-top: 3px solid #fbbf24;">
                    <div class="kpi-label">TỐC ĐỘ PHỔ TẠI UE #{k_idx+1}</div>
                    <div class="kpi-value" style="color: #fbbf24;">{rates_cf[k_idx]:.3f} <span style="font-size: 0.85rem;">bps/Hz</span></div>
                    <div class="kpi-sub">Cellular cùng vị trí: {rates_cell[k_idx]:.3f} bps/Hz</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            fig_map = go.Figure()

            # Lớp nền đường đồng mức sóng nhẹ (Subtle Iso-lines) giúp bản đồ có chiều sâu kỹ thuật
            fig_map.add_trace(go.Contour(
                x=gx, y=gy, z=field_cf_dbm,
                contours=dict(coloring='lines', showlabels=True, labelfont=dict(size=10, color='#64748b')),
                line=dict(width=1, dash='dot'),
                colorscale='Tealgrn',
                opacity=0.35,
                showscale=False,
                hoverinfo='skip',
                name='Đường đẳng thế sóng'
            ))

            # Tia Beamforming xanh dương đậm nét đứt
            for ap_idx in top_serving_aps:
                fig_map.add_trace(go.Scatter(
                    x=[ap_c[ap_idx, 0], ue_c[k_idx, 0]],
                    y=[ap_c[ap_idx, 1], ue_c[k_idx, 1]],
                    mode='lines',
                    line=dict(color='#0284c7', width=2.8, dash='dash'),
                    hoverinfo='skip',
                    showlegend=False
                ))

            # AP thông thường
            other_aps = [i for i in range(st.session_state.M) if i not in top_serving_aps]
            fig_map.add_trace(go.Scatter(
                x=ap_c[other_aps, 0], y=ap_c[other_aps, 1],
                mode='markers',
                marker=dict(symbol='triangle-up', size=11, color='#ef4444', opacity=0.78, line=dict(color='#991b1b', width=0.9)),
                name='AP Phân tán (Ngoài cụm)',
                hovertemplate='<b>AP #%{text}</b><br>Tọa độ: (%{x:.1f}m, %{y:.1f}m)<extra></extra>',
                text=[str(i+1) for i in other_aps]
            ))

            # Cụm AP phục vụ
            fig_map.add_trace(go.Scatter(
                x=ap_c[top_serving_aps, 0], y=ap_c[top_serving_aps, 1],
                mode='markers+text',
                marker=dict(symbol='triangle-up', size=18, color='#f59e0b', line=dict(color='#0f172a', width=2)),
                name=f'Cụm AP Phục Vụ (Top {nc_eff})',
                text=[f"AP #{i+1}" for i in top_serving_aps],
                textposition="bottom center",
                textfont=dict(size=11, color='#b45309', family='JetBrains Mono'),
                hovertemplate='<b>AP Phục vụ #%{text}</b><br>Tọa độ: (%{x:.1f}m, %{y:.1f}m)<extra></extra>'
            ))

            # UE thông thường
            other_ues = [i for i in range(st.session_state.K) if i != k_idx]
            fig_map.add_trace(go.Scatter(
                x=ue_c[other_ues, 0], y=ue_c[other_ues, 1],
                mode='markers',
                marker=dict(symbol='circle', size=9, color='#475569', opacity=0.85, line=dict(color='#ffffff', width=1)),
                name='Thiết bị UE khác',
                hovertemplate='<b>UE #%{text}</b><br>Tọa độ: (%{x:.1f}m, %{y:.1f}m)<br>Tốc độ: %{customdata:.3f} bps/Hz<extra></extra>',
                text=[str(i+1) for i in other_ues],
                customdata=rates_cf[other_ues]
            ))

            # UE khảo sát
            fig_map.add_trace(go.Scatter(
                x=[ue_c[k_idx, 0]], y=[ue_c[k_idx, 1]],
                mode='markers+text',
                marker=dict(symbol='circle', size=19, color='#0284c7', line=dict(color='#0f172a', width=2.5)),
                name=f'UE Đang Khảo Sát (#{k_idx+1})',
                text=[f"UE #{k_idx+1}"],
                textposition="top center",
                textfont=dict(size=12, color='#0369a1', family='JetBrains Mono'),
                hovertemplate=f'<b>UE #{k_idx+1}</b><br>Tốc độ: {rates_cf[k_idx]:.3f} bps/Hz<extra></extra>'
            ))

            fig_map.update_layout(
                template='plotly_white',
                paper_bgcolor='#ffffff',
                plot_bgcolor='#ffffff',
                font=dict(family='Plus Jakarta Sans, sans-serif', color='#0f172a', size=12),
                height=460,
                margin=dict(l=20, r=20, t=20, b=20),
                xaxis=dict(
                    title=dict(text="Tọa độ không gian X (mét)", font=dict(color="#0f172a", size=13)),
                    tickfont=dict(color="#0f172a", size=12),
                    showgrid=True, gridcolor='#e2e8f0', zeroline=False, linecolor='#64748b', mirror=True,
                    range=[-25, st.session_state.L + 25]
                ),
                yaxis=dict(
                    title=dict(text="Tọa độ không gian Y (mét)", font=dict(color="#0f172a", size=13)),
                    tickfont=dict(color="#0f172a", size=12),
                    showgrid=True, gridcolor='#e2e8f0', zeroline=False, linecolor='#64748b', mirror=True,
                    range=[-25, st.session_state.L + 25]
                ),
                legend=dict(
                    orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0.0,
                    bgcolor="#f8fafc", bordercolor="#cbd5e1", borderwidth=1.5,
                    font=dict(color="#0f172a", size=12)
                )
            )
            st.plotly_chart(fig_map, use_container_width=True, theme=None)

        st.markdown(f"""
        <div class="insight-card">
            <p style="margin: 0 0 8px 0; font-weight: 800; font-size: 1rem; color: #a3e635;">
                📡 ĐÁNH GIÁ CỤM PHỤC VỤ LẤY NGƯỜI DÙNG LÀM TRUNG TÂM (USER-CENTRIC SERVING) — UE #{k_idx+1}:
            </p>
            <ul style="margin: 0; padding-left: 20px; line-height: 1.75;">
                <li><b>Vị trí & Cự ly:</b> Thiết bị nằm tại tọa độ <code>({ue_c[k_idx, 0]:.1f}m, {ue_c[k_idx, 1]:.1f}m)</code>, cách điểm truy cập vật lý gần nhất <b>{min_dist:.1f} m</b>.</li>
                <li><b>Cụm phục vụ động ({nc_eff} AP):</b> Tập hợp <b>{srv_list}</b> có hệ số kênh truyền lớn nhất tự động hình thành cụm búp sóng liên hợp (Conjugate Beamforming).</li>
                <li><b>Phân tập vĩ mô (Macro-Diversity):</b> Thu sóng đồng thời từ {nc_eff} hướng độc lập giúp bù đắp suy hao vật cản (Shadowing 8 dB) và xóa bỏ điểm mù tín hiệu.</li>
                <li><b>Chất lượng thu thực tế:</b> Đạt <b>SINR = {ue_sinr_db:.2f} dB</b> và tốc độ phổ <b>{rates_cf[k_idx]:.3f} bps/Hz</b> (vượt xa mạng Cellular tập trung chỉ đạt <b>{rates_cell[k_idx]:.3f} bps/Hz</b>).</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    # --------------------------------------------------------------------------
    # CHẾ ĐỘ 2: TRƯỜNG CƯỜNG ĐỘ PHỦ SÓNG (SMOOTH ISO-CONTOUR & ĐỊA HÌNH 3D)
    # --------------------------------------------------------------------------
    elif st.session_state.view_mode == 'coverage':
        with st.container(border=True):
            c_title, c_mode = st.columns([2.1, 1.2])
            with c_title:
                st.markdown(f"<h3 style='margin:0;'>🌊 Mô Phỏng Trường Cường Độ Phủ Sóng Vô Tuyến ({st.session_state.M} APs)</h3>", unsafe_allow_html=True)
                st.caption("Nội suy trường điện từ liên tục (Iso-Contour) và địa hình năng lượng 3D — không dùng lưới pixel rời rạc.")
            with c_mode:
                style_opts = [
                    "🗺️ Bản Đồ Đẳng Thế Sóng (Iso-Contour)",
                    "🏔️ Địa Hình Trường Năng Lượng 3D (Surface)"
                ]
                chosen_style = st.selectbox(
                    "Chế độ hiển thị trường sóng:",
                    style_opts,
                    index=0 if st.session_state.cov_style == 'contour' else 1,
                    label_visibility="collapsed"
                )
                st.session_state.cov_style = 'contour' if "Iso-Contour" in chosen_style else '3d'

            min_cf, max_cf, mean_cf = float(np.min(field_cf_dbm)), float(np.max(field_cf_dbm)), float(np.mean(field_cf_dbm))
            min_cell = float(np.min(field_cell_dbm))
            cov_above_75 = float(np.mean(field_cf_dbm >= -75.0) * 100.0)

            st.markdown(f"""
            <div class="kpi-grid" style="margin-top: 10px;">
                <div class="kpi-card" style="border-top: 3px solid #a3e635;">
                    <div class="kpi-label">MỨC THU TRUNG BÌNH TOÀN MẠNG</div>
                    <div class="kpi-value" style="color: #a3e635;">{mean_cf:.1f} <span style="font-size: 0.85rem;">dBm</span></div>
                    <div class="kpi-sub">Đỉnh bức xạ: {max_cf:.1f} dBm</div>
                </div>
                <div class="kpi-card" style="border-top: 3px solid #38bdf8;">
                    <div class="kpi-label">CƯỜNG ĐỘ TẠI BIÊN (CELL-FREE)</div>
                    <div class="kpi-value" style="color: #38bdf8;">{min_cf:.1f} <span style="font-size: 0.85rem;">dBm</span></div>
                    <div class="kpi-sub">Cellular tại biên sụt còn: {min_cell:.1f} dBm</div>
                </div>
                <div class="kpi-card" style="border-top: 3px solid #c084fc;">
                    <div class="kpi-label">ĐỘ ĐỒNG ĐỀU TRƯỜNG SÓNG</div>
                    <div class="kpi-value" style="color: #c084fc;">±{np.std(field_cf_dbm):.1f} <span style="font-size: 0.85rem;">dB</span></div>
                    <div class="kpi-sub">Cellular lệch chuẩn: ±{np.std(field_cell_dbm):.1f} dB</div>
                </div>
                <div class="kpi-card" style="border-top: 3px solid #fbbf24;">
                    <div class="kpi-label">DIỆN TÍCH PHỦ SÓNG TỐT (≥ -75 dBm)</div>
                    <div class="kpi-value" style="color: #fbbf24;">{cov_above_75:.1f}<span style="font-size: 0.95rem;">%</span></div>
                    <div class="kpi-sub">Xóa bỏ hoàn toàn hố đen suy hao</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            if st.session_state.cov_style == 'contour':
                fig_cov = go.Figure()

                # Bản đồ Đẳng thế sóng nội suy mượt (Smooth Iso-Contour) chuẩn phần mềm quy hoạch RF
                fig_cov.add_trace(go.Contour(
                    x=gx, y=gy, z=field_cf_dbm,
                    colorscale='YlGnBu',
                    reversescale=True,
                    ncontours=22,
                    contours=dict(
                        coloring='heatmap',
                        showlabels=True,
                        labelfont=dict(size=11, color='#0f172a', family='JetBrains Mono')
                    ),
                    line=dict(color='rgba(15, 23, 42, 0.35)', width=1.1, smoothing=1.3),
                    colorbar=dict(
                        title=dict(text="Công suất thu (dBm)", font=dict(color="#0f172a", size=12)),
                        tickfont=dict(color="#0f172a", family='JetBrains Mono')
                    ),
                    hovertemplate='Tọa độ: (%{x:.0f}m, %{y:.0f}m)<br>Trường đẳng thế RSSI: <b>%{z:.1f} dBm</b><extra></extra>'
                ))

                # Đặt các trạm AP lên trên mặt phẳng đẳng thế
                fig_cov.add_trace(go.Scatter(
                    x=ap_c[:, 0], y=ap_c[:, 1],
                    mode='markers',
                    marker=dict(symbol='triangle-up', size=10, color='#ffffff', line=dict(color='#0f172a', width=1.5)),
                    name='Điểm truy cập AP',
                    hovertemplate='<b>AP #%{text}</b><br>Tọa độ: (%{x:.1f}m, %{y:.1f}m)<extra></extra>',
                    text=[str(i+1) for i in range(st.session_state.M)]
                ))

                # Đặt thiết bị UE lên bản đồ
                fig_cov.add_trace(go.Scatter(
                    x=ue_c[:, 0], y=ue_c[:, 1],
                    mode='markers+text',
                    marker=dict(symbol='circle', size=11, color='#ef4444', line=dict(color='#ffffff', width=2)),
                    text=[f"U{i+1}" for i in range(st.session_state.K)],
                    textposition="top center",
                    textfont=dict(size=10, color='#991b1b', family='JetBrains Mono'),
                    name='Thiết bị UE',
                    hovertemplate='<b>UE #%{text}</b><br>Tốc độ: %{customdata:.2f} bps/Hz<extra></extra>',
                    customdata=rates_cf
                ))

                fig_cov.update_layout(
                    template='plotly_white',
                    paper_bgcolor='#ffffff',
                    plot_bgcolor='#ffffff',
                    font=dict(family='Plus Jakarta Sans, sans-serif', color='#0f172a', size=12),
                    height=460,
                    margin=dict(l=20, r=20, t=25, b=20),
                    xaxis=dict(
                        title=dict(text="Tọa độ không gian X (mét)", font=dict(color="#0f172a", size=13)),
                        tickfont=dict(color="#0f172a", size=12),
                        range=[0, st.session_state.L], mirror=True, linecolor='#64748b'
                    ),
                    yaxis=dict(
                        title=dict(text="Tọa độ không gian Y (mét)", font=dict(color="#0f172a", size=13)),
                        tickfont=dict(color="#0f172a", size=12),
                        range=[0, st.session_state.L], mirror=True, linecolor='#64748b'
                    ),
                    legend=dict(
                        orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0.0,
                        bgcolor="#f8fafc", bordercolor="#cbd5e1", borderwidth=1.5,
                        font=dict(color="#0f172a", size=12)
                    )
                )
                st.plotly_chart(fig_cov, use_container_width=True, theme=None)

            else:
                # Mô hình Địa hình Trường Năng Lượng 3D (So sánh trực quan Cao nguyên Cell-Free vs Đỉnh đơn Cellular)
                fig_3d = go.Figure()

                fig_3d.add_trace(go.Surface(
                    x=gx, y=gy, z=field_cf_dbm,
                    colorscale='Viridis',
                    name='Cell-Free 6G (Phân tán)',
                    colorbar=dict(
                        title=dict(text="Cell-Free (dBm)", font=dict(color="#0f172a", size=11)),
                        tickfont=dict(color="#0f172a"),
                        x=1.02
                    ),
                    contours=dict(
                        z=dict(show=True, usecolormap=True, highlightcolor="#a3e635", project_z=True)
                    ),
                    hovertemplate='<b>Cell-Free 6G</b><br>X: %{x:.0f}m | Y: %{y:.0f}m<br>Mức thu: <b>%{z:.1f} dBm</b><extra></extra>'
                ))

                fig_3d.add_trace(go.Surface(
                    x=gx, y=gy, z=field_cell_dbm,
                    colorscale='Hot',
                    opacity=0.55,
                    showscale=False,
                    name='Cellular Cổ Điển (Trạm tâm)',
                    hovertemplate='<b>Cellular Trạm Tâm</b><br>X: %{x:.0f}m | Y: %{y:.0f}m<br>Mức thu: <b>%{z:.1f} dBm</b><extra></extra>'
                ))

                fig_3d.update_layout(
                    template='plotly_white',
                    paper_bgcolor='#ffffff',
                    font=dict(family='Plus Jakarta Sans, sans-serif', color='#0f172a', size=12),
                    height=470,
                    margin=dict(l=10, r=10, t=15, b=10),
                    scene=dict(
                        xaxis=dict(title='Trục X (m)', backgroundcolor='#f8fafc', gridcolor='#cbd5e1'),
                        yaxis=dict(title='Trục Y (m)', backgroundcolor='#f8fafc', gridcolor='#cbd5e1'),
                        zaxis=dict(title='Công suất thu RSSI (dBm)', backgroundcolor='#f1f5f9', gridcolor='#cbd5e1'),
                        camera=dict(eye=dict(x=1.55, y=1.45, z=0.95))
                    )
                )
                st.plotly_chart(fig_3d, use_container_width=True, theme=None)

        st.markdown(f"""
        <div class="insight-card">
            <p style="margin: 0 0 8px 0; font-weight: 800; font-size: 1rem; color: #a3e635;">
                🌊 PHÂN TÍCH TRƯỜNG ĐẲNG THẾ & ĐỊA HÌNH NĂNG LƯỢNG VÔ TUYẾN (RF COVERAGE TOPOGRAPHY):
            </p>
            <ul style="margin: 0; padding-left: 20px; line-height: 1.75;">
                <li><b>Đường đồng mức đẳng thế (Iso-Contour):</b> Thay vì chia ô vuông pixel rời rạc, các đường đồng mức nội suy chính xác ranh giới suy hao công suất (từ <b>{max_cf:.1f} dBm</b> tại tâm cụm AP đến <b>{min_cf:.1f} dBm</b> tại vùng giao thoa).</li>
                <li><b>Hiệu ứng "Cao nguyên năng lượng" (3D Surface):</b> Trên đồ thị 3D, kiến trúc Cell-Free tạo thành một mặt phẳng năng lượng cao và ổn định trên khắp không gian {st.session_state.L}×{st.session_state.L}m, trái ngược hoàn toàn với mạng Cellular (lớp lưới cam mờ) chỉ nhọn ở tâm và sụt sâu xuống <b>{min_cell:.1f} dBm</b> ở rìa.</li>
                <li><b>Triệt tiêu điểm mù (Dead-Zone Elimination):</b> Nhờ {st.session_state.M} AP phân tán kết hợp cụm $N_c={st.session_state.Nc}$, <b>{cov_above_75:.1f}%</b> diện tích mạng đạt ngưỡng thu mạnh $\\ge -75\\text{{ dBm}}$.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    # --------------------------------------------------------------------------
    # CHẾ ĐỘ 3: ĐỒ THỊ CDF & ĐÁNH GIÁ TÍNH CÔNG BẰNG (NỀN TRẮNG TƯƠNG PHẢN CAO)
    # --------------------------------------------------------------------------
    elif st.session_state.view_mode == 'chart':
        rate_5_cf = float(np.percentile(rates_cf, 5))
        rate_5_cell = float(np.percentile(rates_cell, 5))
        mean_sinr_cf_db = 10 * np.log10(np.mean(sinr_cf) + 1e-15)
        mean_rate_cf = float(np.mean(rates_cf))
        mean_rate_cell = float(np.mean(rates_cell))

        st.markdown(f"""
        <div class="kpi-grid">
            <div class="kpi-card" style="border-top: 3px solid #a3e635;">
                <div class="kpi-label">5%-USER RATE (BIÊN MẠNG)</div>
                <div class="kpi-value" style="color: #a3e635;">{rate_5_cf:.3f} <span style="font-size: 0.82rem; color: #94a3b8;">bps/Hz</span></div>
                <div class="kpi-sub">Cellular đối chứng: <b>{rate_5_cell:.3f} bps/Hz</b></div>
            </div>
            <div class="kpi-card" style="border-top: 3px solid #38bdf8;">
                <div class="kpi-label">JAIN'S FAIRNESS INDEX (J)</div>
                <div class="kpi-value" style="color: #38bdf8;">{jain_cf:.3f} <span style="font-size: 0.82rem; color: #94a3b8;">/ 1.000</span></div>
                <div class="kpi-sub">Cellular đối chứng: <b>{jain_cell:.3f}</b></div>
            </div>
            <div class="kpi-card" style="border-top: 3px solid #c084fc;">
                <div class="kpi-label">SINR TRUNG BÌNH (Nc={st.session_state.Nc})</div>
                <div class="kpi-value" style="color: #c084fc;">{mean_sinr_cf_db:.1f} <span style="font-size: 0.82rem; color: #94a3b8;">dB</span></div>
                <div class="kpi-sub">Độ lợi phân tập không gian cao</div>
            </div>
            <div class="kpi-card" style="border-top: 3px solid #fbbf24;">
                <div class="kpi-label">TỐC ĐỘ PHỔ TRUNG BÌNH</div>
                <div class="kpi-value" style="color: #fbbf24;">{mean_rate_cf:.3f} <span style="font-size: 0.82rem; color: #94a3b8;">bps/Hz</span></div>
                <div class="kpi-sub">Cellular đối chứng: <b>{mean_rate_cell:.3f} bps/Hz</b></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        with st.container(border=True):
            st.markdown("<h3 style='margin:0 0 4px 0;'>📈 Đồ Thị Phân Phối Tích Lũy (CDF) Hiệu Suất Phổ Người Dùng</h3>", unsafe_allow_html=True)
            st.caption("Đường cong càng dịch sang phải và dốc đứng chứng tỏ tốc độ toàn mạng càng cao và đồng đều giữa mọi người dùng.")

            fig_cdf = go.Figure()
            cdf_y = np.arange(1, st.session_state.K + 1) / st.session_state.K

            fig_cdf.add_trace(go.Scatter(
                x=np.sort(rates_cf), y=cdf_y, mode='lines+markers',
                name=f'Cell-Free 6G User-Centric (Nc={st.session_state.Nc} AP/UE)',
                line=dict(color='#16a34a', width=3.5),
                marker=dict(size=7, color='#15803d', line=dict(color='#ffffff', width=1)),
                hovertemplate='<b>Cell-Free 6G</b><br>Tốc độ: %{x:.3f} bps/Hz<br>Xác suất CDF: %{y:.2f}<extra></extra>'
            ))
            fig_cdf.add_trace(go.Scatter(
                x=np.sort(rates_cell), y=cdf_y, mode='lines+markers',
                name='Cellular MIMO Cổ Điển (Trạm tâm đồng vị trí)',
                line=dict(color='#f59e0b', width=3, dash='dot'),
                marker=dict(size=6, color='#d97706'),
                hovertemplate='<b>Cellular Cổ Điển</b><br>Tốc độ: %{x:.3f} bps/Hz<br>Xác suất CDF: %{y:.2f}<extra></extra>'
            ))
            fig_cdf.add_hline(
                y=0.05,
                line_dash="dash",
                line_color="#dc2626",
                line_width=1.8,
                annotation_text="Ngưỡng 5%-User Rate (Outage Threshold)",
                annotation_position="top right",
                annotation_font=dict(color="#b91c1c", size=12)
            )

            fig_cdf.update_layout(
                template='plotly_white',
                paper_bgcolor='#ffffff',
                plot_bgcolor='#ffffff',
                font=dict(family='Plus Jakarta Sans, sans-serif', color='#0f172a', size=12),
                height=420,
                margin=dict(l=20, r=20, t=25, b=20),
                xaxis=dict(
                    title=dict(text="Hiệu suất phổ người dùng — Spectral Efficiency (bps/Hz)", font=dict(color="#0f172a", size=13)),
                    tickfont=dict(color="#0f172a", size=12),
                    showgrid=True, gridcolor='#e2e8f0', zeroline=False, linecolor='#64748b', mirror=True
                ),
                yaxis=dict(
                    title=dict(text="Xác suất tích lũy CDF — P(Rate ≤ x)", font=dict(color="#0f172a", size=13)),
                    tickfont=dict(color="#0f172a", size=12),
                    showgrid=True, gridcolor='#e2e8f0', zeroline=False, linecolor='#64748b', mirror=True,
                    range=[0, 1.06]
                ),
                legend=dict(
                    orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0.0,
                    bgcolor="#f8fafc", bordercolor="#cbd5e1", borderwidth=1.5,
                    font=dict(color="#0f172a", size=12)
                )
            )
            st.plotly_chart(fig_cdf, use_container_width=True, theme=None)

        st.markdown(f"""
        <div class="insight-card">
            <p style="margin: 0 0 8px 0; font-weight: 800; font-size: 1rem; color: #a3e635;">
                ⚖️ ĐÁNH GIÁ HIỆU NĂNG PHỔ TẦN & TÍNH CÔNG BẰNG HỆ THỐNG (FAIRNESS BENCHMARK):
            </p>
            <ul style="margin: 0; padding-left: 20px; line-height: 1.75;">
                <li><b>5%-User Rate (Biên mạng):</b> Đạt <b>{rate_5_cf:.3f} bps/Hz</b> trên Cell-Free 6G với cụm $N_c={st.session_state.Nc}$ AP (Cellular cổ điển chỉ đạt <b>{rate_5_cell:.3f} bps/Hz</b>).</li>
                <li><b>Jain's Fairness Index:</b> Đạt <b>J = {jain_cf:.3f} / 1.000</b> (Cellular cổ điển đạt <b>{jain_cell:.3f}</b>), khẳng định tài nguyên được chia đều cho mọi UE.</li>
                <li><b>Độ dốc đường CDF:</b> Đường cong Cell-Free màu xanh lá đậm dốc đứng về bên phải, chứng minh chất lượng dịch vụ đồng nhất trên toàn vùng phủ.</li>
                <li><b>Tổng thể toàn mạng:</b> Tốc độ phổ trung bình đạt <b>{mean_rate_cf:.3f} bps/Hz</b> | Mức thu trung bình đạt <b>{mean_sinr_cf_db:.1f} dB</b>.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)