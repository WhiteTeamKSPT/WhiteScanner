package ru.spbstu.kspt.white.whitescanner;

import android.support.annotation.Nullable;
import android.util.Log;

import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.HashSet;
import java.util.Set;

/**
 * Created by artyom on 02.12.15.
 */
public class Network {
    private static final String COMPONENT = "Network";
    static final String BASE_URL = "http://whiteteam.cloudapp.net:8080";
    static final String UPLOAD_PATH = "/client/upload";
    static final String FINISH_PATH = "/client/finished";
    static final String RESULT_PATH = "/client/result";
    static final String MODELS_PATH = "/client/models";

    public static String makeUploadURL(String user, int set, int number) {
        return BASE_URL + UPLOAD_PATH + "/" + user + "/" + set + "/" + number + "/";
    }

    public static String makeFinishURL(String user, int set) {
        return BASE_URL + FINISH_PATH + "/" + user + "/" + set + "/";
    }

    public static String makeResultURL(String user, int set) {
        return BASE_URL + RESULT_PATH + "/" + user + "/" + set + "/";
    }

    public static String makeModelsURL(String user) {
        return BASE_URL + MODELS_PATH + "/" + user + "/";
    }

    // Given a URL, establishes an HttpUrlConnection and retrieves
    // the web page content as a InputStream, which it returns as
    // a string.
    public static void doPOST(String uploadURL, @Nullable byte[] payload) throws IOException {
        OutputStream os = null;
        Log.d(COMPONENT, "Do POST to " + uploadURL);

        try {
            URL url = new URL(uploadURL);
            HttpURLConnection conn = (HttpURLConnection) url.openConnection();
            conn.setReadTimeout(10000 /* milliseconds */);
            conn.setConnectTimeout(15000 /* milliseconds */);
            conn.setRequestMethod("POST");
            conn.setDoOutput(true);
            if (payload != null) {
                Log.d(COMPONENT, "Payload size is  " + payload.length);
                conn.setFixedLengthStreamingMode(payload.length);
            }
            // Starts the query
            conn.connect();
            os = conn.getOutputStream();
            if (payload != null) {
                os.write(payload);
            }
            os.flush();
            os.close();

            int response = conn.getResponseCode();
            Log.d(COMPONENT, "The response is: " + response);

            // Makes sure that the InputStream is closed after the app is
            // finished using it.
        } finally {
            if (os != null) {
                os.close();
            }
        }
    }

    public static HttpResponse doGET(String uploadURL) throws IOException {
        InputStream is = null;
        Log.d(COMPONENT, "Do GET to " + uploadURL);

        ByteArrayOutputStream baos = new ByteArrayOutputStream();
        HttpResponse response = new HttpResponse();

        try {
            URL url = new URL(uploadURL);
            HttpURLConnection conn = (HttpURLConnection) url.openConnection();
            conn.setReadTimeout(10000 /* milliseconds */);
            conn.setConnectTimeout(15000 /* milliseconds */);
            conn.setRequestProperty("User-Agent", "Mozilla/5.0 ( compatible ) ");
            conn.setRequestProperty("Accept", "*/*");

            // Starts the query
            conn.connect();

            response.code = conn.getResponseCode();
            Log.d(COMPONENT, "The response is: " + response.code);
            // TODO
            if (response.code == 200) {
                is = conn.getInputStream();
                byte[] buffer = new byte[4096];
                int n;

                while ((n = is.read(buffer)) > 0) {
                    baos.write(buffer, 0, n);
                }
            }

            // Makes sure that the InputStream is closed after the app is
            // finished using it.
        } finally {
            if (is != null) {
                is.close();
            }
        }
        response.data = baos.toByteArray();
        return response;
    }

    public static Set<Integer> pollModels() {
        Set<Integer> set = new HashSet<>();
        try {
            HttpResponse response = Network.doGET(Network.makeModelsURL(Requests.username));
            String string = new String(response.data);
            String[] models = string.split(";");
            for (String model : models) {
                if (!model.isEmpty()) {
                    Integer integer = Integer.parseInt(model);
                    set.add(integer);
                }
            }
        } catch (Exception e) {
            Log.d(COMPONENT, "Network issues in service: " + e);
        }
        return set;
    }
}

class HttpResponse {
    byte[] data;
    int code;
}