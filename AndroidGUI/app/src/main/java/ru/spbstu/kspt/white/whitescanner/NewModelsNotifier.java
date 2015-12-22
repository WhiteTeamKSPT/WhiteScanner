package ru.spbstu.kspt.white.whitescanner;

import android.app.Notification;
import android.app.NotificationManager;
import android.app.PendingIntent;
import android.app.Service;
import android.content.Intent;
import android.os.IBinder;
import android.util.Log;

import com.codebutler.android_websockets.WebSocketClient;

import org.apache.http.message.BasicNameValuePair;

import java.io.IOException;
import java.net.URI;
import java.util.ArrayList;
import java.util.HashSet;
import static java.util.concurrent.TimeUnit.*;
import java.util.Set;
import java.util.concurrent.Executors;
import java.util.concurrent.ScheduledExecutorService;
import java.util.concurrent.ScheduledFuture;

public class NewModelsNotifier extends Service {
    private static final String COMPONENT = "NewModelsNotifier";

    private static Set<Integer> sets = new HashSet<>();
    NotificationManager nm;
    WebSocketClient client;

    private final ScheduledExecutorService scheduler =
            Executors.newScheduledThreadPool(1);


    public NewModelsNotifier() {
    }

    @Override
    public void onCreate() {
        super.onCreate();
        nm = (NotificationManager) getSystemService(NOTIFICATION_SERVICE);
        client = webSocket();
        Log.d(COMPONENT, "onCreate");
    }

    @Override
    public int onStartCommand(Intent intent, int flags, int startId) {
        Log.d(COMPONENT, "onStartCommand");
        sendNotification("Service started", "Models are monitored");

        scheduler.scheduleAtFixedRate(pollRunnable(), 0, 1, MINUTES);
        client.connect();

        return super.onStartCommand(intent, flags, startId);
    }

    @Override
    public void onDestroy() {
        super.onDestroy();
        client.disconnect();
        Log.d(COMPONENT, "onDestroy");
    }

    public IBinder onBind(Intent intent) {
        Log.d(COMPONENT, "onBind");
        return null;
    }

    Runnable pollRunnable() {
        return new Runnable() {
            public void run() {
                pollModels();
            }
        };
    }

    void pollModels() {
        Set<Integer> new_set = Network.pollModels();
        if (!sets.containsAll(new_set)) {
            sendNotification("New model!", "Check it");
            sets.addAll(new_set);
        }
    }

    void sendNotification(String title, String text) {
        Intent intent = new Intent(this, FullscreenActivity.class);
        PendingIntent pIntent = PendingIntent.getActivity(this, 0, intent, 0);

        Notification notification = new Notification.Builder(this)
                .setContentTitle(title)
                .setContentText(text)
                .setSmallIcon(R.drawable.models)
                .setContentIntent(pIntent)
                .setAutoCancel(true)
                .build();

        // отправляем
        nm.notify(1, notification);
    }

    WebSocketClient webSocket() {
        String address = Network.makeWebSocketAddress(Requests.username);
        return new WebSocketClient(URI.create(address), new WebSocketClient.Listener() {
            @Override
            public void onConnect() {
                Log.d(COMPONENT, "Connected!");
            }

            @Override
            public void onMessage(String message) {
                Log.d(COMPONENT, String.format("Got string message! %s", message));
                sendNotification("New model!", "Check it");
            }

            @Override
            public void onMessage(byte[] data) {
                // Log.d(COMPONENT, String.format("Got binary message! %s", toHexString(data)));
            }

            @Override
            public void onDisconnect(int code, String reason) {
                Log.d(COMPONENT, String.format("Disconnected! Code: %d Reason: %s", code, reason));
            }

            @Override
            public void onError(Exception error) {
                Log.e(COMPONENT, "Error!", error);
            }

        }, new ArrayList<BasicNameValuePair>());
    }
}