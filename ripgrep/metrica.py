from datetime import datetime, timedelta, timezone
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests

# ==========================================
# 1. CONFIGURAÇÕES E VARIÁVEIS INICIAIS
# ==========================================
GITHUB_TOKEN = ""  # Insira seu token do GitHub aqui (opcional para repositórios públicos)[cite: 3]
OWNER = "BurntSushi"  #[cite: 3]
REPO = "ripgrep"  #[cite: 3]
BRANCH = "master"  #[cite: 3]

DAYS_BACK = 720  # Ex: buscar commits dos últimos 2 anos[cite: 2]
BASE_URL = "https://api.github.com"  #[cite: 2, 3]


def build_headers(token=None):
  headers = {
      "Accept": "application/vnd.github+json",  #[cite: 2, 3]
      "X-GitHub-Api-Version": "2022-11-28",  #[cite: 2, 3]
  }
  if token and token.strip():  #[cite: 2]
    headers["Authorization"] = f"Bearer {token.strip()}"  #[cite: 2]
  return headers


HEADERS = build_headers(GITHUB_TOKEN)  #[cite: 2]


# ==========================================
# 2. FUNÇÕES DE REQUISIÇÃO DA API DO GITHUB
# ==========================================
def github_get(url: str, params=None):
  resp = requests.get(url, headers=HEADERS, params=params, timeout=30)  #[cite: 2]
  if resp.status_code == 401:  #[cite: 2]
    raise RuntimeError(  #[cite: 2]
        "401 Unauthorized. Tente usar GITHUB_TOKEN=None para repos públicos ou"  #[cite: 2]
        " defina um token válido."
    )
  resp.raise_for_status()  #[cite: 2]
  return resp.json()  #[cite: 2]


def get_commits_last_n_days(
    owner: str, repo: str, branch: str, days_back: int
):
  since = (
      datetime.now(timezone.utc) - timedelta(days=days_back)
  ).isoformat()  #[cite: 2]
  page = 1  #[cite: 2]
  all_commits = []  #[cite: 2]

  while True:
    url = f"{BASE_URL}/repos/{owner}/{repo}/commits"  #[cite: 2]
    params = {
        "sha": branch,  #[cite: 2]
        "since": since,  #[cite: 2]
        "per_page": 100,  #[cite: 2]
        "page": page,  #[cite: 2]
    }

    data = github_get(url, params=params)  #[cite: 2]
    if not data:  #[cite: 2]
      break

    all_commits.extend(data)  #[cite: 2]
    page += 1  #[cite: 2]

  return all_commits  #[cite: 2]


def get_all_contributors(owner: str, repo: str):
  contributors = []  #[cite: 3]
  page = 1  #[cite: 3]

  while True:
    url = f"{BASE_URL}/repos/{owner}/{repo}/contributors"  #[cite: 3]
    params = {"per_page": 100, "page": page}  #[cite: 3]
    resp = requests.get(
        url, headers=HEADERS, params=params, timeout=30
    )  #[cite: 3]
    resp.raise_for_status()  #[cite: 3]

    data = resp.json()  #[cite: 3]
    if not data:  #[cite: 3]
      break

    contributors.extend(data)  #[cite: 3]
    page += 1  #[cite: 3]

  return contributors  #[cite: 3]


def commits_to_dataframe(commits):
  rows = []  #[cite: 2]

  for c in commits:  #[cite: 2]
    github_author = c.get("author") or {}  #[cite: 2]
    commit_author = (c.get("commit") or {}).get("author") or {}  #[cite: 2]

    username = github_author.get("login")  #[cite: 2]
    name = commit_author.get("name")  #[cite: 2]
    email = commit_author.get("email")  #[cite: 2]
    date = commit_author.get("date")  #[cite: 2]

    label = username or name or email or "unknown"  #[cite: 2]

    rows.append({
        "label": label,  #[cite: 2]
        "username": username,  #[cite: 2]
        "name": name,  #[cite: 2]
        "email": email,  #[cite: 2]
        "date": date,  #[cite: 2]
        "sha": c.get("sha"),  #[cite: 2]
    })

  df = pd.DataFrame(rows)  #[cite: 2]

  summary = (
      df.groupby("label", dropna=False)  #[cite: 2]
      .agg(
          commit_count=("sha", "count"),  #[cite: 2]
          username=("username", "first"),  #[cite: 2]
          name=("name", "first"),  #[cite: 2]
          email=("email", "first"),  #[cite: 2]
          first_commit=("date", "min"),  #[cite: 2]
          last_commit=("date", "max"),  #[cite: 2]
      )
      .reset_index()  #[cite: 2]
      .sort_values("commit_count", ascending=False)  #[cite: 2]
  )

  return df, summary  #[cite: 2]


