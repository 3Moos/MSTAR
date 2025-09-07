import numpy as np
import pandas as pd
from pathlib import Path
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

# -------- paths --------
FILE_PATH = "/Users/moose/Desktop/MSTAR/CSV data/CaClO4/15% conc/30% sat/07082025 15% CaClO4 30% sat ink 18V New fine JSC W temp SENSOR 4 cell 15 NN-KO.csv"
OUT_CSV   = "/Users/moose/Desktop/MSTAR/bihill_fit_results.csv"
OUT_PNG   = "/Users/moose/Desktop/MSTAR/bihill_fit.png"

# -------- column names in your CSV --------
TIME_COL    = "Latest: Time (s)"
OXY_COL     = "Latest: Oxygen Gas (ppm)"
CURRENT_COL = "Latest: Current (A)"

def bihill(x, Pm, Ka, Ki, Ha, Hi):
    # y = Pm/(1+(Ka/x)^Ha)/(1+(x/Ki)^Hi)  (requires x>0)
    return Pm / (1.0 + (Ka / x)**Ha) / (1.0 + (x / Ki)**Hi)

def _halfmax_x(x, y, side="left"):
    ymax = np.max(y); hm = 0.5 * ymax
    if side == "left":
        idx = np.where(y >= hm)[0]
        if idx.size == 0: return np.percentile(x, 25)
        j = idx[0]
        if j == 0: return x[0]
        x0, x1 = x[j-1], x[j]; y0, y1 = y[j-1], y[j]
    else:
        idx = np.where(y >= hm)[0]
        if idx.size == 0: return np.percentile(x, 75)
        j = idx[-1]
        if j == len(x)-1: return x[-1]
        x0, x1 = x[j], x[j+1]; y0, y1 = y[j], y[j+1]
    if y1 == y0:
        return x1
    t = (hm - y0) / (y1 - y0)
    return x0 + t*(x1 - x0)

def fit_bihill_df(raw: pd.DataFrame):
    df = raw.copy()

    # ---- force numeric
    for c in (TIME_COL, OXY_COL, CURRENT_COL):
        df[c] = pd.to_numeric(df[c], errors="coerce")
    df = df.sort_values(TIME_COL)

    # ---- mask where Current > 0
    mask_cur = df[CURRENT_COL] > 0
    n_cur = int(mask_cur.sum())

    # ---- baseline from first Current>0 row
    if n_cur == 0:
        raise ValueError("No rows with Current > 0.")
    i0 = df.index[mask_cur][0]
    baseline = float(df.loc[i0, OXY_COL])

    # ---- build x,y using ALL Current>0 rows; downshift O2 by baseline
    x_all = df.loc[mask_cur, TIME_COL].to_numpy(float)
    y_all = (df.loc[mask_cur, OXY_COL] - baseline).to_numpy(float)

    # ---- cleanup for fitting: need finite and x>0 (model divides by x)
    m_fin = np.isfinite(x_all) & np.isfinite(y_all)
    m_pos = x_all > 0
    m = m_fin & m_pos
    x = x_all[m]
    y = y_all[m]

    # diagnostics
    print(f"rows Current>0 (raw):      {n_cur}")
    print(f"…minus NaNs (time/oxygen): {n_cur - int(m_fin.sum())}")
    print(f"…minus Time<=0:            {int(m_fin.sum()) - int(m.sum())}")
    print(f"= points used in fit:      {len(x)}")

    if len(x) < 10:
        raise ValueError("Not enough valid points after cleaning.")

    # ---- initial guesses from data (no extra trimming)
    Pm0 = float(max(y.max(), 1e-6))
    Ka0 = float(_halfmax_x(x, y, "left"))
    Ki0 = float(_halfmax_x(x, y, "right"))
    Ha0, Hi0 = 6.0, 6.0

    xmin, xmax = float(x.min()), float(x.max())
    # reasonable bounds tied to data
    lower = [0.1*Pm0, 0.1*xmin, 0.1*xmin, 0.5, 0.5]
    upper = [2.0*Pm0, 5.0*xmax, 5.0*xmax, 20.0, 20.0]
    p0    = [Pm0, Ka0, Ki0, Ha0, Hi0]

    popt, pcov = curve_fit(bihill, x, y, p0=p0, bounds=(lower, upper), maxfev=80000)
    Pm, Ka, Ki, Ha, Hi = map(float, popt)
    perr = np.sqrt(np.diag(pcov)) if np.all(np.isfinite(pcov)) else [np.nan]*5

    # R^2
    yhat = bihill(x, *popt)
    ss_res = float(np.sum((y - yhat)**2))
    ss_tot = float(np.sum((y - y.mean())**2))
    r2 = 1.0 - ss_res/ss_tot if ss_tot > 0 else np.nan

    return {
        "x": x, "y": y, "yhat": yhat,
        "n_points_used": int(len(x)),
        "n_points_current_gt0": n_cur,
        "dropped_nans": int(n_cur - int(m_fin.sum())),
        "dropped_time_le0": int(int(m_fin.sum()) - int(m.sum())),
        "baseline_shift": baseline,
        "Pm": Pm, "Pm_err": float(perr[0]),
        "Ka": Ka, "Ka_err": float(perr[1]),
        "Ki": Ki, "Ki_err": float(perr[2]),
        "Ha": Ha, "Ha_err": float(perr[3]),
        "Hi": Hi, "Hi_err": float(perr[4]),
        "R2": r2
    }

