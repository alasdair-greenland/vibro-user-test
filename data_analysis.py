import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

data_folder = os.path.join(BASE_DIR, "raw-data")
out_folder = os.path.join(BASE_DIR, "results")

os.makedirs(out_folder, exist_ok=True)

sns.set(style="whitegrid")

all_data = []

files = [f for f in os.listdir(data_folder) if f.endswith(".csv")]
if not files:
    raise FileNotFoundError(f"No CSV files found in {data_folder}")

for file in files:
    file_path = os.path.join(data_folder, file)
    df = pd.read_csv(file_path, sep=None, engine="python", header=None)
    filename = os.path.basename(file_path)

    df = df.iloc[:, :2]
    df.columns = ["intended", "perceived"]

    df["intended"] = df["intended"].astype(str).str.strip().str.lower()
    df["perceived"] = df["perceived"].fillna("").astype(str).str.strip().str.lower()

    participant = int(filename.split("p")[1].split("-")[0])
    set_num = int(filename.split("s")[1].split(".")[0])
    task = "input" if "input" in filename else "vibration"

    df["correct"] = (df["intended"] == df["perceived"]).astype(int)
    df["participant"] = participant
    df["set"] = set_num
    df["task"] = task

    all_data.append(df)

print(f"Working: Loaded {len(all_data)} files from {data_folder}")



data = pd.concat(all_data, ignore_index=True)
print("Confirmed Working: Loaded", len(data), "rows from", len(all_data), "files.")

# Average accuracy by participant, task, and set
grouped = data.groupby(["task", "participant", "set"])["correct"].mean().reset_index()
summary = grouped.groupby(["task", "set"])["correct"].agg(["mean", "std"]).reset_index()

print("\n=== Summary of Accuracy ===")
print(summary)

summary.to_csv(os.path.join(out_folder, "accuracy_summary.csv"), index=False)

symbol_acc = data.groupby(["task", "set", "intended"])["correct"].mean().reset_index()
symbol_acc.to_csv(os.path.join(out_folder, "symbol_accuracy.csv"), index=False)

# Bar chart for average accuracy 
plt.figure(figsize=(6, 4))
sns.barplot(data=summary, x="set", y="mean", hue="task")
plt.title("Average Accuracy by Task and Set")
plt.ylabel("Mean Accuracy")
plt.ylim(0, 1)
plt.tight_layout()
plt.savefig(os.path.join(out_folder, "accuracy_by_set.png"))
plt.close()

#Confusion matrices
print("\nMaking confusion matrices...")

for task in data["task"].unique():
    for s in sorted(data["set"].unique()):
        subset = data[(data["task"] == task) & (data["set"] == s)]
        if subset.empty:
            continue

        counts = pd.crosstab(subset["intended"], subset["perceived"])
        perc = counts.div(counts.sum(axis=1), axis=0) * 100
        perc.columns = [c if c.strip() != "" else "no response" for c in perc.columns]

        plt.figure(figsize=(6, 5))
        sns.heatmap(
            perc,
            annot=True,
            fmt=".1f",
            cmap="Blues",
            cbar=False
        )
        plt.title(f"{task.capitalize()} Set {s}")
        plt.ylabel("Actual (Intended)")
        plt.xlabel("Perceived / Inputted")
        plt.tight_layout()
        save_path = os.path.join(out_folder, f"confusion_{task}_set{s}.png")
        plt.savefig(save_path)
        plt.close()
        print("Saved", save_path)

#Emoji accuracy heatmap
heat = symbol_acc.pivot_table(index="intended", columns=["task", "set"], values="correct")
plt.figure(figsize=(7, 5))
sns.heatmap(heat * 100, annot=True, fmt=".1f", cmap="YlGnBu", linewidths=0.3)
plt.title("Emoji Accuracy by Task and Set (%)")
plt.tight_layout()
plt.savefig(os.path.join(out_folder, "symbol_accuracy_heatmap.png"))
plt.close()

#Emoji accuracy Bar
g = sns.catplot(
    data=symbol_acc,
    x="intended",
    y="correct",
    hue="task",
    col="set",
    kind="bar",
    height=4,
    aspect=1
)
g.set_titles("Set {col_name}")
g.set_ylabels("Accuracy")
g.set_xlabels("Emoji")
plt.subplots_adjust(top=0.85)
plt.suptitle("Emoji Accuracy per Task and Set")
plt.savefig(os.path.join(out_folder, "symbol_accuracy_bars.png"))
plt.close()

print("\nResults saved in:", os.path.abspath(out_folder))
