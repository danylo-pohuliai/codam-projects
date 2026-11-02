import importlib
import importlib.metadata

if __name__ == "__main__":
    installed_packages = importlib.metadata.distributions()
    dependencies = {
        "pandas": ("Data manipulation ready",
                   "Not found, use pip install pandas"),
        "numpy": ("Numerical computation ready",
                  "Not found, use pip install numpy"),
        "matplotlib": ("Visualization ready",
                       "Not found, use pip install matplotlib")}
    packages_dict = {}
    for package in installed_packages:
        packages_dict[package.metadata['Name']] = package.version
    print("\nLOADING STATUS: Loading programs...\n")
    for dependance in dependencies.keys():
        if dependance in packages_dict.keys():
            print(f"[OK] {dependance} ({packages_dict[dependance]}) "
                  f"- {dependencies[dependance][0]}")
        else:
            print(f"[ERROR] {dependance} {dependencies[dependance][1]}")
    if all(dep in packages_dict.keys() for dep in dependencies.keys()):
        pd = importlib.import_module("pandas")
        np = importlib.import_module("numpy")
        plt = importlib.import_module("matplotlib.pyplot")
        print("\nAnalyzing Matrix data...")
        print("Processing 1000 data points...")
        data = np.random.randn(1000)
        df = pd.DataFrame(data, columns=["Signal"])
        rolling_mean = df["Signal"].rolling(window=50).mean()
        print("Generating visualization...")
        plt.figure(figsize=(10, 6))
        plt.plot(df["Signal"], label="Raw Matrix Signal",
                 alpha=0.3, color="green")
        plt.plot(rolling_mean, label="Moving Average (50 points)",
                 color="red", linewidth=2)
        plt.title("Matrix Data Analysis")
        plt.xlabel("Time (ticks)")
        plt.ylabel("Signal Amplitude")
        plt.legend()
        plt.grid(True, linestyle="--", alpha=0.5)
        filename = "matrix_analysis.png"
        plt.savefig(filename)
        print("\nAnalysis complete!")
        print("Results saved to: " + filename)
    else:
        print("\nNot enoght dependencies, abort")
        print("To install all dependencies using pip:")
        print("pip install -r requirements.txt")
        print("To install all dependencies using poetry:")
        print("poetry install && poetry run python loading.py")
