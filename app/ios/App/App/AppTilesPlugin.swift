import Foundation
import Capacitor

/// Reads the map tiles built into the app (public/tiles/map.pmtiles).
/// The map asks for small pieces of the 140 MB file, and the page calls read({offset, length}) here.
/// The file is read from the app itself, so it keeps working after an over-the-air website update.
@objc(AppTilesPlugin)
public class AppTilesPlugin: CAPPlugin, CAPBridgedPlugin {
    public let identifier = "AppTilesPlugin"
    public let jsName = "AppTiles"
    public let pluginMethods: [CAPPluginMethod] = [
        CAPPluginMethod(name: "info", returnType: CAPPluginReturnPromise),
        CAPPluginMethod(name: "read", returnType: CAPPluginReturnPromise)
    ]

    private let queue = DispatchQueue(label: "uk.co.allblacktaxis.explorelondon.tiles")
    private var handle: FileHandle?
    private var size: UInt64 = 0
    private var path = ""

    private func open() throws -> FileHandle {
        if let h = handle { return h }
        guard let url = Bundle.main.url(forResource: "map", withExtension: "pmtiles", subdirectory: "public/tiles") else {
            throw NSError(domain: "AppTiles", code: 1, userInfo: [NSLocalizedDescriptionKey: "No built-in map tiles"])
        }
        let attrs = try FileManager.default.attributesOfItem(atPath: url.path)
        size = (attrs[.size] as? NSNumber)?.uint64Value ?? 0
        path = url.path
        let h = try FileHandle(forReadingFrom: url)
        handle = h
        return h
    }

    @objc func info(_ call: CAPPluginCall) {
        queue.async {
            do {
                _ = try self.open()
                // path: the page reads the file directly through the app's own file server (faster than read())
                call.resolve(["available": true, "size": Double(self.size), "path": self.path])
            } catch {
                call.resolve(["available": false])
            }
        }
    }

    @objc func read(_ call: CAPPluginCall) {
        let offset = UInt64(max(0, call.getDouble("offset") ?? 0))
        let length = Int(max(0, call.getDouble("length") ?? 0))
        queue.async {
            do {
                let h = try self.open()
                guard offset < self.size else { call.reject("Out of range"); return }
                try h.seek(toOffset: offset)
                let data = try h.read(upToCount: length) ?? Data()
                call.resolve(["data": data.base64EncodedString()])
            } catch {
                call.reject("Could not read the map tiles: \(error.localizedDescription)", nil, error)
            }
        }
    }
}
