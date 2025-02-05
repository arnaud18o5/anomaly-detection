package org.anomalydetection;

import org.apache.storm.task.OutputCollector;
import org.apache.storm.task.TopologyContext;
import org.apache.storm.topology.OutputFieldsDeclarer;
import org.apache.storm.topology.base.BaseRichBolt;
import org.apache.storm.tuple.Tuple;

import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.Map;

public class PrometheusAlertBolt extends BaseRichBolt {
    private OutputCollector collector;
    private String postUrl;

    public PrometheusAlertBolt(String postUrl) {
        this.postUrl = postUrl;
    }

    @Override
    public void prepare(Map<String, Object> conf, TopologyContext context, OutputCollector collector) {
        this.collector = collector;
    }

    @Override
    public void execute(Tuple input) {
        try {
            URL url = new URL(postUrl);
            HttpURLConnection conn = (HttpURLConnection) url.openConnection();
            conn.setRequestMethod("POST");
            conn.setRequestProperty("Content-Type", "application/json");
            conn.setDoOutput(true);
            System.out.println("Sending alert to Prometheus: " + input);
            String jsonPayload = "{\"metric_value\": " + input.getDoubleByField("metricValue") + ", \"type\":\"" + input.getStringByField("type")+"\"}";
            System.out.println("Sending alert to Prometheus: " + jsonPayload);
            try (OutputStream os = conn.getOutputStream()) {
                byte[] inputBytes = jsonPayload.getBytes("utf-8");
                os.write(inputBytes, 0, inputBytes.length);
            }

            int responseCode = conn.getResponseCode();
            if (responseCode == 200) {
                collector.ack(input);
            } else {
                collector.fail(input);
            }
        } catch (Exception e) {
            collector.fail(input);
        }
    }

    @Override
    public void declareOutputFields(OutputFieldsDeclarer declarer) {
        // No output fields
    }
}