import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder

data = pd.read_csv('Titanic_train.csv')

data = data[['Pclass', 'Sex', 'Age', 'Fare', 'Survived']].dropna()

le = LabelEncoder()
data['Sex'] = le.fit_transform(data['Sex'])  

X = data[['Pclass', 'Sex', 'Age', 'Fare']]
y = data['Survived']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


model = LogisticRegression()
model.fit(X_train, y_train)


st.title("Titanic Passenger Survival Prediction")

name = st.text_input("Passenger Name")
pclass = st.selectbox("Passenger Class", [1, 2, 3])
sex = st.selectbox("Sex", ['male', 'female'])
age = st.number_input("Age", min_value=0, max_value=100)
fare = st.number_input("Fare", min_value=0.0)


if st.button("Submit"):
    sex_encoded = 1 if sex == 'male' else 0  

   
    new_data = pd.DataFrame({
        'Pclass': [pclass],
        'Sex': [sex_encoded],
        'Age': [age],
        'Fare': [fare]
    })


    survival_prediction = model.predict(new_data)[0]
    survival_prob = model.predict_proba(new_data)[0][1] 

   
    st.write("New Passenger Data:")
    st.dataframe(new_data)

    if survival_prediction == 1:
        st.success(f"This passenger is likely to survive with a probability of {survival_prob * 100:.2f}%")
    else:
        st.error(f"This passenger is unlikely to survive with a probability of {survival_prob * 100:.2f}%")


