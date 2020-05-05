package com.example.foodstock.data;

import android.content.ContentValues;
import android.content.Context;
import android.database.Cursor;
import android.database.sqlite.SQLiteDatabase;
import android.database.sqlite.SQLiteOpenHelper;

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
            DROP_TABLE = "DROP TABLE " + name + " IF EXISTS";
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


    //Stock table operations
    //---------------------------------------------------------


    //Estimations table operations
    //---------------------------------------------------------
}
