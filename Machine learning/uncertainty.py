import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from xgboost import XGBRegressor
from joblib import dump

model_save_path = 'F:/聚球藻/new/' 
global_feature_file = 'F:/聚球藻/new/data_2023_demo.xlsx' 
tuning_results_file = 'F:/聚球藻/new/hyperparameter_tuning.xlsx' 
output_folder = "F:/聚球藻/new/uncertainty_results_normalized-2023-new" 

os.makedirs(model_save_path, exist_ok=True)
os.makedirs(output_folder, exist_ok=True)


global_data = pd.read_excel(global_feature_file)
coordinates = global_data.iloc[:, 1:3]  
X_global = global_data.iloc[:, 3:]  

tuning_results = pd.read_excel(tuning_results_file)


#target_variables = [
#    "Shannon_bac", "Shannon_arc", "Shannon_fungi", "Shannon_vir",
#    "BC_bac", "BC_arc", "BC_fungi", "BC_vir",
#    'Carbon_fixation','ANR','Denitrification','DNR','Nitrification','Nitrogen_fixation','Photosynthesis','ASR','DSR','Sulfur_oxidation'
#]
target_variables = [
    "species abundance", "gene abundance"
]


n_iterations = 1000  
random_seeds = np.random.randint(0, 10000, size=n_iterations)


category_point_uncertainties = pd.DataFrame(coordinates)


for target_variable in target_variables:
    print(f"正在处理目标变量: {target_variable}")


    best_params = tuning_results[tuning_results['Target Variable'] == target_variable]
    if best_params.empty:
        print(f"\t未找到目标变量 {target_variable} 的最佳超参数，跳过。")
        continue

    best_params = eval(best_params.iloc[0]['Best Parameters'])  


    adjusted_params = {key.split('__')[-1]: value for key, value in best_params.items()}


    data = pd.read_csv("F:/聚球藻/new/abundance - new.csv")
    features = X_global.columns
    X = data[features]
    y = data[target_variable]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=42)

    global_predictions = []

    for seed in random_seeds:
        np.random.seed(seed)

        # bootstrap sampling
        boot_idx = np.random.choice(len(X_train), len(X_train), replace=True)
        X_boot = X_train.iloc[boot_idx]
        y_boot = y_train.iloc[boot_idx]

        model = XGBRegressor(random_state=seed, **adjusted_params)

        model.fit(X_boot, y_boot)

        predictions = model.predict(X_global)

        global_predictions.append(predictions)


    global_predictions = np.array(global_predictions)


    mean_predictions = np.mean(global_predictions, axis=0)
    std_predictions = np.std(global_predictions, axis=0)
    cv_uncertainty = std_predictions / (mean_predictions + 1e-10)


    results = pd.DataFrame({
        'Longitude': global_data['lon'],
        'Latitude': global_data['lat'],
        'Mean_Prediction': mean_predictions,
        'Std_Prediction': std_predictions,
        'CV_Uncertainty': cv_uncertainty
    })


    output_file = os.path.join(output_folder, f'{target_variable}_uncertainty.csv')
    results.to_csv(output_file, index=False)
    print(f"\t不确定性分析完成，结果保存至 {output_file}")
