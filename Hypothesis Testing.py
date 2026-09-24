# ============================================================
# WEEK 3 TASK
# Statistical Analysis and Hypothesis Testing in Python
# ============================================================

# ------------------------------------------------------------
# 1. IMPORT LIBRARIES
# ------------------------------------------------------------

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from scipy import stats
from scipy.stats import (
    ttest_ind,
    chi2_contingency,
    f_oneway,
    shapiro,
    levene,
    pearsonr
)

import statsmodels.api as sm
from statsmodels.stats.weightstats import zconfint

import warnings
warnings.filterwarnings("ignore")


# ------------------------------------------------------------
# 2. CREATE DATASET
# ------------------------------------------------------------

np.random.seed(42)

n = 150

data = {
    "Student_ID": range(1, n + 1),
    "Study_Hours": np.random.randint(1, 11, n),
    "Attendance": np.random.randint(60, 101, n),
    "Assignments_Completed": np.random.randint(3, 11, n),
    "Sleep_Hours": np.round(np.random.uniform(5, 9, n), 1)
}

df = pd.DataFrame(data)

# Generate exam score based partly on study hours
df["Exam_Score"] = (
    40
    + df["Study_Hours"] * 4
    + df["Attendance"] * 0.15
    + np.random.normal(0, 7, n)
)

# Keep scores between 0 and 100
df["Exam_Score"] = df["Exam_Score"].clip(0, 100).round(2)


# ------------------------------------------------------------
# 3. CREATE STUDY GROUP
# ------------------------------------------------------------

df["Study_Group"] = np.where(
    df["Study_Hours"] >= 6,
    "High Study",
    "Low Study"
)

# Pass/Fail category
df["Result"] = np.where(
    df["Exam_Score"] >= 50,
    "Pass",
    "Fail"
)


# ------------------------------------------------------------
# 4. DISPLAY DATA
# ------------------------------------------------------------

print("First 10 rows:")
print(df.head(10))

print("\nDataset Shape:")
print(df.shape)

print("\nColumn Names:")
print(df.columns)

print("\nData Types:")
print(df.dtypes)


# ------------------------------------------------------------
# 5. CHECK MISSING VALUES
# ------------------------------------------------------------

print("\nMissing Values:")
print(df.isnull().sum())


# ------------------------------------------------------------
# 6. DESCRIPTIVE STATISTICS
# ------------------------------------------------------------

print("\nDescriptive Statistics:")
print(df.describe())


# ------------------------------------------------------------
# 7. MEAN, MEDIAN, MODE, STANDARD DEVIATION
# ------------------------------------------------------------

print("\nMean Exam Score:")
print(df["Exam_Score"].mean())

print("\nMedian Exam Score:")
print(df["Exam_Score"].median())

print("\nMode Exam Score:")
print(df["Exam_Score"].mode()[0])

print("\nStandard Deviation:")
print(df["Exam_Score"].std())

print("\nVariance:")
print(df["Exam_Score"].var())


# ============================================================
# HYPOTHESIS 1
# Independent Two-Sample T-Test
# ============================================================

print("\n" + "="*60)
print("HYPOTHESIS 1: INDEPENDENT T-TEST")
print("="*60)

# Research Question:
# Do high-study students have different average exam scores
# compared with low-study students?

high_study = df[df["Study_Group"] == "High Study"]["Exam_Score"]

low_study = df[df["Study_Group"] == "Low Study"]["Exam_Score"]

print("\nHigh Study Group Statistics:")
print(high_study.describe())

print("\nLow Study Group Statistics:")
print(low_study.describe())


# ------------------------------------------------------------
# 8. CHECK NORMALITY
# ------------------------------------------------------------

shapiro_high = shapiro(high_study)
shapiro_low = shapiro(low_study)

print("\nShapiro-Wilk Test - High Study:")
print(shapiro_high)

print("\nShapiro-Wilk Test - Low Study:")
print(shapiro_low)


# ------------------------------------------------------------
# 9. TEST EQUALITY OF VARIANCES
# ------------------------------------------------------------

levene_test = levene(high_study, low_study)

print("\nLevene's Test:")
print(levene_test)


# ------------------------------------------------------------
# 10. INDEPENDENT T-TEST
# ------------------------------------------------------------

t_stat, p_value = ttest_ind(
    high_study,
    low_study,
    equal_var=False
)

print("\nIndependent T-Test:")
print("T-statistic:", t_stat)
print("P-value:", p_value)


# ------------------------------------------------------------
# 11. INTERPRET T-TEST
# ------------------------------------------------------------

alpha = 0.05

if p_value < alpha:
    print("\nResult:")
    print("Reject the Null Hypothesis.")
    print("There is a statistically significant difference")
    print("between the two study groups.")
else:
    print("\nResult:")
    print("Fail to Reject the Null Hypothesis.")
    print("There is no statistically significant difference.")


# ------------------------------------------------------------
# 12. MEAN DIFFERENCE
# ------------------------------------------------------------

mean_high = high_study.mean()
mean_low = low_study.mean()

mean_difference = mean_high - mean_low

