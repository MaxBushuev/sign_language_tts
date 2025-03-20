import { createRequire } from 'module';const require = createRequire(import.meta.url);
import {
  findClosestIonContent,
  scrollToTop
} from "./chunk-E6Q63HII.js";
import "./chunk-X6NTSWHZ.js";
import {
  readTask,
  writeTask
} from "./chunk-XNRZJ4YG.js";
import {
  componentOnReady
} from "./chunk-I5X3O2IP.js";
import {
  __async
} from "./chunk-5P6RLSS7.js";

// node_modules/@ionic/core/components/status-tap.js
var startStatusTap = () => {
  const win = window;
  win.addEventListener("statusTap", () => {
    readTask(() => {
      const width = win.innerWidth;
      const height = win.innerHeight;
      const el = document.elementFromPoint(width / 2, height / 2);
      if (!el) {
        return;
      }
      const contentEl = findClosestIonContent(el);
      if (contentEl) {
        new Promise((resolve) => componentOnReady(contentEl, resolve)).then(() => {
          writeTask(() => __async(void 0, null, function* () {
            contentEl.style.setProperty("--overflow", "hidden");
            yield scrollToTop(contentEl, 300);
            contentEl.style.removeProperty("--overflow");
          }));
        });
      }
    });
  });
};
export {
  startStatusTap
};
/*! Bundled license information:

@ionic/core/components/status-tap.js:
  (*!
   * (C) Ionic http://ionicframework.com - MIT License
   *)
*/
//# sourceMappingURL=status-tap-3473UFGT.js.map
