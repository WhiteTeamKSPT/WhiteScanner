package ru.spbstu.kspt.white.whitescanner;

import android.content.Intent;
import android.os.AsyncTask;
import android.os.Bundle;
import android.support.v4.widget.SwipeRefreshLayout;
import android.support.v7.app.AppCompatActivity;
import android.util.Log;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.ListView;

import java.io.IOException;
import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;
import java.util.Iterator;
import java.util.Map;
import java.util.Set;

/**
 * Created by Victor on 24.10.2015.
 */


public class ModelsList extends AppCompatActivity implements SwipeRefreshLayout.OnRefreshListener {

    public final static String EXTRA_MESSAGE = "ru.spbstu.kspt.white.whitescanner.MODEL_NAME";
    private static final String COMPONENT = "ModelsList";

    ListView listView ;
    SwipeRefreshLayout mSwipeRefreshLayout;
    ArrayAdapter<String> adapter;

    ArrayList<String> listViewItems = new ArrayList<>();

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.models_list);

        // Get ListView object from xml
        listView = (ListView) findViewById(R.id.modelsList);

        // Defined Array values to show in ListView
        String[] values = new String[] { "ashtray",
                "coke_can",
                "skateboard"
        };
        Collections.addAll(listViewItems, values);

        mSwipeRefreshLayout = (SwipeRefreshLayout) findViewById(R.id.swipe_refresh);
        mSwipeRefreshLayout.setOnRefreshListener(this);
        // делаем повеселее
//        mSwipeRefreshLayout.setColorSchemeResources(R.color.blue, R.color.green, R.color.yellow, R.color.red);

        // Define a new Adapter
        // First parameter - Context
        // Second parameter - Layout for the row
        // Third parameter - ID of the TextView to which the data is written
        // Forth - the Array of data

        adapter = new ArrayAdapter<String>(this,
                android.R.layout.simple_list_item_1, android.R.id.text1, listViewItems);

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

//                try {
//                    int number = Integer.parseInt(itemValue);
//
//                } catch (NumberFormatException e) {
//                    // Show model
//                    showModel(itemValue);
//                }
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

    @Override
    public void onRefresh() {
        mSwipeRefreshLayout.setRefreshing(true);
        new GetPhotos().execute();
    }

    private class GetPhotos extends AsyncTask<Void, Void, Boolean> {
        @Override
        protected Boolean doInBackground(Void... params) {

            // params comes from the execute() call: params[0] is the url.
            try {
                Iterator<Integer> iterator = Requests.pendingRequests.listIterator();
                while (iterator.hasNext()) {
                    Integer set = iterator.next();
                    Log.d(COMPONENT, "Fetching set " + set.toString());
                    String url = Network.makeResultURL("user", set);
                    HttpResponse resp = Network.doGET(url);
                    if (resp.code != 500) {
                        Log.d(COMPONENT, "Set is fetched: " + set.toString());
                        Requests.models.put(set, resp.data);
                        iterator.remove();
                    } else {
                        Log.d(COMPONENT, "Set not ready: " + set.toString());
                    }
                }
            } catch (IOException e) {
                Log.e(COMPONENT, e.toString());
                return false;
            }
            return true;
        }
        // onPostExecute displays the results of the AsyncTask.
        @Override
        protected void onPostExecute(Boolean result) {
            listViewItems.clear();
            for (Integer model: Requests.models.keySet()) {
                listViewItems.add(model.toString());
            }
            adapter.notifyDataSetChanged();
            mSwipeRefreshLayout.setRefreshing(false);
        }
    }
}