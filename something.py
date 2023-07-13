import pandas as pd
# Load the dataset into a DataFrame
df2 = pd.read_excel("Recommendation.xlsx")

# Remove leading and trailing spaces from the column names
df2.columns = df2.columns.str.strip()


# Initialize an empty list to store the selected items
selected_items = []

for _ in range(3):
    # Sort the DataFrame by 'Days_on_Stock' column in descending order
    sorted_df2 = df2.sort_values(by='Days_on_Stock', ascending=False)
    
    # Iterate through the sorted DataFrame and select a unique item
    for _, row in sorted_df2.iterrows():
        # Check if the current item is already selected
        if row['Product'] not in selected_items:
            # Add the current item to the selected items list
            selected_items.append(row['Product'])
            
            # Remove the selected item from the DataFrame
            df2 = df2[df2['Product'] != row['Product']]
            
            break

# Print the selected items
print(selected_items)