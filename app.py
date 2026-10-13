#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Sistem Informasi Perkembangan Siswa — Professional Edition"""
from flask import Flask, request, redirect, url_for, render_template_string, flash, Response
import sqlite3, os, secrets, csv, io, json

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'walimurid.db')

SCHOOL = {
    'name': 'SD Negeri Contoh',
    'address': 'Jl. Pendidikan No. 1, Kota Contoh',
    'npsn': '12345678',
    'logo': '\U0001F3DB',
    'year': '2025/2026',
    'headmaster': 'Drs. H. Ahmad Subarjo, M.Pd.',
}

ASPECTS = ['Membaca', 'Menulis', 'Berhitung', 'Menghafal']
ASPECT_SCORES = {'L': 90, 'CL': 80, 'KL': 70}
ASPECT_LABELS = {'L': 'Lancar', 'CL': 'Cukup Lancar', 'KL': 'Kurang Lancar', '': 'Belum dinilai'}
PERIODS = ['STS 1', 'STS 2', 'SAS']
CLASS_INFO = {
    '4B': {'wali': 'Siti Aminah, S.Pd.'},
    '4C': {'wali': 'Ahmad Fauzi, S.Pd.'},
    '4D': {'wali': 'Nur Hasanah, S.Pd.'},
}

SEED = {
    '4B': [
        ('ADZKIYA RARAS MAHFUDZA','CL','KL','L','L'),('ALMAIRA ZEA ACHMAD','CL','CL','L','L'),
        ('ANANDA SYIFA FATHIMATUZZAHRA','KL','CL','KL','KL'),('APRILIA RAFANIA','KL','KL','KL','CL'),
        ('ARUM BAHARI LUTHFIKA ALI','L','L','CL','CL'),('ARUM ZAHWA ALIFA','L','L','L','L'),
        ('AYRA ASKADINA SALSABILA','CL','CL','KL','KL'),('ELVINA AMIRA SALSABILA','KL','L','KL','KL'),
        ('EMBUN SEKAR ARUMINGRATRI','KL','KL','KL','KL'),('FITRIYA FATHIYYATURAHMA','CL','KL','KL','KL'),
        ('JANE CALISTA PUTRI','CL','KL','KL','KL'),('KAILA ZAFIRA','CL','KL','L','CL'),
        ('MAFAZA ILYANA PRAYUDI','CL','L','L','L'),('MARSA AZKA FITRIA','KL','CL','CL','L'),
        ('NAJMA ASHFA GAYATRI','CL','L','L','L'),('NESSA ARYANA TSURAYYA','L','KL','L','L'),
        ('YOLANDA SISILIA','L','L','L','L'),('ZIVANA ADZKIYA AULIA','KL','KL','KL','KL'),
    ],
    '4C': [
        ('ABDUL JALAL SAPUTRA','KL','KL','KL','KL'),('ABIDZAR DWIQI AL FATIH','KL','KL','KL','KL'),
        ('ADE ARVIE ASSLAM','','','',''),('AHMAD ATHALLA OKTAVIAN','CL','L','CL','L'),
        ('AHMAD BRILIANSYAH','L','KL','KL','KL'),('AHMAD FAIZ HUSAIN NAJIB','KL','KL','KL','KL'),
        ('AHMAD TAJ ATHIF','CL','CL','L','L'),('ALFA FALAQUN NAJAH','L','L','L','L'),
        ('ANDRYAN PRADIPTA','L','KL','KL','KL'),('ARKA WIJAYANTO','KL','L','CL','L'),
        ('ATHA RAQILLA KHALIF','KL','KL','L','L'),('HAIDAR FARUQ','CL','KL','L','L'),
        ('MUHAMMAD ABBAD NAILUN NABHAN','KL','KL','KL','KL'),('MUHAMMAD ASYRAF ABRORI','L','L','CL','CL'),
        ('MUHAMMAD DAVID NAJMI','KL','KL','KL','KL'),('MUHAMMAD FALAH AKBAR','L','KL','KL','KL'),
        ('MUHAMMAD HAWWIN ALAINA','KL','CL','L','L'),('MUHAMMAD KENZIE ARZIQI PUTRA','L','L','CL','L'),
        ('MUHAMMAD RAKHUL ABYAN AQIL','KL','L','L','L'),('MUHAMMAD SHOLAHUDDIN AL HADI','CL','L','L','L'),
        ('RAJA AHZA AHURAYAZDA','KL','KL','KL','CL'),('SATRIA WICAKSONO PUTRA RIFAN','L','KL','KL','KL'),
        ('YUSHFIKA ARFAN MAULANA','CL','KL','CL','L'),('YUSUF FATIH ARZAQI','KL','KL','KL','CL'),
        ('ZAIDAN ARIYANTO','KL','KL','KL','L'),
    ],
    '4D': [
        ('ABYAN SHIHAB PRANAJA','','','',''),('AHMAD FAIZUL MUIZ','L','L','L','L'),
        ('AHMAD FARIS HABIBI','KL','KL','KL','KL'),('AHMAD HISYAM MAULANA','CL','KL','KL','KL'),
        ('AHMAD MUGHNI LABIB','L','L','L','L'),('AHMAD ULIN NUHA','L','L','L','L'),
        ('ARCHANDRA SEAN ALFARIZ','KL','KL','KL','KL'),('ARSYA AHMAD JAKA ARDHANI','KL','KL','KL','KL'),
        ('AULIAN GHAIDA FATTANA','KL','KL','KL','KL'),('AZKA EVAN MAULANA','L','L','L','L'),
        ('AZKAL HIMAM SYAUQI','L','KL','L','CL'),('ISMAIL NIZAM ARKANUDDIN EL KAFEEL','CL','L','CL','L'),
        ('MALVIN MESHACH AGAM AGLER','KL','KL','KL','KL'),('MUHAMMAD ABID RAJENDRA','KL','KL','KL','KL'),
        ('MUHAMMAD ADRIAN PRADIPTA','KL','CL','KL','L'),('MUHAMMAD AL GENTZA','KL','KL','CL','CL'),
        ('MUHAMMAD BAYU SATRIO','KL','KL','KL','KL'),('MUHAMMAD BIMA MUJTABA','L','KL','KL','CL'),
        ('MUHAMMAD LUTHFI','CL','L','CL','L'),('MUHAMMAD MAULANA ISHAQ','CL','CL','KL','L'),
        ('MUHAMMAD SALUM ASWHIN DARMAWAN','L','L','L','L'),('MUHAMMAD ULIL ALBAB','L','CL','CL','L'),
        ('RAFAN SAUQI FIL ARDHA','KL','CL','CL','L'),('SHAQUILLE GIBRAN ALAIKASSALAM','L','L','CL','L'),
        ('SUKMA ARFAN FAELANI','L','KL','KL','KL'),
    ],
}