# ==========================================
# 3. EXECUÇÃO PRINCIPAL E PROCESSAMENTO
# ==========================================
if __name__ == "__main__":
  print("Extraindo dados de commits...")
  commits = get_commits_last_n_days(
      OWNER, REPO, BRANCH, DAYS_BACK
  )  #[cite: 2]
  df_raw, df_summary = commits_to_dataframe(commits)  #[cite: 2]

  # Processamento da Saúde do Repositório
  df = df_raw.copy()  #[cite: 1]
  USER_COL = "name"  # Identificador do usuário[cite: 1]
  DATE_COL = "date"  #[cite: 1]

  df[DATE_COL] = pd.to_datetime(df[DATE_COL])  #[cite: 1]
  df["month"] = (
      df[DATE_COL].dt.to_period("M").dt.to_timestamp()
  )  # Período mensal[cite: 1]

  # Primeira contribuição de cada usuário
  first_seen = (
      df.groupby(USER_COL)[DATE_COL]
      .min()
      .reset_index(name="first_date")  #[cite: 1]
  )
  first_seen["month"] = (
      first_seen["first_date"].dt.to_period("M").dt.to_timestamp()
  )  #[cite: 1]

  # Contribuidores novos e ativos por mês
  new_per_month = (
      first_seen.groupby("month")[USER_COL]
      .nunique()
      .reset_index(name="new_contributors")  #[cite: 1]
  )
  active_per_month = (
      df.groupby("month")[USER_COL]
      .nunique()
      .reset_index(name="active_contributors")  #[cite: 1]
  )

  # Consolidar Métricas
  health_df = pd.merge(
      active_per_month, new_per_month, on="month", how="outer"
  ).fillna(0)  #[cite: 1]
  health_df = health_df.sort_values("month").reset_index(
      drop=True
  )  #[cite: 1]

  # Acumulado e taxa de participação
  health_df["cumulative_contributors"] = health_df[
      "new_contributors"
  ].cumsum()  #[cite: 1]
  health_df["participation_ratio"] = np.where(
      health_df["cumulative_contributors"] > 0,
      health_df["active_contributors"]
      / health_df["cumulative_contributors"],  #[cite: 1]
      0,
  )

  # Normalização dos dados (escala de 0 a 1)
  max_active = health_df["active_contributors"].max()  #[cite: 1]
  max_new = health_df["new_contributors"].max()  #[cite: 1]

  health_df["norm_active"] = np.where(
      max_active > 0, health_df["active_contributors"] / max_active, 0
  )  #[cite: 1]
  health_df["norm_new"] = np.where(
      max_new > 0, health_df["new_contributors"] / max_new, 0
  )  #[cite: 1]

  # Pesos das Métricas
  WEIGHT_PARTICIPATION = 0.50  # 50%[cite: 1]
  WEIGHT_ACTIVE = 0.30  # 30%[cite: 1]
  WEIGHT_NEW = 0.20  # 20%[cite: 1]

  # Cálculo do Health Score (0 a 100)
  health_df["health_score"] = (
      (health_df["participation_ratio"] * WEIGHT_PARTICIPATION)
      + (health_df["norm_active"] * WEIGHT_ACTIVE)
      + (health_df["norm_new"] * WEIGHT_NEW)
  ) * 100  #[cite: 1]

  # ==========================================
  # 4. PLOTAGEM DO GRÁFICO
  # ==========================================
  plot_df = health_df.copy().sort_values("month").reset_index(drop=True)  #[cite: 4]

  plt.figure(figsize=(12, 6))  #[cite: 4]
  plt.plot(
      plot_df["month"],
      plot_df["health_score"],
      marker="o",
      label="Health score",  #[cite: 4]
  )

  plt.xlabel("Mês")  #[cite: 4]
  plt.ylabel("Health score")  #[cite: 4]
  plt.title(
      "Métrica de saúde ao longo do tempo com linha de tendência"
  )  #[cite: 4]
  plt.legend()  #[cite: 4]
  plt.tight_layout()  #[cite: 4]
  plt.savefig('grafico_MetricaDeSaudeRipgrep.png', dpi=300)
  plt.show()  #[cite: 4]