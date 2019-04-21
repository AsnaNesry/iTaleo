import pandas as pd             #to read csv file
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn import metrics     #data frame
from sklearn.externals.six import StringIO
from IPython.display import Image
from sklearn.tree import export_graphviz
import pydotplus       #plotting
import pickle          #to save and read data model to or from file(trained model in file)

col_names = ['salaries', 'experience', 'primary_skill_score', 'secondary_skill_score', 'education', 'selected']
# load dataset
job_code = 'JC01'

data_set = pd.read_csv(job_code+"_dataset.csv", header=None, names=col_names, skiprows=1)
data_set.head()  #arranging

# split dataset in features and target variable
feature_cols = ['salaries', 'experience', 'primary_skill_score', 'secondary_skill_score', 'education']
X = data_set[feature_cols]  # Features
y = data_set.selected  # Target variable

# Split dataset into training set and test set
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=1)  # 70% training and 30% test



# Create Decision Tree classifier object
model = DecisionTreeClassifier() # blank model creation

# Train Decision Tree Classifier
model = model.fit(X_train, y_train)


# Predict the response for test dataset
y_pred = model.predict(X_test)  #result of test data of the trained model
proba = model.predict_proba(X_test, check_input=True)
print("Probability = ", proba)
# Model Accuracy, how often is the classifier correct?
print("Accuracy:", metrics.accuracy_score(y_test, y_pred))

filename = job_code+'.sav'
pickle.dump(model, open(filename, 'wb'))


# Below code creates a png image of our decision tree model #standard code
dot_data = StringIO()
export_graphviz(model, out_file=dot_data,
                filled=True, rounded=True,
                special_characters=True, feature_names=feature_cols, class_names=['0', '1'])
graph = pydotplus.graph_from_dot_data(dot_data.getvalue())
graph.write_png(job_code+'.png')
Image(graph.create_png())
print("Decision Tree Built. Quit Running")
