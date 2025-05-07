import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output, State
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError

# PostgreSQL Connection
DATABASE_URL = "postgresql+psycopg2://postgres:postgres@student_postgres:5432/student_analytics_db"
engine = create_engine(DATABASE_URL)

# Dash App Init with custom theme
app = dash.Dash(__name__, external_stylesheets=[
    "https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css",
    "https://cdnjs.cloudflare.com/ajax/libs/animate.css/4.1.1/animate.min.css",
    "https://cdnjs.cloudflare.com/ajax/libs/aos/2.3.4/aos.css"
])
app.title = "Student Well-being & Performance Insights"
server = app.server

# Global style enhancements
APP_STYLE = {
    'fontFamily': 'Segoe UI, Roboto, Helvetica Neue, sans-serif',
    'backgroundColor': '#f8f9fa',
    'padding': '20px'
}

HEADER_STYLE = {
    'fontSize': '32px',
    'fontWeight': '700',
    'textAlign': 'center',
    'color': '#003366',
    'marginBottom': '20px',
    'textShadow': '1px 1px 2px rgba(0,0,0,0.1)'
}

# Safe SQL Loaders
def safe_sql_query(query):
    try:
        return pd.read_sql(query, engine)
    except SQLAlchemyError as e:
        print(f"SQL error: {e}")
        return pd.DataFrame()

##def load_student_data():
 ##   return safe_sql_query("SELECT * FROM student")
def load_student_data():
    df = safe_sql_query("SELECT * FROM student")
    df['region'] = df['region'].replace([None, 'null', pd.NA], 'USA')
    return df


def load_factors_data():
    return safe_sql_query("SELECT * FROM student_performance")

def layout_home():
    students_df = load_student_data()
    perf_df = load_factors_data()

    if students_df.empty or perf_df.empty:
        return dbc.Alert("Student or performance data is unavailable.", color="danger")

    try:
        avg_exam = round(pd.to_numeric(perf_df['exam_score'], errors='coerce').mean(), 1)
    except: avg_exam = 'N/A'

    try:
        avg_dep = round(pd.to_numeric(students_df['todep'], errors='coerce').mean(), 2)
    except: avg_dep = 'N/A'

    try:
        avg_sleep = round(pd.to_numeric(perf_df['sleep_hours'], errors='coerce').mean(), 2)
    except: avg_sleep = 'N/A'

    try:
        avg_study = round(pd.to_numeric(perf_df['hours_studied'], errors='coerce').mean(), 2)
    except: avg_study = 'N/A'

    try:
        risk_students = students_df[students_df['depsev'].str.lower().isin(['severe', 'moderate'])]
        risk_pct = round(len(risk_students) / len(students_df) * 100, 1)
    except:
        risk_pct = 'N/A'

    kpi_cards = dbc.Row([
        dbc.Col(dbc.Card(dbc.CardBody([
            html.H6("Average Exam Score", className="text-muted"),
            html.H3(avg_exam, className="fw-bold text-primary")
        ]), className="shadow border-0"), width=2),
        dbc.Col(dbc.Card(dbc.CardBody([
            html.H6("Avg Depression Score", className="text-muted"),
            html.H3(avg_dep, className="fw-bold text-danger")
        ]), className="shadow border-0"), width=2),
        dbc.Col(dbc.Card(dbc.CardBody([
            html.H6("Avg Sleep Hours", className="text-muted"),
            html.H3(avg_sleep, className="fw-bold text-dark")
        ]), className="shadow border-0"), width=2),
        dbc.Col(dbc.Card(dbc.CardBody([
            html.H6("Avg Study Hours", className="text-muted"),
            html.H3(avg_study, className="fw-bold text-dark")
        ]), className="shadow border-0"), width=2),
        dbc.Col(dbc.Card(dbc.CardBody([
            html.H6("% At-Risk (Dep) Students", className="text-muted"),
            html.H3(f"{risk_pct}%", className="fw-bold text-danger")
        ]), className="shadow border-0"), width=3)
    ], className="mb-4")

    bar_fig, heat_fig = {}, {}
    try:
        merged = perf_df.merge(students_df[['student_id', 'suicide']], on='student_id', how='left')
        bar_data = merged.groupby('suicide')['exam_score'].mean().reset_index()
        bar_fig = px.bar(bar_data, x='suicide', y='exam_score', color='suicide', title='Avg Exam Score by Suicidal Thoughts')
    except Exception as e:
        print(f"Bar chart error: {e}")

    try:
        vars_of_interest = ['hours_studied', 'sleep_hours', 'previous_scores', 'exam_score']
        numeric_df = perf_df[vars_of_interest].apply(pd.to_numeric, errors='coerce').dropna()
        if not numeric_df.empty:
            heat_fig = px.imshow(numeric_df.corr(), text_auto=True, color_continuous_scale='RdBu', title='Correlation Heatmap')
    except Exception as e:
        print(f"Heatmap error: {e}")

    return dbc.Container([
        html.H2("🌐 Holistic Student Overview", style=HEADER_STYLE),
        kpi_cards,
        html.Hr(),
        #dbc.Row([
        #    dbc.Col(dcc.Graph(figure=bar_fig), width=6),
        #    dbc.Col(dcc.Graph(figure=heat_fig), width=6)
        #dbc.Row([
        #dbc.Col(dcc.Graph(figure=heat_fig, config={'displayModeBar': False}), width=12)
        dbc.Row([
    dbc.Col(
        dcc.Graph(figure=heat_fig, config={'displayModeBar': False}),
        width=12,
        style={"padding": "0", "margin": "0"}
    )
], className="g-0")  # Removes gutter spacing

        ])
 #   ], fluid=True)

