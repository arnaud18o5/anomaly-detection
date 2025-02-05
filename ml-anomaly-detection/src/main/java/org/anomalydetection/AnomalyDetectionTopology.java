package org.anomalydetection;

import org.apache.storm.Config;
//import org.apache.storm.LocalCluster;
import org.apache.storm.StormSubmitter;
import org.apache.storm.topology.TopologyBuilder;
import org.apache.storm.topology.base.BaseWindowedBolt.Duration;

public class AnomalyDetectionTopology {
    public static void main(String[] args) throws Exception {
        // Create a TopologyBuilder
        TopologyBuilder builder = new TopologyBuilder();

        // Set the spout and bolt
//        builder.setSpout("metric-spout", new MetricSpout());
        builder.setSpout("metric-spout", new MetricPrometheusSpout());
        builder.setBolt("spike-detection-bolt", new SpikeDetectionBolt()
                        .withWindow(Duration.seconds(29), Duration.seconds(1)))
                .shuffleGrouping("metric-spout");
        builder.setBolt("levelshift-detection-bolt", new LevelShiftDetectionBolt()
                        .withWindow(Duration.seconds(20), Duration.seconds(1)))
                .shuffleGrouping("metric-spout");
        builder.setBolt("dbscan-detection-bolt", new DBSCANBolt()
                        .withWindow(Duration.seconds(20), Duration.seconds(1)))
                .shuffleGrouping("metric-spout");
        builder.setBolt("prometheus-alert-bolt", new PrometheusAlertBolt("http://anomaly-exporter:12345/update-metric"))
                .shuffleGrouping("levelshift-detection-bolt")
                .shuffleGrouping("spike-detection-bolt")
                .shuffleGrouping("dbscan-detection-bolt");
        // Create a configuration
        Config conf = new Config();
        conf.setDebug(true);

        // Create a local cluster
//        LocalCluster cluster = new LocalCluster();

        conf.setNumWorkers(1);
        // Submit the topology
        // cluster.submitTopology("anomaly-detection-topology", conf, builder.createTopology());

        // Submit the topology to the cluster
        StormSubmitter.submitTopology("anomaly-detection-topology", conf, builder.createTopology());

        // Keep the cluster running for a specified time (e.g., 60 seconds)
//        while (true) {
//            Thread.sleep(60000); // Petite pause pour éviter d'utiliser trop de CPU
//        }

        // Shutdown the cluster
//        cluster.shutdown();
//        Thread.sleep(2000);
    }
}