def main():
    path = Path(FILE_PATH)
    df = pd.read_csv(path)

    res = fit_bihill_df(df)

    # ---- write/append results CSV (with counts so you can audit) ----
    out_csv = Path(OUT_CSV)
    row = {
        "Filename": path.name,
        "baseline_shift": res["baseline_shift"],
        "n_current_gt0": res["n_points_current_gt0"],
        "n_used": res["n_points_used"],
        "dropped_nans": res["dropped_nans"],
        "dropped_time_le0": res["dropped_time_le0"],
        "Pm": res["Pm"], "Pm_err": res["Pm_err"],
        "Ka": res["Ka"], "Ka_err": res["Ka_err"],
        "Ki": res["Ki"], "Ki_err": res["Ki_err"],
        "Ha": res["Ha"], "Ha_err": res["Ha_err"],
        "Hi": res["Hi"], "Hi_err": res["Hi_err"],
        "R2": res["R2"],
    }
    pd.DataFrame([row]).to_csv(
        out_csv,
        mode=("a" if out_csv.exists() else "w"),
        header=not out_csv.exists(),
        index=False
    )

    # ---- plot (baseline-shifted O2) ----
    plt.figure(figsize=(10,6))
    plt.scatter(res["x"], res["y"], s=8, label="Data (O₂ shifted)")
    xg = np.linspace(res["x"].min(), res["x"].max(), 900)
    plt.plot(xg, bihill(xg, res["Pm"], res["Ka"], res["Ki"], res["Ha"], res["Hi"]),
             label="BiHill fit")
    plt.xlabel(TIME_COL)
    plt.ylabel(f"{OXY_COL} (shifted)")
    plt.title(f"BiHill fit (R²={res['R2']:.4f}) — used {res['n_points_used']}/{res['n_points_current_gt0']} powered points")
    plt.legend()
    plt.tight_layout()
    plt.savefig(OUT_PNG, dpi=150)
    plt.show()

    print(f"[OK] Current>0 raw: {res['n_points_current_gt0']}  |  used in fit: {res['n_points_used']}")
    print(f"[OK] Dropped NaNs: {res['dropped_nans']}  |  Dropped Time<=0: {res['dropped_time_le0']}")
    print(f"[OK] Baseline O₂ at first Current>0: {res['baseline_shift']:.6g}")
    print(f"[OK] R² = {res['R2']:.5f}")
    print(f"[OK] Results -> {out_csv}")
    print(f"[OK] Plot    -> {OUT_PNG}")

if __name__ == "__main__":
    main()
