package com.example.foodstock.util;

import android.os.Build;

import androidx.annotation.RequiresApi;

import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.time.LocalDate;
import java.util.Calendar;
import java.util.Date;

import static android.os.Build.VERSION_CODES.O;

public class Util {

    //Database constants
    public static final int DATABASE_VERSION = 2;
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
    public static final String  CREATE_PRODUCT_HISTORY_TABLE = "CREATE TABLE " + PRODUCT_HISTORY_TABLE + "(" + HISTORY_ID +" INTEGER PRIMARY KEY, " + PRODUCT_ID + " INTEGER, " + ADDED_DATE + " TEXT NOT NULL, " + REMOVED_DATE + " TEXT NOT NULL, " + ACTUAL_RATE + " INTEGER NOT NULL, FOREIGN KEY ("+ PRODUCT_ID +") REFERENCES " + PRODUCT_TABLE +" ("+ PRODUCT_ID +"))";
    public static final String  CREATE_STOCK_TABLE = "CREATE TABLE " + STOCK_TABLE + "(" + PRODUCT_ID + " INTEGER PRIMARY KEY, " + QUANTITY + " INTEGER NOT NULL, " + ADDED_DATE + " TEXT NOT NULL, " + EXPIRE_DATE + " TEXT, FOREIGN KEY (" + PRODUCT_ID + ") REFERENCES " + PRODUCT_TABLE + "("+ PRODUCT_ID + "))";
    public static final String  CREATE_MONTHS_TABLE = "CREATE TABLE " + MONTHS_TABLE + "(" + MONTH_ID + " INTEGER PRIMARY KEY, " + MONTH_NAME + " TEXT)";
    public static final String  CREATE_ESTIMATED_RATES_TABLE = "CREATE TABLE " + ESTIMATED_RATES_TABLE +  "(" + PRODUCT_ID + " INTEGER, " + MONTH_ID + " INTEGER, " + ESTIMATED_RATE + " INTEGER, FOREIGN KEY (" + PRODUCT_ID + ") REFERENCES " + PRODUCT_TABLE + "("+ PRODUCT_ID + "), FOREIGN KEY (" + MONTH_ID + ") REFERENCES " + MONTHS_TABLE + "("+ MONTH_ID + "), PRIMARY KEY(" +PRODUCT_ID +", " + MONTH_ID +"))";
    public static final String[] CREATE_TABLES = {CREATE_PRODUCT_TABLE, CREATE_PRODUCT_HISTORY_TABLE, CREATE_STOCK_TABLE, CREATE_MONTHS_TABLE, CREATE_ESTIMATED_RATES_TABLE};
    public static final String[] TABLE_NAMES = {ESTIMATED_RATES_TABLE, PRODUCT_HISTORY_TABLE, STOCK_TABLE, MONTHS_TABLE, PRODUCT_TABLE};

    public static final String[] MONTHS = {"January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"};

    /**
     * Turns string to date object.
     * @param dateString : the date as a string with the format "yyyy-mm-dd"
     * @return date object of string
     */
    public Date stringToDate(String dateString){
        SimpleDateFormat format = new SimpleDateFormat("yyyy-mm-dd");
        Date date = null;
        try {
            date = format.parse(dateString);
        } catch (ParseException e) {
            e.printStackTrace();
        }
        return date;
    }

    /**
     * This method compares to dates and returns the date that the
     * took the majority of time. Like added 29/4 and 15/5, here the second
     * date will be returned since most of the occurred in that month.
     * @param added : the date an item was added to stock
     * @param removed : the date an item was removed from stock
     * @return : maximum date
     */
    public Date compareDates(Date added, Date removed){
        Calendar c = Calendar.getInstance();
        c.setTime(added);
        int lastDay = c.getActualMaximum(Calendar.DAY_OF_MONTH);
        int dayAdded= c.get(Calendar.DAY_OF_MONTH);
        c.setTime(removed);
        int dayRemoved= c.get(Calendar.DAY_OF_MONTH);
        if((lastDay - dayAdded) > dayRemoved){
            return added;
        }
        else{
            return removed;
        }
    }


}




