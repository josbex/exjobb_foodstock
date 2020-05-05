package com.example.foodstock.util;

public class Util {

    //Database constants
    public static final int DATABASE_VERSION = 1;
    public static final String DATABASE_NAME = "foodstock_db";
    public static final String PRODUCT_TABLE = "products";
    public static final String  PRODUCT_HISTORY_TABLE = "history";
    public static final String STOCK_TABLE = "stock";
    public static final String MONTHS_TABLE = "months";
    public static final String ESTIMATED_RATES_TABLE = "estimated_rates";

    //Table column names
    public static final String PRODUCT_ID = "product_id";
    public static final String PRODUCT_NAME = "name";
    public static final String HISTORY_ID = "history_id";
    public static final String ADDED_DATE = "added_date";
    public static final String REMOVED_DATE = "removed_date";
    public static final String EXPIRE_DATE = "expire_date";
    public static final String ACTUAL_RATE = "actual_rate";
    public static final String MONTH_ID = "month_id";
    public static final String MONTH_NAME = "month_name";
    public static final String QUANTITY = "qty";
    public static final String ESTIMATED_RATE = "estimated_rate";


    public static final String  CREATE_PRODUCT_TABLE = "CREATE TABLE " + PRODUCT_TABLE + "(" + PRODUCT_ID + " INTEGER PRIMARY KEY, " + PRODUCT_NAME + " TEXT NOT NULL)";
    public static final String  CREATE_PRODUCT_HISTORY_TABLE = "CREATE TABLE " + PRODUCT_HISTORY_TABLE + "(" + HISTORY_ID +" INTEGER PRIMARY KEY, " + PRODUCT_ID + " INTEGER, " + ADDED_DATE + " DATE NOT NULL, " + REMOVED_DATE + " DATE NOT NULL, " + ACTUAL_RATE + " INTEGER NOT NULL, FOREIGN KEY ("+ PRODUCT_ID +") REFERENCES " + PRODUCT_TABLE +" ("+ PRODUCT_ID +"))";
    public static final String  CREATE_STOCK_TABLE = "CREATE TABLE " + STOCK_TABLE + "(" + PRODUCT_ID + " INTEGER PRIMARY KEY, " + QUANTITY + " INTEGER NOT NULL, " + ADDED_DATE + " DATE NOT NULL, " + EXPIRE_DATE + " DATE, FOREIGN KEY (" + PRODUCT_ID + ") REFERENCES " + PRODUCT_TABLE + "("+ PRODUCT_ID + "))";
    public static final String  CREATE_MONTHS_TABLE = "CREATE TABLE " + MONTHS_TABLE + "(" + MONTH_ID + " INTEGER PRIMARY KEY, " + MONTH_NAME + " TEXT)";
    public static final String  CREATE_ESTIMATED_RATES_TABLE = "CREATE TABLE " + ESTIMATED_RATES_TABLE +  "(" + PRODUCT_ID + " INTEGER, " + MONTH_ID + " INTEGER, " + ESTIMATED_RATE + " INTEGER, FOREIGN KEY (" + PRODUCT_ID + ") REFERENCES " + PRODUCT_TABLE + "("+ PRODUCT_ID + "), FOREIGN KEY (" + MONTH_ID + ") REFERENCES " + MONTHS_TABLE + "("+ MONTH_ID + "), PRIMARY KEY(" +PRODUCT_ID +", " + MONTH_ID +"))";
    public static final String[] CREATE_TABLES = {CREATE_PRODUCT_TABLE, CREATE_PRODUCT_HISTORY_TABLE, CREATE_STOCK_TABLE, CREATE_MONTHS_TABLE, CREATE_ESTIMATED_RATES_TABLE};
    public static final String[] TABLE_NAMES = {ESTIMATED_RATES_TABLE, PRODUCT_HISTORY_TABLE, STOCK_TABLE, MONTHS_TABLE, PRODUCT_TABLE};

    public static final String[] MONTHS = {"January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"};
}




