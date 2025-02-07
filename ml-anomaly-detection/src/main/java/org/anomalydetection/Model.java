package org.anomalydetection;

public enum Model {
    SPIKE,
    LEVEL_SHIFT,
    DBSCAN;

    public String getFileName() {
        switch (this) {
            case SPIKE:
                return "/storm/ml-models/persistAD.py";
            case LEVEL_SHIFT:
                return "/storm/ml-models/level-shift.py";
            case DBSCAN:
                return "/storm/ml-models/dbscan.py";

            default:
                return null;
        }
    }
}
