package org.anomalydetection;

import org.apache.storm.Config;
import org.apache.storm.task.OutputCollector;
import org.apache.storm.task.TopologyContext;
import org.apache.storm.topology.OutputFieldsDeclarer;
import org.apache.storm.topology.base.BaseWindowedBolt;
import org.apache.storm.tuple.Fields;
import org.apache.storm.tuple.Tuple;
import org.apache.storm.tuple.Values;
import org.apache.storm.windowing.TupleWindow;

import java.io.IOException;
import java.util.List;
import java.util.Map;

public class SpikeDetectionBolt extends BaseWindowedBolt {
    private IsolationForest model;
    private OutputCollector collector;

    @Override
    public void prepare(Map<String, Object> topoConf, TopologyContext context, OutputCollector collector) {
        model = new IsolationForest(Model.SPIKE);
        this.collector = collector;
    }

    @Override
    public void execute(TupleWindow inputWindow) {
        double[] values = new double[inputWindow.get().size()];
        double[] timestamps = new double[inputWindow.get().size()];
        int index = 0;
        for (Tuple input : inputWindow.get()) {
            double metricValue = input.getDoubleByField("metricValue");
            double timestamp = input.getDoubleByField("timestamp");
            timestamps[index] = timestamp;
            values[index++] = metricValue;
        }
        try {
            List<List<Boolean>> anomalies = model.predict(values);
            for (int i = 0; i < anomalies.size(); i++) {             // Emit an alert if an anomaly is detected
               if (anomalies.get(i).get(0).equals(true)) {
                   double metricValue = values[i];
                   double timestamp = timestamps[i];
                   emitAlert(metricValue, timestamp);
               }
            }
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }

    private void emitAlert(double metricValue, double timestamp) {
        this.collector.emit(new Values("spike", metricValue, timestamp));
    }

    @Override
    public void declareOutputFields(OutputFieldsDeclarer outputFieldsDeclarer) {
        outputFieldsDeclarer.declare(new Fields("type", "metricValue", "timestamp"));
    }

    @Override
    public Map<String, Object> getComponentConfiguration() {
        Map<String, Object> conf = super.getComponentConfiguration();
        conf.put(Config.TOPOLOGY_BOLTS_WINDOW_LENGTH_DURATION_MS, 60000); // Fenêtre de 60 secondes
        conf.put(Config.TOPOLOGY_BOLTS_SLIDING_INTERVAL_DURATION_MS, 1000); // Intervalle de glissement de 10 secondes
        return conf;
    }

}
