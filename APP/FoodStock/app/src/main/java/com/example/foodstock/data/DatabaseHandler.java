package com.example.foodstock.data;

import android.content.ContentValues;
import android.content.Context;
import android.database.Cursor;
import android.database.sqlite.SQLiteDatabase;
import android.database.sqlite.SQLiteOpenHelper;

import com.example.foodstock.model.Estimation;
import com.example.foodstock.model.History;
import com.example.foodstock.model.InStock;
import com.example.foodstock.model.Month;
import com.example.foodstock.model.Product;
import com.example.foodstock.util.Util;

import java.util.ArrayList;
import java.util.List;

public class DatabaseHandler extends SQLiteOpenHelper {
    /**
     * @param context : current context of the app
     */
    public DatabaseHandler(Context context) {
        super(context, Util.DATABASE_NAME, null, Util.DATABASE_VERSION);
    }

    @Override
    public void onCreate(SQLiteDatabase db) {
        for(String table : Util.CREATE_TABLES){
            db.execSQL(table);
        }


    }

    @Override
    public void onUpgrade(SQLiteDatabase db, int oldVersion, int newVersion) {
        String DROP_TABLE = "";
        //Drop all tables in db when reseting
        for(String name : Util.TABLE_NAMES) {
            DROP_TABLE = "DROP TABLE IF EXISTS " + name;
            db.execSQL(DROP_TABLE);
        }
        onCreate(db);
    }

    /*CRUD Operations*/

    //Product table operations
    //---------------------------------------------------------
    public void addProduct(Product product){
        SQLiteDatabase db = this.getWritableDatabase();
        ContentValues values = new ContentValues();
        values.put(Util.PRODUCT_NAME, product.getName());
        db.insert(Util.PRODUCT_TABLE, null, values);
        db.close();
    }

    public Product getProduct(int id){
        SQLiteDatabase db = this.getReadableDatabase();
        Cursor cursor = db.query(Util.PRODUCT_TABLE, new String[]{Util.PRODUCT_ID, Util.PRODUCT_NAME}, Util.PRODUCT_ID + "=?", new String[]{String.valueOf(id)}, null, null, null);
        if(cursor != null){
            cursor.moveToFirst();
        }
        Product product = new Product();
        product.setId(Integer.parseInt(cursor.getString(0)));
        product.setName(cursor.getString(1));
        return product;
    }

    public List<Product> getAllProducts(){
      List<Product> productList = new ArrayList<>();
      SQLiteDatabase db = this.getReadableDatabase();
      String selectAll = "SELECT * FROM " + Util.PRODUCT_TABLE;
      Cursor cursor = db.rawQuery(selectAll, null);
      //If the cursor is not null
      if(cursor.moveToFirst()){
          //Add all products until there is no next one
          do{
              Product product = new Product();
              product.setId(Integer.parseInt(cursor.getString(0)));
              product.setName(cursor.getString(1));
              productList.add(product);
          }while(cursor.moveToNext());
      }
    return productList;
    }

    //Month table operations
    //---------------------------------------------------------
    public void addMonths(){
        SQLiteDatabase db = this.getWritableDatabase();
        for(String month : Util.MONTHS){
            addMonth(db, month);
        }
        db.close();
    }

    public void addMonth(SQLiteDatabase db, String month){
        ContentValues values = new ContentValues();
        values.put(Util.MONTH_NAME, month);
        db.insert(Util.MONTHS_TABLE, null, values);
    }

    public Month getMonth(int id){
        SQLiteDatabase db = this.getReadableDatabase();
        Cursor cursor = db.query(Util.MONTHS_TABLE, new String[]{Util.MONTH_ID, Util.MONTH_NAME}, Util.MONTH_ID + "=?", new String[]{String.valueOf(id)}, null, null, null);
        if(cursor != null){
            cursor.moveToFirst();
        }
        Month month= new Month();
        month.setId(Integer.parseInt(cursor.getString(0)));
        month.setName(cursor.getString(1));
        return month;
    }

    public List<Month> getAllMonths(){
        List<Month> monthList = new ArrayList<>();
        SQLiteDatabase db = this.getReadableDatabase();
        String selectAll = "SELECT * FROM " + Util.MONTHS_TABLE;
        Cursor cursor = db.rawQuery(selectAll, null);
        //If the cursor is not null
        if(cursor.moveToFirst()){
            //Add all months until there is no next one
            do{
                Month month = new Month();
                month.setId(Integer.parseInt(cursor.getString(0)));
                month.setName(cursor.getString(1));
                monthList.add(month);
            }while(cursor.moveToNext());
        }
        return monthList;
    }

