package org.anomalydetection;

import org.apache.storm.spout.SpoutOutputCollector;
import org.apache.storm.task.TopologyContext;
import org.apache.storm.topology.OutputFieldsDeclarer;
import org.apache.storm.topology.base.BaseRichSpout;
import org.apache.storm.tuple.Fields;
import org.apache.storm.tuple.Values;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.Map;

public class MetricPrometheusSpout extends BaseRichSpout {
    private SpoutOutputCollector collector;

    @Override
    public void open(Map conf, TopologyContext context, SpoutOutputCollector collector) {
        this.collector = collector;
    }

    private double fetchMetricFromApp() {
        try {
            URL url = new URL("http://prometheus:9090/api/v1/query?query=metric_value{instance='python-metrics-app:8000'}");
            HttpURLConnection conn = (HttpURLConnection) url.openConnection();
            conn.setRequestMethod("GET");

            BufferedReader reader = new BufferedReader(new InputStreamReader(conn.getInputStream()));
            StringBuilder response = new StringBuilder();
            String line;
            while ((line = reader.readLine()) != null) {
                response.append(line);
            }
            reader.close();

            // Parse the JSON response to extract the metric value
            String jsonResponse = response.toString();
            System.out.println("Response from Prometheus: " + jsonResponse);
            // Assuming the response is in the format: {"status":"success","data":{"resultType":"vector","result":[{"metric":{},"value":[timestamp, value]}]}}
            int valueIndex = jsonResponse.indexOf("[", jsonResponse.indexOf("value")) + 1;
            int valueEndIndex = jsonResponse.indexOf("]", valueIndex);
            String valueString = jsonResponse.substring(valueIndex, valueEndIndex).split(",")[1].trim();
            System.out.println("Extracted metric value: " + valueString);
            // enlever les "" autour de la valeur
            valueString = valueString.substring(1, valueString.length() - 1);
            return Double.parseDouble(valueString);
        } catch (Exception e) {
            e.printStackTrace();
            return 0;
        }
    }

    @Override
    public void nextTuple() {
        double metricValue = fetchMetricFromApp();
        System.out.println("Emitting metric value: " + metricValue);
        String timestamp = new SimpleDateFormat("yyyy/MM/dd HH:mm:ss").format(new Date());
        collector.emit(new Values(timestamp, metricValue));
        try {
            Thread.sleep(1000);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }

    @Override
    public void declareOutputFields(OutputFieldsDeclarer outputFieldsDeclarer) {
        outputFieldsDeclarer.declare(new Fields("timestamp", "metricValue"));
    }
}
