import UIKit
import Capacitor

/// The app's main screen: Capacitor's web view, plus the app's own AppTiles plugin.
class AppViewController: CAPBridgeViewController {
    override open func capacitorDidLoad() {
        bridge?.registerPluginInstance(AppTilesPlugin())
    }
}
