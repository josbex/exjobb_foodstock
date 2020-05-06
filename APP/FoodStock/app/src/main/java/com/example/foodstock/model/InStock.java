package com.example.foodstock.model;

public class InStock {

    private int product_id;
    private int quantity;
    private String added_date;
    private String expire_date;

    public InStock() {
    }

    public InStock(int product_id, int quantity, String added_date, String expire_date) {
        this.product_id = product_id;
        this.quantity = quantity;
        this.added_date = added_date;
        this.expire_date = expire_date;
    }

    public int getProduct_id() {
        return product_id;
    }

    public void setProduct_id(int product_id) {
        this.product_id = product_id;
    }

    public int getQuantity() {
        return quantity;
    }

    public void setQuantity(int quantity) {
        this.quantity = quantity;
    }

    public String getAdded_date() {
        return added_date;
    }

    public void setAdded_date(String added_date) {
        this.added_date = added_date;
    }

    public String getExpire_date() {
        return expire_date;
    }

    public void setExpire_date(String expire_date) {
        this.expire_date = expire_date;
    }
}