BASE = r"""<!DOCTYPE html>
<html lang="id" data-theme="light">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>{{ title }} · {{ school.name }}</title>
<meta name="theme-color" content="#1e40af">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"></script>
<style>
:root{
--bg:#f8fafc;--surface:#ffffff;--surface-2:#f1f5f9;--text:#0f172a;--text-2:#475569;--muted:#64748b;
--border:#e2e8f0;--border-2:#cbd5e1;--primary:#1e40af;--primary-600:#1d4ed8;--primary-50:#eff6ff;
--success:#059669;--success-bg:#ecfdf5;--warning:#b45309;--warning-bg:#fffbeb;
--danger:#dc2626;--danger-bg:#fef2f2;--info-bg:#eff6ff;
--shadow-sm:0 1px 2px rgba(15,23,42,.05);
--shadow:0 1px 3px rgba(15,23,42,.08),0 1px 2px rgba(15,23,42,.04);
--shadow-md:0 4px 6px -1px rgba(15,23,42,.08),0 2px 4px -2px rgba(15,23,42,.06);
--shadow-lg:0 10px 15px -3px rgba(15,23,42,.08),0 4px 6px -4px rgba(15,23,42,.05);
}
[data-theme="dark"]{
--bg:#0b1220;--surface:#131c2e;--surface-2:#1a2438;--text:#e2e8f0;--text-2:#cbd5e1;--muted:#94a3b8;
--border:#26324a;--border-2:#334155;--primary:#60a5fa;--primary-600:#3b82f6;--primary-50:#1e293b;
--success-bg:#064e3b;--warning-bg:#78350f;--danger-bg:#7f1d1d;--info-bg:#1e3a8a;
}
*{box-sizing:border-box;margin:0;padding:0;transition:background-color .2s,color .2s,border-color .2s}
body{font-family:'Inter',-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;
background:var(--bg);color:var(--text);line-height:1.55;font-size:14px;
-webkit-font-smoothing:antialiased;min-height:100vh}

/* ===== HEADER ===== */
.header{background:var(--surface);border-bottom:1px solid var(--border);
position:sticky;top:0;z-index:100;box-shadow:var(--shadow-sm)}
.header .inner{max-width:1200px;margin:0 auto;padding:.85rem 1.25rem;
display:flex;justify-content:space-between;align-items:center;gap:1rem;flex-wrap:wrap}
.brand{display:flex;align-items:center;gap:.75rem;text-decoration:none;color:inherit}
.brand .logo{width:42px;height:42px;background:linear-gradient(135deg,var(--primary),#3b82f6);
border-radius:10px;display:flex;align-items:center;justify-content:center;
font-size:1.35rem;color:#fff;flex-shrink:0;box-shadow:var(--shadow-sm)}
.brand .txt h1{font-size:.95rem;font-weight:700;letter-spacing:-.2px;line-height:1.2}
.brand .txt p{font-size:.72rem;color:var(--muted);font-weight:500}
.nav{display:flex;align-items:center;gap:.35rem;flex-wrap:wrap}
.nav a{color:var(--text-2);text-decoration:none;padding:.45rem .8rem;border-radius:8px;
font-size:.85rem;font-weight:500;transition:all .15s}
.nav a:hover{background:var(--surface-2);color:var(--primary)}
.nav a.active{background:var(--primary-50);color:var(--primary);font-weight:600}
.theme-btn{width:38px;height:38px;border:1px solid var(--border);background:var(--surface);
color:var(--text);border-radius:8px;cursor:pointer;font-size:1rem;
display:flex;align-items:center;justify-content:center;transition:all .2s}
.theme-btn:hover{background:var(--surface-2);border-color:var(--border-2)}

/* ===== LAYOUT ===== */
.container{max-width:1200px;margin:0 auto;padding:1.5rem 1.25rem 4rem}
.card{background:var(--surface);border:1px solid var(--border);border-radius:12px;
padding:1.5rem;box-shadow:var(--shadow);margin-bottom:1.25rem;animation:up .4s ease both}
@keyframes up{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:translateY(0)}}
.card-pad{padding:1.25rem 1.5rem}
h2{font-size:1.35rem;font-weight:700;letter-spacing:-.4px;color:var(--text);margin-bottom:.25rem}
h3{font-size:1rem;font-weight:600;color:var(--text);margin-bottom:.85rem;
display:flex;align-items:center;gap:.5rem}
.sub{color:var(--muted);font-size:.875rem;margin-bottom:1.25rem}
.section-head{display:flex;justify-content:space-between;align-items:flex-start;gap:1rem;
flex-wrap:wrap;margin-bottom:1.25rem}

/* ===== BUTTONS ===== */
.btn{display:inline-flex;align-items:center;gap:.45rem;padding:.6rem 1.1rem;
border-radius:9px;font-size:.875rem;font-weight:600;text-decoration:none;
border:1px solid transparent;cursor:pointer;font-family:inherit;
transition:all .15s;white-space:nowrap;line-height:1}
.btn-primary{background:var(--primary);color:#fff;box-shadow:var(--shadow-sm)}
.btn-primary:hover{background:var(--primary-600);transform:translateY(-1px);box-shadow:var(--shadow-md)}
.btn-outline{background:var(--surface);color:var(--text);border-color:var(--border-2)}
.btn-outline:hover{background:var(--surface-2);border-color:var(--primary);color:var(--primary)}
.btn-success{background:var(--success);color:#fff}
.btn-success:hover{filter:brightness(1.1);transform:translateY(-1px)}
.btn-sm{padding:.4rem .75rem;font-size:.8rem;border-radius:7px}

/* ===== FORM ===== */
input,select,textarea{width:100%;padding:.6rem .8rem;border:1px solid var(--border-2);
border-radius:8px;font-size:.875rem;font-family:inherit;background:var(--surface);color:var(--text);
transition:border-color .15s,box-shadow .15s}
input:focus,select:focus,textarea:focus{outline:none;border-color:var(--primary);
box-shadow:0 0 0 3px rgba(30,64,175,.1)}
label{display:block;margin-bottom:.4rem;font-size:.8rem;font-weight:600;color:var(--text-2)}
.form-group{margin-bottom:1rem}
.search{position:relative;margin-bottom:1rem}
.search input{padding-left:2.4rem;background:var(--surface)}
.search::before{content:'\1F50D';position:absolute;left:.85rem;top:50%;
transform:translateY(-50%);font-size:.85rem;opacity:.5;pointer-events:none}

/* ===== ALERT ===== */
.alert{padding:.75rem 1rem;border-radius:8px;margin-bottom:1rem;font-size:.85rem;
border-left:3px solid;font-weight:500}
.alert-success{background:var(--success-bg);color:var(--success);border-color:var(--success)}
.alert-error{background:var(--danger-bg);color:var(--danger);border-color:var(--danger)}
.alert-info{background:var(--info-bg);color:var(--primary);border-color:var(--primary)}

/* ===== BADGE ===== */
.badge{display:inline-flex;align-items:center;justify-content:center;
padding:.28rem .7rem;border-radius:6px;font-size:.75rem;font-weight:700;
letter-spacing:.2px;min-width:38px}
.badge-l{background:var(--success-bg);color:var(--success)}
.badge-cl{background:var(--warning-bg);color:var(--warning)}
.badge-kl{background:var(--danger-bg);color:var(--danger)}
.badge-empty{background:var(--surface-2);color:var(--muted)}
.badge-hadir{background:var(--success-bg);color:var(--success)}
.badge-sakit{background:var(--warning-bg);color:var(--warning)}
.badge-izin{background:var(--info-bg);color:var(--primary)}
.badge-alfa{background:var(--danger-bg);color:var(--danger)}

/* ===== GRID ===== */
.grid{display:grid;gap:1rem}
.grid-2{grid-template-columns:repeat(auto-fit,minmax(320px,1fr))}
.grid-3{grid-template-columns:repeat(auto-fit,minmax(220px,1fr))}
.grid-4{grid-template-columns:repeat(auto-fit,minmax(160px,1fr))}

/* ===== CLASS CARD ===== */
.class-card{display:block;padding:1.75rem 1.5rem;background:var(--surface);
border:1px solid var(--border);border-radius:12px;text-decoration:none;color:var(--text);
transition:all .2s;position:relative;overflow:hidden;box-shadow:var(--shadow-sm)}
.class-card::after{content:'';position:absolute;top:0;left:0;right:0;height:3px;
background:linear-gradient(90deg,var(--primary),#3b82f6);transform:scaleX(0);
transform-origin:left;transition:transform .3s}
.class-card:hover{transform:translateY(-3px);box-shadow:var(--shadow-lg);border-color:var(--primary)}
.class-card:hover::after{transform:scaleX(1)}
.class-card .icon{width:56px;height:56px;background:var(--primary-50);color:var(--primary);
border-radius:12px;display:flex;align-items:center;justify-content:center;
font-size:1.5rem;font-weight:700;margin-bottom:1rem}
.class-card .nama{font-size:1.25rem;font-weight:700;letter-spacing:-.3px;margin-bottom:.15rem}
.class-card .jml{font-size:.85rem;color:var(--muted)}
.class-card .wali{font-size:.78rem;color:var(--text-2);margin-top:.5rem;
padding-top:.5rem;border-top:1px solid var(--border);font-weight:500}
.class-card .arrow{position:absolute;bottom:1.25rem;right:1.25rem;color:var(--primary);
font-size:1.1rem;transition:transform .25s;font-weight:700}
.class-card:hover .arrow{transform:translateX(4px)}

/* ===== STUDENT ROW ===== */
.student-row{display:flex;align-items:center;gap:.9rem;padding:.85rem 1rem;
background:var(--surface);border:1px solid var(--border);border-radius:10px;
text-decoration:none;color:var(--text);transition:all .15s;margin-bottom:.4rem}
.student-row:hover{border-color:var(--primary);background:var(--primary-50);transform:translateX(2px)}
[data-theme="dark"] .student-row:hover{background:var(--surface-2)}
.avatar{width:38px;height:38px;border-radius:9px;display:flex;align-items:center;
justify-content:center;font-weight:700;color:#fff;font-size:.8rem;flex-shrink:0}
.avatar.c0{background:linear-gradient(135deg,#3b82f6,#2563eb)}
.avatar.c1{background:linear-gradient(135deg,#10b981,#059669)}
.avatar.c2{background:linear-gradient(135deg,#f59e0b,#d97706)}
.avatar.c3{background:linear-gradient(135deg,#8b5cf6,#7c3aed)}
.avatar.c4{background:linear-gradient(135deg,#ec4899,#db2777)}
.avatar.c5{background:linear-gradient(135deg,#06b6d4,#0891b2)}
.student-row .info{flex:1;min-width:0}
.student-row .nama{font-weight:600;font-size:.9rem;white-space:nowrap;
overflow:hidden;text-overflow:ellipsis}
.student-row .meta{font-size:.78rem;color:var(--muted);margin-top:.1rem}
.student-row .score{font-size:1.35rem;font-weight:800;line-height:1;letter-spacing:-.5px}

/* ===== TABLE ===== */
.table-wrap{overflow-x:auto;border-radius:10px;border:1px solid var(--border)}
table{width:100%;border-collapse:collapse;font-size:.85rem}
th,td{padding:.7rem .85rem;text-align:left;border-bottom:1px solid var(--border)}
th{background:var(--surface-2);font-weight:600;font-size:.75rem;text-transform:uppercase;
letter-spacing:.4px;color:var(--text-2);white-space:nowrap}
tbody tr:last-child td{border-bottom:none}
tbody tr:hover{background:var(--surface-2)}
td.center,th.center{text-align:center}

/* ===== ASPECT CARD ===== */
.aspect{position:relative;padding:1.1rem .9rem;border:1px solid var(--border);
border-radius:10px;background:var(--surface);text-align:center;overflow:hidden;
transition:all .2s}
.aspect::before{content:'';position:absolute;top:0;left:0;right:0;height:3px;background:var(--border)}
.aspect[data-val="L"]::before{background:var(--success)}
.aspect[data-val="CL"]::before{background:var(--warning)}
.aspect[data-val="KL"]::before{background:var(--danger)}
.aspect:hover{box-shadow:var(--shadow-md);transform:translateY(-2px)}
.aspect .lbl{font-size:.72rem;color:var(--muted);text-transform:uppercase;
letter-spacing:.6px;font-weight:700;margin-bottom:.6rem}
.aspect .desc{font-size:.75rem;color:var(--text-2);margin-top:.4rem}
.aspect .sc{font-size:.7rem;color:var(--muted);margin-top:.35rem}

/* ===== SCORE ===== */
.score-big{font-size:3.2rem;font-weight:800;line-height:1;letter-spacing:-2px}
.s-baik{color:var(--success)}.s-cukup{color:var(--warning)}.s-perlu{color:var(--danger)}.s-empty{color:var(--muted)}
.progress{height:6px;background:var(--surface-2);border-radius:99px;overflow:hidden;margin-top:.75rem}
.progress-bar{height:100%;background:linear-gradient(90deg,var(--primary),#3b82f6);
border-radius:99px;width:0;transition:width 1s cubic-bezier(.4,0,.2,1)}

/* ===== TABS ===== */
.tabs{display:flex;gap:.25rem;border-bottom:1px solid var(--border);margin-bottom:1.25rem;
overflow-x:auto;padding-bottom:0}
.tab{padding:.7rem 1rem;border:none;background:none;cursor:pointer;font-size:.85rem;
font-weight:600;color:var(--muted);border-bottom:2px solid transparent;margin-bottom:-1px;
transition:all .15s;font-family:inherit;white-space:nowrap}
.tab.active{color:var(--primary);border-bottom-color:var(--primary)}
.tab:hover{color:var(--text)}
.tab-content{display:none;animation:up .3s ease}
.tab-content.active{display:block}

/* ===== TIMELINE ===== */
.timeline{position:relative;padding-left:1.5rem}
.timeline::before{content:'';position:absolute;left:5px;top:8px;bottom:8px;width:2px;
background:var(--border)}
.tl-item{position:relative;padding-bottom:1rem}
.tl-item::before{content:'';position:absolute;left:-1.5rem;top:6px;width:10px;height:10px;
border-radius:50%;background:var(--primary);border:2px solid var(--surface);
box-shadow:0 0 0 2px var(--primary-50)}
.tl-item .date{font-size:.72rem;color:var(--muted);font-weight:600;margin-bottom:.2rem;
text-transform:uppercase;letter-spacing:.3px}
.tl-item .text{font-size:.875rem;line-height:1.55}

/* ===== STAT ===== */
.stat{display:flex;align-items:center;gap:1rem;padding:1.1rem 1.25rem;
background:var(--surface);border:1px solid var(--border);border-radius:10px;box-shadow:var(--shadow-sm)}
.stat-icon{width:44px;height:44px;border-radius:10px;display:flex;align-items:center;
justify-content:center;font-size:1.3rem;flex-shrink:0}
.stat-icon.blue{background:var(--primary-50);color:var(--primary)}
.stat-icon.green{background:var(--success-bg);color:var(--success)}
.stat-icon.amber{background:var(--warning-bg);color:var(--warning)}
.stat-icon.red{background:var(--danger-bg);color:var(--danger)}
.stat-val{font-size:1.55rem;font-weight:800;line-height:1;letter-spacing:-.5px}
.stat-lbl{font-size:.75rem;color:var(--muted);font-weight:600;
text-transform:uppercase;letter-spacing:.4px;margin-top:.2rem}

/* ===== CHART ===== */
.chart-square{position:relative;height:200px;max-width:200px;margin:0 auto}
.chart-wide{position:relative;height:240px}

/* ===== PERIOD ===== */
.periods{display:flex;gap:.4rem;flex-wrap:wrap;margin-bottom:1.25rem;
padding:.35rem;background:var(--surface-2);border-radius:10px;width:fit-content}
.period{padding:.4rem 1rem;border-radius:7px;font-size:.82rem;font-weight:600;
color:var(--text-2);text-decoration:none;transition:all .15s}
.period:hover{color:var(--primary)}
.period.active{background:var(--surface);color:var(--primary);box-shadow:var(--shadow-sm)}

/* ===== REC ===== */
.rec{padding:1rem 1.15rem;border-radius:10px;background:var(--info-bg);
border-left:3px solid var(--primary);font-size:.875rem;line-height:1.65;
color:var(--text-2)}
[data-theme="dark"] .rec{color:var(--text)}
.rec ul{margin:.6rem 0 0 1.2rem}
.rec li{margin-bottom:.3rem}

/* ===== BREADCRUMB ===== */
.crumb{font-size:.82rem;color:var(--muted);margin-bottom:.75rem;font-weight:500}
.crumb a{color:var(--primary);text-decoration:none}
.crumb a:hover{text-decoration:underline}
.crumb span{margin:0 .35rem;opacity:.5}

/* ===== ATTENDANCE ===== */
.att-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:.75rem;margin-bottom:.75rem}
.att-item{padding:.9rem;border-radius:10px;text-align:center;border:1px solid var(--border)}
.att-item.hadir{background:var(--success-bg);color:var(--success);border-color:transparent}
.att-item.sakit{background:var(--warning-bg);color:var(--warning);border-color:transparent}
.att-item.izin{background:var(--info-bg);color:var(--primary);border-color:transparent}
.att-item.alfa{background:var(--danger-bg);color:var(--danger);border-color:transparent}
.att-item .num{font-size:1.5rem;font-weight:800;line-height:1}
.att-item .lbl{font-size:.72rem;font-weight:600;margin-top:.15rem;opacity:.85}

/* ===== FOOTER ===== */
.footer{text-align:center;padding:2rem 1.25rem;color:var(--muted);font-size:.8rem;
border-top:1px solid var(--border);background:var(--surface)}
.footer strong{color:var(--text-2)}

/* ===== EMPTY ===== */
.empty{padding:2rem;text-align:center;color:var(--muted);font-size:.875rem}
.empty .ico{font-size:2rem;margin-bottom:.5rem;opacity:.5}

/* ===== PRINT ===== */
@media print{
  .header,.footer,.btn,.theme-btn,.tabs,.periods,.crumb,.no-print{display:none!important}
  .card{box-shadow:none;border:1px solid #ddd;page-break-inside:avoid;margin-bottom:1rem}
  .tab-content{display:block!important;margin-bottom:1rem}
  .tab-content::before{content:attr(data-title);display:block;font-weight:700;
  font-size:1rem;margin-bottom:.5rem;padding-bottom:.35rem;border-bottom:2px solid #333}
  body{background:#fff;color:#000}
  .container{padding:0;max-width:100%}
}

@media(max-width:640px){
  .header .inner{padding:.75rem 1rem}
  .brand .txt h1{font-size:.85rem}
  .container{padding:1rem .85rem 3rem}
  .card{padding:1.15rem}
  .score-big{font-size:2.6rem}
  .att-grid{grid-template-columns:repeat(2,1fr)}
}
</style>
</head>
<body>
<header class="header">
  <div class="inner">
    <a href="{{ url_for('home') }}" class="brand">
      <div class="logo">{{ school.logo }}</div>
      <div class="txt">
        <h1>{{ school.name }}</h1>
        <p>NPSN {{ school.npsn }} · T.A. {{ school.year }}</p>
      </div>
    </a>
    <nav class="nav">
      <a href="{{ url_for('home') }}" class="{{ 'active' if request.endpoint == 'home' else '' }}">Beranda</a>
      <a href="{{ url_for('admin') }}" class="{{ 'active' if request.endpoint and request.endpoint.startswith('admin') else '' }}">Panel Guru</a>
      <button class="theme-btn" onclick="toggleTheme()" title="Ganti tema" id="themeBtn">&#127769;</button>
    </nav>
  </div>
</header>
<div class="container">
  {% with messages = get_flashed_messages(with_categories=true) %}
    {% for cat, msg in messages %}
      <div class="alert alert-{{ cat }}">{{ msg }}</div>
    {% endfor %}
  {% endwith %}
  {{ body|safe }}
</div>
<footer class="footer">
  <div><strong>{{ school.name }}</strong> &middot; {{ school.address }}</div>
  <div style="margin-top:.4rem;">Sistem Informasi Perkembangan Siswa &copy; {{ school.year }}</div>
</footer>
<script>
function toggleTheme(){
  const h=document.documentElement;
  const n=h.getAttribute('data-theme')==='dark'?'light':'dark';
  h.setAttribute('data-theme',n);
  localStorage.setItem('theme',n);
  document.getElementById('themeBtn').innerHTML=n==='dark'?'&#9728;':'&#127769;';
  if(window.updateCharts)window.updateCharts();
}
(function(){
  const s=localStorage.getItem('theme')||'light';
  document.documentElement.setAttribute('data-theme',s);
  document.addEventListener('DOMContentLoaded',()=>{
    const b=document.getElementById('themeBtn');
    if(b)b.innerHTML=s==='dark'?'&#9728;':'&#127769;';
    document.querySelectorAll('.progress-bar').forEach(x=>{
      setTimeout(()=>{x.style.width=x.dataset.w+'%';},150);
    });
  });
})();
function showTab(id,btn){
  document.querySelectorAll('.tab-content').forEach(t=>t.classList.remove('active'));
  document.querySelectorAll('.tab').forEach(t=>t.classList.remove('active'));
  document.getElementById(id).classList.add('active');
  btn.classList.add('active');
}
function filterRows(q,sel){
  const s=q.toLowerCase();
  document.querySelectorAll(sel).forEach(r=>{
    r.style.display=r.textContent.toLowerCase().includes(s)?'':'none';
  });
}
// ===== ANAK SAYA (Shortcut) =====
function getFavs(){try{return JSON.parse(localStorage.getItem('favs')||'[]')}catch(e){return []}}
function setFavs(a){localStorage.setItem('favs',JSON.stringify(a))}
function toggleFav(kode,nama,kelas){
  let f=getFavs();
  const i=f.findIndex(x=>x.kode===kode);
  if(i>=0){f.splice(i,1);}else{f.unshift({kode:kode,nama:nama,kelas:kelas});}
  setFavs(f);
  renderFavBtn(kode);
  renderFavSection();
}
function toggleFavFromBtn(b){
  toggleFav(b.dataset.kode,b.dataset.nama,b.dataset.kelas);
}
function renderFavBtn(kode){
  const b=document.getElementById('favBtn');
  if(!b)return;
  const f=getFavs();
  const ok=f.some(x=>x.kode===kode);
  b.innerHTML=ok?'&#9733; Tersimpan di Anak Saya':'&#9734; Simpan ke Anak Saya';
  b.style.color=ok?'#d97706':'';
  b.style.borderColor=ok?'#d97706':'';
}
function renderFavSection(){
  const box=document.getElementById('favSection');
  if(!box)return;
  const f=getFavs();
  if(!f.length){box.innerHTML='';return;}
  let cards='';
  f.forEach(x=>{
    cards+='<a href="/anak/'+x.kode+'" class="class-card" style="position:relative">'
      +'<button onclick="event.preventDefault();event.stopPropagation();removeFav(\''+x.kode+'\')" title="Hapus" '
      +'style="position:absolute;top:.75rem;right:.75rem;background:transparent;border:none;'
      +'font-size:1.05rem;cursor:pointer;color:var(--muted);padding:.25rem;line-height:1">&times;</button>'
      +'<div class="icon">'+x.kelas+'</div>'
      +'<div class="nama">'+x.nama+'</div>'
      +'<div class="jml">Kode '+x.kode+'</div>'
      +'<div class="arrow">&rarr;</div></a>';
  });
  box.innerHTML='<div class="section-head" style="margin-top:.5rem">'
    +'<div><h2>&#9733; Anak Saya</h2>'
    +'<p class="sub" style="margin-bottom:0">Akses cepat ke laporan perkembangan anak Anda</p></div></div>'
    +'<div class="grid grid-3" style="margin-bottom:1.5rem">'+cards+'</div>';
}
function removeFav(kode){
  let f=getFavs();
  f=f.filter(x=>x.kode!==kode);
  setFavs(f);
  renderFavSection();
  renderFavBtn(kode);
}
function copyShortUrl(){
  const inp=document.getElementById('shortUrl');
  inp.select();
  const done=()=>{
    const b=document.getElementById('copyBtn');
    const old=b.innerHTML;
    b.innerHTML='&#10003; Tersalin!';
    setTimeout(()=>{b.innerHTML=old;},1500);
  };
  if(navigator.clipboard){navigator.clipboard.writeText(inp.value).then(done).catch(()=>{document.execCommand('copy');done();});}
  else{document.execCommand('copy');done();}
}
document.addEventListener('DOMContentLoaded',()=>{
  renderFavSection();
  const b=document.getElementById('favBtn');
  if(b)renderFavBtn(b.dataset.kode);
});
</script>
</body>
</html>"""


