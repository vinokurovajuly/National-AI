
import streamlit as st
import pandas as pd
import plotly.express as px
import html
from pathlib import Path

# =========================================================
# НАСТРОЙКИ
# =========================================================


# =========================================================
# Corporate visual palette
# =========================================================
MAIN_BLUE = "#1E3A5F"
SECONDARY_BLUE = "#6B8FB3"
LIGHT_BLUE = "#DDEAF6"
GRID_COLOR = "#E6EAF0"

status_colors = {
    "В плане": "#A7C7A1",
    "Зона внимания": "#E6C875",
    "Критическое отклонение": "#D98B8B",
}

decision_colors = {
    "Масштабировать": "#A7C7A1",
    "Доработать": "#E6C875",
    "Закрыть": "#D98B8B",
}

risk_colors = {
    "Высокий": "#D98B8B",
    "Средний": "#6B8FB3",
    "Низкий": "#DDEAF6",
}


st.set_page_config(
    page_title="Дашборд нацпроекта ИИ",
    page_icon="📊",
    layout="wide"
)

DATA_DIR = Path(__file__).parent / "data"


# =========================================================
# ЗАГРУЗКА ДАННЫХ
# =========================================================

@st.cache_data
def load_data():
    return {
        "national": pd.read_csv(DATA_DIR / "national_kpi.csv"),
        "streams": pd.read_csv(DATA_DIR / "streams.csv"),
        "industries": pd.read_csv(DATA_DIR / "industries.csv"),
        "regions": pd.read_csv(DATA_DIR / "regions.csv"),
        "projects": pd.read_csv(DATA_DIR / "projects.csv"),
    }


dfs = load_data()
national = dfs["national"]
streams = dfs["streams"]
industries = dfs["industries"]
regions = dfs["regions"]
projects = dfs["projects"]


# =========================================================
# ПЕРЕВОДЫ
# =========================================================

stream_ru = {
    "Economy & Productivity": "Экономика и производительность",
    "Social Services & Quality of Life": "Социальная сфера и качество жизни",
    "Public Administration Efficiency": "Эффективность госуправления",
    "Technological Sovereignty": "Технологический суверенитет",
    "Regional AI Development": "Региональное развитие ИИ",
    "Data": "Данные",
    "Infrastructure": "Инфраструктура",
    "Talent & Competences": "Кадры и компетенции",
    "Safety, Trust & Regulation": "Безопасность, доверие и регулирование",
}

industry_ru = {
    "Industry": "Промышленность",
    "Healthcare": "Здравоохранение",
    "Transport & Logistics": "Транспорт и логистика",
    "Agriculture": "Сельское хозяйство",
    "Public Administration": "Государственное управление",
    "Education": "Образование",
    "Energy": "Энергетика",
    "Housing & Utilities": "ЖКХ",
}

region_ru = {
    "Moscow": "Москва",
    "Saint Petersburg": "Санкт-Петербург",
    "Tatarstan": "Республика Татарстан",
    "Moscow Oblast": "Московская область",
    "Novosibirsk Oblast": "Новосибирская область",
    "Sverdlovsk Oblast": "Свердловская область",
    "Krasnodar Krai": "Краснодарский край",
    "Nizhny Novgorod Oblast": "Нижегородская область",
    "Samara Oblast": "Самарская область",
    "Rostov Oblast": "Ростовская область",
    "Perm Krai": "Пермский край",
    "Krasnoyarsk Krai": "Красноярский край",
    "Chelyabinsk Oblast": "Челябинская область",
    "Bashkortostan": "Республика Башкортостан",
    "Voronezh Oblast": "Воронежская область",
    "Primorsky Krai": "Приморский край",
    "Irkutsk Oblast": "Иркутская область",
    "Tyumen Oblast": "Тюменская область",
    "Khabarovsk Krai": "Хабаровский край",
    "Yakutia": "Республика Саха (Якутия)",
    "Kaliningrad Oblast": "Калининградская область",
    "Tomsk Oblast": "Томская область",
    "Sakhalin Oblast": "Сахалинская область",
    "Murmansk Oblast": "Мурманская область",
    "Dagestan": "Республика Дагестан",
}

federal_district_ru = {
    "Central": "Центральный",
    "Northwestern": "Северо-Западный",
    "Southern": "Южный",
    "North Caucasian": "Северо-Кавказский",
    "Volga": "Приволжский",
    "Ural": "Уральский",
    "Siberian": "Сибирский",
    "Far Eastern": "Дальневосточный",
}

kpi_ru = {
    "AI contribution to GDP": "Вклад ИИ в ВВП",
    "Confirmed economic effect": "Подтверждённый экономический эффект",
    "Productivity growth from AI": "Прирост производительности за счёт ИИ",
    "Citizen hours saved": "Сэкономленные часы граждан",
    "Sovereign critical AI systems": "Суверенные критические ИИ-системы",
    "Scaled AI solutions": "Масштабированные ИИ-решения",
    "Regional AI gap reduction": "Сокращение регионального разрыва",
    "downtime reduction": "Снижение простоев",
    "defect rate reduction": "Снижение брака",
    "cost reduction": "Снижение себестоимости",
    "waiting time reduction": "Сокращение времени ожидания",
    "doctor workload reduction": "Снижение нагрузки врачей",
    "early detection growth": "Рост ранней диагностики",
    "delivery time reduction": "Сокращение времени доставки",
    "accident reduction": "Снижение аварийности",
    "route cost reduction": "Снижение стоимости маршрутов",
    "yield growth": "Рост урожайности",
    "resource consumption reduction": "Снижение расхода ресурсов",
    "forecast accuracy": "Точность прогнозирования",
    "service time reduction": "Сокращение срока оказания услуг",
    "manual operations reduction": "Снижение ручных операций",
    "complaints reduction": "Снижение числа жалоб",
    "teacher workload reduction": "Снижение нагрузки преподавателей",
    "learning outcome growth": "Рост образовательных результатов",
    "personalized coverage": "Охват персонализированным обучением",
    "network loss reduction": "Снижение потерь в сетях",
    "outage reduction": "Снижение аварийных отключений",
    "maintenance cost reduction": "Снижение затрат на обслуживание",
    "accident prevention": "Предотвращение аварий",
    "repair time reduction": "Сокращение времени ремонта",
    "resource loss reduction": "Снижение потерь ресурсов",
}

