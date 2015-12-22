package ru.spbstu.kspt.white.whitescanner;

import android.app.Service;
import android.content.Intent;
import android.os.IBinder;

public class NewModelsNotifier extends Service {
    public NewModelsNotifier() {
    }

    @Override
    public IBinder onBind(Intent intent) {
        // TODO: Return the communication channel to the service.
        throw new UnsupportedOperationException("Not yet implemented");
    }
}