# ==================== SETTINGS ====================
def get_setting(key, default=''):
    try:
        conn = get_db()
        r = conn.execute("SELECT value FROM settings WHERE key=?", (key,)).fetchone()
        conn.close()
        return r['value'] if r else default
    except Exception:
        return default


def set_setting(key, value):
    conn = get_db()
    conn.execute("CREATE TABLE IF NOT EXISTS settings (key TEXT PRIMARY KEY, value TEXT)")
    conn.execute("INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)", (key, value))
    conn.commit()
    conn.close()


def get_school():
    return {
        'name': get_setting('school_name', SCHOOL['name']),
        'address': get_setting('school_address', SCHOOL['address']),
        'npsn': get_setting('school_npsn', SCHOOL['npsn']),
        'logo': get_setting('school_logo', SCHOOL['logo']),
        'year': get_setting('school_year', SCHOOL['year']),
        'headmaster': get_setting('school_headmaster', SCHOOL['headmaster']),
    }


def get_wali(kelas):
    return get_setting('wali_' + kelas, CLASS_INFO.get(kelas, {}).get('wali', ''))


def ensure_schema():
    try:
        conn = get_db()
        conn.execute("CREATE TABLE IF NOT EXISTS settings (key TEXT PRIMARY KEY, value TEXT)")
        defaults = {
            'school_name': SCHOOL['name'],
            'school_address': SCHOOL['address'],
            'school_npsn': SCHOOL['npsn'],
            'school_logo': SCHOOL['logo'],
            'school_year': SCHOOL['year'],
            'school_headmaster': SCHOOL['headmaster'],
        }
        for k, v in CLASS_INFO.items():
            defaults['wali_' + k] = v.get('wali', '')
        for k, v in defaults.items():
            conn.execute("INSERT OR IGNORE INTO settings (key, value) VALUES (?, ?)", (k, v))
        conn.commit()
        conn.close()
    except Exception as e:
        print("ensure_schema warning:", e)


