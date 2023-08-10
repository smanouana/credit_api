from flask import Flask, jsonify, request, send_file 
import pandas as pd
import lightgbm as lgb
#import plotly.express as px
import shap
#from sklearn.model_selection import train_test_split
#from flask import Flask, send_file
import pickle

app = Flask(__name__) 

# Load the dataset notencoded
dataset = pd.read_csv('notencoded.csv')

# Load the dataset encoded
dataset2 = pd.read_csv('encoded.csv')




# pour supprimer tout ce quoi est Jason caractères
import re
dataset2 = dataset2.rename(columns = lambda x:re.sub('[^A-Za-z0-9_]+', '', x))


@app.route('/') 
def racine():
    return "hello simon" 

def client_name(client_id):
     if client_id ==10: 
        return "Simon"
     else:
        return "Isaac"
     


def EXT_SOURCE_3(client_id):
    valeur_dfn = dataset[dataset["SK_ID_CURR"]==(client_id)]
    valeur = valeur_dfn["EXT_SOURCE_3"].values[0]
    return valeur
    
def EXT_SOURCE_2(client_id):
    valeur_dfn = dataset[dataset["SK_ID_CURR"]==(client_id)]
    valeur = valeur_dfn["EXT_SOURCE_2"].values[0]
    return valeur

def AMT_GOODS_PRICE(client_id):
    valeur_dfn = dataset[dataset["SK_ID_CURR"]==(client_id)]
    valeur = valeur_dfn["AMT_GOODS_PRICE"].values[0]
    return valeur

def EXT_SOURCE_1(client_id):
    valeur_dfn = dataset[dataset["SK_ID_CURR"]==(client_id)]
    valeur = valeur_dfn["EXT_SOURCE_1"].values[0]
    return valeur

def AMT_CREDIT(client_id):
    valeur_dfn = dataset[dataset["SK_ID_CURR"]==(client_id)]
    valeur = valeur_dfn["AMT_CREDIT"].values[0]
    return valeur

def CODE_GENDER(client_id):
    valeur_dfn = dataset[dataset["SK_ID_CURR"]==(client_id)]
    valeur = valeur_dfn["CODE_GENDER"].values[0]
    return valeur

def AGE_RANGE_D(client_id):
    valeur_dfn = dataset[dataset["SK_ID_CURR"]==(client_id)]
    valeur = valeur_dfn["AGE_RANGE_D"].values[0]
    return valeur     



@app.route('/infos_client', methods=['POST']) 
def post_data():
    data = request.get_json() 
    client_id = data['client_id'] 
    if client_id in dataset["SK_ID_CURR"].values:
        valeur2 = EXT_SOURCE_3(client_id)
        valeur3 = EXT_SOURCE_2(client_id)
        valeur4 = AMT_GOODS_PRICE(client_id)
        valeur5 = EXT_SOURCE_1(client_id)
        valeur6 = AMT_CREDIT(client_id)
        valeur7 = CODE_GENDER(client_id)
        valeur8 = AGE_RANGE_D(client_id)   
        response = {'EXT_SOURCE_3': valeur2,
                'EXT_SOURCE_2': valeur3,
                'AMT_GOODS_PRICE': valeur4,
                'EXT_SOURCE_1': valeur5,
                'AMT_CREDIT': valeur6,
                'CODE_GENDER': valeur7,
                'AGE_RANGE_D': valeur8,} 
        return jsonify(response) 
    else :
        response ={'ID client ': 'inconnu'}
        return jsonify(response) 
    






@app.route('/score_credit', methods=['POST']) 
def post_data2():
    data = request.get_json() 
    client_id = data['client_id'] 
        
    X2 = dataset2.drop(columns=['TARGET','FLAG_OWN_CAR_Y'])
    # Extraire les données du client spécifié
    client_data = X2[X2["SK_ID_CURR"] == client_id]
    # Effectuer la prédiction pour le client donné
    # Charger le modèle à partir du fichier 
    with open('modele_sauvegarde.pkl','rb') as fichier:
        model_charge = pickle.load(fichier)
    prediction = model_charge.predict_proba(client_data)
    # Supposons que le modèle retourne 0 pour non-défaut et 1 pour défaut
    # Calculer le score
    #score = prediction[0]  # Obtenir la prédiction pour le premier client (index 0)
    score = prediction[0][0]
    
    
    
    # Afficher le score du client
    #print("Le score du client avec l'ID", client_id, "est :", score)

    response = {'SCORE ID CLIENT' : score}
    return jsonify(response)





@app.route('/analyze_variable', methods=['POST'])
def analyze_variable():
	# get variables client_id, variable
    data = request.get_json() 
    client_id = data['client_id']
    variable = data['variable']

       

    variable_client_id = dataset[dataset['SK_ID_CURR'] == client_id][variable].values[0]
    variable_data = list(dataset[variable])
    return jsonify({"variable_client_id":variable_client_id,"variable_data":variable_data,})



    
    
@app.route('/shap_plot2', methods=['POST'] )
def serve_shap_plot2():
    data = request.get_json() 
    client_id = data['client_id']
    # Pour le chargement dans Flask
    #import pickle

    # Load the explainer
    with open('explainer.pkl', 'rb') as f:
        explainer = pickle.load(f)

    # Load the SHAP values
    with open('shap_values.pkl', 'rb') as f:
        shap_values = pickle.load(f)

    # Pour charger le dataset dans flask
    with open('data_final.pkl','rb') as fichier:
        data_final = pickle.load(fichier)

    # Déterminons elt_index
    # dans le code flask
    elt_index = data_final.index[data_final['SK_ID_CURR']==client_id]
    X = data_final.drop(['SK_ID_CURR'], axis=1)
    shap.initjs()
    image2 = shap.force_plot(explainer.expected_value[1], shap_values[1][elt_index], X.iloc[elt_index, :])
    shap.save_html("image2.html", image2)


    
    
    with open('image2.html', 'r', encoding='utf-8') as file:
        html_content = file.read()
    

    return jsonify({"key":html_content})
    

if __name__ == '__main__': 
    app.run("127.0.0.1","9000",debug=True)








