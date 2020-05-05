package com.example.foodstock.model;

public class Product {
    private int product_id;
    private String name;


    public Product(){

    }

    public Product(int id, String name) {
        this.product_id = id;
        this.name = name;
    }

    public int getId() {
        return product_id;
    }

    public void setId(int id) {
        this.product_id = id;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }
}
