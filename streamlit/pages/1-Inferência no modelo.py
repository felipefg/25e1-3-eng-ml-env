import streamlit as st
import requests


def call_inference(data):

    rows = [
        list(data.values())
    ]

    resp = requests.post(
        'http://localhost:5001/invocations',
        json={
            'inputs': rows,
        }
    )

    inference = resp.json()
    return inference['predictions'][0]


st.markdown("""
# Titanic

Essa página realiza inferência sobre um modelo treinado com os dados do
Titanic.
""")

name = st.session_state.get('name')
if name:
    st.text(f'Olá {name}')

col1, col2 = st.columns(2)

pclass = col1.number_input("Classe do Passageiro", min_value=1, max_value=3)
age = col1.number_input("Idade")
sibsp = col1.number_input('Irmãos ou Cônjuges')
parch = col1.number_input('Pais ou Filhos')

fare = col2.number_input('Preço do Ticket')
sex = col2.radio("Sexo", ['Masculino', 'Feminino'])
embarked = col2.radio("Porto de Embarque", ['Cherbourg', 'Queenstown',
                                            'Southampton'])

input_data = {
    'pclass': pclass,
    'age': age,
    'sibsp': sibsp,
    'parch': parch,
    'fare': fare,
    'Sex_female': sex == 'Feminino',
    'Sex_male': sex == 'Masculino',
    'embarked_c': embarked == 'Cherbourg',
    'embarked_q': embarked == 'Queenstown',
    'embarked_s': embarked == 'Southampton',
}

st.json(list(input_data.values()))

# Assumindo que survived é um booleano, pois o modelo do mlflow está usando a
# função predict.
survived = call_inference(input_data)

st.write(f"Sobreviveu? {'Sim!' if survived else 'Não :-('}")
