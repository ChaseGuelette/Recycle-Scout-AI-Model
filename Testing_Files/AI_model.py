# AI for change hackathon AI 
# uses pandas and sklearn to take in a set of countries that have predictive attributes for construction cost
# uses a linear regression to predict the construction cost index for the countries that do not data available
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import numpy as np

# Read in the data from csv into pandas dataframe and split in into a df 
# with the known construction cost and one with the countries that need to be estimated
data = pd.read_csv('Data.csv')
empty_data = data[data['construction_cost'].isna()]

# Drops all rows that have missing values (all rows without construction costs)
data = data.dropna()

# create a df that is just the inputs of the known construction index entries
# and an empty df that is the inputs for the unknown construction index entries
# (need to remove NaN's because there could be extra rows and function was only called on the inputs df)
training_inputs = data.drop('construction_cost', axis=1)
empty_inputs = empty_data.drop('construction_cost', axis=1)
empty_inputs = empty_inputs.dropna()

# Remove the contries from training and to be estimated df to be added in after training
empty_inputs_countries = empty_inputs['countries']
empty_inputs_countries_df = pd.DataFrame(empty_inputs_countries, columns=['countries'])
empty_inputs = empty_inputs.drop(columns=['countries'])

inputs_countries = training_inputs['countries']
inputs_countries_df = pd.DataFrame(inputs_countries, columns=['countries'])
training_inputs = training_inputs.drop(columns=['countries'])

# Series of known construction costs
known_cost = data['construction_cost']

# Normalize the data to a mean of 0 and std of 1 (z values)
scaler = StandardScaler()
scaled_training_inputs = scaler.fit_transform(training_inputs)

scaler = StandardScaler()
scaled_empty_inputs = scaler.fit_transform(empty_inputs)

# Testing code
# Splits the data into 80% data that will be used to train the AI and the other 20% as data that will test
# The AI's accuracy predicting random state is choosing a config so random will be consistanct each run 
#target_train, target_test, input_train, input_test = train_test_split(target, scaled_inputs, test_size=0.2, random_state=42)

# Convert the data back to a dataframe so we can do the regression. Takes the column headers from original inputs df
scaled_training_inputs_df = pd.DataFrame(scaled_training_inputs, columns=training_inputs.columns)
scaled_empty_inputs_df = pd.DataFrame(scaled_empty_inputs, columns=empty_inputs.columns)

# Create a predictive modle for construction cost from input data
model = LinearRegression()
model.fit(scaled_training_inputs_df, known_cost)

# Use the model to predict the cost of the unknowns then convert both Series of costs to df
predictive_cost = model.predict(scaled_empty_inputs_df)
predictive_cost_df = pd.DataFrame(predictive_cost, columns=['construction_cost'])
known_cost_df = pd.DataFrame(known_cost, columns=['construction_cost'])

# Combining the countries, inputs, and costs df's for the prediction set and training set
prediction_df = pd.concat([empty_inputs_countries_df.reset_index(drop=True), empty_inputs.reset_index(drop=True), predictive_cost_df.reset_index(drop=True)], axis=1)
original_df = pd.concat([inputs_countries_df.reset_index(drop=True), training_inputs.reset_index(drop=True), known_cost_df.reset_index(drop=True)], axis=1)


# combine both of the full df and write to output file
combined_df = pd.concat([original_df, prediction_df], axis=0)
combined_df.to_csv('C:\\dev/hackathon project/output.csv', index=False)


'''mse = mean_squared_error(target_test, target_pred)
r2 = r2_score(target_test, target_pred)

print(f'Mean Squared Error: {mse}')
print(f'R-squared: {r2}')'''

'''
# Calculate residuals
residuals = target_test - target_pred
print("target values")
#print(emptyInputs)
print(target_pred)

# Plotting residuals
plt.figure(figsize=(8, 6))
plt.scatter(target_pred, residuals, color='blue')
plt.axhline(y=0, color='r', linestyle='--')  # Adding a horizontal line at y=0 for reference
plt.title('Residual Plot')
plt.xlabel('Predicted Values')
plt.ylabel('Residuals')
plt.grid(True)
plt.show()'''