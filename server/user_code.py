# Welcome to your Python Sandbox
import pandas as pd

# Create a DataFrame
data = {'Name': ['Alice', 'Bob', 'Charlie', 'David'],
        'Age': [25, 30, 35, 40],
        'City': ['New York', 'Los Angeles', 'Chicago', 'Houston']}
df = pd.DataFrame(data)

# Display the DataFrame
print("Original DataFrame:")
print(df)

# Perform some basic operations
print("\nBasic Operations:")
print("Number of rows:", len(df))
print("Average age:", df['Age'].mean())
print("Oldest person:", df['Name'][df['Age'].idxmax()])

# Add a new column
df['Gender'] = ['Female', 'Male', 'Male', 'Male']

# Display the modified DataFrame
print("\nModified DataFrame:")
print(df)