project_ru = {
    "Predictive maintenance": "Предиктивное обслуживание",
    "AI quality control": "ИИ-контроль качества",
    "Production planning assistant": "Ассистент планирования производства",
    "AI diagnostic triage": "ИИ-триаж диагностики",
    "Medical document automation": "Автоматизация медицинских документов",
    "Patient routing model": "Модель маршрутизации пациентов",
    "Route optimization": "Оптимизация маршрутов",
    "Fleet maintenance AI": "ИИ для обслуживания автопарка",
    "Traffic risk prediction": "Прогноз транспортных рисков",
    "Crop yield forecast": "Прогноз урожайности",
    "Satellite field monitoring": "Спутниковый мониторинг полей",
    "Smart irrigation": "Умное орошение",
    "AI document check": "ИИ-проверка документов",
    "Citizen request classifier": "Классификатор обращений граждан",
    "Proactive service engine": "Движок проактивных услуг",
    "Personal learning assistant": "Персональный образовательный ассистент",
    "Teacher workload copilot": "Копилот для преподавателя",
    "Dropout risk prediction": "Прогноз риска отчисления",
    "Grid load forecasting": "Прогноз нагрузки на сети",
    "Outage prediction": "Прогноз аварийных отключений",
    "Energy loss detection": "Выявление энергопотерь",
    "Utility accident forecast": "Прогноз аварий ЖКХ",
    "Repair prioritization": "Приоритизация ремонтов",
    "Resource leakage detection": "Выявление утечек ресурсов",
}

decision_ru = {
    "Scale": "Масштабировать",
    "Improve": "Доработать",
    "Stop": "Закрыть",
}

status_ru = {
    "Green": "В плане",
    "Yellow": "Зона внимания",
    "Red": "Критическое отклонение",
}

risk_ru = {
    "Low": "Низкий",
    "Medium": "Средний",
    "High": "Высокий",
}

project_stage_ru = {
    "Idea": "Идея",
    "Pilot": "Пилот",
    "Verification": "Верификация",
    "Scale": "Масштабирование",
    "Closed": "Закрыт",
    "idea": "Идея",
    "pilot": "Пилот",
    "verification": "Верификация",
    "scale": "Масштабирование",
    "closed": "Закрыт",
}

owner_ru = {
    "Federal ministry": "Федеральное министерство",
    "Regional government": "Региональное правительство",
    "State corporation": "Госкорпорация",
    "Municipal operator": "Муниципальный оператор",
    "University center": "Университетский центр",
}






# =========================================================
# РУССКИЕ КОЛОНКИ
# =========================================================

def add_russian_columns():
    national["kpi_name_ru"] = national["kpi_name"].map(kpi_ru).fillna(national["kpi_name"])
    national["status_ru"] = national["status"].map(status_ru).fillna(national["status"])

    streams["stream_ru"] = streams["stream"].map(stream_ru).fillna(streams["stream"])
    streams["status_ru"] = streams["status"].map(status_ru).fillna(streams["status"])

    industries["industry_ru"] = industries["industry"].map(industry_ru).fillna(industries["industry"])
    industries["kpi_name_ru"] = industries["kpi_name"].map(kpi_ru).fillna(industries["kpi_name"])

    regions["risk_level_ru"] = regions["risk_level"].map(risk_ru).fillna(regions["risk_level"])
    regions["region_ru"] = regions["region"].map(region_ru).fillna(regions["region"])
    regions["federal_district_ru"] = regions["federal_district"].map(federal_district_ru).fillna(regions["federal_district"])

    projects["stream_ru"] = projects["stream"].map(stream_ru).fillna(projects["stream"])
    projects["industry_ru"] = projects["industry"].map(industry_ru).fillna(projects["industry"])
    projects["project_name_ru"] = projects["project_name"].map(project_ru).fillna(projects["project_name"])
    projects["decision_ru"] = projects["decision"].map(decision_ru).fillna(projects["decision"])
    projects["owner_ru"] = projects["owner"].map(owner_ru).fillna(projects["owner"])
    projects["region_ru"] = projects["region"].map(region_ru).fillna(projects["region"])
    projects["stage_ru"] = projects["status"].map(project_stage_ru).fillna(projects["status"])


add_russian_columns()


# =========================================================
# СТИЛИ И KPI-КАРТОЧКИ
# =========================================================

st.markdown(
    """
    <style>
        .main {
            background-color: #F7F8FA;
        }

        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
            max-width: 1500px;
        }

        h1 {
            color: #202638;
            font-weight: 800;
            margin-bottom: 0.2rem;
            line-height: 1.12;
        }

        h2, h3 {
            color: #0B1F3A;
        }

        .block-title {
            font-size: 22px;
            font-weight: 700;
            color: #10233D;
            margin: 8px 0 10px 0;
        }
        .kpi-card {
            background-color: #FFFFFF;
            border: 1px solid #E5E7EB;
            border-radius: 12px;
            padding: 22px 18px;
            min-height: 118px;
            box-shadow: 0 2px 8px rgba(15, 23, 42, 0.04);
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
        }

        .kpi-title {
            font-size: 13px;
            color: #5B6678;
            font-weight: 600;
            text-align: center;
            margin-bottom: 10px;
            line-height: 1.25;
        }

        .kpi-value {
            font-size: 30px;
            line-height: 1.05;
            color: #172033;
            font-weight: 750;
            text-align: center;
            white-space: nowrap;
        }

        .kpi-unit {
            font-size: 17px;
            margin-left: 6px;
            font-weight: 650;
            color: #172033;
        }

        section[data-testid="stSidebar"] {
            background-color: #FFFFFF;
            border-right: 1px solid #E3E7EF;
        }

        div[data-testid="stDataFrame"] {
            background-color: #FFFFFF;
            border-radius: 14px;
        }

        div[data-testid="stTable"] table {
            width: 100%;
            table-layout: fixed;
        }

        div[data-testid="stTable"] th, div[data-testid="stTable"] td {
            white-space: normal;
            word-break: normal;
            font-size: 15px;
            padding: 10px 12px;
        }

        .section-separator {
            height: 1px;
            background: linear-gradient(90deg, #D7DEE9 0%, rgba(215, 222, 233, 0) 100%);
            margin: 20px 0 10px 0;
        }

        .section-kicker {
            font-size: 11px;
            font-weight: 700;
            letter-spacing: 0.055em;
            text-transform: uppercase;
            color: #6B7280;
            margin: 0 0 4px 0;
        }

        .compact-caption {
            color: #6B7280;
            font-size: 14px;
            margin-top: -2px;
            margin-bottom: 10px;
        }



        .footer-note {    
        h1 {
            font-size: 42px !important;
            line-height: 1.12 !important;
            color: #172033 !important;
            letter-spacing: -0.02em !important;
        }

        [data-testid="stSidebar"] {
            background-color: #F8FAFC;
            border-right: 1px solid #E5E7EB;
        }

        [data-testid="stMetric"] {
            background-color: #FFFFFF;
            border: 1px solid #E5E7EB;
            border-radius: 12px;
            padding: 12px;
        }

        div[data-testid="stDataFrame"] {
            border: 1px solid #E5E7EB;
            border-radius: 12px;
            overflow: hidden;
        }

        </style>
    """,
    unsafe_allow_html=True
)




