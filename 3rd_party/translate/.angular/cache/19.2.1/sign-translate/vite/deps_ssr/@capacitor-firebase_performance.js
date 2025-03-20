import { createRequire } from 'module';const require = createRequire(import.meta.url);
import {
  registerPlugin
} from "./chunk-MFS3WVA5.js";
import "./chunk-5P6RLSS7.js";

// node_modules/@capacitor-firebase/performance/dist/esm/index.js
var FirebasePerformance = registerPlugin("FirebasePerformance", {
  web: () => import("./web-DZCGNRIL.js").then((m) => new m.FirebasePerformanceWeb())
});
export {
  FirebasePerformance
};
//# sourceMappingURL=@capacitor-firebase_performance.js.map
