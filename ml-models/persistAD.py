# isolation_forest.py
import joblib
import sys
import json
import pandas as pd
from adtk.data import validate_series
from adtk.detector import PersistAD


try:
    # Charger le modèle Isolation Forest
    # model =  PersistAD(c=0.5, side="both",window = 10)

    model =  PersistAD(window=10)
    
    # Lire les données envoyées par les arguments du script
    feature_vector = json.loads(sys.argv[1])
    
    print("feature vector: ", feature_vector)
    df = pd.DataFrame(feature_vector, columns=['metric_value'])
    # Ajouter un DatetimeIndex au DataFrame
    df['timestamp'] = pd.date_range(start='1/1/2022', periods=len(df), freq='T')
    df.set_index('timestamp', inplace=True)
    # Faire la prédiction
    df = validate_series(df)
    prediction = model.fit_detect(df)
    print("prediction: ", prediction)
    # Convertir les prédictions en liste
    prediction_list = prediction.values.tolist()
    print(prediction_list)
    
    # Forcer le premier élément à False si c'est NaN
    prediction_list = [[False] if pd.isna(x) else x for x in prediction_list]
    print(prediction_list)

    
    print(json.dumps(prediction_list))

except Exception as e:
    # En cas d'erreur, imprimer l'exception
    print(json.dumps({"error persistAD": str(e)}), file=sys.stderr)
