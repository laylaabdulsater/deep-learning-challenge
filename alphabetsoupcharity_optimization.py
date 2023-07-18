# -*- coding: utf-8 -*-
"""AlphabetSoupCharity_Optimization.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/19hqzougyvxFgDv6OM0xyttLfnx-QEY2a

## Preprocessing
"""

# Import our dependencies
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import pandas as pd
import tensorflow as tf

#  Import and read the charity_data.csv.
import pandas as pd
application_df = pd.read_csv("https://static.bc-edx.com/data/dl-1-2/m21/lms/starter/charity_data.csv")
application_df.head()

# Drop the non-beneficial ID columns, 'EIN' and 'NAME'.
application_df = application_df.drop(['EIN', 'NAME'], axis=1)

# Determine the number of unique values in each column.
application_df.nunique()

# Look at APPLICATION_TYPE value counts for binning
application_df.groupby('APPLICATION_TYPE')['ASK_AMT'].nunique().sort_values(ascending=False)

# Choose a cutoff value and create a list of application types to be replaced
# use the variable name `application_types_to_replace`
application_types_to_replace = ['T9', 'T7', 'T8', 'T19', 'T10', 'T12', 'T13', 'T2', 'T14', 'T25', 'T29', 'T15', 'T17']

# Replace in dataframe
for app in application_types_to_replace:
    application_df['APPLICATION_TYPE'] = application_df['APPLICATION_TYPE'].replace(app,"Other")

# Check to make sure binning was successful
application_df['APPLICATION_TYPE'].value_counts()

# Look at CLASSIFICATION value counts for binning
application_df.groupby('CLASSIFICATION')['ASK_AMT'].nunique().sort_values(ascending=False)

# You may find it helpful to look at CLASSIFICATION value counts >1
application_df.groupby('CLASSIFICATION')['ASK_AMT'].nunique().sort_values(ascending=False).head(35)

class_data = application_df.groupby('CLASSIFICATION')['ASK_AMT'].nunique().sort_values(ascending=False)
class_df = pd.DataFrame(class_data)
# class_df['ASK_AMT'] = class_df['ASK_AMT'].astype(int)
class_df=class_df.reset_index()
class_df

# Choose a cutoff value and create a list of classifications to be replaced
# use the variable name `classifications_to_replace`
classifications_to_replace = []
for row in class_df.index:
    if class_df['ASK_AMT'][row] < 263:
      classifications_to_replace.append(class_df['CLASSIFICATION'][row])
    else:
      continue


# Replace in dataframe
for cls in classifications_to_replace:
    application_df['CLASSIFICATION'] = application_df['CLASSIFICATION'].replace(cls,"Other")

# Check to make sure binning was successful
application_df['CLASSIFICATION'].value_counts()

# Convert categorical data to numeric with `pd.get_dummies`
application_df_dummies = pd.get_dummies(application_df)

# Split our preprocessed data into our features and target arrays
y = application_df_dummies['IS_SUCCESSFUL']
x = application_df_dummies.drop(columns=['IS_SUCCESSFUL'])

# Split the preprocessed data into a training and testing dataset
X_train, X_test, y_train, y_test = train_test_split(x, y, random_state=1, stratify=y)

# Create a StandardScaler instances
scaler = StandardScaler()

# Fit the StandardScaler
X_scaler = scaler.fit(X_train)

# Scale the data
X_train_scaled = X_scaler.transform(X_train)
X_test_scaled = X_scaler.transform(X_test)

"""## Compile, Train and Evaluate the Model"""

# Define the model - deep neural net, i.e., the number of input features and hidden nodes for each layer.
nn = tf.keras.models.Sequential()

# First hidden layer
nn.add(tf.keras.layers.Dense(units=80, activation="relu", input_dim=40))

# Second hidden layer
nn.add(tf.keras.layers.Dense(units=30, activation="relu"))

# Output layer
nn.add(tf.keras.layers.Dense(units=1, activation="sigmoid"))

# Check the structure of the model
nn.summary()

# Compile the model
nn.compile(loss="binary_crossentropy", optimizer="adam", metrics=["accuracy"])

# Train the model
fit_model = nn.fit(X_train_scaled, y_train, epochs=100)

# Evaluate the model using the test data
model_loss, model_accuracy = nn.evaluate(X_test_scaled,y_test,verbose=2)
print(f"Loss: {model_loss}, Accuracy: {model_accuracy}")

# Export our model to HDF5 file
nn.save("AlphabetSoupCharity_Optimization.h5")