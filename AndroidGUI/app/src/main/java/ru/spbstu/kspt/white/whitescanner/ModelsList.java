package ru.spbstu.kspt.white.whitescanner;

import android.content.Intent;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.ListView;

/**
 * Created by Victor on 24.10.2015.
 */


public class ModelsList extends AppCompatActivity {

    public final static String EXTRA_MESSAGE = "ru.spbstu.kspt.white.whitescanner.MODEL_NAME";

    ListView listView ;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.models_list);

        // Get ListView object from xml
        listView = (ListView) findViewById(R.id.modelsList);

        // Defined Array values to show in ListView
        String[] values = new String[] {
                "rabbit"
                //"ashtray",
                //"coke_can",
                //"skateboard"
        };

        // Define a new Adapter
        // First parameter - Context
        // Second parameter - Layout for the row
        // Third parameter - ID of the TextView to which the data is written
        // Forth - the Array of data

        ArrayAdapter<String> adapter = new ArrayAdapter<String>(this,
                android.R.layout.simple_list_item_1, android.R.id.text1, values);

        // Assign adapter to ListView
        listView.setAdapter(adapter);

        // ListView Item Click Listener
        listView.setOnItemClickListener(new AdapterView.OnItemClickListener() {

            @Override
            public void onItemClick(AdapterView<?> parent, View view,
                                    int position, long id) {

                // ListView Clicked item index
                int itemPosition = position;

                // ListView Clicked item value
                String itemValue = (String) listView.getItemAtPosition(position);

                // Show model
                showModel(itemValue);
            }

        });
    }

    /** Called when the user clicks the Show model button */
    public void showModel(String modelName) {
        // Do something in response to button
        Intent intent = new Intent(this, ModelViewer.class);
        intent.putExtra(EXTRA_MESSAGE, modelName);
        startActivity(intent);
    }

}