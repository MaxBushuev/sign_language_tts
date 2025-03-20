import { createRequire } from 'module';const require = createRequire(import.meta.url);
import {
  registerPlugin
} from "./chunk-MFS3WVA5.js";

// node_modules/@capacitor/filesystem/dist/esm/index.js
var Filesystem = registerPlugin("Filesystem", {
  web: () => import("./web-MPIY3TUL.js").then((m) => new m.FilesystemWeb())
});

export {
  Filesystem
};
//# sourceMappingURL=chunk-WBA5LLZH.js.map