def section_title(title, kicker=None, caption=None):
    st.markdown('<div class="section-separator"></div>', unsafe_allow_html=True)
    if kicker:
        st.markdown(f'<div class="section-kicker">{kicker}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="block-title">{title}</div>', unsafe_allow_html=True)
    if caption:
        st.markdown(f'<div class="compact-caption">{caption}</div>', unsafe_allow_html=True)


def info_box(text):
    st.markdown(f'<div class="insight-box">{text}</div>', unsafe_allow_html=True)


def rule_box(text):
    st.markdown(f'<div class="rule-box">{text}</div>', unsafe_allow_html=True)


def footer_note():
    st.markdown(
        '<div class="footer-note">Данные являются синтетическими и используются для демонстрации логики мониторинга национального проекта.</div>',
        unsafe_allow_html=True
    )



def display_number(value, decimals=1):
    try:
        value = float(value)
    except (TypeError, ValueError):
        return value
    rounded = round(value, decimals)
    if rounded.is_integer():
        return f"{int(rounded):,}".replace(",", " ")
    return f"{rounded:,.{decimals}f}".replace(",", " ")


def display_percent(value, decimals=1):
    try:
        return f"{display_number(float(value) * 100, decimals)}%"
    except (TypeError, ValueError):
        return value


def display_table(df):
    out = df.copy()
    for col in out.columns:
        col_l = str(col).lower()
        if "прогресс" in col_l or col_l == "progress":
            out[col] = pd.to_numeric(out[col], errors="coerce").map(lambda x: "" if pd.isna(x) else display_percent(x))
        elif pd.api.types.is_numeric_dtype(out[col]):
            if any(w in col_l for w in ["проекты", "проектов", "регионов", "масштабировано", "количество"]):
                out[col] = out[col].map(lambda x: "" if pd.isna(x) else f"{int(round(x)):,}".replace(",", " "))
            else:
                out[col] = out[col].map(lambda x: "" if pd.isna(x) else display_number(x))
    return out


def group_industry_cells(df):
    out = df.copy()
    if "Отрасль" in out.columns:
        out = out.sort_values(["Отрасль", "KPI"]).reset_index(drop=True)
        out["Отрасль"] = out["Отрасль"].where(out["Отрасль"].ne(out["Отрасль"].shift()), "")
    return out



def render_industry_kpi_rowspan_table(industry_kpis):
    """Render industry KPI table with merged-like industry cells using HTML rowspan."""
    view = rus_table(
        industry_kpis[[
            "industry_ru", "kpi_name_ru", "baseline_value", "current_value", "target_value", "progress", "budget_bn_rub"
        ]],
        {
            "industry_ru": "Отрасль",
            "kpi_name_ru": "KPI",
            "baseline_value": "Базовое значение",
            "current_value": "Текущее значение",
            "target_value": "Целевое значение",
            "progress": "Прогресс",
            "budget_bn_rub": "Бюджет, млрд ₽"
        }
    )
    view = display_table(view)
    view = view.sort_values(["Отрасль", "KPI"]).reset_index(drop=True)

    columns = ["Отрасль", "KPI", "Базовое значение", "Текущее значение", "Целевое значение", "Прогресс", "Бюджет, млрд ₽"]

    html = """
    <style>
        .merged-table-wrap {
            width: 100%;
            overflow-x: auto;
            border: 1px solid #E5E7EB;
            border-radius: 12px;
            margin-top: 8px;
        }
        table.merged-table {
            border-collapse: collapse;
            width: 100%;
            font-size: 15px;
            color: #1F2937;
        }
        table.merged-table th {
            background: #F8FAFC;
            color: #64748B;
            font-weight: 500;
            text-align: left;
            padding: 12px 14px;
            border: 1px solid #E5E7EB;
            white-space: nowrap;
        }
        table.merged-table td {
            padding: 12px 14px;
            border: 1px solid #E5E7EB;
            vertical-align: top;
            background: #FFFFFF;
        }
        table.merged-table td.industry-cell {
            font-weight: 600;
            color: #10233D;
            background: #F8FAFC;
            min-width: 210px;
        }
        table.merged-table td.kpi-cell {
            min-width: 280px;
        }
        table.merged-table td.num-cell {
            white-space: nowrap;
            text-align: left;
        }
    
        h1 {
            font-size: 42px !important;
            line-height: 1.12 !important;
            color: #172033 !important;
            letter-spacing: -0.02em !important;
        }

        [data-testid="stSidebar"] {
            background-color: #F8FAFC;
            border-right: 1px solid #E5E7EB;
        }

        [data-testid="stMetric"] {
            background-color: #FFFFFF;
            border: 1px solid #E5E7EB;
            border-radius: 12px;
            padding: 12px;
        }

        div[data-testid="stDataFrame"] {
            border: 1px solid #E5E7EB;
            border-radius: 12px;
            overflow: hidden;
        }

        </style>
    <div class="merged-table-wrap">
    <table class="merged-table">
        <thead>
            <tr>
    """
    for col in columns:
        html += f"<th>{col}</th>"
    html += "</tr></thead><tbody>"

    for industry, group in view.groupby("Отрасль", sort=False):
        group = group.reset_index(drop=True)
        rowspan = len(group)
        for i, row in group.iterrows():
            html += "<tr>"
            if i == 0:
                html += f'<td class="industry-cell" rowspan="{rowspan}">{industry}</td>'
            html += f'<td class="kpi-cell">{row["KPI"]}</td>'
            html += f'<td class="num-cell">{row["Базовое значение"]}</td>'
            html += f'<td class="num-cell">{row["Текущее значение"]}</td>'
            html += f'<td class="num-cell">{row["Целевое значение"]}</td>'
            html += f'<td class="num-cell">{row["Прогресс"]}</td>'
            html += f'<td class="num-cell">{row["Бюджет, млрд ₽"]}</td>'
            html += "</tr>"
    html += "</tbody></table></div>"
    st.markdown(html, unsafe_allow_html=True)



