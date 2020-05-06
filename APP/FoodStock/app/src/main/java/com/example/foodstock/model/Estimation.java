package com.example.foodstock.model;

public class Estimation {
    private int product_id;
    private int month_id;
    private int estimated_rate;

    public Estimation() {
    }

    public Estimation(int product_id, int month_id, int estimated_rate) {
        this.product_id = product_id;
        this.month_id = month_id;
        this.estimated_rate = estimated_rate;
    }

    public int getProduct_id() {
        return product_id;
    }

    public void setProduct_id(int product_id) {
        this.product_id = product_id;
    }

    public int getMonth_id() {
        return month_id;
    }

    public void setMonth_id(int month_id) {
        this.month_id = month_id;
    }

    public int getEstimated_rate() {
        return estimated_rate;
    }

    public void setEstimated_rate(int estimated_rate) {
        this.estimated_rate = estimated_rate;
    }
}
