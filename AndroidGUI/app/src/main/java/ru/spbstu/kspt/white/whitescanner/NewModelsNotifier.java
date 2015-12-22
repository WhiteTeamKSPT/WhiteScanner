package ru.spbstu.kspt.white.whitescanner;

import android.app.Notification;
import android.app.NotificationManager;
import android.app.PendingIntent;
import android.app.Service;
import android.content.Intent;
import android.os.IBinder;
import android.util.Log;

import java.io.IOException;
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

    private final ScheduledExecutorService scheduler =
            Executors.newScheduledThreadPool(1);


    public NewModelsNotifier() {
    }

    @Override
    public void onCreate() {
        super.onCreate();
        nm = (NotificationManager) getSystemService(NOTIFICATION_SERVICE);
        Log.d(COMPONENT, "onCreate");
    }

    @Override
    public int onStartCommand(Intent intent, int flags, int startId) {
        Log.d(COMPONENT, "onStartCommand");
        sendNotification("Service started", "Models are monitored");

//        new Thread(pollRunnable()).start();

        scheduler.scheduleAtFixedRate(pollRunnable(), 0, 1, MINUTES);

        return super.onStartCommand(intent, flags, startId);
    }

    @Override
    public void onDestroy() {
        super.onDestroy();
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
        try {
            HttpResponse response = Network.doGET(Network.makeModelsURL(Requests.username));
            String string = new String(response.data);
            String[] models = string.split(";");
            for (String model : models) {
                if (!model.isEmpty()) {
                    Integer integer = Integer.parseInt(model);
                    if (!sets.contains(integer)) {
                        sendNotification("New model!", "Check it");
                    }
                    sets.add(integer);
                }
            }
        } catch (Exception e) {
            Log.d(COMPONENT, "Network issues in service: " + e);
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
}