# ==================== DB ====================
def get_db():
    c = sqlite3.connect(DB_PATH)
    c.row_factory = sqlite3.Row
    return c

def init_db():
    if os.path.exists(DB_PATH):
        return
    conn = get_db()
    cur = conn.cursor()
    cur.executescript("""
        CREATE TABLE students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            access_code TEXT UNIQUE NOT NULL,
            nama TEXT NOT NULL,
            kelas TEXT NOT NULL
        );
        CREATE TABLE assessments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            period TEXT NOT NULL,
            aspect_idx INTEGER NOT NULL,
            value TEXT DEFAULT '',
            UNIQUE(student_id, period, aspect_idx)
        );
        CREATE TABLE attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            period TEXT NOT NULL,
            hadir INTEGER DEFAULT 0,
            sakit INTEGER DEFAULT 0,
            izin INTEGER DEFAULT 0,
            alfa INTEGER DEFAULT 0,
            UNIQUE(student_id, period)
        );
        CREATE TABLE notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            period TEXT DEFAULT 'STS 1',
            note TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        );
    """)
    for kelas, students in SEED.items():
        for i, s in enumerate(students, 1):
            cur.execute("INSERT INTO students (access_code,nama,kelas) VALUES (?,?,?)",
                        (f"{kelas}-{i:03d}", s[0], kelas))
            sid = cur.lastrowid
            for j in range(len(ASPECTS)):
                cur.execute("""INSERT INTO assessments (student_id,period,aspect_idx,value)
                               VALUES (?,?,?,?)""", (sid, PERIODS[0], j, s[j+1]))
            cur.execute("""INSERT INTO attendance (student_id,period,hadir,sakit,izin,alfa)
                           VALUES (?,?,?,?,?,?)""", (sid, PERIODS[0], 20, 0, 0, 0))
    conn.commit()
    conn.close()
    print(f"\u2705 Database siap: {DB_PATH}")

def get_assess(sid, period):
    conn = get_db()
    rows = conn.execute("SELECT aspect_idx,value FROM assessments WHERE student_id=? AND period=?",
                        (sid, period)).fetchall()
    conn.close()
    vals = [''] * len(ASPECTS)
    for r in rows:
        if r['aspect_idx'] < len(vals):
            vals[r['aspect_idx']] = r['value']
    return vals

def get_att(sid, period):
    conn = get_db()
    r = conn.execute("SELECT * FROM attendance WHERE student_id=? AND period=?",
                     (sid, period)).fetchone()
    conn.close()
    if r:
        return {k: r[k] for k in ('hadir','sakit','izin','alfa')}
    return {'hadir':0,'sakit':0,'izin':0,'alfa':0}

def get_notes(sid, period=None):
    conn = get_db()
    if period:
        rows = conn.execute("""SELECT * FROM notes WHERE student_id=? AND period=?
                               ORDER BY id DESC""", (sid, period)).fetchall()
    else:
        rows = conn.execute("SELECT * FROM notes WHERE student_id=? ORDER BY id DESC",
                            (sid,)).fetchall()
    conn.close()
    return rows

def get_history(sid):
    conn = get_db()
    rows = conn.execute("""SELECT period,aspect_idx,value FROM assessments
                           WHERE student_id=? ORDER BY period""", (sid,)).fetchall()
    conn.close()
    hist = {}
    for r in rows:
        p = r['period']
        if p not in hist: hist[p] = [''] * len(ASPECTS)
        hist[p][r['aspect_idx']] = r['value']
    return {p: {'nilai': hitung_nilai(a), 'aspects': a} for p, a in hist.items()}

def hitung_nilai(a):
    vals = [x for x in a if x]
    if not vals: return None
    return round(sum(ASPECT_SCORES.get(v,0) for v in vals) / len(vals))

def kategori(n):
    if n is None: return 'Belum Dinilai', 'empty'
    if n >= 85: return 'Baik', 'baik'
    if n >= 75: return 'Cukup', 'cukup'
    return 'Perlu Pendampingan', 'perlu'

def rekomendasi(a):
    if not any(a):
        return "Guru belum menginput nilai. Silakan hubungi wali kelas.", []
    items = []
    for i, v in enumerate(a):
        if v == 'KL':
            items.append(f"Perlu pendampingan intensif pada <b>{ASPECTS[i]}</b>.")
        elif v == 'CL':
            items.append(f"Perlu penguatan rutin pada <b>{ASPECTS[i]}</b>.")
    if not items:
        return "Ananda menunjukkan penguasaan baik di semua aspek. Berikan pengayaan dan apresiasi.", []
    return "Beberapa aspek masih perlu perhatian khusus:", items

def wrap(body, title='Beranda'):
    return render_template_string(BASE, title=title, body=body, school=SCHOOL)


# ==================== PUBLIC ====================
@app.route('/')
def home():
    conn = get_db()
    classes = conn.execute("SELECT kelas, COUNT(*) AS j FROM students GROUP BY kelas ORDER BY kelas").fetchall()
    conn.close()
    rows = ''
    for i, c in enumerate(classes):
        wali = CLASS_INFO.get(c['kelas'], {}).get('wali', '')
        rows += f'''<a href="{url_for('kelas_view', kelas=c['kelas'])}" class="list-row">
          <div class="list-badge">{c['kelas']}</div>
          <div class="list-info">
            <div class="list-title">Kelas {c['kelas']}</div>
            <div class="list-meta">{c['j']} siswa terdaftar{f' &middot; Wali: {wali}' if wali else ''}</div>
          </div>
          <div class="list-arrow">&rarr;</div>
        </a>'''
    body = f'''
    <div id="favSection"></div>
    <div class="section-head">
      <div>
        <h2>Selamat Datang, Bapak/Ibu Walimurid</h2>
        <p class="sub" style="margin-bottom:0">Silakan pilih kelas anak Anda untuk melihat laporan perkembangan belajar.</p>
      </div>
    </div>
    <div class="card card-pad" style="padding:.75rem">
      {rows}
    </div>
    <div class="card" style="margin-top:1.5rem;background:var(--info-bg);border-color:transparent">
      <h3>&#128161; Panduan Penggunaan</h3>
      <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:1rem;margin-top:.5rem">
        <div><b>1.</b> Pilih kelas anak Anda</div>
        <div><b>2.</b> Cari &amp; klik nama anak</div>
        <div><b>3.</b> Lihat nilai, tren, absensi &amp; catatan guru</div>
      </div>
    </div>
    '''
    return wrap(body, 'Beranda')


