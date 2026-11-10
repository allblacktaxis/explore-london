package uk.co.allblacktaxis.explorelondon;

import android.os.Bundle;
import com.getcapacitor.BridgeActivity;

public class MainActivity extends BridgeActivity {
    @Override
    public void onCreate(Bundle savedInstanceState) {
        // the app's own plugin that reads the built-in map tiles (must be registered before super.onCreate)
        registerPlugin(AppTilesPlugin.class);
        super.onCreate(savedInstanceState);
    }
}
