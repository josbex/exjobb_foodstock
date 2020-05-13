package com.example.foodstock.model;

public class History {

    private int history_id;
    private int product_id;
    private String added_date;
    private String removed_date;
    private int actual_rate;

    public History() {
    }

    public History(int history_id, int product_id, String added_date, String removed_date, int actual_rate) {
        this.history_id = history_id;
        this.product_id = product_id;
        this.added_date = added_date;
        this.removed_date = removed_date;
        this.actual_rate = actual_rate;
    }

    public int getHistory_id() {
        return history_id;
    }

    public void setHistory_id(int history_id) {
        this.history_id = history_id;
    }

    public int getProduct_id() {
        return product_id;
    }

    public void setProduct_id(int product_id) {
        this.product_id = product_id;
    }

    public String getAdded_date() {
        return added_date;
    }

    public void setAdded_date(String added_date) {
        this.added_date = added_date;
    }

    public String getRemoved_date() {
        return removed_date;
    }

    public void setRemoved_date(String removed_date) {
        this.removed_date = removed_date;
    }

    public int getActual_rate() {
        return actual_rate;
    }

    public void setActual_rate(int actual_rate) {
        this.actual_rate = actual_rate;
    }
}