@app.route('/anak/<kode>')
def anak_by_code(kode):
    conn = get_db()
    s = conn.execute("SELECT id FROM students WHERE access_code=?", (kode.upper(),)).fetchone()
    conn.close()
    if not s:
        flash('Kode akses tidak ditemukan.', 'error')
        return redirect(url_for('home'))
    return redirect(url_for('siswa_view', sid=s['id']))


@app.route('/kelas/<kelas>')
def kelas_view(kelas):
    conn = get_db()
    students = conn.execute("SELECT * FROM students WHERE kelas=? ORDER BY nama", (kelas,)).fetchall()
    conn.close()
    if not students:
        flash('Kelas tidak ditemukan.', 'error')
        return redirect(url_for('home'))
    wali = CLASS_INFO.get(kelas, {}).get('wali', '')
    rows = ''
    for i, s in enumerate(students):
        a = get_assess(s['id'], PERIODS[0])
        n = hitung_nilai(a)
        kat, cls = kategori(n)
        ini = ''.join([w[0] for w in s['nama'].split()[:2]]).upper()
        rows += f'''<a href="{url_for('siswa_view', sid=s['id'])}" class="student-row">
          <div class="avatar c{i%6}">{ini}</div>
          <div class="info">
            <div class="nama">{s['nama']}</div>
            <div class="meta">{s['access_code']} &middot; {kat}</div>
          </div>
          <div class="score s-{cls}">{n if n is not None else '—'}</div>
        </a>'''
    body = f'''
    <div class="crumb">
      <a href="{url_for('home')}">Beranda</a><span>&rsaquo;</span>Kelas {kelas}
    </div>
    <div class="section-head">
      <div>
        <h2>Kelas {kelas}</h2>
        <p class="sub" style="margin-bottom:0">
          {len(students)} siswa terdaftar{f' &middot; Wali Kelas: <b>{wali}</b>' if wali else ''}
        </p>
      </div>
      <a href="{url_for('home')}" class="btn btn-outline btn-sm">&larr; Kembali</a>
    </div>
    <div class="card card-pad">
      <div class="search">
        <input placeholder="Cari nama anak..." oninput="filterRows(this.value,'.student-row')" autofocus>
      </div>
      {rows}
    </div>
    '''
    return wrap(body, f'Kelas {kelas}')


@app.route('/siswa/<int:sid>')
def siswa_view(sid):
    period = request.args.get('period', PERIODS[0])
    if period not in PERIODS: period = PERIODS[0]
    conn = get_db()
    s = conn.execute("SELECT * FROM students WHERE id=?", (sid,)).fetchone()
    conn.close()
    if not s:
        flash('Siswa tidak ditemukan.', 'error')
        return redirect(url_for('home'))

    a = get_assess(sid, period)
    nilai = hitung_nilai(a)
    kat, kcls = kategori(nilai)
    rek_text, rek_items = rekomendasi(a)
    cnt = {'L': a.count('L'), 'CL': a.count('CL'), 'KL': a.count('KL')}
    att = get_att(sid, period)
    notes = get_notes(sid, period)
    hist = get_history(sid)
    wali = CLASS_INFO.get(s['kelas'], {}).get('wali', '')

    pbtns = ''.join(
        f'<a href="{url_for("siswa_view", sid=sid, period=p)}" class="period {"active" if p==period else ""}">{p}</a>'
        for p in PERIODS)

    aspects_html = ''
    for i, v in enumerate(a):
        bcls = 'l' if v == 'L' else 'cl' if v == 'CL' else 'kl' if v == 'KL' else 'empty'
        lbl = v or '—'
        desc = ASPECT_LABELS.get(v, 'Belum dinilai')
        sc = ASPECT_SCORES.get(v, '—')
        aspects_html += f'''<div class="aspect" data-val="{v}">
          <div class="lbl">{ASPECTS[i]}</div>
          <span class="badge badge-{bcls}" style="font-size:1rem;padding:.4rem .85rem">{lbl}</span>
          <div class="desc">{desc}</div>
          <div class="sc">Skor {sc}</div>
        </div>'''

    tot_hari = att['hadir'] + att['sakit'] + att['izin'] + att['alfa']
    pct = round(att['hadir'] / tot_hari * 100) if tot_hari else 0
    att_html = f'''
    <div class="att-grid">
      <div class="att-item hadir"><div class="num">{att['hadir']}</div><div class="lbl">Hadir</div></div>
      <div class="att-item sakit"><div class="num">{att['sakit']}</div><div class="lbl">Sakit</div></div>
      <div class="att-item izin"><div class="num">{att['izin']}</div><div class="lbl">Izin</div></div>
      <div class="att-item alfa"><div class="num">{att['alfa']}</div><div class="lbl">Alfa</div></div>
    </div>
    <div style="text-align:center;font-size:.85rem;color:var(--muted)">
      Total <b>{tot_hari}</b> hari &middot; Persentase kehadiran <b>{pct}%</b>
    </div>'''

    notes_html = ''
    for n in notes:
        notes_html += f'''<div class="tl-item">
          <div class="date">{n["created_at"]} &middot; {n["period"]}</div>
          <div class="text">{n["note"]}</div>
        </div>'''
    if not notes_html:
        notes_html = '<div class="empty"><div class="ico">&#128221;</div>Belum ada catatan dari guru.</div>'

    rek_html = f'<div class="rec">{rek_text}{"<ul>" + "".join(f"<li>{x}</li>" for x in rek_items) + "</ul>" if rek_items else ""}</div>'

    hist_rows = ''
    labels, data = [], []
    prev = None
    for p in PERIODS:
        if p not in hist: continue
        h = hist[p]
        n = h['nilai']
        if n is None: tr = '<span style="color:var(--muted)">—</span>'
        elif prev is None: tr = '<span style="color:var(--muted)">—</span>'
        elif n > prev: tr = f'<span style="color:var(--success);font-weight:700">▲ +{n-prev}</span>'
        elif n < prev: tr = f'<span style="color:var(--danger);font-weight:700">▼ {n-prev}</span>'
        else: tr = '<span style="color:var(--muted)">=</span>'
        kt, kc = kategori(n)
        sm = ' '.join(
            f'<span class="badge badge-{"l" if v=="L" else "cl" if v=="CL" else "kl" if v=="KL" else "empty"}">{v or "—"}</span>'
            for v in h['aspects'])
        hist_rows += f'''<tr>
          <td><b>{p}</b></td><td>{sm}</td>
          <td class="center"><span class="score-big s-{kc}" style="font-size:1.15rem">{n if n else "—"}</span></td>
          <td>{kt}</td><td class="center">{tr}</td>
        </tr>'''
        if n is not None: labels.append(p); data.append(n)
        prev = n if n is not None else prev

    hist_table = f'''<div class="table-wrap"><table>
      <thead><tr><th>Periode</th><th>Aspek</th><th class="center">Nilai</th><th>Kategori</th><th class="center">Tren</th></tr></thead>
      <tbody>{hist_rows}</tbody></table></div>''' if hist_rows else '<div class="empty">Belum ada riwayat.</div>'

    short_path = url_for('anak_by_code', kode=s['access_code'])
    qr_url = request.host_url.rstrip('/') + short_path

    body = f'''
    <div class="crumb">
      <a href="{url_for('home')}">Beranda</a><span>&rsaquo;</span>
      <a href="{url_for('kelas_view', kelas=s['kelas'])}">Kelas {s['kelas']}</a><span>&rsaquo;</span>
      {s['nama']}
    </div>
    <div class="section-head">
      <div>
        <h2>{s['nama']}</h2>
        <p class="sub" style="margin-bottom:0">
          Kelas <b>{s['kelas']}</b> &middot; Kode <code>{s['access_code']}</code>
          {f' &middot; Wali Kelas: <b>{wali}</b>' if wali else ''}
        </p>
      </div>
      <div style="display:flex;gap:.5rem;flex-wrap:wrap" class="no-print">
        <button class="btn btn-outline btn-sm" id="favBtn"
                data-kode="{s['access_code']}" data-nama="{s['nama']}" data-kelas="{s['kelas']}"
                onclick="toggleFavFromBtn(this)">&#9734; Simpan ke Anak Saya</button>
        <a href="{url_for('kelas_view', kelas=s['kelas'])}" class="btn btn-outline btn-sm">&larr; Kembali</a>
        <button class="btn btn-primary btn-sm" onclick="window.print()">&#128424; Cetak / PDF</button>
      </div>
    </div>

    <div class="periods no-print">
      {pbtns}
    </div>

    <div class="grid grid-2">
      <div class="card" style="text-align:center;display:flex;flex-direction:column;justify-content:center;padding:1.75rem">
        <div style="font-size:.72rem;color:var(--muted);text-transform:uppercase;
        letter-spacing:1.2px;font-weight:700">Nilai Akhir &middot; {period}</div>
        <div class="score-big s-{kcls}" style="margin:.5rem 0">{nilai if nilai is not None else '—'}</div>
        <div style="font-size:1rem;font-weight:700">{kat}</div>
        <div class="progress"><div class="progress-bar" data-w="{nilai if nilai else 0}"></div></div>
        <div style="font-size:.72rem;color:var(--muted);margin-top:.5rem">
          {sum(1 for x in a if x)}/{len(ASPECTS)} aspek terisi
        </div>
      </div>
      <div class="card" style="text-align:center">
        <h3 style="justify-content:center">&#128202; Distribusi Penilaian</h3>
        <div class="chart-square"><canvas id="dc"></canvas></div>
        <div style="display:flex;justify-content:center;gap:1rem;margin-top:.85rem;font-size:.8rem;font-weight:600">
          <span><span class="badge badge-l">L</span> {cnt['L']}</span>
          <span><span class="badge badge-cl">CL</span> {cnt['CL']}</span>
          <span><span class="badge badge-kl">KL</span> {cnt['KL']}</span>
        </div>
      </div>
    </div>

    <div class="card no-print" style="display:flex;gap:1.5rem;align-items:center;flex-wrap:wrap">
      <div style="flex-shrink:0;text-align:center">
        <img src="https://api.qrserver.com/v1/create-qr-code/?size=140x140&margin=8&data={qr_url}"
             alt="QR Code" style="border-radius:8px;border:1px solid var(--border);padding:6px;background:#fff">
        <div style="font-size:.7rem;color:var(--muted);margin-top:.5rem">Scan untuk akses cepat</div>
      </div>
      <div style="flex:1;min-width:240px">
        <h3 style="margin-bottom:.5rem">&#128279; Link Pintas untuk Orang Tua</h3>
        <p style="font-size:.82rem;color:var(--muted);margin-bottom:.75rem;line-height:1.5">
          Simpan link ini di HP Bapak/Ibu agar bisa langsung membuka laporan anak
          tanpa perlu memilih kelas lagi. Bisa juga discan lewat QR di samping.
        </p>
        <div style="display:flex;gap:.5rem;align-items:center;flex-wrap:wrap">
          <input id="shortUrl" value="{qr_url}" readonly
                 style="flex:1;min-width:220px;font-size:.8rem;font-family:monospace;background:var(--surface-2)"
                 onclick="this.select()">
          <button class="btn btn-primary btn-sm" onclick="copyShortUrl()" id="copyBtn">Salin Link</button>
        </div>
      </div>
    </div>

    <div class="card">
      <div class="tabs no-print">
        <button class="tab active" onclick="showTab('t1',this)">Aspek Penilaian</button>
        <button class="tab" onclick="showTab('t2',this)">Riwayat &amp; Tren</button>
        <button class="tab" onclick="showTab('t3',this)">Absensi</button>
        <button class="tab" onclick="showTab('t4',this)">Rekomendasi</button>
        <button class="tab" onclick="showTab('t5',this)">Catatan Guru</button>
      </div>

      <div id="t1" class="tab-content active" data-title="Aspek Penilaian">
        <div class="grid grid-4">{aspects_html}</div>
        <div style="margin-top:1.25rem;padding-top:1rem;border-top:1px solid var(--border);
        font-size:.78rem;color:var(--muted)">
          <b>Keterangan:</b>
          <span class="badge badge-l">L</span> Lancar (90) &nbsp;
          <span class="badge badge-cl">CL</span> Cukup Lancar (80) &nbsp;
          <span class="badge badge-kl">KL</span> Kurang Lancar (70)
        </div>
      </div>

      <div id="t2" class="tab-content" data-title="Riwayat dan Tren">
        <h3>Perkembangan Nilai</h3>
        <div class="chart-wide"><canvas id="tc"></canvas></div>
        <h3 style="margin-top:1.5rem">Riwayat per Periode</h3>
        {hist_table}
      </div>

      <div id="t3" class="tab-content" data-title="Absensi">
        <h3>Rekap Absensi {period}</h3>
        {att_html}
      </div>

      <div id="t4" class="tab-content" data-title="Rekomendasi">{rek_html}</div>

      <div id="t5" class="tab-content" data-title="Catatan Guru">
        <div class="timeline">{notes_html}</div>
      </div>
    </div>

    <script>
    const CC={{light:['#059669','#d97706','#dc2626'],dark:['#34d399','#fbbf24','#f87171']}};
    const isD=document.documentElement.getAttribute('data-theme')==='dark';
    const dc=new Chart(document.getElementById('dc').getContext('2d'),{{
      type:'doughnut',
      data:{{labels:['Lancar','Cukup Lancar','Kurang Lancar'],
        datasets:[{{data:[{cnt['L']},{cnt['CL']},{cnt['KL']}],
        backgroundColor:CC[isD?'dark':'light'],borderWidth:0,hoverOffset:6}}]}},
      options:{{responsive:true,maintainAspectRatio:false,cutout:'70%',
        animation:{{animateRotate:true,duration:1000}},
        plugins:{{legend:{{display:false}}}}}}
    }});
    const L={json.dumps(labels)}, D={json.dumps(data)};
    let tc=null;
    if(L.length>0){{
      tc=new Chart(document.getElementById('tc').getContext('2d'),{{
        type:'line',
        data:{{labels:L,datasets:[{{label:'Nilai Akhir',data:D,
          borderColor:'#1e40af',backgroundColor:'rgba(30,64,175,.1)',
          fill:true,tension:.35,pointRadius:6,pointBackgroundColor:'#1e40af',
          pointBorderColor:'#fff',pointBorderWidth:2,borderWidth:2.5}}]}},
        options:{{responsive:true,maintainAspectRatio:false,
          scales:{{y:{{beginAtZero:true,max:100,ticks:{{color:isD?'#94a3b8':'#64748b'}}}},
                   x:{{ticks:{{color:isD?'#94a3b8':'#64748b'}}}}}},
          plugins:{{legend:{{display:false}}}}}}
      }});
    }}
    window.updateCharts=function(){{
      const d=document.documentElement.getAttribute('data-theme')==='dark';
      dc.data.datasets[0].backgroundColor=CC[d?'dark':'light'];
      dc.update();
      if(tc){{
        tc.options.scales.y.ticks.color=d?'#94a3b8':'#64748b';
        tc.options.scales.x.ticks.color=d?'#94a3b8':'#64748b';
        tc.update();
      }}
    }};
    </script>
    '''
    return wrap(body, s['nama'])