print("\nMean High Study:", mean_high)
print("Mean Low Study:", mean_low)
print("Mean Difference:", mean_difference)


# ============================================================
# HYPOTHESIS 2
# CHI-SQUARE TEST
# ============================================================

print("\n" + "="*60)
print("HYPOTHESIS 2: CHI-SQUARE TEST")
print("="*60)

# Research Question:
# Is study group associated with passing the exam?

contingency_table = pd.crosstab(
    df["Study_Group"],
    df["Result"]
)

print("\nContingency Table:")
print(contingency_table)


# ------------------------------------------------------------
# 13. CHI-SQUARE TEST
# ------------------------------------------------------------

chi2, chi_p, dof, expected = chi2_contingency(
    contingency_table
)

print("\nChi-Square Statistic:", chi2)
print("P-value:", chi_p)
print("Degrees of Freedom:", dof)

print("\nExpected Frequencies:")
print(expected)


# ------------------------------------------------------------
# 14. INTERPRET CHI-SQUARE
# ------------------------------------------------------------

if chi_p < alpha:
    print("\nResult:")
    print("Reject the Null Hypothesis.")
    print("Study group and exam result are significantly associated.")
else:
    print("\nResult:")
    print("Fail to Reject the Null Hypothesis.")
    print("No significant association was found.")


# ============================================================
# HYPOTHESIS 3
# ONE-WAY ANOVA
# ============================================================

print("\n" + "="*60)
print("HYPOTHESIS 3: ONE-WAY ANOVA")
print("="*60)

# Create three study categories

df["Study_Category"] = pd.cut(
    df["Study_Hours"],
    bins=[0, 3, 6, 10],
    labels=["Low", "Medium", "High"]
)

print("\nStudy Category Counts:")
print(df["Study_Category"].value_counts())


# ------------------------------------------------------------
# 15. CREATE GROUPS
# ------------------------------------------------------------

low_group = df[
    df["Study_Category"] == "Low"
]["Exam_Score"]

medium_group = df[
    df["Study_Category"] == "Medium"
]["Exam_Score"]

high_group = df[
    df["Study_Category"] == "High"
]["Exam_Score"]


print("\nLow Study Mean:", low_group.mean())
print("Medium Study Mean:", medium_group.mean())
print("High Study Mean:", high_group.mean())


# ------------------------------------------------------------
# 16. ANOVA
# ------------------------------------------------------------

f_stat, anova_p = f_oneway(
    low_group,
    medium_group,
    high_group
)

print("\nANOVA F-statistic:", f_stat)
print("ANOVA P-value:", anova_p)


# ------------------------------------------------------------
# 17. INTERPRET ANOVA
# ------------------------------------------------------------

if anova_p < alpha:
    print("\nResult:")
    print("Reject the Null Hypothesis.")
    print("At least one study group has a significantly")
    print("different mean exam score.")
else:
    print("\nResult:")
    print("Fail to Reject the Null Hypothesis.")
    print("No significant difference was detected.")


# ============================================================
# HYPOTHESIS 4
# PEARSON CORRELATION
# ============================================================

print("\n" + "="*60)
print("HYPOTHESIS 4: PEARSON CORRELATION")
print("="*60)

# Research Question:
# Is there a relationship between study hours and exam score?

correlation, correlation_p = pearsonr(
    df["Study_Hours"],
    df["Exam_Score"]
)

print("\nPearson Correlation:", correlation)
print("P-value:", correlation_p)


if correlation_p < alpha:
    print("\nResult:")
    print("The relationship is statistically significant.")
else:
    print("\nResult:")
    print("The relationship is not statistically significant.")


# ============================================================
# 18. 95% CONFIDENCE INTERVAL FOR MEAN EXAM SCORE
# ============================================================

print("\n" + "="*60)
print("95% CONFIDENCE INTERVAL")
print("="*60)

sample_mean = df["Exam_Score"].mean()
sample_std = df["Exam_Score"].std()
sample_size = len(df)

standard_error = sample_std / np.sqrt(sample_size)

confidence_level = 0.95

degrees_freedom = sample_size - 1

t_critical = stats.t.ppf(
    (1 + confidence_level) / 2,
    degrees_freedom
)

margin_error = t_critical * standard_error

lower_ci = sample_mean - margin_error
upper_ci = sample_mean + margin_error

print("Sample Mean:", sample_mean)
print("Standard Error:", standard_error)
print("Margin of Error:", margin_error)
print("95% Confidence Interval:")
print("Lower:", lower_ci)
print("Upper:", upper_ci)


# ============================================================
# 19. HISTOGRAM - EXAM SCORE
# ============================================================

plt.figure(figsize=(10, 6))

plt.hist(
    df["Exam_Score"],
    bins=15,
    edgecolor="black"
)

plt.title("Distribution of Exam Scores")
plt.xlabel("Exam Score")
plt.ylabel("Number of Students")

plt.show()


# ============================================================
# 20. HISTOGRAM - STUDY HOURS
# ============================================================

plt.figure(figsize=(10, 6))

plt.hist(
    df["Study_Hours"],
    bins=10,
    edgecolor="black"
)

