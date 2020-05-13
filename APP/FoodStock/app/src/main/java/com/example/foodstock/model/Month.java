package com.example.foodstock.model;

public class Month {

    private int month_id;
    private String name;

    public Month() {
    }

    public Month(int month_id, String name) {
        this.month_id = month_id;
        this.name = name;
    }

    public int getId() {
        return month_id;
    }

    public void setId(int month_id) {
        this.month_id = month_id;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }
}