# ==================== ADMIN ====================
@app.route('/admin')
def admin():
    tab = request.args.get('tab', 'kelas')
    period = request.args.get('period', PERIODS[0])
    if period not in PERIODS: period = PERIODS[0]
    conn = get_db()
    classes = conn.execute("SELECT kelas,COUNT(*) AS j FROM students GROUP BY kelas ORDER BY kelas").fetchall()
    total = conn.execute("SELECT COUNT(*) AS c FROM students").fetchone()['c']
    all_students = conn.execute("SELECT * FROM students ORDER BY kelas, nama").fetchall()
    conn.close()

    pbtns = ''.join(
        f'<a href="{url_for("admin", tab=tab, period=p)}" class="period {"active" if p==period else ""}">{p}</a>'
        for p in PERIODS)

    # ===== TAB 1: Dashboard =====
    rows_kelas = ''
    for c in classes:
        cs = get_db().execute("SELECT id FROM students WHERE kelas=?", (c['kelas'],)).fetchall()
        vals = [hitung_nilai(get_assess(x['id'], period)) for x in cs]
        vals = [v for v in vals if v is not None]
        avg = round(sum(vals)/len(vals)) if vals else None
        kt, kc = kategori(avg)
        rows_kelas += f'''<tr>
          <td><b>{c['kelas']}</b></td><td>{c['j']} siswa</td>
          <td class="center"><span class="score-big s-{kc}" style="font-size:1.15rem">{avg if avg is not None else '—'}</span></td>
          <td>{kt}</td>
          <td class="center"><a href="{url_for('admin_class', kelas=c['kelas'], period=period)}" class="btn btn-outline btn-sm">Kelola &rarr;</a></td>
        </tr>'''

    tab_kelas = f'''
    <div class="periods">{pbtns}</div>
    <div class="grid grid-3" style="margin-bottom:1.5rem">
      <div class="stat"><div class="stat-icon blue">&#128101;</div>
        <div><div class="stat-val">{total}</div><div class="stat-lbl">Total Siswa</div></div></div>
      <div class="stat"><div class="stat-icon green">&#127979;</div>
        <div><div class="stat-val">{len(classes)}</div><div class="stat-lbl">Kelas</div></div></div>
      <div class="stat"><div class="stat-icon amber">&#128203;</div>
        <div><div class="stat-val">{period}</div><div class="stat-lbl">Periode Aktif</div></div></div>
    </div>
    <div class="table-wrap"><table>
      <thead><tr><th>Kelas</th><th>Jumlah</th><th class="center">Rata-rata</th><th>Kategori</th><th class="center">Aksi</th></tr></thead>
      <tbody>{rows_kelas}</tbody>
    </table></div>
    '''

    # ===== TAB 2: Data Siswa =====
    rows_siswa = ''
    for st in all_students:
        rows_siswa += f'''<tr>
          <td><code>{st['access_code']}</code></td>
          <td>{st['nama']}</td>
          <td>{st['kelas']}</td>
          <td class="center" style="white-space:nowrap">
            <a href="{url_for('admin_student_edit', sid=st['id'])}" class="btn btn-outline btn-sm">Edit</a>
            <a href="{url_for('admin_student_delete', sid=st['id'])}" class="btn btn-outline btn-sm"
               style="color:var(--danger);border-color:var(--danger)"
               onclick="return confirm('Hapus siswa ini?')">Hapus</a>
          </td>
        </tr>'''

    tab_siswa = f'''
    <div style="display:flex;justify-content:space-between;align-items:center;gap:1rem;flex-wrap:wrap;margin-bottom:1rem">
      <div class="search" style="flex:1;min-width:220px;margin-bottom:0">
        <input placeholder="Cari nama / kode / kelas..." oninput="filterRows(this.value,'#tblAll tbody tr')">
      </div>
      <a href="{url_for('admin_student_add')}" class="btn btn-primary btn-sm">+ Tambah Siswa</a>
    </div>
    <div class="table-wrap">
      <table id="tblAll">
        <thead><tr><th>Kode</th><th>Nama</th><th>Kelas</th><th class="center">Aksi</th></tr></thead>
        <tbody>{rows_siswa}</tbody>
      </table>
    </div>
    '''

    # ===== TAB 3: Pengaturan =====
    sc = get_school()
    wali_rows = ''
    for c in classes:
        k = c['kelas']
        wali_rows += '<div class="form-group"><label>Wali Kelas ' + k + '</label>' \
            + '<input name="wali_' + k + '" value="' + get_wali(k) + '"></div>'

    tab_setting = f'''
    <form method="post" action="{url_for('admin_settings')}">
      <div class="card">
        <h3>&#127979; Informasi Sekolah</h3>
        <div class="grid grid-2">
          <div class="form-group"><label>Nama Sekolah</label>
            <input name="school_name" value="{sc['name']}"></div>
          <div class="form-group"><label>NPSN</label>
            <input name="school_npsn" value="{sc['npsn']}"></div>
          <div class="form-group"><label>Alamat</label>
            <input name="school_address" value="{sc['address']}"></div>
          <div class="form-group"><label>Logo (emoji / URL)</label>
            <input name="school_logo" value="{sc['logo']}"></div>
          <div class="form-group"><label>Tahun Ajaran</label>
            <input name="school_year" value="{sc['year']}"></div>
          <div class="form-group"><label>Kepala Sekolah</label>
            <input name="school_headmaster" value="{sc['headmaster']}"></div>
        </div>
      </div>
      <div class="card">
        <h3>&#128101; Wali Kelas</h3>
        <div class="grid grid-2">{wali_rows}</div>
      </div>
      <button class="btn btn-primary">&#128190; Simpan Pengaturan</button>
    </form>
    '''

    body = f'''
    <div class="section-head">
      <div>
        <h2>Panel Guru</h2>
        <p class="sub" style="margin-bottom:0">Kelola nilai, siswa, dan pengaturan</p>
      </div>
    </div>

    <div class="tabs">
      <button class="tab {"active" if tab=="kelas" else ""}" onclick="showTab('tk',this)">&#128202; Nilai</button>
      <button class="tab {"active" if tab=="siswa" else ""}" onclick="showTab('ts',this)">&#128101; Siswa</button>
      <button class="tab {"active" if tab=="setting" else ""}" onclick="showTab('tt',this)">&#9881; Pengaturan</button>
    </div>

    <div id="tk" class="tab-content {"active" if tab=="kelas" else ""}">{tab_kelas}</div>
    <div id="ts" class="tab-content {"active" if tab=="siswa" else ""}">{tab_siswa}</div>
    <div id="tt" class="tab-content {"active" if tab=="setting" else ""}">{tab_setting}</div>
    '''
    return wrap(body, 'Panel Guru')


