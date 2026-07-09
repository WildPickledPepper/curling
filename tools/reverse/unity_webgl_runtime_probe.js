/*
 * Passive runtime probe for the curling Unity WebGL build.
 *
 * Usage:
 *   1. Open the Unity WebGL page.
 *   2. Paste this file into DevTools Console before or during page startup.
 *   3. After the game has loaded, run:
 *        __curlingProbe.scanAndHookFS()
 *        __curlingProbe.installKnownCurlingHooks()
 *        __curlingProbe.installPhysXNativeHooks()
 *   4. Run sampling in the page, then export:
 *        __curlingProbe.downloadEvents()
 *
 * The probe records runtime evidence only. It does not call Unity methods,
 * does not mutate physics objects, and table hooks are opt-in.
 */
(function installCurlingRuntimeProbe(global) {
  "use strict";

  if (global.__curlingProbe && global.__curlingProbe.installed) {
    console.warn("[curlingProbe] already installed");
    return;
  }

  var probe = {
    installed: true,
    installedAt: new Date().toISOString(),
    events: [],
    instances: [],
    memories: [],
    tables: [],
    hooks: [],
    maxPreviewBytes: 256,
    autoCookedHullHook: !!(
      global.__curlingProbeConfig &&
      global.__curlingProbeConfig.autoCookedHullHook
    ),
    knownFunctionIndices: [
      { index: 10894, name: "CurlingStoneNew.Start", signature: "vii" },
      { index: 10896, name: "CurlingStoneNew.OnCollisionEnter", signature: "viii" },
      { index: 12126, name: "ExtendedColliders3D.Awake", signature: "vii" },
      { index: 10660, name: "AutoDCP.HandleMessage", signature: "viii" },
      { index: 10932, name: "DCP.HandleMessage", signature: "viii" },
      { index: 11172, name: "FastDCP.CopyGameState", signature: "vii" },
      { index: 11203, name: "FastDCP.Update", signature: "vii" }
    ],
    physxNativeHookTargets: [
      {
        index: 120118,
        wasm: "func70576",
        name: "PxcPCMContactConvexConvex",
        signature: "iiiiiiiii",
        role: "stone-stone PCM ContactBuffer producer",
        capture: "arm",
        windowBytes: 8192,
        nestedBytes: 2048
      },
      {
        index: 120119,
        wasm: "func70577",
        name: "PxcPCMContactConvexMesh",
        signature: "iiiiiiiii",
        role: "stone-rink PCM ContactBuffer producer",
        capture: "whenArmed",
        windowBytes: 8192,
        nestedBytes: 1024
      },
      {
        index: 120204,
        wasm: "func70739",
        name: "PxsContext.contactManagerDiscreteUpdate",
        signature: "vi",
        role: "contact manager task",
        capture: "whenArmed",
        windowBytes: 2048,
        nestedBytes: 1024
      },
      {
        index: 120587,
        wasm: "func71272",
        name: "PxsDynamics.createFinalizeContacts",
        signature: "vi",
        role: "contact finalization task",
        capture: "whenArmed",
        windowBytes: 4096,
        nestedBytes: 2048
      },
      {
        index: 120379,
        wasm: "func70963",
        name: "createFinalizeSolverContacts4",
        signature: "iiiifffffi",
        role: "4-wide solver contact row writer",
        capture: "whenArmed",
        windowBytes: 8192,
        nestedBytes: 2048
      },
      {
        index: 120487,
        wasm: "func71103",
        name: "createFinalizeSolverContacts",
        signature: "iiiifffffii",
        role: "single-pair solver contact row writer",
        capture: "whenArmed",
        windowBytes: 8192,
        nestedBytes: 2048
      }
    ],
    physxNativeCapture: {
      armedUntilMs: 0,
      armSerial: 0
    }
  };

  function nowMs() {
    if (global.performance && typeof global.performance.now === "function") {
      return global.performance.now();
    }
    return Date.now();
  }

  function pushEvent(type, data) {
    var event = {
      t: nowMs(),
      type: type,
      data: data || {}
    };
    probe.events.push(event);
    return event;
  }

  function describeObject(value) {
    if (value === null) return "null";
    if (value === undefined) return "undefined";
    if (typeof value !== "object" && typeof value !== "function") return typeof value;
    var keys = [];
    try {
      keys = Object.keys(value).slice(0, 24);
    } catch (err) {
      keys = ["<keys unavailable: " + err.message + ">"];
    }
    return {
      tag: Object.prototype.toString.call(value),
      keys: keys
    };
  }

  function bytesPreview(bufferLike, maxBytes) {
    var maxLen = maxBytes || probe.maxPreviewBytes;
    try {
      var view;
      if (typeof bufferLike === "string") {
        return bufferLike.length <= maxLen ? bufferLike : bufferLike.slice(0, maxLen) + "...";
      }
      if (bufferLike instanceof ArrayBuffer) {
        view = new Uint8Array(bufferLike, 0, Math.min(bufferLike.byteLength, maxLen));
      } else if (ArrayBuffer.isView(bufferLike)) {
        view = new Uint8Array(
          bufferLike.buffer,
          bufferLike.byteOffset,
          Math.min(bufferLike.byteLength, maxLen)
        );
      } else {
        return describeObject(bufferLike);
      }
      return Array.prototype.map.call(view, function toHex(v) {
        return ("0" + v.toString(16)).slice(-2);
      }).join(" ");
    } catch (err) {
      return "<preview failed: " + err.message + ">";
    }
  }

  function textPreview(bufferLike, maxBytes) {
    var maxLen = maxBytes || probe.maxPreviewBytes;
    try {
      if (typeof bufferLike === "string") {
        return bufferLike.length <= maxLen ? bufferLike : bufferLike.slice(0, maxLen) + "...";
      }
      var view;
      if (bufferLike instanceof ArrayBuffer) {
        view = new Uint8Array(bufferLike, 0, Math.min(bufferLike.byteLength, maxLen));
      } else if (ArrayBuffer.isView(bufferLike)) {
        view = new Uint8Array(
          bufferLike.buffer,
          bufferLike.byteOffset,
          Math.min(bufferLike.byteLength, maxLen)
        );
      } else {
        return null;
      }
      var chars = [];
      for (var i = 0; i < view.length; i += 1) {
        if (view[i] === 0) break;
        chars.push(String.fromCharCode(view[i]));
      }
      return chars.join("");
    } catch (err) {
      return "<text preview failed: " + err.message + ">";
    }
  }

  function describeImports(importObject) {
    var result = {};
    if (!importObject || typeof importObject !== "object") return result;
    Object.keys(importObject).forEach(function describeNamespace(ns) {
      var scope = importObject[ns];
      if (!scope || typeof scope !== "object") {
        result[ns] = describeObject(scope);
        return;
      }
      result[ns] = Object.keys(scope).slice(0, 512);
    });
    return result;
  }

  function shouldTraceImport(ns, name) {
    var key = (ns + "." + name).toLowerCase();
    return (
      key.indexOf("websocket") !== -1 ||
      key.indexOf("socket") !== -1 ||
      key.indexOf("filesystem") !== -1 ||
      key.indexOf("file_system") !== -1 ||
      key.indexOf("idbfs") !== -1 ||
      key.indexOf("syncfs") !== -1 ||
      key.indexOf("sendmessage") !== -1 ||
      key.indexOf("webrequest") !== -1
    );
  }

  function sanitizeArg(value) {
    if (typeof value === "bigint") return value.toString() + "n";
    if (typeof value === "number" || typeof value === "string" || typeof value === "boolean") return value;
    return describeObject(value);
  }

  function latestMemoryBuffer() {
    var memory = probe.latestMemory && probe.latestMemory();
    return memory && memory.buffer;
  }

  function memoryPreviewAt(ptr, maxBytes) {
    var buffer = latestMemoryBuffer();
    if (!buffer || typeof ptr !== "number" || !Number.isInteger(ptr)) return null;
    if (ptr <= 0 || ptr >= buffer.byteLength) return null;
    var limit = Math.min(maxBytes || probe.maxPreviewBytes, buffer.byteLength - ptr);
    if (limit <= 0) return null;
    try {
      var view = new Uint8Array(buffer, ptr, limit);
      return {
        ptr: ptr,
        bytes: limit,
        hex: bytesPreview(view, limit),
        text: textPreview(view, limit)
      };
    } catch (err) {
      return { ptr: ptr, error: err.message };
    }
  }

  function pointerPreviews(args) {
    var previews = [];
    Array.prototype.slice.call(args, 0, 8).forEach(function previewArg(value, argIndex) {
      var preview = memoryPreviewAt(value, 160);
      if (preview) {
        preview.argIndex = argIndex;
        previews.push(preview);
      }
    });
    return previews;
  }

  function wrapImportObject(importObject) {
    if (!importObject || typeof importObject !== "object") return importObject;
    Object.keys(importObject).forEach(function wrapNamespace(ns) {
      var scope = importObject[ns];
      if (!scope || typeof scope !== "object") return;
      Object.keys(scope).forEach(function wrapImport(name) {
        var fn = scope[name];
        if (typeof fn !== "function" || fn.__curlingProbeWrapped) return;
        if (!shouldTraceImport(ns, name)) return;
        var wrapped = function hookedImportFunction() {
          var args = Array.prototype.slice.call(arguments, 0, 16);
          pushEvent("wasm.import.call", {
            namespace: ns,
            name: name,
            argc: arguments.length,
            args: args.map(sanitizeArg),
            pointerPreviews: pointerPreviews(arguments)
          });
          return fn.apply(this, arguments);
        };
        wrapped.__curlingProbeWrapped = true;
        scope[name] = wrapped;
      });
    });
    return importObject;
  }

  function recordInstance(instance, source) {
    if (!instance || !instance.exports) {
      pushEvent("wasm.instance.no_exports", { source: source, value: describeObject(instance) });
      return instance;
    }

    var exports = instance.exports;
    var exportKeys = Object.keys(exports);
    var memoryKeys = [];
    var tableKeys = [];

    exportKeys.forEach(function inspectExport(key) {
      var value = exports[key];
      if (value instanceof WebAssembly.Memory) {
        memoryKeys.push(key);
        probe.memories.push({ source: source, key: key, memory: value });
      } else if (value instanceof WebAssembly.Table) {
        tableKeys.push(key);
        probe.tables.push({ source: source, key: key, table: value });
      }
    });

    probe.instances.push({ source: source, instance: instance, exports: exportKeys });
    pushEvent("wasm.instance", {
      source: source,
      exports: exportKeys,
      memories: memoryKeys,
      tables: tableKeys
    });
    if (probe.autoCookedHullHook && !probe._cookedHullHookAttempted && probe.tables.length) {
      probe._cookedHullHookAttempted = true;
      if (typeof probe.installCookedHullHook === "function") {
        probe.installCookedHullHook();
      } else {
        pushEvent("table_hook.failed", {
          index: 122108,
          name: "QuickHullConvexHullLib.fillConvexMeshDesc",
          reason: "installCookedHullHook unavailable"
        });
      }
    }
    return instance;
  }

  function normalizeInstantiateResult(result, source) {
    if (result && result.instance) {
      recordInstance(result.instance, source);
    } else {
      recordInstance(result, source);
    }
    return result;
  }

  function hookWebAssembly() {
    if (!global.WebAssembly || probe._webAssemblyHooked) return;
    probe._webAssemblyHooked = true;

    var originalInstantiate = WebAssembly.instantiate;
    if (typeof originalInstantiate === "function") {
      WebAssembly.instantiate = function hookedInstantiate(bufferSource, importObject) {
        pushEvent("wasm.instantiate.call", {
          buffer: describeObject(bufferSource),
          imports: describeObject(importObject),
          importKeys: describeImports(importObject)
        });
        wrapImportObject(importObject);
        return originalInstantiate.apply(this, arguments).then(function onInstantiate(result) {
          return normalizeInstantiateResult(result, "WebAssembly.instantiate");
        });
      };
    }

    var originalInstantiateStreaming = WebAssembly.instantiateStreaming;
    if (typeof originalInstantiateStreaming === "function") {
      WebAssembly.instantiateStreaming = function hookedInstantiateStreaming(source, importObject) {
        pushEvent("wasm.instantiateStreaming.call", {
          source: describeObject(source),
          imports: describeObject(importObject),
          importKeys: describeImports(importObject)
        });
        wrapImportObject(importObject);
        return originalInstantiateStreaming.apply(this, arguments).then(function onStreaming(result) {
          return normalizeInstantiateResult(result, "WebAssembly.instantiateStreaming");
        });
      };
    }
  }

  function hookCreateUnityInstance() {
    if (probe._createUnityHooked) return;
    probe._createUnityHooked = true;

    var descriptor = Object.getOwnPropertyDescriptor(global, "createUnityInstance");
    if (descriptor && typeof descriptor.value === "function") {
      wrapCreateUnityInstance(descriptor.value);
      return;
    }

    var pendingValue;
    Object.defineProperty(global, "createUnityInstance", {
      configurable: true,
      enumerable: true,
      get: function getCreateUnityInstance() {
        return pendingValue;
      },
      set: function setCreateUnityInstance(value) {
        pendingValue = value;
        if (typeof value === "function") {
          wrapCreateUnityInstance(value);
        }
      }
    });
  }

  function wrapCreateUnityInstance(fn) {
    if (fn && fn.__curlingProbeWrapped) return;
    var wrapped = function hookedCreateUnityInstance(canvas, config, onProgress) {
      pushEvent("unity.create.call", {
        canvas: describeObject(canvas),
        configKeys: config ? Object.keys(config) : [],
        companyName: config && config.companyName,
        productName: config && config.productName,
        productVersion: config && config.productVersion,
        dataUrl: config && config.dataUrl,
        frameworkUrl: config && config.frameworkUrl,
        codeUrl: config && config.codeUrl,
        streamingAssetsUrl: config && config.streamingAssetsUrl
      });
      var result = fn.apply(this, arguments);
      if (result && typeof result.then === "function") {
        return result.then(function onUnityInstance(unityInstance) {
          probe.unityInstance = unityInstance;
          pushEvent("unity.create.result", {
            instance: describeObject(unityInstance),
            module: describeObject(unityInstance && unityInstance.Module)
          });
          probe.scanAndHookFS();
          return unityInstance;
        });
      }
      probe.unityInstance = result;
      pushEvent("unity.create.result", { instance: describeObject(result) });
      probe.scanAndHookFS();
      return result;
    };
    wrapped.__curlingProbeWrapped = true;
    global.createUnityInstance = wrapped;
  }

  function hookWebSocket() {
    if (!global.WebSocket || probe._webSocketHooked) return;
    probe._webSocketHooked = true;

    var OriginalWebSocket = global.WebSocket;
    var HookedWebSocket = function HookedWebSocket(url, protocols) {
      var socket = protocols === undefined
        ? new OriginalWebSocket(url)
        : new OriginalWebSocket(url, protocols);

      pushEvent("websocket.opening", { url: String(url), protocols: protocols || null });

      socket.addEventListener("open", function onOpen() {
        pushEvent("websocket.open", { url: String(url) });
      });
      socket.addEventListener("close", function onClose(event) {
        pushEvent("websocket.close", {
          url: String(url),
          code: event.code,
          reason: event.reason,
          wasClean: event.wasClean
        });
      });
      socket.addEventListener("error", function onError(event) {
        pushEvent("websocket.error", { url: String(url), event: describeObject(event) });
      });
      socket.addEventListener("message", function onMessage(event) {
        pushEvent("websocket.recv", {
          url: String(url),
          dataType: typeof event.data,
          dataPreview: bytesPreview(event.data),
          textPreview: textPreview(event.data)
        });
      });

      var originalSend = socket.send;
      socket.send = function hookedSend(data) {
        pushEvent("websocket.send", {
          url: String(url),
          dataType: typeof data,
          dataPreview: bytesPreview(data),
          textPreview: textPreview(data)
        });
        return originalSend.apply(this, arguments);
      };
      return socket;
    };

    HookedWebSocket.prototype = OriginalWebSocket.prototype;
    HookedWebSocket.CONNECTING = OriginalWebSocket.CONNECTING;
    HookedWebSocket.OPEN = OriginalWebSocket.OPEN;
    HookedWebSocket.CLOSING = OriginalWebSocket.CLOSING;
    HookedWebSocket.CLOSED = OriginalWebSocket.CLOSED;
    global.WebSocket = HookedWebSocket;
  }

  function findLikelyModules() {
    var modules = [];
    ["Module", "unityFramework", "unityInstance"].forEach(function inspectGlobal(key) {
      try {
        var value = global[key];
        if (value) modules.push({ key: key, module: value.Module || value });
      } catch (err) {
        pushEvent("module.inspect_error", { key: key, error: err.message });
      }
    });

    if (probe.unityInstance) {
      modules.push({ key: "probe.unityInstance", module: probe.unityInstance.Module || probe.unityInstance });
    }
    return modules;
  }

  function wrapMethod(owner, name, eventType, formatter) {
    if (!owner || typeof owner[name] !== "function") return false;
    if (owner[name].__curlingProbeWrapped) return true;

    var original = owner[name];
    owner[name] = function wrappedMethod() {
      var payload = {};
      try {
        payload = formatter ? formatter(arguments) : { args: Array.prototype.slice.call(arguments) };
      } catch (err) {
        payload = { formatterError: err.message };
      }
      pushEvent(eventType, payload);
      return original.apply(this, arguments);
    };
    owner[name].__curlingProbeWrapped = true;
    return true;
  }

  probe.scanAndHookFS = function scanAndHookFS() {
    var hooked = [];
    findLikelyModules().forEach(function inspectModule(entry) {
      var module = entry.module;
      var fs = module && (module.FS || module.filesystem || module.FS_createDataFile && module);
      if (!fs) return;

      [
        ["writeFile", "fs.writeFile"],
        ["readFile", "fs.readFile"],
        ["mkdir", "fs.mkdir"],
        ["mkdirTree", "fs.mkdirTree"],
        ["unlink", "fs.unlink"],
        ["rmdir", "fs.rmdir"],
        ["syncfs", "fs.syncfs"]
      ].forEach(function hookItem(item) {
        var ok = wrapMethod(fs, item[0], item[1], function formatFS(args) {
          return {
            module: entry.key,
            path: args[0],
            argCount: args.length,
            dataPreview: args.length > 1 ? bytesPreview(args[1]) : null
          };
        });
        if (ok) hooked.push(entry.key + "." + item[0]);
      });
    });
    pushEvent("fs.scan", { hooked: hooked });
    return hooked;
  };

  probe.installTableHook = function installTableHook(index, name, options) {
    var opts = options || {};
    var signature = opts.signature || "vii";
    var tableRecord = opts.tableRecord || probe.tables[probe.tables.length - 1];
    if (!tableRecord || !tableRecord.table) {
      pushEvent("table_hook.failed", { index: index, name: name, reason: "no table captured" });
      return null;
    }

    var table = tableRecord.table;
    var original;
    try {
      original = table.get(index);
    } catch (err) {
      pushEvent("table_hook.failed", { index: index, name: name, reason: err.message });
      return null;
    }
    if (typeof original !== "function") {
      pushEvent("table_hook.failed", { index: index, name: name, reason: "entry is not a function" });
      return null;
    }

    var hookRecord = {
      index: index,
      name: name || ("wasm.table[" + index + "]"),
      tableRecord: tableRecord,
      original: original,
      calls: 0
    };

    var wrapper = function hookedWasmTableFunction() {
      var args = Array.prototype.slice.call(arguments, 0, 16);
      hookRecord.calls += 1;
      if (typeof opts.beforeCall === "function") {
        try {
          opts.beforeCall(arguments, hookRecord);
        } catch (beforeErr) {
          pushEvent("table_hook.before_failed", {
            index: index,
            name: hookRecord.name,
            reason: beforeErr.message
          });
        }
      }
      if (opts.traceCallEvent !== false) {
        pushEvent("wasm.table.call", {
          index: index,
          name: hookRecord.name,
          signature: signature,
          argc: arguments.length,
          args: args.slice(0, 12)
        });
      }
      var result = original.apply(this, arguments);
      if (typeof opts.afterCall === "function") {
        try {
          opts.afterCall(arguments, result, hookRecord);
        } catch (afterErr) {
          pushEvent("table_hook.after_failed", {
            index: index,
            name: hookRecord.name,
            reason: afterErr.message
          });
        }
      }
      return result;
    };

    var wasmCallable = makeWasmCallable(wrapper, signature, table);
    if (!wasmCallable || !wasmCallable.fn) {
      pushEvent("table_hook.failed", {
        index: index,
        name: name,
        signature: signature,
        reason: wasmCallable && wasmCallable.reason ? wasmCallable.reason : "no wasm callable factory available"
      });
      return null;
    }

    try {
      table.set(index, wasmCallable.fn);
    } catch (err2) {
      pushEvent("table_hook.failed", {
        index: index,
        name: name,
        signature: signature,
        strategy: wasmCallable.strategy,
        reason: err2.message
      });
      return null;
    }

    probe.hooks.push(hookRecord);
    pushEvent("table_hook.installed", {
      index: index,
      name: hookRecord.name,
      signature: signature,
      strategy: wasmCallable.strategy,
      tableSource: tableRecord.source,
      tableKey: tableRecord.key
    });
    return hookRecord;
  };

  function wasmTypeFromSignatureChar(ch) {
    if (ch === "i") return "i32";
    if (ch === "j") return "i64";
    if (ch === "f") return "f32";
    if (ch === "d") return "f64";
    return null;
  }

  function wasmFunctionType(signature) {
    var sig = signature || "vii";
    var resultType = wasmTypeFromSignatureChar(sig.charAt(0));
    var params = [];
    for (var i = 1; i < sig.length; i += 1) {
      var paramType = wasmTypeFromSignatureChar(sig.charAt(i));
      if (!paramType) return null;
      params.push(paramType);
    }
    return {
      parameters: params,
      results: resultType ? [resultType] : []
    };
  }

  function findAddFunction() {
    var candidates = [];
    findLikelyModules().forEach(function collectModule(entry) {
      if (entry.module && typeof entry.module.addFunction === "function") {
        candidates.push({ key: entry.key, fn: entry.module.addFunction });
      }
    });
    if (typeof global.addFunction === "function") {
      candidates.push({ key: "global.addFunction", fn: global.addFunction });
    }
    return candidates[0] || null;
  }

  function makeWasmCallable(wrapper, signature, table) {
    var type = wasmFunctionType(signature);
    if (!type) {
      return { reason: "unsupported signature: " + signature };
    }

    try {
      if (typeof WebAssembly.Function === "function") {
        return {
          strategy: "WebAssembly.Function",
          fn: new WebAssembly.Function(type, wrapper)
        };
      }
    } catch (err) {
      pushEvent("table_hook.factory_failed", {
        strategy: "WebAssembly.Function",
        signature: signature,
        reason: err.message
      });
    }

    try {
      return {
        strategy: "imported-wasm-wrapper",
        fn: convertJsFunctionToWasm(wrapper, signature)
      };
    } catch (err3) {
      pushEvent("table_hook.factory_failed", {
        strategy: "imported-wasm-wrapper",
        signature: signature,
        reason: err3.message
      });
    }

    var addFunction = findAddFunction();
    if (addFunction) {
      try {
        var allocatedIndex = addFunction.fn(wrapper, signature);
        var allocatedFn = table.get(allocatedIndex);
        return {
          strategy: "addFunction:" + addFunction.key,
          fn: allocatedFn,
          allocatedIndex: allocatedIndex
        };
      } catch (err2) {
        pushEvent("table_hook.factory_failed", {
          strategy: "addFunction:" + addFunction.key,
          signature: signature,
          reason: err2.message
        });
      }
    }

    return { reason: "WebAssembly.Function/addFunction unavailable" };
  }

  function encodeULEB(value) {
    var out = [];
    var remaining = value >>> 0;
    do {
      var byte = remaining & 0x7f;
      remaining >>>= 7;
      if (remaining !== 0) byte |= 0x80;
      out.push(byte);
    } while (remaining !== 0);
    return out;
  }

  function encodeString(value) {
    var out = encodeULEB(value.length);
    for (var i = 0; i < value.length; i += 1) {
      out.push(value.charCodeAt(i));
    }
    return out;
  }

  function appendSection(bytes, sectionId, payload) {
    bytes.push(sectionId);
    Array.prototype.push.apply(bytes, encodeULEB(payload.length));
    Array.prototype.push.apply(bytes, payload);
  }

  function valTypeCode(typeName) {
    if (typeName === "i32") return 0x7f;
    if (typeName === "i64") return 0x7e;
    if (typeName === "f32") return 0x7d;
    if (typeName === "f64") return 0x7c;
    throw new Error("unsupported wasm value type: " + typeName);
  }

  function convertJsFunctionToWasm(fn, signature) {
    var type = wasmFunctionType(signature);
    if (!type) throw new Error("unsupported signature: " + signature);
    var bytes = [0x00, 0x61, 0x73, 0x6d, 0x01, 0x00, 0x00, 0x00];
    var typePayload = [0x01, 0x60, type.parameters.length];
    type.parameters.forEach(function appendParam(param) {
      typePayload.push(valTypeCode(param));
    });
    typePayload.push(type.results.length);
    type.results.forEach(function appendResult(result) {
      typePayload.push(valTypeCode(result));
    });
    appendSection(bytes, 1, typePayload);

    var importPayload = [0x01];
    Array.prototype.push.apply(importPayload, encodeString("e"));
    Array.prototype.push.apply(importPayload, encodeString("f"));
    importPayload.push(0x00, 0x00);
    appendSection(bytes, 2, importPayload);

    var exportPayload = [0x01];
    Array.prototype.push.apply(exportPayload, encodeString("f"));
    exportPayload.push(0x00, 0x00);
    appendSection(bytes, 7, exportPayload);

    var module = new WebAssembly.Module(new Uint8Array(bytes));
    var instance = new WebAssembly.Instance(module, { e: { f: fn } });
    return instance.exports.f;
  }

  probe.uninstallTableHook = function uninstallTableHook(record) {
    var hookRecord = record;
    if (typeof record === "number") {
      hookRecord = probe.hooks.filter(function byIndex(hook) {
        return hook.index === record;
      }).slice(-1)[0];
    }
    if (!hookRecord) return false;
    hookRecord.tableRecord.table.set(hookRecord.index, hookRecord.original);
    pushEvent("table_hook.uninstalled", {
      index: hookRecord.index,
      name: hookRecord.name,
      calls: hookRecord.calls
    });
    return true;
  };

  probe.installKnownCurlingHooks = function installKnownCurlingHooks() {
    return probe.knownFunctionIndices.map(function installKnown(item) {
      return probe.installTableHook(item.index, item.name, { signature: item.signature });
    }).filter(Boolean);
  };

  probe.latestMemory = function latestMemory() {
    var record = probe.memories[probe.memories.length - 1];
    return record && record.memory;
  };

  probe.readCString = function readCString(ptr, maxLen) {
    var memory = probe.latestMemory();
    if (!memory) return null;
    var view = new Uint8Array(memory.buffer);
    var limit = Math.min(view.length, ptr + (maxLen || 4096));
    var chars = [];
    for (var i = ptr; i < limit && view[i] !== 0; i += 1) {
      chars.push(String.fromCharCode(view[i]));
    }
    return chars.join("");
  };

  probe.readF32 = function readF32(ptr, count) {
    var memory = probe.latestMemory();
    if (!memory) return null;
    var view = new Float32Array(memory.buffer, ptr, count);
    return Array.prototype.slice.call(view);
  };

  probe.readU32 = function readU32(ptr, count) {
    var memory = probe.latestMemory();
    if (!memory) return null;
    var view = new Uint32Array(memory.buffer, ptr, count);
    return Array.prototype.slice.call(view);
  };

  function dataView() {
    var memory = probe.latestMemory();
    if (!memory) return null;
    return new DataView(memory.buffer);
  }

  function inMemoryRange(view, ptr, byteLength) {
    return (
      view &&
      typeof ptr === "number" &&
      Number.isInteger(ptr) &&
      ptr > 0 &&
      byteLength >= 0 &&
      ptr + byteLength <= view.byteLength
    );
  }

  function readU16LE(view, ptr) {
    return view.getUint16(ptr, true);
  }

  function readU32LE(view, ptr) {
    return view.getUint32(ptr, true);
  }

  function readF32LE(view, ptr) {
    return view.getFloat32(ptr, true);
  }

  function readBytesArray(view, ptr, count) {
    if (!inMemoryRange(view, ptr, count)) return null;
    var bytes = new Uint8Array(view.buffer, ptr, count);
    return Array.prototype.slice.call(bytes);
  }

  function cleanFloatValue(value) {
    if (Number.isNaN(value)) return "NaN";
    if (value === Infinity) return "Infinity";
    if (value === -Infinity) return "-Infinity";
    return value;
  }

  function readU32Preview(view, ptr, count) {
    var out = [];
    var limit = Math.min(count || 32, Math.floor((view.byteLength - ptr) / 4));
    for (var i = 0; i < limit; i += 1) {
      out.push(readU32LE(view, ptr + i * 4));
    }
    return out;
  }

  function readF32Preview(view, ptr, count) {
    var out = [];
    var limit = Math.min(count || 32, Math.floor((view.byteLength - ptr) / 4));
    for (var i = 0; i < limit; i += 1) {
      out.push(cleanFloatValue(readF32LE(view, ptr + i * 4)));
    }
    return out;
  }

  function isPointerLike(view, value, minBytes) {
    return (
      view &&
      typeof value === "number" &&
      Number.isInteger(value) &&
      value > 0 &&
      value + (minBytes || 4) <= view.byteLength
    );
  }

  function decodeContactBufferCandidate(view, ptr, maxContacts) {
    var totalBytes = 4112;
    if (!inMemoryRange(view, ptr, totalBytes)) return null;
    var count = readU32LE(view, ptr + 4096);
    if (count > 64) return null;

    var contacts = [];
    var limit = Math.min(count, maxContacts || 8);
    for (var i = 0; i < limit; i += 1) {
      var cp = ptr + i * 64;
      contacts.push({
        normal: [readF32LE(view, cp), readF32LE(view, cp + 4), readF32LE(view, cp + 8)].map(cleanFloatValue),
        separation: cleanFloatValue(readF32LE(view, cp + 12)),
        point: [readF32LE(view, cp + 16), readF32LE(view, cp + 20), readF32LE(view, cp + 24)].map(cleanFloatValue),
        maxImpulse: cleanFloatValue(readF32LE(view, cp + 28)),
        targetVel: [readF32LE(view, cp + 32), readF32LE(view, cp + 36), readF32LE(view, cp + 40)].map(cleanFloatValue),
        staticFriction: cleanFloatValue(readF32LE(view, cp + 44)),
        materialFlags: view.getUint8(cp + 48),
        forInternalUse: readU16LE(view, cp + 50),
        internalFaceIndex1: readU32LE(view, cp + 52),
        dynamicFriction: cleanFloatValue(readF32LE(view, cp + 56)),
        restitution: cleanFloatValue(readF32LE(view, cp + 60))
      });
    }

    return {
      layout: "Gu::ContactBuffer",
      countOffset: 4096,
      count: count,
      contactsPreview: contacts
    };
  }

  function pointerTargetsInWindow(view, label, ptr, byteLength, options) {
    var opts = options || {};
    var targets = [];
    var seen = {};
    var scanBytes = Math.min(byteLength, opts.pointerScanBytes || 512);
    var maxTargets = opts.maxNestedPointers || 24;
    for (var offset = 0; offset + 4 <= scanBytes && targets.length < maxTargets; offset += 4) {
      var candidate = readU32LE(view, ptr + offset);
      if (!isPointerLike(view, candidate, 4)) continue;
      if (seen[candidate]) continue;
      seen[candidate] = true;
      var nestedBytes = Math.min(
        opts.nestedBytes || 512,
        view.byteLength - candidate
      );
      var nested = probe.dumpMemoryWindow(
        label + ".pointee@" + offset,
        candidate,
        nestedBytes,
        {
          includeRawBytes: opts.includeNestedRawBytes === true,
          includePointers: false,
          previewBytes: opts.previewBytes || 192,
          u32PreviewCount: opts.nestedU32PreviewCount || 32,
          f32PreviewCount: opts.nestedF32PreviewCount || 32,
          contactPreviewCount: opts.contactPreviewCount || 8
        }
      );
      nested.sourceOffset = offset;
      targets.push(nested);
    }
    return targets;
  }

  probe.dumpMemoryWindow = function dumpMemoryWindow(label, ptr, byteLength, options) {
    var opts = options || {};
    var view = dataView();
    if (!view) return { ok: false, label: label, ptr: ptr, reason: "no wasm memory" };
    var length = Math.max(0, Math.min(byteLength || probe.maxPreviewBytes, view.byteLength - ptr));
    if (!inMemoryRange(view, ptr, length)) {
      return {
        ok: false,
        label: label,
        ptr: ptr,
        byteLength: byteLength,
        reason: "pointer out of wasm memory"
      };
    }

    var previewBytes = Math.min(opts.previewBytes || 256, length);
    var dump = {
      ok: true,
      label: label,
      ptr: ptr,
      byteLength: length,
      hexPreview: bytesPreview(new Uint8Array(view.buffer, ptr, previewBytes), previewBytes),
      u32Preview: readU32Preview(view, ptr, opts.u32PreviewCount || 32),
      f32Preview: readF32Preview(view, ptr, opts.f32PreviewCount || 32),
      contactBufferCandidate: decodeContactBufferCandidate(view, ptr, opts.contactPreviewCount || 8)
    };

    if (opts.includeRawBytes !== false) {
      dump.rawBytes = readBytesArray(view, ptr, length);
    }
    if (opts.includePointers !== false) {
      dump.pointerTargets = pointerTargetsInWindow(view, label, ptr, length, opts);
    }
    return dump;
  };

  probe.dumpPointerArgs = function dumpPointerArgs(argsLike, options) {
    var opts = options || {};
    var view = dataView();
    if (!view) return [];
    var args = Array.prototype.slice.call(argsLike, 0, opts.maxArgs || 12);
    var windows = [];
    args.forEach(function dumpArg(value, argIndex) {
      if (!isPointerLike(view, value, 4)) return;
      var byteLength = Math.min(opts.windowBytes || 2048, view.byteLength - value);
      var dump = probe.dumpMemoryWindow(
        (opts.labelPrefix || "arg") + argIndex,
        value,
        byteLength,
        opts
      );
      dump.argIndex = argIndex;
      dump.argValue = value;
      windows.push(dump);
    });
    return windows;
  };

  probe.armPhysXNativeCapture = function armPhysXNativeCapture(reason, armMs) {
    var duration = armMs || 2000;
    var until = nowMs() + duration;
    probe.physxNativeCapture.armedUntilMs = Math.max(
      probe.physxNativeCapture.armedUntilMs || 0,
      until
    );
    probe.physxNativeCapture.armSerial += 1;
    pushEvent("physx.native.capture_armed", {
      reason: reason,
      armMs: duration,
      armedUntilMs: probe.physxNativeCapture.armedUntilMs,
      armSerial: probe.physxNativeCapture.armSerial
    });
    return probe.physxNativeCapture;
  };

  function physxNativeCaptureIsArmed() {
    return nowMs() <= (probe.physxNativeCapture.armedUntilMs || 0);
  }

  function shouldDumpPhysXNativeTarget(target, options) {
    var opts = options || {};
    if (opts.captureMode === "always") return true;
    if (target.capture === "always" || target.capture === "arm") return true;
    return physxNativeCaptureIsArmed();
  }

  function physxNativeDumpOptions(target, options) {
    var opts = options || {};
    return {
      maxArgs: opts.maxPointerArgs || 12,
      windowBytes: opts.argWindowBytes || target.windowBytes || 4096,
      nestedBytes: opts.nestedBytes || target.nestedBytes || 1024,
      pointerScanBytes: opts.pointerScanBytes || 512,
      maxNestedPointers: opts.maxNestedPointers || 24,
      includeRawBytes: opts.includeRawBytes !== false,
      includeNestedRawBytes: opts.includeNestedRawBytes === true,
      previewBytes: opts.previewBytes || 256,
      u32PreviewCount: opts.u32PreviewCount || 48,
      f32PreviewCount: opts.f32PreviewCount || 48,
      nestedU32PreviewCount: opts.nestedU32PreviewCount || 32,
      nestedF32PreviewCount: opts.nestedF32PreviewCount || 32,
      contactPreviewCount: opts.contactPreviewCount || 8,
      labelPrefix: target.name + ".arg"
    };
  }

  function physxNativePayload(phase, target, argsLike, result, record, dumpState, options) {
    return {
      phase: phase,
      hook: {
        index: target.index,
        wasm: target.wasm,
        name: target.name,
        role: target.role,
        signature: target.signature,
        capture: target.capture
      },
      callIndex: record.calls,
      dumpIndex: dumpState.dumpIndex,
      dumpId: dumpState.dumpId,
      armSerial: dumpState.armSerial,
      armed: physxNativeCaptureIsArmed(),
      args: Array.prototype.slice.call(argsLike, 0, 16).map(sanitizeArg),
      result: phase === "after" ? sanitizeArg(result) : undefined,
      pointerWindows: probe.dumpPointerArgs(argsLike, physxNativeDumpOptions(target, options))
    };
  }

  function installPhysXNativeTarget(target, options) {
    var opts = options || {};
    return probe.installTableHook(target.index, target.name, {
      signature: target.signature,
      traceCallEvent: opts.traceTableCalls === true,
      beforeCall: function beforePhysXNativeCall(args, record) {
        if (target.capture === "arm") {
          probe.armPhysXNativeCapture(target.name, opts.armMs || 2000);
        }
        if (!shouldDumpPhysXNativeTarget(target, opts)) {
          record.__physxNativeDump = null;
          return;
        }
        var maxDumps = opts.maxDumpsPerHook || opts.maxCallsPerHook || 16;
        record.nativeDumpCount = record.nativeDumpCount || 0;
        if (record.nativeDumpCount >= maxDumps) {
          record.__physxNativeDump = null;
          return;
        }
        record.nativeDumpCount += 1;
        record.__physxNativeDump = {
          dumpIndex: record.nativeDumpCount,
          armSerial: probe.physxNativeCapture.armSerial,
          dumpId: target.wasm + "#" + record.calls + "/" + record.nativeDumpCount
        };
        pushEvent(
          "physx.native.before",
          physxNativePayload("before", target, args, undefined, record, record.__physxNativeDump, opts)
        );
      },
      afterCall: function afterPhysXNativeCall(args, result, record) {
        var dumpState = record.__physxNativeDump;
        if (!dumpState) return;
        pushEvent(
          "physx.native.after",
          physxNativePayload("after", target, args, result, record, dumpState, opts)
        );
        record.__physxNativeDump = null;
      }
    });
  }

  probe.installPhysXNativeHooks = function installPhysXNativeHooks(options) {
    var opts = options || {};
    var targets = opts.targets || probe.physxNativeHookTargets;
    var installed = [];
    targets.forEach(function installTarget(target) {
      if (opts.indices && opts.indices.indexOf(target.index) === -1) return;
      if (opts.names && opts.names.indexOf(target.name) === -1) return;
      var existing = probe.hooks.filter(function sameIndex(hook) {
        return hook.index === target.index && hook.name === target.name;
      }).slice(-1)[0];
      if (existing && !opts.reinstall) {
        installed.push(existing);
        return;
      }
      if (existing && opts.reinstall) probe.uninstallTableHook(existing);
      var hook = installPhysXNativeTarget(target, opts);
      if (hook) installed.push(hook);
    });
    pushEvent("physx.native.hooks_installed", {
      count: installed.length,
      targets: installed.map(function summarizeHook(hook) {
        return { index: hook.index, name: hook.name };
      })
    });
    return installed;
  };

  probe.dumpCookedHullDesc = function dumpCookedHullDesc(descPtr, hullLibPtr) {
    var view = dataView();
    if (!view) return { ok: false, reason: "no wasm memory" };
    if (!inMemoryRange(view, descPtr, 36)) {
      return { ok: false, reason: "desc pointer out of range", descPtr: descPtr };
    }

    var pointsStride = readU32LE(view, descPtr + 0);
    var pointsData = readU32LE(view, descPtr + 4);
    var pointsCount = readU32LE(view, descPtr + 8);
    var polygonsStride = readU32LE(view, descPtr + 12);
    var polygonsData = readU32LE(view, descPtr + 16);
    var polygonsCount = readU32LE(view, descPtr + 20);
    var indicesStride = readU32LE(view, descPtr + 24);
    var indicesData = readU32LE(view, descPtr + 28);
    var indicesCount = readU32LE(view, descPtr + 32);

    var header = {
      descPtr: descPtr,
      hullLibPtr: hullLibPtr,
      points: { stride: pointsStride, data: pointsData, count: pointsCount },
      polygons: { stride: polygonsStride, data: polygonsData, count: polygonsCount },
      indices: { stride: indicesStride, data: indicesData, count: indicesCount }
    };

    var sanity = [];
    if (pointsStride !== 12) sanity.push("points.stride != 12");
    if (polygonsStride !== 20) sanity.push("polygons.stride != 20");
    if (indicesStride !== 4) sanity.push("indices.stride != 4");
    if (pointsCount <= 0 || pointsCount >= 256) sanity.push("points.count outside expected cooked range");
    if (polygonsCount <= 0 || polygonsCount > 512) sanity.push("polygons.count outside expected range");
    if (indicesCount <= 0 || indicesCount > 4096) sanity.push("indices.count outside expected range");
    if (!inMemoryRange(view, pointsData, pointsCount * pointsStride)) sanity.push("points.data out of range");
    if (!inMemoryRange(view, polygonsData, polygonsCount * polygonsStride)) sanity.push("polygons.data out of range");
    if (!inMemoryRange(view, indicesData, indicesCount * indicesStride)) sanity.push("indices.data out of range");

    if (sanity.length) {
      return {
        ok: false,
        reason: "sanity check failed",
        sanity: sanity,
        header: header
      };
    }

    var vertices = [];
    for (var vi = 0; vi < pointsCount; vi += 1) {
      var vp = pointsData + vi * pointsStride;
      vertices.push([readF32LE(view, vp), readF32LE(view, vp + 4), readF32LE(view, vp + 8)]);
    }

    var polygons = [];
    for (var pi = 0; pi < polygonsCount; pi += 1) {
      var pp = polygonsData + pi * polygonsStride;
      polygons.push({
        plane: [
          readF32LE(view, pp),
          readF32LE(view, pp + 4),
          readF32LE(view, pp + 8),
          readF32LE(view, pp + 12)
        ],
        nbVerts: readU16LE(view, pp + 16),
        indexBase: readU16LE(view, pp + 18)
      });
    }

    var indices = [];
    for (var ii = 0; ii < indicesCount; ii += 1) {
      indices.push(readU32LE(view, indicesData + ii * indicesStride));
    }

    return {
      ok: true,
      header: header,
      vertices: vertices,
      polygons: polygons,
      indices: indices,
      raw: {
        pointsBytes: readBytesArray(view, pointsData, pointsCount * pointsStride),
        polygonsBytes: readBytesArray(view, polygonsData, polygonsCount * polygonsStride),
        indicesBytes: readBytesArray(view, indicesData, indicesCount * indicesStride)
      }
    };
  };

  probe.installCookedHullHook = function installCookedHullHook(options) {
    var opts = options || {};
    var index = opts.index || 122108; // QuickHullConvexHullLib::fillConvexMeshDesc / func72915
    return probe.installTableHook(index, "QuickHullConvexHullLib.fillConvexMeshDesc", {
      signature: "vii",
      afterCall: function afterFillConvexMeshDesc(args) {
        var hullLibPtr = args[0];
        var descPtr = args[1];
        var dump = probe.dumpCookedHullDesc(descPtr, hullLibPtr);
        pushEvent("physx.cooked_hull.desc", dump);
        if (dump.ok) {
          console.log(
            "[curlingProbe] cooked hull desc",
            "vertices=" + dump.vertices.length,
            "polygons=" + dump.polygons.length,
            "indices=" + dump.indices.length
          );
        } else {
          console.warn("[curlingProbe] cooked hull desc dump failed", dump.reason, dump);
        }
      }
    });
  };

  probe.downloadEvents = function downloadEvents(filename) {
    var content = JSON.stringify({
      installedAt: probe.installedAt,
      exportedAt: new Date().toISOString(),
      events: probe.events
    }, null, 2);
    var blob = new Blob([content], { type: "application/json" });
    var link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    link.download = filename || "curling_runtime_probe_events.json";
    document.body.appendChild(link);
    link.click();
    setTimeout(function cleanupDownload() {
      URL.revokeObjectURL(link.href);
      link.remove();
    }, 0);
  };

  global.__curlingProbe = probe;
  hookWebAssembly();
  hookCreateUnityInstance();
  hookWebSocket();
  pushEvent("probe.installed", { userAgent: global.navigator && global.navigator.userAgent });
  console.log(
    "[curlingProbe] installed. Use __curlingProbe.installKnownCurlingHooks() or " +
    "__curlingProbe.installPhysXNativeHooks() after Unity loads."
  );
})(typeof window !== "undefined" ? window : globalThis);
