import math
import numpy as np
import pandas as pd
import scipy.stats as st
from functools import reduce

def p_value(row,
            col,
            control_bucket="control_group",
            treatment_bucket="treatment"):
    n_control = row[f"{control_bucket}_view_user_cnt"]
    n_variant = row[f"{treatment_bucket}_view_user_cnt"]

    crv_control = row[f"{control_bucket}_{col}"]
    crv_variant = row[f"{treatment_bucket}_{col}"]

    # Variance
    var_control = crv_control * (1 - crv_control)
    var_variant = crv_variant * (1 - crv_variant)

    conversions_control = crv_control * n_control
    conversions_variant = crv_variant * n_variant

    # Create combined random variable S
    mean_control = crv_control
    mean_variant = crv_variant
    S_mean = mean_variant - mean_control
    S_var = (var_control / n_control) + (var_variant / n_variant)

    Z_score = S_mean / np.sqrt(abs(S_var))

    p_value_1_tail = 1 - st.norm.cdf(Z_score)
    p_value_2_tail = p_value_1_tail * 2

    if p_value_2_tail > 1:
        p_value_2_tail = 2 - p_value_2_tail

    return p_value_2_tail

def calculate_sample_size(alpha, power_level, p, delta):
    if p > 0.5:
        p = 1.0 - p

    t_alpha2 = st.norm.ppf(1.0 - alpha / 2)
    t_beta = st.norm.ppf(power_level)

    sd1 = math.sqrt(2 * p * (1.0 - p))
    sd2 = math.sqrt(p * (1.0 - p) + (p + delta) * (1.0 - p - delta))

    return ((t_alpha2 * sd1 + t_beta * sd2) ** 2) / (delta ** 2)

def ab_test_calculations(df):
    # Calculate CTR and CR
    df["ctr"] = df["click_user_cnt"] / df["view_user_cnt"]
    df["cr"] = df["order_user_cnt"] / df["view_user_cnt"]

    dfs = []
    cols = ["cr", "ctr", "view_user_cnt"]
    if "dy" in df.columns:
        cols = ["dy"] + cols

    # Create buckets
    bucket_cols = df["experiments"].unique()
    for bucket in bucket_cols:
        sub_df = df.loc[df["experiments"] == bucket, cols].reset_index(drop=True).add_prefix(f"{bucket}_")

        if "dy" in df.columns:
            sub_df.rename(columns={f"{bucket}_dy": "dy"}, inplace=True)
        dfs.append(sub_df)

    if "dy" in df.columns:
        df = reduce(lambda df1, df2: pd.merge(df1, df2, "inner", on="dy"), dfs)
    else:
        df = pd.concat(dfs, axis=1)

    # Calculate p-values
    p_value_cols = ["cr", "ctr"]
    for p_value_col in p_value_cols:
        df[f"p-value-{p_value_col}"] = df.apply(lambda x: p_value(x, p_value_col), axis=1)

    dfs = []
    for bucket in bucket_cols:
        cols = [f"{bucket}_view_user_cnt",
                f"{bucket}_ctr",
                f"{bucket}_cr",
                "p-value-cr",
                "p-value-ctr"]

        if "dy" in df.columns:
            cols = ["dy"] + cols

        sub_df = df[cols]
        sub_df["experiments"] = bucket
        sub_df.columns = [col.replace(f"{bucket}_", "") for col in sub_df.columns]
        dfs.append(sub_df)

    # Sort and organize results
    df = pd.concat(dfs)
    if "dy" in df.columns:
        df = df.sort_values("dy").reset_index(drop=True)

    # Add significance columns
    for p_value_col in p_value_cols:
        df[f"significant_{p_value_col}"] = np.where(df[f"p-value-{p_value_col}"] <= 0.05, "Yes", "No")

    return df

def ab_test_calculations_overall(df):
    df = pd.DataFrame(df.groupby("experiments", as_index=False).sum())
    df = ab_test_calculations(df)

    return df