@app.route('/admin/class/<kelas>')
def admin_class(kelas):
    period = request.args.get('period', PERIODS[0])
    if period not in PERIODS: period = PERIODS[0]
    conn = get_db()
    students = conn.execute("SELECT * FROM students WHERE kelas=? ORDER BY nama", (kelas,)).fetchall()
    conn.close()

    pbtns = ''.join(
        f'<a href="{url_for("admin_class", kelas=kelas, period=p)}" class="period {"active" if p==period else ""}">{p}</a>'
        for p in PERIODS)

    def b(v):
        cls = 'l' if v == 'L' else 'cl' if v == 'CL' else 'kl' if v == 'KL' else 'empty'
        return f'<span class="badge badge-{cls}">{v or "—"}</span>'

    rows = ''
    for s in students:
        a = get_assess(s['id'], period)
        n = hitung_nilai(a)
        _, kc = kategori(n)
        cells = ''.join(f'<td class="center">{b(v)}</td>' for v in a)
        rows += f'''<tr>
          <td><code style="font-size:.78rem">{s['access_code']}</code></td>
          <td>{s['nama']}</td>{cells}
          <td class="center"><span class="score-big s-{kc}" style="font-size:1.1rem">{n if n is not None else '—'}</span></td>
          <td class="center"><a href="{url_for('admin_edit', sid=s['id'], period=period)}" class="btn btn-primary btn-sm">Edit</a></td>
        </tr>'''

    asp_h = ''.join(f'<th class="center">{a}</th>' for a in ASPECTS)

    body = f'''
    <div class="crumb">
      <a href="{url_for('admin')}">Panel Guru</a><span>&rsaquo;</span>Kelas {kelas}
    </div>
    <div class="section-head">
      <div>
        <h2>Kelas {kelas}</h2>
        <p class="sub" style="margin-bottom:0">{len(students)} siswa &middot; Klik tombol Edit untuk mengubah nilai</p>
      </div>
      <div style="display:flex;gap:.5rem">
        <a href="{url_for('admin')}" class="btn btn-outline btn-sm">&larr; Kembali</a>
        <a href="{url_for('admin_export', kelas=kelas, period=period)}" class="btn btn-success btn-sm">&#128229; Export CSV</a>
      </div>
    </div>

    <div class="periods">{pbtns}</div>

    <div class="card">
      <div class="search">
        <input placeholder="Cari nama siswa..." oninput="filterRows(this.value,'#tbl tbody tr')">
      </div>
      <div class="table-wrap">
        <table id="tbl">
          <thead><tr><th>Kode</th><th>Nama</th>{asp_h}<th class="center">Nilai</th><th class="center">Aksi</th></tr></thead>
          <tbody>{rows}</tbody>
        </table>
      </div>
    </div>
    '''
    return wrap(body, f'Kelas {kelas}')


@app.route('/admin/edit/<int:sid>', methods=['GET', 'POST'])
def admin_edit(sid):
    period = request.args.get('period', PERIODS[0])
    if period not in PERIODS: period = PERIODS[0]
    conn = get_db()
    if request.method == 'POST':
        period = request.form.get('period', period)
        for i in range(len(ASPECTS)):
            v = request.form.get(f'a{i}', '')
            conn.execute("""INSERT OR REPLACE INTO assessments
                            (student_id,period,aspect_idx,value) VALUES (?,?,?,?)""",
                         (sid, period, i, v))
        conn.execute("""INSERT OR REPLACE INTO attendance
                        (student_id,period,hadir,sakit,izin,alfa) VALUES (?,?,?,?,?,?)""",
                     (sid, period,
                      int(request.form.get('hadir', 0) or 0),
                      int(request.form.get('sakit', 0) or 0),
                      int(request.form.get('izin', 0) or 0),
                      int(request.form.get('alfa', 0) or 0)))
        note = request.form.get('note', '').strip()
        if note:
            conn.execute("INSERT INTO notes (student_id,period,note) VALUES (?,?,?)",
                         (sid, period, note))
        conn.commit()
        kelas = conn.execute("SELECT kelas FROM students WHERE id=?", (sid,)).fetchone()['kelas']
        conn.close()
        flash(f'Data {period} berhasil disimpan.', 'success')
        return redirect(url_for('admin_class', kelas=kelas, period=period))

    s = conn.execute("SELECT * FROM students WHERE id=?", (sid,)).fetchone()
    conn.close()
    if not s:
        flash('Siswa tidak ditemukan.', 'error')
        return redirect(url_for('admin'))

    a = get_assess(sid, period)
    att = get_att(sid, period)
    notes = get_notes(sid, period)
    n_val = hitung_nilai(a)
    kat, kc = kategori(n_val)

    def opts(cur):
        return ''.join(f'<option value="{v}" {"selected" if v==cur else ""}>{v or "— kosong —"}</option>'
                       for v in ['','L','CL','KL'])

    asp_form = ''.join(
        f'<div class="form-group"><label>{ASPECTS[i]}</label><select name="a{i}">{opts(a[i])}</select></div>'
        for i in range(len(ASPECTS)))

    notes_html = ''
    for n in notes:
        notes_html += f'''<div class="tl-item">
          <div class="date">{n["created_at"]} &middot; {n["period"]}</div>
          <div class="text">{n["note"]}</div>
        </div>'''
    if not notes_html:
        notes_html = '<div class="empty"><div class="ico">&#128221;</div>Belum ada catatan.</div>'

    body = f'''
    <div class="crumb">
      <a href="{url_for('admin')}">Panel Guru</a><span>&rsaquo;</span>
      <a href="{url_for('admin_class', kelas=s['kelas'], period=period)}">Kelas {s['kelas']}</a><span>&rsaquo;</span>
      Edit
    </div>
    <div class="section-head">
      <div>
        <h2>{s['nama']}</h2>
        <p class="sub" style="margin-bottom:0">Kelas {s['kelas']} &middot; Periode <b>{period}</b></p>
      </div>
      <a href="{url_for('admin_class', kelas=s['kelas'], period=period)}" class="btn btn-outline btn-sm">&larr; Kembali</a>
    </div>

    <div class="grid grid-2">
      <div class="card">
        <h3>&#128221; Form Penilaian</h3>
        <form method="post">
          <input type="hidden" name="period" value="{period}">
          <div class="grid grid-4">{asp_form}</div>

          <h3 style="margin-top:1rem">&#128197; Absensi {period}</h3>
          <div class="grid grid-4">
            <div class="form-group"><label>Hadir</label><input name="hadir" type="number" min="0" value="{att['hadir']}"></div>
            <div class="form-group"><label>Sakit</label><input name="sakit" type="number" min="0" value="{att['sakit']}"></div>
            <div class="form-group"><label>Izin</label><input name="izin" type="number" min="0" value="{att['izin']}"></div>
            <div class="form-group"><label>Alfa</label><input name="alfa" type="number" min="0" value="{att['alfa']}"></div>
          </div>

          <div class="form-group">
            <label>Catatan Guru (opsional)</label>
            <textarea name="note" rows="3" placeholder="Contoh: Ananda aktif dalam diskusi kelompok hari ini..."></textarea>
          </div>
          <button class="btn btn-primary">&#128190; Simpan Perubahan</button>
        </form>
      </div>

      <div class="card">
        <h3>Pratinjau Nilai</h3>
        <div style="text-align:center;padding:1rem 0">
          <div class="score-big s-{kc}" style="font-size:3rem">{n_val if n_val is not None else '—'}</div>
          <div style="font-size:.95rem;font-weight:600;margin-top:.35rem">{kat}</div>
        </div>
        <div style="border-top:1px solid var(--border);padding-top:1rem;margin-top:1rem">
          <h3 style="font-size:.9rem">Riwayat Catatan</h3>
          <div class="timeline">{notes_html}</div>
        </div>
      </div>
    </div>
    '''
    return wrap(body, f'Edit {s["nama"]}')