def render_industry_kpi_pivot_table(df):
    """Render the industries KPI table like a pivot table: one merged industry cell per KPI group."""
    view = rus_table(
        df.sort_values(["industry_ru", "progress"], ascending=[True, False]),
        {
            "industry_ru": "Отрасль",
            "kpi_name_ru": "KPI",
            "baseline": "Базовое значение",
            "actual": "Текущее значение",
            "target": "Целевое значение",
            "progress": "Прогресс",
            "budget_bn_rub": "Бюджет, млрд ₽",
            "effect_bn_rub": "Эффект, млрд ₽",
            "projects_count": "Количество проектов",
            "scaled_projects": "Масштабированные проекты",
        },
    )

    # Keep the table compact and readable.
    columns = [
        "Отрасль",
        "KPI",
        "Базовое значение",
        "Текущее значение",
        "Целевое значение",
        "Прогресс",
        "Бюджет, млрд ₽",
        "Эффект, млрд ₽",
        "Количество проектов",
        "Масштабированные проекты",
    ]
    view = view[[c for c in columns if c in view.columns]]
    view = display_table(view)
    view = view.sort_values(["Отрасль", "KPI"]).reset_index(drop=True)

    html_table = """
    <style>
        .pivot-table-wrap {
            width: 100%;
            overflow-x: auto;
            border: 1px solid #E5E7EB;
            border-radius: 12px;
            margin-top: 8px;
        }
        table.pivot-table {
            border-collapse: collapse;
            width: 100%;
            font-size: 15px;
            color: #1F2937;
        }
        table.pivot-table th {
            background: #F8FAFC;
            color: #64748B;
            font-weight: 500;
            text-align: left;
            padding: 12px 14px;
            border: 1px solid #E5E7EB;
            white-space: nowrap;
        }
        table.pivot-table td {
            padding: 12px 14px;
            border: 1px solid #E5E7EB;
            vertical-align: top;
            background: #FFFFFF;
        }
        table.pivot-table td.industry-cell {
            font-weight: 600;
            color: #10233D;
            background: #F8FAFC;
            min-width: 230px;
            vertical-align: middle;
        }
        table.pivot-table td.kpi-cell {
            min-width: 300px;
        }
        table.pivot-table td.num-cell {
            white-space: nowrap;
            text-align: left;
        }
    
        h1 {
            font-size: 42px !important;
            line-height: 1.12 !important;
            color: #172033 !important;
            letter-spacing: -0.02em !important;
        }

        [data-testid="stSidebar"] {
            background-color: #F8FAFC;
            border-right: 1px solid #E5E7EB;
        }

        [data-testid="stMetric"] {
            background-color: #FFFFFF;
            border: 1px solid #E5E7EB;
            border-radius: 12px;
            padding: 12px;
        }

        div[data-testid="stDataFrame"] {
            border: 1px solid #E5E7EB;
            border-radius: 12px;
            overflow: hidden;
        }

        </style>
    <div class="pivot-table-wrap">
    <table class="pivot-table">
        <thead><tr>
    """

    for col in view.columns:
        html_table += f"<th>{html.escape(str(col))}</th>"
    html_table += "</tr></thead><tbody>"

    for industry, group in view.groupby("Отрасль", sort=False):
        group = group.reset_index(drop=True)
        rowspan = len(group)
        for i, row in group.iterrows():
            html_table += "<tr>"
            if i == 0:
                html_table += f'<td class="industry-cell" rowspan="{rowspan}">{html.escape(str(industry))}</td>'
            for col in view.columns:
                if col == "Отрасль":
                    continue
                cls = "kpi-cell" if col == "KPI" else "num-cell"
                html_table += f'<td class="{cls}">{html.escape(str(row[col]))}</td>'
            html_table += "</tr>"

    html_table += "</tbody></table></div>"
    st.markdown(html_table, unsafe_allow_html=True)


def kpi_card(title, value):
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">{title}</div>
            <div class="kpi-value">{value}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def safe_mean(series):
    return 0 if len(series) == 0 else series.mean()


def safe_sum(series):
    return 0 if len(series) == 0 else series.sum()


def format_bn(value):
    return f"{display_number(value)}<span class=\"kpi-unit\">млрд ₽</span>"


def format_number(value, decimals=1):
    """Форматирует число: 85.0 -> 85, 2385.3 -> 2 385.3."""
    try:
        value = float(value)
    except (TypeError, ValueError):
        return value

    rounded = round(value, decimals)
    if rounded.is_integer():
        return f"{int(rounded):,}".replace(",", " ")
    return f"{rounded:,.{decimals}f}".replace(",", " ")


def format_percent_value(value, decimals=1):
    """Форматирует долю как процент: 0.622 -> 62.2%, 0.600 -> 60%."""
    try:
        return f"{format_number(float(value) * 100, decimals)}%"
    except (TypeError, ValueError):
        return value


def display_table(df):
    """Форматирует числовые колонки таблиц: без лишних .0, с пробелами между разрядами."""
    out = df.copy()
    for col in out.columns:
        col_l = str(col).lower()
        if "прогресс" in col_l or col_l == "progress":
            out[col] = pd.to_numeric(out[col], errors="coerce").map(
                lambda x: "" if pd.isna(x) else format_percent_value(x)
            )
        elif pd.api.types.is_numeric_dtype(out[col]):
            if any(word in col_l for word in ["количество", "проекты", "регионов", "масштабировано"]):
                out[col] = out[col].map(lambda x: "" if pd.isna(x) else f"{int(round(x)):,}".replace(",", " "))
            else:
                out[col] = out[col].map(lambda x: "" if pd.isna(x) else format_number(x))
    return out


def grouped_industry_kpi_table(df):
    """Имитирует объединение повторяющихся ячеек отрасли: отрасль указана только в первой строке группы."""
    out = df.copy()
    if "Отрасль" in out.columns:
        out = out.sort_values(["Отрасль", "KPI"]).reset_index(drop=True)
        out["Отрасль"] = out["Отрасль"].where(out["Отрасль"].ne(out["Отрасль"].shift()), "")
    return out




def format_number(value, decimals=1):
    """Форматирует число: разделяет разряды пробелом и убирает .0."""
    try:
        value = float(value)
    except (TypeError, ValueError):
        return value

    rounded = round(value, decimals)
    if rounded.is_integer():
        return f"{int(rounded):,}".replace(",", " ")
    return f"{rounded:,.{decimals}f}".replace(",", " ")


def format_percent_value(value, decimals=1):
    """Форматирует долю как процент: 0.622 -> 62.2%, 0.600 -> 60%."""
    try:
        return f"{format_number(float(value) * 100, decimals)}%"
    except (TypeError, ValueError):
        return value


def display_table(df):
    """Форматирует числовые колонки таблиц для отображения."""
    out = df.copy()
    for col in out.columns:
        col_l = str(col).lower()
        if "прогресс" in col_l or col_l == "progress":
            out[col] = pd.to_numeric(out[col], errors="coerce").map(
                lambda x: "" if pd.isna(x) else format_percent_value(x)
            )
        elif pd.api.types.is_numeric_dtype(out[col]):
            if any(word in col_l for word in ["количество", "проекты", "регионов"]):
                out[col] = out[col].map(lambda x: "" if pd.isna(x) else f"{int(round(x)):,}".replace(",", " "))
            else:
                out[col] = out[col].map(lambda x: "" if pd.isna(x) else format_number(x))
    return out




def fmt1(value):
    """Число с 1 десятичным знаком."""
    return f"{value:.1f}"


def fmt_pct1(value):
    """Доля как процент с 1 десятичным знаком."""
    return f"{value * 100:.1f}%"


