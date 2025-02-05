# isolation_forest.py
import joblib
import sys
import json
import pandas as pd
from adtk.data import validate_series
from adtk.detector import PersistAD


try:
    # Charger le modèle Isolation Forest
    model =  PersistAD(c=1.7, side="both",window = 1)
    
    # Lire les données envoyées par les arguments du script
    feature_vector = json.loads(sys.argv[1])
    
    df = pd.DataFrame(feature_vector, columns=['metric_value'])
    # Ajouter un DatetimeIndex au DataFrame
    df['timestamp'] = pd.date_range(start='1/1/2022', periods=len(df), freq='T')
    df.set_index('timestamp', inplace=True)
    # Faire la prédiction
    prediction = model.fit_predict(df)
    
    # Convertir les prédictions en liste
    prediction_list = prediction.values.tolist()
    
    # Forcer le premier élément à False si c'est NaN
    if pd.isna(prediction_list[0]):
        prediction_list[0] = [False]
    
    print(json.dumps(prediction_list))

except Exception as e:
    # En cas d'erreur, imprimer l'exception
    print(json.dumps({"error": str(e)}), file=sys.stderr)
