import { createRequire } from 'module';const require = createRequire(import.meta.url);
import {
  ConsentStatus,
  ConsentType
} from "./chunk-NUFML27Q.js";
import {
  registerPlugin
} from "./chunk-MFS3WVA5.js";
import "./chunk-5P6RLSS7.js";

// node_modules/@capacitor-firebase/analytics/dist/esm/index.js
var FirebaseAnalytics = registerPlugin("FirebaseAnalytics", {
  web: () => import("./web-5PP7PTZR.js").then((m) => new m.FirebaseAnalyticsWeb())
});
export {
  ConsentStatus,
  ConsentType,
  FirebaseAnalytics
};
//# sourceMappingURL=@capacitor-firebase_analytics.js.map