def display_table(df):
    """Форматирует числовые колонки для отображения в таблицах."""
    out = df.copy()
    for col in out.columns:
        col_lower = str(col).lower()
        if "progress" in col_lower or "прогресс" in col_lower:
            out[col] = pd.to_numeric(out[col], errors="coerce").map(lambda x: "" if pd.isna(x) else fmt_pct1(x))
        elif pd.api.types.is_numeric_dtype(out[col]):
            if "количество" in str(col).lower() or "проект" in str(col).lower() or "регионов" in str(col).lower():
                out[col] = out[col].map(lambda x: "" if pd.isna(x) else f"{int(round(x))}")
            else:
                out[col] = out[col].map(lambda x: "" if pd.isna(x) else fmt1(x))
    return out


def format_pct(value):
    return display_percent(value)


def rus_table(df, columns_map):
    existing = [c for c in columns_map.keys() if c in df.columns]
    return df[existing].rename(columns=columns_map)





def apply_compact_map_style(fig, height=500):
    fig.update_layout(
        height=height,
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="#FFFFFF",
        geo=dict(domain=dict(x=[0, 1], y=[0, 1])),
        coloraxis_colorbar=dict(
            title="Индекс ИИ-зрелости",
            lenmode="fraction",
            len=0.78,
            y=0.50,
            thickness=16
        )
    )
    return fig


def apply_corporate_fig_style(fig, height=None, showlegend=True):
    fig.update_layout(
        font=dict(family="Arial, sans-serif", color="#5B6678", size=13),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="#FFFFFF",
        legend=dict(
            title_font=dict(color="#6B7280", size=13),
            font=dict(color="#334155", size=12),
            bgcolor="rgba(255,255,255,0)"
        ),
        margin=dict(l=5, r=15, t=0, b=15),
        showlegend=showlegend,
    )
    if height is not None:
        fig.update_layout(height=height)
    fig.update_xaxes(
        gridcolor="#E6EAF0",
        zerolinecolor="#E6EAF0",
        tickfont=dict(color="#7A869A"),
        title_font=dict(color="#7A869A"),
    )
    fig.update_yaxes(
        gridcolor="#E6EAF0",
        zerolinecolor="#E6EAF0",
        tickfont=dict(color="#7A869A"),
        title_font=dict(color="#7A869A"),
    )
    return fig


def style_percent_bar(fig, height, right_margin=110):
    """Единый корпоративный стиль для stacked bar chart."""
    fig.update_traces(
        textposition="inside",
        insidetextanchor="middle",
        cliponaxis=False,
        textfont_size=12,
        textfont_color="#172033"
    )
    fig.update_layout(
        height=height,
        xaxis_tickformat=".0%",
        legend_title_text="Статус выполнения",
        uniformtext_minsize=9,
        uniformtext_mode="show",
        margin=dict(l=10, r=right_margin, t=10, b=30)
    )
    fig.update_yaxes(automargin=True)
    fig = apply_corporate_fig_style(fig, height=height)
    return fig


# =========================================================
# ФИЛЬТРЫ
# =========================================================

st.sidebar.title("Нацпроект ИИ")

page = st.sidebar.radio(
    "Раздел дашборда",
    [
        "1. Национальный обзор",
        "2. Стримы",
        "3. Отрасли",
        "4. Регионы",
        "5. Портфель проектов",
    ],
)

all_quarters = sorted(national["quarter"].unique())
selected_quarters = st.sidebar.multiselect(
    "Кварталы",
    all_quarters,
    default=[all_quarters[-1]],
)

selected_streams_ru = st.sidebar.multiselect(
    "Стримы",
    sorted(projects["stream_ru"].unique()),
    default=[],
    placeholder="Все стримы",
)

selected_industries_ru = st.sidebar.multiselect(
    "Отрасли",
    sorted(projects["industry_ru"].unique()),
    default=[],
    placeholder="Все отрасли",
)

selected_regions = st.sidebar.multiselect(
    "Регионы",
    sorted(projects["region"].unique()),
    default=[],
    placeholder="Все регионы",
)

selected_decisions_ru = st.sidebar.multiselect(
    "Решения",
    sorted(projects["decision_ru"].unique()),
    default=[],
    placeholder="Все решения",
)

selected_statuses = st.sidebar.multiselect(
    "Стадии проектов",
    sorted(projects["stage_ru"].unique()),
    default=[],
    placeholder="Все стадии",
)



def normalize_stage_selection(values):
    if not values:
        return values
    return [project_stage_ru.get(v, v) for v in values]


def filter_by_multiselect(df, column, selected_values):
    if selected_values:
        return df[df[column].isin(selected_values)]
    return df


def filter_projects(df):
    out = df.copy()
    out = filter_by_multiselect(out, "stream_ru", selected_streams_ru)
    out = filter_by_multiselect(out, "industry_ru", selected_industries_ru)
    out = filter_by_multiselect(out, "region_ru", selected_regions)
    out = filter_by_multiselect(out, "decision_ru", selected_decisions_ru)
    out = filter_by_multiselect(out, "stage_ru", normalize_stage_selection(selected_statuses))
    return out


def filter_quarters(df):
    if selected_quarters:
        return df[df["quarter"].isin(selected_quarters)]
    return df


# =========================================================
# 1. НАЦИОНАЛЬНЫЙ ОБЗОР
# =========================================================

