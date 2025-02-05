package org.anomalydetection;

import com.google.gson.Gson;

import java.io.*;
import java.util.ArrayList;
import java.util.List;

public class IsolationForest {
    private String pythonScriptPath;

    public IsolationForest(Model model) {
        this.pythonScriptPath = model.getFileName();
    }

    public List<List<Boolean>> predict(double[] featureVector) throws IOException {
        Gson gson = new Gson();
        String json = gson.toJson(featureVector);
        System.out.println("Feature vector: " + json);
        String[] command = {"/opt/venv/bin/python3", pythonScriptPath, json};

        List<List<Boolean>> resultList = new ArrayList<>();
        try{
            // Lancer le processus
            ProcessBuilder processBuilder = new ProcessBuilder(command);
            processBuilder.redirectErrorStream(true); // Rediriger stderr vers stdout
            Process process = processBuilder.start();

            // Lire les logs et extraire la dernière ligne JSON valide
            BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()));
            String line;
            String lastValidJson = null; // Stocke la dernière ligne JSON valide

            while ((line = reader.readLine()) != null) {
                System.out.println("Python Log: " + line); // Afficher les logs

                // Vérifier si la ligne est un JSON valide (contient '[' ou '{')
                if (line.trim().startsWith("[") ) {
                    lastValidJson = line; // Met à jour la dernière ligne valide
                }
            }
            reader.close();

            // Attendre la fin du processus
            int exitCode = process.waitFor();
            if (exitCode != 0) {
                System.err.println("Python script exited with code: " + exitCode);
            }

            // Convertir la dernière ligne JSON valide en liste Java
            if (lastValidJson != null) {
                System.out.println("Last valid JSON: " + lastValidJson);
                resultList = gson.fromJson(lastValidJson, List.class);
            }

        } catch (IOException e) {
            throw new RuntimeException(e);
        } catch (InterruptedException e) {
            throw new RuntimeException(e);
        }

        return resultList;

    }
}

