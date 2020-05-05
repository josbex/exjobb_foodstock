package com.example.foodstock;

import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;
import android.util.Log;

import com.example.foodstock.data.DatabaseHandler;
import com.example.foodstock.model.Month;

import java.util.List;

public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {

        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        DatabaseHandler db = new DatabaseHandler(MainActivity.this);
        //db.addMonths();

        List<Month> months = db.getAllMonths();
        for(Month m: months){
            Log.d("MainActivity", "OnCreate: " + m.getName() +" ID: " + m.getId());
        }

    }
}