if page == "1. Национальный обзор":
    st.title("Панель управления национальным проектом по развитию ИИ")
    st.caption(
        "Прототип дашборда для мониторинга реализации нацпроекта. "
        "Данные синтетические и используются для демонстрации управленческой логики."
    )

    current_kpi = filter_quarters(national).copy()
    current_streams = filter_quarters(streams).copy()
    filtered_projects = filter_projects(projects)

    c1, c2, c3, c4 = st.columns(4, gap="small")

    with c1:
        kpi_card("Прогресс KPI", format_pct(safe_mean(current_kpi["progress"])))
    with c2:
        kpi_card("Подтверждённый эффект", format_bn(safe_sum(filtered_projects["actual_effect_bn_rub"])))
    with c3:
        kpi_card("Средний ROI проектов", f"{safe_mean(filtered_projects['roi']):.2f}x")
    with c4:
        kpi_card("К масштабированию", f"{(filtered_projects['decision'] == 'Scale').sum()}")

    section_title("Прогресс по национальным KPI", "Основная динамика", "Степень достижения целевых показателей по ключевым направлениям нацпроекта.")

    kpi_chart = (
        current_kpi
        .groupby(["kpi_name_ru", "status_ru"], as_index=False)
        .agg(progress=("progress", "mean"))
        .sort_values("progress")
    )

    fig = px.bar(
        kpi_chart,
        x="progress",
        y="kpi_name_ru",
        orientation="h",
        text=kpi_chart["progress"].apply(lambda x: format_percent_value(x)),
        color="status_ru",
        color_discrete_map=status_colors,
        labels={
            "progress": "Прогресс к цели 2030",
            "kpi_name_ru": "",
            "status_ru": "Статус выполнения",
        },
    )
    fig = style_percent_bar(fig, height=410, right_margin=130)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    # Карта перенесена ниже и сделана крупной
    section_title("Карта ИИ-зрелости регионов", "География")

    region_map = regions.copy()
    if selected_regions:
        region_map = region_map[region_map["region_ru"].isin(selected_regions)]

    fig_map = px.scatter_geo(
        region_map,
        lat="lat",
        lon="lon",
        size="economic_effect_bn_rub",
        color="ai_maturity_index",
        hover_name="region_ru",
        hover_data={
            "federal_district_ru": True,
            "scaled_projects": True,
            "risk_level_ru": True,
            "economic_effect_bn_rub": True,
            "lat": False,
            "lon": False,
        },
        projection="natural earth",
        labels={
            "ai_maturity_index": "Индекс ИИ-зрелости",
            "economic_effect_bn_rub": "Экономический эффект, млрд ₽",
            "federal_district_ru": "Федеральный округ",
            "scaled_projects": "Масштабированные проекты",
            "risk_level_ru": "Риск",
        },
    )
    fig_map.update_geos(showcountries=True, showland=True, fitbounds="locations")
    fig_map.update_layout(
        height=650,
        margin=dict(l=0, r=0, t=10, b=10),
        coloraxis_colorbar=dict(
            title="Индекс ИИ-зрелости",
            lenmode="fraction",
            len=0.64,
            y=0.50,
            thickness=18
        )
    )
    fig_map = apply_corporate_fig_style(fig_map)
    fig_map = apply_compact_map_style(fig_map, height=500)
    st.plotly_chart(fig_map, use_container_width=True, config={"displayModeBar": False})

    section_title("Статус стратегических стримов", "Контроль исполнения", "Распределение прогресса стримов по статусам выполнения.")

    stream_chart = (
        current_streams
        .groupby(["stream_ru", "status_ru"], as_index=False)
        .agg(progress=("progress", "mean"))
        .sort_values("progress", ascending=True)
    )

    fig2 = px.bar(
        stream_chart,
        x="progress",
        y="stream_ru",
        orientation="h",
        color="status_ru",
        color_discrete_map=status_colors,
        text=stream_chart["progress"].apply(lambda x: format_percent_value(x)),
        labels={
            "progress": "Прогресс",
            "stream_ru": "",
            "status_ru": "Статус выполнения",
        },
    )
    fig2 = style_percent_bar(fig2, height=460, right_margin=140)
    st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})

    section_title("Управленческая логика решений", "Решения", "Сводка по портфельным решениям и связанному эффекту.")

    decision = (
        filtered_projects
        .groupby(["decision_ru"], as_index=False)
        .agg(
            projects=("project_id", "count"),
            budget_bn_rub=("budget_bn_rub", "sum"),
            effect_bn_rub=("actual_effect_bn_rub", "sum"),
            avg_roi=("roi", "mean"),
        )
        .rename(
            columns={
                "decision_ru": "Решение",
                "projects": "Проекты",
                "budget_bn_rub": "Бюджет, млрд ₽",
                "effect_bn_rub": "Эффект, млрд ₽",
                "avg_roi": "ROI",
            }
        )
    )

    if len(decision) == 0:
        st.info("Нет проектов по выбранным фильтрам.")
    else:
        decision["Бюджет, млрд ₽"] = decision["Бюджет, млрд ₽"].round(1)
        decision["Эффект, млрд ₽"] = decision["Эффект, млрд ₽"].round(1)
        decision["ROI"] = decision["ROI"].round(1)
        st.table(display_table(decision[["Решение", "Проекты", "Бюджет, млрд ₽", "Эффект, млрд ₽", "ROI"]]))


# =========================================================
# 2. СТРИМЫ
# =========================================================

elif page == "2. Стримы":
    st.title("Эффективность стратегических стримов")
    st.caption("Прогресс, бюджет, подтверждённый эффект и риски по каждому направлению нацпроекта.")

    df = filter_quarters(streams).copy()
    df = filter_by_multiselect(df, "stream_ru", selected_streams_ru)

    c1, c2, c3, c4 = st.columns(4, gap="small")
    with c1:
        kpi_card("Количество стримов", f"{df['stream_ru'].nunique()}")
    with c2:
        kpi_card("Совокупный бюджет", format_bn(safe_sum(df["budget_bn_rub"])))
    with c3:
        kpi_card("Совокупный эффект", format_bn(safe_sum(df["effect_bn_rub"])))
    with c4:
        kpi_card("Средний риск", f"{format_number(safe_mean(df['risk_score']))}/100")

    st.markdown('<div class="block-title">Прогресс по стримам</div>', unsafe_allow_html=True)

    stream_summary = (
        df.groupby(["stream_ru", "status_ru"], as_index=False)
        .agg(progress=("progress", "mean"))
        .sort_values("progress", ascending=True)
    )

    section_title(
        "Прогресс по стратегическим стримам",
        "Контроль исполнения",
        "Распределение статусов по ключевым направлениям нацпроекта."
    )

    fig = px.bar(
        stream_summary,
        x="progress",
        y="stream_ru",
        orientation="h",
        color="status_ru",
        color_discrete_map=status_colors,
        text=stream_summary["progress"].apply(lambda x: format_percent_value(x)),
        labels={"progress": "Прогресс", "stream_ru": "", "status_ru": "Статус выполнения"},
    )
    fig = style_percent_bar(fig, height=500, right_margin=140)
    fig = apply_compact_map_style(fig, height=500)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    st.markdown('<div class="block-title">Эффект относительно освоенных средств</div>', unsafe_allow_html=True)

    stream_scatter = (
        df.groupby("stream_ru", as_index=False)
        .agg(
            spent_bn_rub=("spent_bn_rub", "sum"),
            effect_bn_rub=("effect_bn_rub", "sum"),
            budget_bn_rub=("budget_bn_rub", "sum"),
            risk_score=("risk_score", "mean"),
        )
    )

    fig2 = px.scatter(
        stream_scatter,
        x="spent_bn_rub",
        y="effect_bn_rub",
        size="budget_bn_rub",
        color="risk_score",
        hover_name="stream_ru",
        labels={
            "spent_bn_rub": "Освоено, млрд ₽",
            "effect_bn_rub": "Эффект, млрд ₽",
            "budget_bn_rub": "Бюджет, млрд ₽",
            "risk_score": "Индекс риска",
        },
    )
    fig2.update_layout(height=460, margin=dict(l=10, r=10, t=20, b=10))
    fig2 = apply_corporate_fig_style(fig2)
    st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})

    st.markdown('<div class="block-title">Динамика прогресса по кварталам</div>', unsafe_allow_html=True)

    fig3 = px.line(
        df,
        x="quarter",
        y="progress",
        color="stream_ru",
        markers=True,
        labels={"quarter": "Квартал", "progress": "Прогресс", "stream_ru": "Стрим"},
    )
    fig3.update_layout(height=430, yaxis_tickformat=".0%", legend_title_text="Стрим")
    fig3 = apply_corporate_fig_style(fig3)
    st.plotly_chart(fig3, use_container_width=True, config={"displayModeBar": False})

    section_title("Таблица стримов", "Детализация")
    st.dataframe(
        display_table(rus_table(
            df.sort_values("risk_score", ascending=False),
            {
                "quarter": "Квартал",
                "stream_ru": "Стрим",
                "owner": "Ответственный",
                "budget_bn_rub": "Бюджет, млрд ₽",
                "spent_bn_rub": "Освоено, млрд ₽",
                "effect_bn_rub": "Эффект, млрд ₽",
                "progress": "Прогресс",
                "risk_score": "Риск",
                "status_ru": "Статус выполнения",
            },
        )),
        use_container_width=True,
        hide_index=True,
    )


