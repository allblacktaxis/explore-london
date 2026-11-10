package uk.co.allblacktaxis.explorelondon;

import android.content.res.AssetFileDescriptor;
import android.util.Base64;
import com.getcapacitor.JSObject;
import com.getcapacitor.Plugin;
import com.getcapacitor.PluginCall;
import com.getcapacitor.PluginMethod;
import com.getcapacitor.annotation.CapacitorPlugin;
import java.io.FileInputStream;
import java.io.IOException;
import java.nio.ByteBuffer;
import java.nio.channels.FileChannel;

/**
 * Reads the map tiles built into the app (public/tiles/map.pmtiles).
 * The map asks for small pieces of the 140 MB file ("bytes 1000 to 2000"), which the
 * web view's own file server can't do, so the page calls read({offset, length}) here instead.
 */
@CapacitorPlugin(name = "AppTiles")
public class AppTilesPlugin extends Plugin {
    private static final String ASSET = "public/tiles/map.pmtiles";
    private FileChannel channel;
    private long start;
    private long size = -1;

    private synchronized void open() throws IOException {
        if (channel != null) return;
        AssetFileDescriptor fd = getContext().getAssets().openFd(ASSET); // works because the file is stored uncompressed
        FileInputStream in = fd.createInputStream();
        channel = in.getChannel();
        start = fd.getStartOffset();
        size = fd.getLength();
    }

    @PluginMethod
    public void info(PluginCall call) {
        JSObject r = new JSObject();
        try {
            open();
            r.put("available", true);
            r.put("size", size);
        } catch (IOException e) {
            r.put("available", false);
        }
        call.resolve(r);
    }

    @PluginMethod
    public void read(PluginCall call) {
        try {
            open();
            long offset = call.getDouble("offset", 0.0).longValue();
            int length = call.getDouble("length", 0.0).intValue();
            if (offset < 0 || length < 0 || offset >= size) {
                call.reject("Out of range");
                return;
            }
            length = (int) Math.min(length, size - offset);
            ByteBuffer buf = ByteBuffer.allocate(length);
            long pos = start + offset;
            while (buf.hasRemaining()) {
                int n = channel.read(buf, pos);
                if (n < 0) break;
                pos += n;
            }
            JSObject r = new JSObject();
            r.put("data", Base64.encodeToString(buf.array(), 0, buf.position(), Base64.NO_WRAP));
            call.resolve(r);
        } catch (IOException e) {
            call.reject("Could not read the map tiles", e);
        }
    }
}