@app.route('/admin/export/<kelas>')
def admin_export(kelas):
    period = request.args.get('period', PERIODS[0])
    if period not in PERIODS: period = PERIODS[0]
    conn = get_db()
    students = conn.execute("SELECT * FROM students WHERE kelas=? ORDER BY nama", (kelas,)).fetchall()
    conn.close()

    buf = io.StringIO()
    w = csv.writer(buf)
    w.writerow(['Kode','Nama','Kelas'] + ASPECTS + ['Nilai Akhir','Kategori','Hadir','Sakit','Izin','Alfa'])
    for s in students:
        a = get_assess(s['id'], period)
        n = hitung_nilai(a)
        kt, _ = kategori(n)
        att = get_att(s['id'], period)
        w.writerow([s['access_code'], s['nama'], s['kelas']] + a +
                   [n if n is not None else '', kt,
                    att['hadir'], att['sakit'], att['izin'], att['alfa']])

    fn = f"rekap_{kelas}_{period.replace(' ','_')}.csv"
    return Response('\ufeff' + buf.getvalue(), mimetype='text/csv; charset=utf-8',
                    headers={'Content-Disposition': f'attachment; filename={fn}'})


# ==================== ADMIN: SETTINGS & STUDENTS ====================
@app.route('/admin/settings', methods=['GET', 'POST'])
def admin_settings():
    if request.method == 'POST':
        for key in ['school_name','school_address','school_npsn',
                    'school_logo','school_year','school_headmaster']:
            v = request.form.get(key, '').strip()
            if v:
                set_setting(key, v)
        conn = get_db()
        classes = [r['kelas'] for r in conn.execute(
            "SELECT DISTINCT kelas FROM students ORDER BY kelas").fetchall()]
        conn.close()
        for k in classes:
            set_setting('wali_' + k, request.form.get('wali_' + k, '').strip())
        flash('Pengaturan berhasil disimpan.', 'success')
    return redirect(url_for('admin', tab='setting'))


@app.route('/admin/students')
def admin_students():
    conn = get_db()
    students = conn.execute("SELECT * FROM students ORDER BY kelas, nama").fetchall()
    conn.close()

    rows = ''
    for st in students:
        rows += f'''<tr>
          <td><code>{st['access_code']}</code></td>
          <td>{st['nama']}</td>
          <td>{st['kelas']}</td>
          <td class="center" style="white-space:nowrap">
            <a href="{url_for('admin_student_edit', sid=st['id'])}" class="btn btn-outline btn-sm">Edit</a>
            <a href="{url_for('admin_student_delete', sid=st['id'])}" class="btn btn-outline btn-sm"
               style="color:var(--danger);border-color:var(--danger)"
               onclick="return confirm('Hapus siswa ini?')">Hapus</a>
          </td>
        </tr>'''

    body = f'''
    <div class="crumb">
      <a href="{url_for('admin')}">Panel Guru</a><span>&rsaquo;</span>Data Siswa
    </div>
    <div class="section-head">
      <div>
        <h2>Data Siswa</h2>
        <p class="sub" style="margin-bottom:0">Total {len(students)} siswa</p>
      </div>
      <div style="display:flex;gap:.5rem">
        <a href="{url_for('admin')}" class="btn btn-outline btn-sm">&larr; Kembali</a>
        <a href="{url_for('admin_student_add')}" class="btn btn-primary btn-sm">+ Tambah Siswa</a>
      </div>
    </div>

    <div class="card">
      <div class="search">
        <input placeholder="Cari nama / kode / kelas..." oninput="filterRows(this.value,'#tblStu tbody tr')">
      </div>
      <div class="table-wrap">
        <table id="tblStu">
          <thead><tr><th>Kode</th><th>Nama</th><th>Kelas</th><th class="center">Aksi</th></tr></thead>
          <tbody>{rows}</tbody>
        </table>
      </div>
    </div>
    '''
    return wrap(body, 'Data Siswa')


@app.route('/admin/student/add', methods=['GET', 'POST'])
def admin_student_add():
    if request.method == 'POST':
        nama = request.form.get('nama', '').strip()
        kelas = request.form.get('kelas', '').strip().upper()
        kode = request.form.get('kode', '').strip().upper()
        if not nama or not kelas or not kode:
            flash('Semua field wajib diisi.', 'error')
        else:
            conn = get_db()
            try:
                cur = conn.cursor()
                cur.execute("INSERT INTO students (access_code, nama, kelas) VALUES (?,?,?)",
                            (kode, nama, kelas))
                sid = cur.lastrowid
                for period in PERIODS:
                    for i in range(len(ASPECTS)):
                        conn.execute("INSERT INTO assessments (student_id, period, aspect_idx, value) VALUES (?,?,?,'')",
                                     (sid, period, i))
                    conn.execute("INSERT INTO attendance (student_id, period) VALUES (?,?)",
                                 (sid, period))
                conn.commit()
                conn.close()
                flash(f'Siswa {nama} berhasil ditambahkan.', 'success')
                return redirect(url_for('admin', tab='siswa'))
            except sqlite3.IntegrityError:
                flash('Kode akses sudah dipakai siswa lain.', 'error')
                conn.close()

    body = f'''
    <div class="crumb">
      <a href="{url_for('admin')}">Panel Guru</a><span>&rsaquo;</span>
      <a href="{url_for('admin_students')}">Data Siswa</a><span>&rsaquo;</span>Tambah
    </div>
    <div class="section-head">
      <div><h2>Tambah Siswa</h2></div>
      <a href="{url_for('admin_students')}" class="btn btn-outline btn-sm">&larr; Kembali</a>
    </div>

    <div class="card" style="max-width:640px">
      <form method="post">
        <div class="form-group"><label>Nama Lengkap</label>
          <input name="nama" required autofocus placeholder="Nama lengkap siswa"></div>
        <div class="grid grid-2">
          <div class="form-group"><label>Kelas</label>
            <input name="kelas" required placeholder="Contoh: 4B" style="text-transform:uppercase"></div>
          <div class="form-group"><label>Kode Akses</label>
            <input name="kode" required placeholder="Contoh: 4B-019" style="text-transform:uppercase"></div>
        </div>
        <p style="font-size:.8rem;color:var(--muted);margin-bottom:1rem">
          Setiap siswa otomatis mendapat slot nilai &amp; absensi untuk semua periode.</p>
        <div style="display:flex;gap:.5rem">
          <button class="btn btn-primary">&#128190; Simpan</button>
          <a href="{url_for('admin_students')}" class="btn btn-outline">Batal</a>
        </div>
      </form>
    </div>
    '''
    return wrap(body, 'Tambah Siswa')


@app.route('/admin/student/<int:sid>/edit', methods=['GET', 'POST'])
def admin_student_edit(sid):
    conn = get_db()
    st = conn.execute("SELECT * FROM students WHERE id=?", (sid,)).fetchone()
    conn.close()
    if not st:
        flash('Siswa tidak ditemukan.', 'error')
        return redirect(url_for('admin', tab='siswa'))

    if request.method == 'POST':
        nama = request.form.get('nama', '').strip()
        kelas = request.form.get('kelas', '').strip().upper()
        kode = request.form.get('kode', '').strip().upper()
        if not nama or not kelas or not kode:
            flash('Semua field wajib diisi.', 'error')
        else:
            conn = get_db()
            try:
                conn.execute("UPDATE students SET nama=?, kelas=?, access_code=? WHERE id=?",
                             (nama, kelas, kode, sid))
                conn.commit()
                conn.close()
                flash('Data siswa berhasil diperbarui.', 'success')
                return redirect(url_for('admin', tab='siswa'))
            except sqlite3.IntegrityError:
                flash('Kode akses sudah dipakai siswa lain.', 'error')
                conn.close()

    body = f'''
    <div class="crumb">
      <a href="{url_for('admin')}">Panel Guru</a><span>&rsaquo;</span>
      <a href="{url_for('admin_students')}">Data Siswa</a><span>&rsaquo;</span>Edit
    </div>
    <div class="section-head">
      <div><h2>Edit Siswa</h2>
        <p class="sub" style="margin-bottom:0">{st['nama']}</p></div>
      <a href="{url_for('admin_students')}" class="btn btn-outline btn-sm">&larr; Kembali</a>
    </div>

    <div class="card" style="max-width:640px">
      <form method="post">
        <div class="form-group"><label>Nama Lengkap</label>
          <input name="nama" required value="{st['nama']}"></div>
        <div class="grid grid-2">
          <div class="form-group"><label>Kelas</label>
            <input name="kelas" required value="{st['kelas']}" style="text-transform:uppercase"></div>
          <div class="form-group"><label>Kode Akses</label>
            <input name="kode" required value="{st['access_code']}" style="text-transform:uppercase"></div>
        </div>
        <div style="display:flex;gap:.5rem">
          <button class="btn btn-primary">&#128190; Simpan</button>
          <a href="{url_for('admin_students')}" class="btn btn-outline">Batal</a>
        </div>
      </form>
    </div>
    '''
    return wrap(body, 'Edit Siswa')


@app.route('/admin/student/<int:sid>/delete')
def admin_student_delete(sid):
    conn = get_db()
    st = conn.execute("SELECT nama FROM students WHERE id=?", (sid,)).fetchone()
    if st:
        conn.execute("DELETE FROM students WHERE id=?", (sid,))
        conn.execute("DELETE FROM assessments WHERE student_id=?", (sid,))
        conn.execute("DELETE FROM attendance WHERE student_id=?", (sid,))
        conn.execute("DELETE FROM notes WHERE student_id=?", (sid,))
        conn.commit()
        flash(f'Siswa {st["nama"]} berhasil dihapus.', 'success')
    conn.close()
    return redirect(url_for('admin', tab='siswa'))




if __name__ == '__main__':
    init_db()
    ensure_schema()
    print("\n" + "="*50)
    print("  SISTEM INFORMASI PERKEMBANGAN SISWA")
    print("="*50)
    print("  Beranda (walimurid) : http://127.0.0.1:5000/")
    print("  Panel Guru (admin)  : http://127.0.0.1:5000/admin")
    print("="*50 + "\n")
    app.run(host='0.0.0.0', port=5000, debug=False)