# =========================================================
# 3. ОТРАСЛИ
# =========================================================

elif page == "3. Отрасли":
    st.title("Отраслевое каскадирование KPI")
    st.caption("Связь национальных целей с отраслевыми процессами, бюджетом, эффектом и масштабированием решений.")

    df = industries.copy()
    df = filter_by_multiselect(df, "industry_ru", selected_industries_ru)

    summary = (
        df.groupby("industry_ru", as_index=False)
        .agg(
            effect_bn_rub=("effect_bn_rub", "sum"),
            budget_bn_rub=("budget_bn_rub", "sum"),
            projects_count=("projects_count", "sum"),
            scaled_projects=("scaled_projects", "sum"),
            avg_progress=("progress", "mean"),
        )
    )

    c1, c2, c3, c4 = st.columns(4, gap="small")
    with c1:
        kpi_card("Отраслей", f"{summary['industry_ru'].nunique()}")
    with c2:
        kpi_card("Совокупный эффект", format_bn(safe_sum(summary["effect_bn_rub"])))
    with c3:
        kpi_card("Масштабировано", f"{int(safe_sum(summary['scaled_projects']))}")
    with c4:
        kpi_card("Прогресс KPI", format_pct(safe_mean(summary["avg_progress"])))

    section_title(
        "Аналитика по отраслям",
        "Отраслевой срез",
        "Сопоставление экономического эффекта, бюджета и прогресса KPI по ключевым отраслям."
    )

    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.markdown('<div class="block-title">Экономический эффект по отраслям</div>', unsafe_allow_html=True)

        fig = px.bar(
            summary.sort_values("effect_bn_rub", ascending=False),
            x="industry_ru",
            y="effect_bn_rub",
            labels={"effect_bn_rub": "Эффект, млрд ₽", "industry_ru": ""},
        )
        fig.update_layout(height=430, xaxis_tickangle=-30)
        fig = apply_corporate_fig_style(fig)
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    with col2:
        st.markdown('<div class="block-title">Эффект и бюджет по отраслям</div>', unsafe_allow_html=True)

        fig2 = px.scatter(
            summary,
            x="budget_bn_rub",
            y="effect_bn_rub",
            size="scaled_projects",
            color="avg_progress",
            hover_name="industry_ru",
            labels={
                "budget_bn_rub": "Бюджет, млрд ₽",
                "effect_bn_rub": "Эффект, млрд ₽",
                "scaled_projects": "Масштабированные проекты",
                "avg_progress": "Средний прогресс",
            },
        )
        fig2.update_layout(height=430)
        fig2 = apply_corporate_fig_style(fig2)
        st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})

    section_title("Отраслевые KPI", "Детализация", "Список отраслевых KPI с базовыми, текущими и целевыми значениями.")
    render_industry_kpi_pivot_table(df)


# =========================================================
# 4. РЕГИОНЫ
# =========================================================

