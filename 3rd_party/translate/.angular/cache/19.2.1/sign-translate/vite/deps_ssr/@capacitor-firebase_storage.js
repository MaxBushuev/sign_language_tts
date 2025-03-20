import { createRequire } from 'module';const require = createRequire(import.meta.url);
import {
  registerPlugin
} from "./chunk-MFS3WVA5.js";
import "./chunk-5P6RLSS7.js";

// node_modules/@capacitor-firebase/storage/dist/esm/index.js
var FirebaseStorage = registerPlugin("FirebaseStorage", {
  web: () => import("./web-5TZFZQLC.js").then((m) => new m.FirebaseStorageWeb())
});
export {
  FirebaseStorage
};
//# sourceMappingURL=@capacitor-firebase_storage.js.map