plt.title("Distribution of Study Hours")
plt.xlabel("Study Hours per Week")
plt.ylabel("Number of Students")

plt.show()


# ============================================================
# 21. BOXPLOT - STUDY GROUP VS EXAM SCORE
# ============================================================

plt.figure(figsize=(10, 6))

sns.boxplot(
    data=df,
    x="Study_Group",
    y="Exam_Score"
)

plt.title("Exam Scores by Study Group")
plt.xlabel("Study Group")
plt.ylabel("Exam Score")

plt.show()


# ============================================================
# 22. BOXPLOT - THREE STUDY CATEGORIES
# ============================================================

plt.figure(figsize=(10, 6))

sns.boxplot(
    data=df,
    x="Study_Category",
    y="Exam_Score"
)

plt.title("Exam Scores by Study Category")
plt.xlabel("Study Category")
plt.ylabel("Exam Score")

plt.show()


# ============================================================
# 23. SCATTER PLOT
# ============================================================

plt.figure(figsize=(10, 6))

plt.scatter(
    df["Study_Hours"],
    df["Exam_Score"],
    alpha=0.7
)

plt.title("Study Hours vs Exam Score")
plt.xlabel("Study Hours")
plt.ylabel("Exam Score")

plt.show()


# ============================================================
# 24. REGRESSION LINE
# ============================================================

plt.figure(figsize=(10, 6))

sns.regplot(
    data=df,
    x="Study_Hours",
    y="Exam_Score"
)

plt.title("Study Hours vs Exam Score with Regression Line")
plt.xlabel("Study Hours")
plt.ylabel("Exam Score")

plt.show()


# ============================================================
# 25. BAR CHART - MEAN SCORE BY STUDY GROUP
# ============================================================

group_means = df.groupby(
    "Study_Group",
    observed=True
)["Exam_Score"].mean()

plt.figure(figsize=(10, 6))

group_means.plot(
    kind="bar",
    edgecolor="black"
)

plt.title("Average Exam Score by Study Group")
plt.xlabel("Study Group")
plt.ylabel("Average Exam Score")

plt.xticks(rotation=0)

plt.show()


# ============================================================
# 26. BAR CHART - PASS/FAIL
# ============================================================

result_counts = df["Result"].value_counts()

plt.figure(figsize=(8, 6))

result_counts.plot(
    kind="bar",
    edgecolor="black"
)

plt.title("Pass and Fail Distribution")
plt.xlabel("Result")
plt.ylabel("Number of Students")

plt.xticks(rotation=0)

plt.show()


# ============================================================
# 27. CORRELATION MATRIX
# ============================================================

correlation_matrix = df[
    [
        "Study_Hours",
        "Attendance",
        "Assignments_Completed",
        "Sleep_Hours",
        "Exam_Score"
    ]
].corr()

print("\nCorrelation Matrix:")
print(correlation_matrix)


# ============================================================
# 28. CORRELATION HEATMAP
# ============================================================

plt.figure(figsize=(10, 7))

sns.heatmap(
    correlation_matrix,
    annot=True,
    cmap="coolwarm",
    fmt=".2f"
)

plt.title("Correlation Matrix")

plt.show()


# ============================================================
# 29. SUMMARY TABLE
# ============================================================

summary = pd.DataFrame({
    "Test": [
        "Independent T-Test",
        "Chi-Square Test",
        "One-Way ANOVA",
        "Pearson Correlation"
    ],
    "Statistic": [
        t_stat,
        chi2,
        f_stat,
        correlation
    ],
    "P_Value": [
        p_value,
        chi_p,
        anova_p,
        correlation_p
    ],
    "Significant": [
        "Yes" if p_value < alpha else "No",
        "Yes" if chi_p < alpha else "No",
        "Yes" if anova_p < alpha else "No",
        "Yes" if correlation_p < alpha else "No"
    ]
})

print("\n" + "="*60)
print("STATISTICAL TEST SUMMARY")
print("="*60)

print(summary)


# ============================================================
# 30. AUTOMATIC FINAL CONCLUSION
# ============================================================

print("\n" + "="*60)
print("FINAL CONCLUSION")
print("="*60)

print("\n1. Independent T-Test:")

if p_value < 0.05:
    print(
        "There is a statistically significant difference "
        "between high-study and low-study students."
    )
else:
    print(
        "There is no statistically significant difference "
        "between high-study and low-study students."
    )


print("\n2. Chi-Square Test:")

if chi_p < 0.05:
    print(
        "Study group and exam result have a statistically "
        "significant association."
    )
else:
    print(
        "No statistically significant association was found "
        "between study group and exam result."
    )


print("\n3. One-Way ANOVA:")

if anova_p < 0.05:
    print(
        "There is a statistically significant difference "
        "among the three study-hour groups."
    )
else:
    print(
        "There is no statistically significant difference "
        "among the three study-hour groups."
    )


print("\n4. Pearson Correlation:")

if correlation_p < 0.05:
    print(
        "Study hours and exam scores have a statistically "
        "significant linear relationship."
    )
else:
    print(
        "No statistically significant linear relationship "
        "was detected."
    )


print("\nOverall Analysis Completed Successfully.")