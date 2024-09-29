
import pandas as pd  # Import pandas library and assign it to alias 'pd'
import matplotlib.pyplot as plt  # Import matplotlib library and assign it to alias 'plt'

# Define the input dataframe
data = {
    "ID": [1, 2, 3, 4, 5, 6, 7, 8, 9],
    "Name": ["Employee_1", "Employee_2", "Employee_3", 
                 "Employee_4", "Employee_5", "Employee_6",
                 "Employee_7", "Employee_8", "Employee_9"],
    "Age": [23, 30, 32, 41, 63, 54, 30, 63, 54],
    "Salary": [92678, 103662, 72538, 38062, 98077, 95082,
                    68944, 50245, 80532],
    "Department": ["HR", "HR", "HR", "Marketing", "Finance", 
                          "Marketing", "IT", "HR", "HR"],
    "Start Date": ["2020-01-31", "2020-02-29", "2020-03-31",
                           "2020-04-30", "2020-05-31", "2020-06-30", 
                           "2020-07-31", "2020-08-31", "2020-09-30"]
}

# Create a DataFrame from the dictionary
df = pd.DataFrame(data)

# Define the function to create the specific graph
def generate_pie_chart(df):
    # Group the data by 'Department' column
    department_counts = df['Department'].value_counts()

    # Create a pie chart using matplotlib
    plt.figure(figsize=(8, 6))
    plt.pie(department_counts, labels=department_counts.index,
                autopct='%1.1f%%')
    plt.title('Employee Department Distribution')

# Call the function to generate the pie chart and display it
generate_pie_chart(df)

# Save the plot as 'plot.png'
plt.savefig('plot.png')
## 