def layout_performance():
    df = load_factors_data()
    if df.empty:
        return dbc.Alert("Performance data is missing or malformed.", color="danger")
    fig = px.box(df, x="gender", y="exam_score", color="gender", title="Exam Scores by Gender")
    return dcc.Graph(figure=fig)

def layout_mental_health():
    df = load_student_data()
    if df.empty:
        return dbc.Alert("Mental health data is unavailable.", color="danger")
    fig = px.histogram(df, x="depsev", title="Distribution of Depression Severity")
    return dcc.Graph(figure=fig)

def layout_language_impact():
    df = load_student_data()
    if df.empty:
        return dbc.Alert("Language data is unavailable.", color="danger")
    try:
        fig = px.strip(
            df,
            x="academic", y="english", color="gender",
            title="English Proficiency by Academic Level",
            stripmode="overlay",
            hover_data=["region", "student_id"]
        )
    except Exception as e:
        print(f"Language tab error: {e}")
        return dbc.Alert("Error rendering language chart.", color="danger")
    return dcc.Graph(figure=fig)

def layout_demographics():
    df = load_student_data()
    if df.empty:
        return dbc.Alert("Demographic data is unavailable.", color="danger")
    fig = px.pie(df, names="region", title="Suicide Case Distribution by Region")
    return dcc.Graph(figure=fig)

app.layout = html.Div(style=APP_STYLE, children=[
    html.Link(rel="stylesheet", href="https://cdnjs.cloudflare.com/ajax/libs/aos/2.3.4/aos.css"),
    html.Script(src="https://cdnjs.cloudflare.com/ajax/libs/aos/2.3.4/aos.js"),
    html.Script("AOS.init();", type="text/javascript"),
    html.Div([
        html.Img(
            src="https://www.yu.edu/themes/custom/yu_sub/img/katz/katz-logo.png",
            style={"height": "60px", "marginBottom": "10px", "display": "block", "marginLeft": "auto", "marginRight": "auto"},
            **{"data-aos": "zoom-in"}
        )
    ]),
    html.H1("🧠 Student Well-being & Performance Insights", style=HEADER_STYLE),
    dcc.Tabs(id="tabs", value="home", children=[
        dcc.Tab(label="Overview", value="home"),
        dcc.Tab(label="Performance", value="performance"),
        dcc.Tab(label="Mental Health", value="mental_health"),
        dcc.Tab(label="Language & Academics", value="language"),
        dcc.Tab(label="Suicide Demographics", value="demographics")
    ], className="mb-4"),
    html.Div(id="tab-content", className="mt-4")
])

@app.callback(
    Output("tab-content", "children"),
    Input("tabs", "value")
)
def render_tab(tab):
    try:
        if tab == "home":
            return layout_home()
        elif tab == "performance":
            return layout_performance()
        elif tab == "mental_health":
            return layout_mental_health()
        elif tab == "language":
            return layout_language_impact()
        elif tab == "demographics":
            return layout_demographics()
        else:
            return dbc.Alert("Invalid tab selected", color="warning")
    except Exception as e:
        print(f"Callback error: {e}")
        return dbc.Alert("An error occurred while rendering the tab.", color="danger")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8050)