elif page == "4. Регионы":
    st.title("Региональное развитие ИИ")
    st.caption("ИИ-зрелость регионов, экономический эффект, инфраструктура, кадровый дефицит и риски.")

    df = regions.copy()
    df = filter_by_multiselect(df, "region_ru", selected_regions)

    c1, c2, c3, c4 = st.columns(4, gap="small")
    with c1:
        kpi_card("Регионов", f"{len(df)}")
    with c2:
        kpi_card("Средняя ИИ-зрелость", f"{format_number(safe_mean(df['ai_maturity_index']))}/100")
    with c3:
        kpi_card("Экономический эффект", format_bn(safe_sum(df["economic_effect_bn_rub"])))
    with c4:
        kpi_card("Социальный эффект", f"{format_number(safe_mean(df['social_effect_score']))}/100")

    # Карта сделана отдельным крупным блоком на всю ширину
    section_title("Карта ИИ-зрелости регионов", "География")

    fig = px.scatter_geo(
        df,
        lat="lat",
        lon="lon",
        size="economic_effect_bn_rub",
        color="ai_maturity_index",
        hover_name="region_ru",
        hover_data={
            "federal_district_ru": True,
            "scaled_projects": True,
            "risk_level_ru": True,
            "talent_gap": True,
            "lat": False,
            "lon": False,
        },
        projection="natural earth",
        labels={
            "ai_maturity_index": "ИИ-зрелость",
            "economic_effect_bn_rub": "Экономический эффект, млрд ₽",
            "federal_district_ru": "Федеральный округ",
            "scaled_projects": "Масштабированные проекты",
            "risk_level_ru": "Риск",
            "talent_gap": "Дефицит кадров",
        },
    )
    fig.update_geos(showcountries=True, showland=True, fitbounds="locations")
    fig.update_layout(
        height=650,
        margin=dict(l=0, r=0, t=10, b=10),
        coloraxis_colorbar=dict(
            title="Индекс ИИ-зрелости",
            lenmode="fraction",
            len=0.64,
            y=0.50,
            thickness=18
        )
    )
    fig = apply_corporate_fig_style(fig)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    col1, col2 = st.columns([1, 1], gap="large")

    with col1:
        section_title("Топ регионов по ИИ-зрелости", "Рейтинг")

        top = df.sort_values("ai_maturity_index", ascending=False).head(10)
        fig2 = px.bar(
            top,
            x="ai_maturity_index",
            y="region_ru",
            orientation="h",
            labels={"ai_maturity_index": "ИИ-зрелость", "region_ru": ""},
        )
        fig2.update_layout(height=470, yaxis=dict(autorange="reversed"))
        fig2 = apply_corporate_fig_style(fig2)
        st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})

    with col2:
        section_title("Инфраструктура и кадровый дефицит", "Риски регионов")

        fig3 = px.scatter(
            df,
            x="infrastructure_score",
            y="talent_gap",
            size="economic_effect_bn_rub",
            color="risk_level_ru",
            color_discrete_map=risk_colors,
            hover_name="region_ru",
            category_orders={"risk_level_ru": ["Высокий", "Средний", "Низкий"]},
            labels={
                "infrastructure_score": "Инфраструктура",
                "talent_gap": "Дефицит кадров",
                "economic_effect_bn_rub": "Экономический эффект, млрд ₽",
                "risk_level_ru": "Риск",
            },
        )
        fig3.update_layout(height=470, legend_title_text="Риск")
        fig3 = apply_corporate_fig_style(fig3)
        st.plotly_chart(fig3, use_container_width=True, config={"displayModeBar": False})

    section_title("Типология регионов для управленческих решений", "Управленческая сегментация")
    typology_df = df.copy()
    typology_df["Тип региона"] = typology_df.apply(
        lambda row: "Лидер" if row["ai_maturity_index"] >= 70 and row["economic_effect_bn_rub"] >= df["economic_effect_bn_rub"].median()
        else ("Потенциал масштабирования" if row["infrastructure_score"] >= 65 and row["scaled_projects"] < df["scaled_projects"].median()
        else ("Зона кадровой поддержки" if row["talent_gap"] >= 55 else "Риск отставания")),
        axis=1
    )
    typology_summary = (
        typology_df
        .groupby("Тип региона", as_index=False)
        .agg(
            Регионы=("region_ru", "count"),
            Средняя_ИИ_зрелость=("ai_maturity_index", "mean"),
            Средний_эффект=("economic_effect_bn_rub", "mean")
        )
        .rename(columns={
            "Средняя_ИИ_зрелость": "Средняя ИИ-зрелость",
            "Средний_эффект": "Средний эффект, млрд ₽"
        })
    )
    st.table(display_table(typology_summary))

    section_title("Профиль регионов", "Детализация")
    st.dataframe(
        display_table(rus_table(
            df.sort_values("ai_maturity_index", ascending=False),
            {
                "region_ru": "Регион",
                "federal_district_ru": "Федеральный округ",
                "ai_maturity_index": "Индекс ИИ-зрелости",
                "economic_effect_bn_rub": "Экономический эффект, млрд ₽",
                "social_effect_score": "Социальный эффект",
                "scaled_projects": "Масштабированные проекты",
                "talent_gap": "Дефицит кадров",
                "infrastructure_score": "Инфраструктура",
                "data_readiness": "Готовность данных",
                "safety_score": "Безопасность",
                "risk_level_ru": "Риск",
            },
        )),
        use_container_width=True,
        hide_index=True,
    )


# =========================================================
# 5. ПОРТФЕЛЬ ПРОЕКТОВ
# =========================================================

else:
    st.title("Портфель ИИ-проектов")
    st.caption("Управленческая логика портфеля: масштабировать, доработать или закрыть проект.")

    rule_box(
        "<b>Правило принятия решений:</b><br>"
        "• <b>Масштабировать</b> — ROI ≥ 1.5 и риск находится в допустимой зоне.<br>"
        "• <b>Доработать</b> — эффект есть, но требуется снижение риска или уточнение модели внедрения.<br>"
        "• <b>Закрыть</b> — отсутствует подтверждённый эффект или риск превышает допустимый уровень."
    )

    df = filter_projects(projects)

    section_title("KPI портфеля", "Executive view")

    c1, c2, c3, c4 = st.columns(4, gap="small")
    with c1:
        kpi_card("Проектов", f"{len(df)}")
    with c2:
        kpi_card("Бюджет", format_bn(safe_sum(df["budget_bn_rub"])))
    with c3:
        kpi_card("Подтверждённый эффект", format_bn(safe_sum(df["actual_effect_bn_rub"])))
    with c4:
        kpi_card("Средний ROI", f"{format_number(safe_mean(df['roi']))}x")

    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.markdown('<div class="block-title">Проекты по управленческому решению</div>', unsafe_allow_html=True)

        decision_counts = df.groupby(["decision_ru"], as_index=False).size()

        fig = px.pie(
            decision_counts,
            names="decision_ru",
            values="size",
            color="decision_ru",
            color_discrete_map=decision_colors,
            labels={"decision_ru": "Решение", "size": "Количество"},
        
            hole=0.56)
        fig.update_traces(textfont_color="#10233D", textfont_size=13)
        fig.update_layout(height=430, legend_title_text="Решение")
        fig = apply_corporate_fig_style(fig)
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    with col2:
        section_title("Матрица ROI и риска", "Приоритизация")

        fig2 = px.scatter(
            df,
            x="risk_score",
            y="roi",
            color="decision_ru",
            size="budget_bn_rub",
            hover_name="project_name_ru",
            hover_data={
                "project_id": True,
                "industry_ru": True,
                "region_ru": True,
                "stage_ru": True,
                "budget_bn_rub": True,
            },
            color_discrete_map=decision_colors,
            labels={
                "risk_score": "Риск",
                "roi": "ROI",
                "decision_ru": "Решение",
                "budget_bn_rub": "Бюджет, млрд ₽",
                "project_id": "ID проекта",
                "industry_ru": "Отрасль",
                "region_ru": "Регион",
                "stage_ru": "Стадия",
            },
        )
        fig2.add_hline(y=1.5, line_dash="dash")
        fig2.add_vline(x=60, line_dash="dash")
        fig2.update_layout(height=430, legend_title_text="Решение")
        fig2 = apply_corporate_fig_style(fig2)
        st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})

    section_title("Реестр проектов", "Детализация")

    st.dataframe(
        display_table(rus_table(
            df.sort_values(["decision_ru", "roi"], ascending=[True, False]),
            {
                "project_id": "ID проекта",
                "project_name_ru": "Название проекта",
                "decision_ru": "Решение",
                "stage_ru": "Стадия",
                "stream_ru": "Стрим",
                "industry_ru": "Отрасль",
                "region_ru": "Регион",
                "owner_ru": "Ответственный",
                "budget_bn_rub": "Бюджет, млрд ₽",
                "actual_effect_bn_rub": "Эффект, млрд ₽",
                "roi": "ROI",
                "risk_score": "Риск",
                "baseline_kpi": "Базовый KPI",
                "target_kpi": "Целевой KPI",
                "actual_kpi": "Текущий KPI",
            },
        )),
        use_container_width=True,
        hide_index=True,
    )

    csv = df.to_csv(index=False).encode("utf-8-sig")
    st.download_button(
        "Скачать отфильтрованный портфель CSV",
        csv,
        "filtered_ai_projects.csv",
        "text/csv",
    )


footer_note()