    //Product history table operations
    //---------------------------------------------------------
    public void addToHistory(History history){
        SQLiteDatabase db = this.getWritableDatabase();
        ContentValues values = new ContentValues();
        values.put(Util.PRODUCT_ID, history.getProduct_id());
        values.put(Util.ADDED_DATE, history.getAdded_date());
        values.put(Util.REMOVED_DATE, history.getRemoved_date());
        values.put(Util.ACTUAL_RATE, history.getActual_rate());
        db.insert(Util.PRODUCT_HISTORY_TABLE, null, values);
        db.close();
    }

    public List<History> getHistories(int product_id){
        List<History> historyList = new ArrayList<>();
        SQLiteDatabase db = this.getReadableDatabase();
        String selectAll = "SELECT * FROM " + Util.PRODUCT_HISTORY_TABLE + " WHERE " + Util.PRODUCT_ID + "=?";
        Cursor cursor = db.rawQuery(selectAll, new String[]{String.valueOf(product_id)});
        //If the cursor is not null
        if(cursor.moveToFirst()){
            do{
                History history = new History();
                history.setHistory_id(Integer.parseInt(cursor.getString(0)));
                history.setProduct_id(Integer.parseInt(cursor.getString(1)));
                history.setAdded_date(cursor.getString(2));
                history.setRemoved_date(cursor.getString(3));
                history.setActual_rate(Integer.parseInt(cursor.getString(4)));
                historyList.add(history);
            }while(cursor.moveToNext());
        }
        return historyList;
    }

    //Stock table operations
    //---------------------------------------------------------
    public void addToStock(InStock stock){
        SQLiteDatabase db = this.getWritableDatabase();
        ContentValues values = new ContentValues();
        values.put(Util.PRODUCT_ID, stock.getProduct_id());
        values.put(Util.ADDED_DATE, stock.getAdded_date());
        values.put(Util.EXPIRE_DATE, stock.getExpire_date());
        values.put(Util.QUANTITY, stock.getQuantity());
        db.insert(Util.STOCK_TABLE, null, values);
        db.close();
    }

    public List<InStock> getStock(){
        List<InStock> stockList = new ArrayList<>();
        SQLiteDatabase db = this.getReadableDatabase();
        String selectAll = "SELECT * FROM " + Util.STOCK_TABLE;
        Cursor cursor = db.rawQuery(selectAll, null);
        //If the cursor is not null
        if(cursor.moveToFirst()){
            do{
                InStock stock = new InStock();
                stock.setProduct_id(Integer.parseInt(cursor.getString(0)));
                stock.setQuantity(Integer.parseInt(cursor.getString(1)));
                stock.setAdded_date(cursor.getString(2));
                stock.setExpire_date(cursor.getString(3));
                stockList.add(stock);
            }while(cursor.moveToNext());
        }
        return stockList;
    }

    public InStock getStockItem(int product_id){
        SQLiteDatabase db = this.getReadableDatabase();
        Cursor cursor = db.query(Util.STOCK_TABLE, new String[]{Util.PRODUCT_ID, Util.QUANTITY, Util.ADDED_DATE, Util.EXPIRE_DATE}, Util.PRODUCT_ID + "=?", new String[]{String.valueOf(product_id)}, null, null, null);
        if(cursor != null){
            cursor.moveToFirst();
        }
        InStock stock = new InStock();
        stock.setProduct_id(Integer.parseInt(cursor.getString(0)));
        stock.setQuantity(Integer.parseInt(cursor.getString(1)));
        stock.setAdded_date(cursor.getString(2));
        stock.setExpire_date(cursor.getString(3));
        return stock;
    }

    //Update stock

    //Remove from stock



    //Estimations table operations
    //---------------------------------------------------------
    public void addEstimation(Estimation estimation){
        SQLiteDatabase db = this.getWritableDatabase();
        ContentValues values = new ContentValues();
        values.put(Util.PRODUCT_ID, estimation.getProduct_id());
        values.put(Util.MONTH_ID, estimation.getMonth_id());
        values.put(Util.ESTIMATED_RATE, estimation.getEstimated_rate());
        db.insert(Util.ESTIMATED_RATES_TABLE, null, values);
        db.close();
    }

    public Estimation getEstimation(int product_id, int month_id){
        SQLiteDatabase db = this.getReadableDatabase();
        Cursor cursor = db.query(Util.ESTIMATED_RATES_TABLE, new String[]{Util.PRODUCT_ID, Util.MONTH_ID, Util.ESTIMATED_RATE}, Util.PRODUCT_ID + "=? AND " + Util.MONTH_ID + "=?", new String[]{String.valueOf(product_id), String.valueOf(month_id)}, null, null, null);
        if(cursor != null){
            cursor.moveToFirst();
        }
        Estimation estimation = new Estimation();
        estimation.setProduct_id(Integer.parseInt(cursor.getString(0)));
        estimation.setMonth_id(Integer.parseInt(cursor.getString(1)));
        estimation.setEstimated_rate(Integer.parseInt(cursor.getString(2)));
        return estimation;
    }

    //Update estimation
}
