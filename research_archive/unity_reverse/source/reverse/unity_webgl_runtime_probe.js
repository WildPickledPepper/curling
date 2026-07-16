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
 * The probe records runtime evidence only by default.  The optional
 * resetAllStoneRotations mode is an explicit sampling-only mutation: it
 * restores a captured startup quaternion after RESETPOSITION.
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
    eventSinkUrl: global.__curlingProbeConfig && global.__curlingProbeConfig.eventSinkUrl,
    // A 12-shot batch produces thousands of passive observations.  Sending
    // each one in a standalone fetch leaves an unbounded request backlog, so
    // preserve individual events but deliver them to the JSONL sink in order
    // in small batches.
    eventSinkQueue: [],
    eventSinkFlushTimer: null,
    eventSinkFlushActive: false,
    // The wire protocol intentionally omits Rigidbody quaternion on
    // RESETPOSITION.  Keep the most recent reset/release pair so the optional
    // A10 hook can attach the native pose observed at that release boundary.
    protocolMessageSerial: 0,
    lastResetProtocol: null,
    pendingReleaseProtocol: null,
    storeEvents: !(
      global.__curlingProbeConfig &&
      global.__curlingProbeConfig.storeEvents === false
    ),
    autoCookedHullHook: !!(
      global.__curlingProbeConfig &&
      global.__curlingProbeConfig.autoCookedHullHook
    ),
    knownFunctionIndices: [
      { index: 10894, name: "CurlingStoneNew.Start", signature: "vii" },
      {
        index: 10896,
        name: "CurlingStoneNew.OnCollisionEnter",
        signature: "viii",
        dumpPointerArgs: {
          labelPrefix: "OnCollisionEnter.arg",
          maxArgs: 3,
          windowBytes: 256,
          previewBytes: 128,
          includeRawBytes: true,
          includePointers: false
        }
      },
      { index: 12126, name: "ExtendedColliders3D.Awake", signature: "vii" },
      { index: 10660, name: "AutoDCP.HandleMessage", signature: "viii" },
      { index: 10932, name: "DCP.HandleMessage", signature: "viii" },
      { index: 11172, name: "FastDCP.CopyGameState", signature: "vii" },
      { index: 11203, name: "FastDCP.Update", signature: "vii" }
    ],
    gameObjectActivationHook: {
      index: 129063,
      name: "UnityEngine.GameObject.SetActive",
      signature: "vii",
      role: "engine hierarchy/component activation dispatcher"
    },
    meshColliderActivationHook: {
      index: 122045,
      name: "MeshCollider.activationFlush",
      signature: "viiii",
      role: "func73295/f_bkdd: MeshCollider slot44 activation callback"
    },
    meshColliderTransformRefreshHook: {
      index: 122156,
      name: "MeshCollider.transformRefresh",
      signature: "vii",
      role: "func72952/f_wwcd: MeshCollider slot43 shape-transform refresh"
    },
    meshColliderStateRefreshHook: {
      index: 122155,
      name: "MeshCollider.stateRefresh",
      signature: "vi",
      role: "func72949/f_twcd: MeshCollider slot42 collider-state refresh"
    },
    overlapCreatedHook: {
      index: 120736,
      name: "ScScene.OnOverlapCreatedTask",
      signature: "vi",
      role: "func71504: broadphase overlap -> ShapeInteraction/contact-manager creation"
    },
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
        role: "stone-rink or stone-mesh PCM ContactBuffer producer",
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
      },
      {
        index: 120346,
        wasm: "func71040",
        name: "solveContactBlock",
        signature: "viii",
        role: "single-pair dynamic-dynamic contact solver batch wrapper",
        capture: "whenArmed",
        windowBytes: 2048,
        nestedBytes: 1024
      },
      {
        index: 120348,
        wasm: "func71043",
        name: "solveContact_BStaticBlock",
        signature: "viii",
        role: "single-pair static-body contact solver batch wrapper",
        capture: "whenArmed",
        windowBytes: 2048,
        nestedBytes: 1024
      },
      {
        index: 120349,
        wasm: "func70916",
        name: "solveContact4Block",
        signature: "viii",
        role: "4-wide dynamic contact solver batch wrapper",
        capture: "whenArmed",
        windowBytes: 2048,
        nestedBytes: 1024
      },
      {
        index: 120350,
        wasm: "func70918",
        name: "solveContact4StaticBlock",
        signature: "viii",
        role: "4-wide static-body contact solver batch wrapper",
        capture: "whenArmed",
        windowBytes: 2048,
        nestedBytes: 1024
      },
      {
        index: 120352,
        wasm: "func71042",
        name: "solveContactBlockWithWriteback",
        signature: "viii",
        role: "single-pair dynamic-dynamic contact solver plus body writeback wrapper",
        capture: "whenArmed",
        windowBytes: 2048,
        nestedBytes: 1024
      },
      {
        index: 120354,
        wasm: "func71045",
        name: "solveContact_BStaticBlockWithWriteback",
        signature: "viii",
        role: "single-pair static-body contact solver plus body writeback wrapper",
        capture: "whenArmed",
        windowBytes: 2048,
        nestedBytes: 1024
      },
      {
        index: 120355,
        wasm: "func70922",
        name: "solveContact4BlockWithWriteback",
        signature: "viii",
        role: "4-wide dynamic contact solver plus body writeback wrapper",
        capture: "whenArmed",
        windowBytes: 2048,
        nestedBytes: 1024
      },
      {
        index: 120356,
        wasm: "func70923",
        name: "solveContact4StaticBlockWithWriteback",
        signature: "viii",
        role: "4-wide static-body contact solver plus body writeback wrapper",
        capture: "whenArmed",
        windowBytes: 2048,
        nestedBytes: 1024
      },
      {
        index: 120358,
        wasm: "func71041",
        name: "solveContactConcludeBlock",
        signature: "viii",
        role: "single-pair dynamic-dynamic contact solver consume/writeback",
        capture: "whenArmed",
        windowBytes: 2048,
        nestedBytes: 1024
      },
      {
        index: 120360,
        wasm: "func71044",
        name: "solveContact_BStaticConcludeBlock",
        signature: "viii",
        role: "single-pair static-body contact solver consume/writeback",
        capture: "whenArmed",
        windowBytes: 2048,
        nestedBytes: 1024
      },
      {
        index: 120361,
        wasm: "func70920",
        name: "solveContact4ConcludeBlock",
        signature: "viii",
        role: "4-wide dynamic contact solver consume/writeback",
        capture: "whenArmed",
        windowBytes: 2048,
        nestedBytes: 1024
      },
      {
        index: 120362,
        wasm: "func70921",
        name: "solveContact4StaticConcludeBlock",
        signature: "viii",
        role: "4-wide static-body contact solver consume/writeback",
        capture: "whenArmed",
        windowBytes: 2048,
        nestedBytes: 1024
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
    if (probe.storeEvents) {
      probe.events.push(event);
    }
    if (probe.eventSinkUrl) {
      probe.eventSinkQueue.push(event);
      if (probe.eventSinkQueue.length >= 128) {
        flushEventSink();
      } else if (!probe.eventSinkFlushTimer) {
        probe.eventSinkFlushTimer = global.setTimeout(function flushQueuedEvents() {
          probe.eventSinkFlushTimer = null;
          flushEventSink();
        }, 40);
      }
    }
    return event;
  }

  function flushEventSink() {
    if (!probe.eventSinkUrl || probe.eventSinkFlushActive || !probe.eventSinkQueue.length) return;
    if (probe.eventSinkFlushTimer) {
      global.clearTimeout(probe.eventSinkFlushTimer);
      probe.eventSinkFlushTimer = null;
    }
    var batch = probe.eventSinkQueue.splice(0, 128);
    probe.eventSinkFlushActive = true;
    try {
      global.fetch(probe.eventSinkUrl, {
        method: "POST",
        mode: "cors",
        headers: { "Content-Type": "text/plain;charset=UTF-8" },
        body: JSON.stringify(batch)
      }).catch(function ignoreSinkError() {}).then(function onSinkDone() {
        probe.eventSinkFlushActive = false;
        if (probe.eventSinkQueue.length) flushEventSink();
      });
    } catch (err) {
      probe.eventSinkFlushActive = false;
      // The sink is diagnostic only; never let it perturb Unity execution.
    }
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
        var receivedText = textPreview(event.data);
        if (typeof receivedText === "string") {
          var commandText = receivedText.replace(/\0/g, "").trim();
          if (/^RESETPOSITION(?:\s|$)/.test(commandText)) {
            probe.protocolMessageSerial += 1;
            probe.lastResetProtocol = {
              serial: probe.protocolMessageSerial,
              text: commandText,
              receivedAtMs: performance.now()
            };
          } else if (/^BESTSHOT(?:\s|$)/.test(commandText)) {
            probe.protocolMessageSerial += 1;
            probe.pendingReleaseProtocol = {
              serial: probe.protocolMessageSerial,
              text: commandText,
              receivedAtMs: performance.now(),
              reset: probe.lastResetProtocol
            };
          }
        }
        pushEvent("websocket.recv", {
          url: String(url),
          dataType: typeof event.data,
          dataPreview: bytesPreview(event.data),
          textPreview: receivedText
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
      var beforePointerWindows = null;
      if (opts.dumpPointerArgs && probe.dumpPointerArgs) {
        try {
          beforePointerWindows = probe.dumpPointerArgs(arguments, opts.dumpPointerArgs);
        } catch (dumpErr) {
          beforePointerWindows = [{ ok: false, reason: dumpErr.message }];
        }
      }
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
        var callPayload = {
          index: index,
          name: hookRecord.name,
          signature: signature,
          argc: arguments.length,
          args: args.slice(0, 12)
        };
        if (beforePointerWindows) callPayload.pointerWindowsBefore = beforePointerWindows;
        pushEvent("wasm.table.call", callPayload);
      }
      var overridden = null;
      if (typeof opts.overrideCall === "function") {
        try {
          overridden = opts.overrideCall(arguments, hookRecord);
        } catch (overrideErr) {
          pushEvent("table_hook.override_failed", {
            index: index,
            name: hookRecord.name,
            reason: overrideErr.message
          });
        }
      }
      var result = overridden && overridden.handled
        ? overridden.result : original.apply(this, arguments);
      if (opts.dumpPointerArgs && probe.dumpPointerArgs) {
        var afterPointerWindows = null;
        try {
          afterPointerWindows = probe.dumpPointerArgs(arguments, opts.dumpPointerArgs);
        } catch (dumpAfterErr) {
          afterPointerWindows = [{ ok: false, reason: dumpAfterErr.message }];
        }
        pushEvent("wasm.table.call.after", {
          index: index,
          name: hookRecord.name,
          signature: signature,
          argc: arguments.length,
          args: args.slice(0, 12),
          result: sanitizeArg(result),
          pointerWindowsAfter: afterPointerWindows
        });
      }
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
      return probe.installTableHook(item.index, item.name, {
        signature: item.signature,
        dumpPointerArgs: item.dumpPointerArgs
      });
    }).filter(Boolean);
  };

  probe.installGameObjectActivationHook = function installGameObjectActivationHook(options) {
    var opts = options || {};
    var target = probe.gameObjectActivationHook;
    var existing = probe.hooks.filter(function sameActivationHook(hook) {
      return hook.index === target.index && hook.name === target.name;
    }).slice(-1)[0];
    if (existing && !opts.reinstall) return existing;
    if (existing) probe.uninstallTableHook(existing);

    return probe.installTableHook(target.index, target.name, {
      signature: target.signature,
      beforeCall: function beforeGameObjectSetActive(args, record) {
        var view = dataView();
        var objectPtr = args[0];
        var active = !!args[1];
        var window = null;
        var native = null;
        if (view && isPointerLike(view, objectPtr, 64)) {
          window = probe.dumpMemoryWindow(
            target.name + ".gameObject.before",
            objectPtr,
            Math.min(opts.windowBytes || 128, view.byteLength - objectPtr),
            {
              includeRawBytes: opts.includeRawBytes === true,
              includePointers: false,
              previewBytes: opts.previewBytes || 64,
              u32PreviewCount: 24,
              f32PreviewCount: 12
            }
          );
          native = decodeNativeGameObjectActivation(view, objectPtr, opts);
        }
        record.__gameObjectActivation = {
          objectPtr: sanitizeArg(objectPtr),
          active: active,
          beforeWindow: window,
          nativeBefore: native
        };
        pushEvent("game_object.set_active.before", {
          hook: target,
          callIndex: record.calls,
          objectPtr: sanitizeArg(objectPtr),
          active: active,
          gameObjectWindow: window,
          nativeGameObject: native
        });
      },
      afterCall: function afterGameObjectSetActive(args, result, record) {
        var snapshot = record.__gameObjectActivation;
        if (!snapshot) return;
        var view = dataView();
        var afterWindow = null;
        var nativeAfter = null;
        if (view && isPointerLike(view, args[0], 64)) {
          afterWindow = probe.dumpMemoryWindow(
            target.name + ".gameObject.after",
            args[0],
            Math.min(opts.windowBytes || 128, view.byteLength - args[0]),
            {
              includeRawBytes: opts.includeRawBytes === true,
              includePointers: false,
              previewBytes: opts.previewBytes || 64,
              u32PreviewCount: 24,
              f32PreviewCount: 12
            }
          );
          nativeAfter = decodeNativeGameObjectActivation(view, args[0], opts);
        }
        pushEvent("game_object.set_active.after", {
          hook: target,
          callIndex: record.calls,
          objectPtr: snapshot.objectPtr,
          active: snapshot.active,
          gameObjectWindowBefore: snapshot.beforeWindow,
          gameObjectWindowAfter: afterWindow,
          nativeGameObjectBefore: snapshot.nativeBefore,
          nativeGameObjectAfter: nativeAfter
        });
        record.__gameObjectActivation = null;
      }
    });
  };

  function installMeshColliderComponentHook(target, eventStem, options) {
    var opts = options || {};
    var existing = probe.hooks.filter(function sameMeshColliderHook(hook) {
      return hook.index === target.index && hook.name === target.name;
    }).slice(-1)[0];
    if (existing && !opts.reinstall) return existing;
    if (existing) probe.uninstallTableHook(existing);

    var emitted = 0;
    var maxEvents = opts.maxEvents || 128;
    function snapshot(view, componentPtr) {
      if (!view || !isPointerLike(view, componentPtr, 64)) return null;
      var colliderBackendPtr = view.getUint32(componentPtr + 40, true); // a[10]
      var gameObjectPtr = view.getUint32(componentPtr + 28, true); // a[7]
      return {
        componentPtr: componentPtr,
        gameObjectPtr: gameObjectPtr,
        colliderBackendPtr: colliderBackendPtr,
        enabledBit: view.getUint8(componentPtr + 61),
        activationBit: view.getUint8(componentPtr + 62),
        componentWindow: probe.dumpMemoryWindow(
          target.name + ".component",
          componentPtr,
          Math.min(opts.componentBytes || 192, view.byteLength - componentPtr),
          {
            includeRawBytes: opts.includeRawBytes !== false,
            includePointers: true,
            previewBytes: opts.previewBytes || 96,
            u32PreviewCount: 48,
            f32PreviewCount: 24,
            pointerScanBytes: opts.pointerScanBytes || 192
          }
        ),
        backendWindow: isPointerLike(view, colliderBackendPtr, 64)
          ? probe.dumpMemoryWindow(
              target.name + ".colliderBackend",
              colliderBackendPtr,
              Math.min(opts.backendBytes || 320, view.byteLength - colliderBackendPtr),
              {
                includeRawBytes: opts.includeRawBytes !== false,
                includePointers: true,
                previewBytes: opts.previewBytes || 128,
                u32PreviewCount: 80,
                f32PreviewCount: 32,
                pointerScanBytes: opts.pointerScanBytes || 320
              }
            )
          : null
      };
    }

    return probe.installTableHook(target.index, target.name, {
      signature: target.signature,
      traceCallEvent: false,
      beforeCall: function beforeMeshColliderActivation(args, record) {
        if (emitted >= maxEvents) return;
        var state = snapshot(dataView(), args[0]);
        record.__meshColliderActivation = {
          args: [sanitizeArg(args[0]), sanitizeArg(args[1]), sanitizeArg(args[2]), sanitizeArg(args[3])],
          before: state
        };
        pushEvent(eventStem + ".before", {
          hook: target,
          callIndex: record.calls,
          args: record.__meshColliderActivation.args,
          state: state
        });
      },
      afterCall: function afterMeshColliderActivation(args, result, record) {
        var before = record.__meshColliderActivation;
        if (!before || emitted >= maxEvents) return;
        emitted += 1;
        pushEvent(eventStem + ".after", {
          hook: target,
          callIndex: record.calls,
          args: before.args,
          result: sanitizeArg(result),
          before: before.before,
          after: snapshot(dataView(), args[0])
        });
        record.__meshColliderActivation = null;
      }
    });
  }

  probe.installMeshColliderActivationHook = function installMeshColliderActivationHook(options) {
    return installMeshColliderComponentHook(
      probe.meshColliderActivationHook,
      "mesh_collider.activation",
      options
    );
  };

  probe.installMeshColliderPhysicsHooks = function installMeshColliderPhysicsHooks(options) {
    var opts = options || {};
    var installed = [
      probe.installMeshColliderActivationHook(opts),
      installMeshColliderComponentHook(
        probe.meshColliderTransformRefreshHook,
        "mesh_collider.transform_refresh",
        opts
      ),
      installMeshColliderComponentHook(
        probe.meshColliderStateRefreshHook,
        "mesh_collider.state_refresh",
        opts
      )
    ];
    return installed.every(Boolean);
  };

  probe.installOverlapCreatedHook = function installOverlapCreatedHook(options) {
    var opts = options || {};
    var target = probe.overlapCreatedHook;
    var existing = probe.hooks.filter(function sameOverlapCreatedHook(hook) {
      return hook.index === target.index && hook.name === target.name;
    }).slice(-1)[0];
    if (existing && !opts.reinstall) return existing;
    if (existing) probe.uninstallTableHook(existing);

    var emitted = 0;
    var maxEvents = opts.maxEvents || 128;
    function readU32(view, address) {
      return isPointerLike(view, address, 4) ? view.getUint32(address, true) : 0;
    }
    function snapshot(view, taskPtr) {
      if (!view || !isPointerLike(view, taskPtr, 56)) return null;
      // func71504 uses a[7..13] for NPhaseCore, overlap arrays, output bits and count.
      var nphaseCorePtr = readU32(view, taskPtr + 28);
      var overlapPtr = readU32(view, taskPtr + 32);
      // Sc::Scene::OnOverlapCreatedTask layout. These are preallocated
      // object arrays, not the later narrowphase touch-output arrays.
      var filterInfoPtr = readU32(view, taskPtr + 36);
      var contactManagersPtr = readU32(view, taskPtr + 40);
      var shapeInteractionsPtr = readU32(view, taskPtr + 44);
      var interactionMarkersPtr = readU32(view, taskPtr + 48);
      var count = readU32(view, taskPtr + 52);
      var overlaps = [];
      var capped = Math.min(count, opts.maxPairs || 32);
      for (var i = 0; i < capped; i += 1) {
        var entry = overlapPtr + i * 12;
        overlaps.push({
          index: i,
          volume0: readU32(view, entry),
          volume1: readU32(view, entry + 4),
          overlapFlags: readU32(view, entry + 8),
          preallocatedContactManager: readU32(view, contactManagersPtr + i * 4),
          preallocatedShapeInteraction: readU32(view, shapeInteractionsPtr + i * 4),
          preallocatedInteractionMarker: readU32(view, interactionMarkersPtr + i * 4)
        });
      }
      return {
        taskPtr: taskPtr,
        nphaseCorePtr: nphaseCorePtr,
        overlapPtr: overlapPtr,
        filterInfoPtr: filterInfoPtr,
        contactManagersPtr: contactManagersPtr,
        shapeInteractionsPtr: shapeInteractionsPtr,
        interactionMarkersPtr: interactionMarkersPtr,
        pairCount: count,
        overlaps: overlaps
      };
    }

    return probe.installTableHook(target.index, target.name, {
      signature: target.signature,
      traceCallEvent: false,
      beforeCall: function beforeOverlapCreated(args, record) {
        var state = snapshot(dataView(), args[0]);
        if (!state || state.pairCount === 0 || emitted >= maxEvents) return;
        record.__overlapCreated = state;
        pushEvent("physx.overlap_created.before", {
          hook: target,
          callIndex: record.calls,
          state: state
        });
      },
      afterCall: function afterOverlapCreated(args, result, record) {
        var before = record.__overlapCreated;
        if (!before || emitted >= maxEvents) return;
        emitted += 1;
        pushEvent("physx.overlap_created.after", {
          hook: target,
          callIndex: record.calls,
          before: before,
          after: snapshot(dataView(), args[0])
        });
        record.__overlapCreated = null;
      }
    });
  };

  function decodeNativeGameObjectActivation(view, managedGameObjectPtr, options) {
    // func79964 resolves GameObject.m_CachedPtr from managedObject + 8.
    var nativePtr = view.getUint32(managedGameObjectPtr + 8, true);
    if (!isPointerLike(view, nativePtr, 40)) return null;
    var entriesPtr = view.getUint32(nativePtr + 28, true); // native GameObject::m_Components
    var componentCount = view.getUint32(nativePtr + 36, true); // m_ComponentCount
    var componentLimit = Math.min(componentCount, options.maxComponents || 32);
    var components = [];
    if (isPointerLike(view, entriesPtr, componentLimit * 8)) {
      for (var index = 0; index < componentLimit; index += 1) {
        var entryPtr = entriesPtr + index * 8;
        var componentPtr = view.getUint32(entryPtr + 4, true);
        var vtablePtr = isPointerLike(view, componentPtr, 4)
          ? view.getUint32(componentPtr, true)
          : 0;
        // func79993 resolves this native component type key through its
        // activation registry before invoking the enable handler.
        var componentTypeKey = isPointerLike(view, componentPtr, 8)
          ? view.getUint32(componentPtr + 4, true)
          : null;
        // func80182 invokes component vtable slot 24 for the disable path.
        var activationCallbackTableIndex = isPointerLike(view, vtablePtr + 96, 4)
          ? view.getUint32(vtablePtr + 96, true)
          : null;
        components.push({
          entryIndex: index,
          componentTypeId: view.getUint32(entryPtr, true),
          componentPtr: componentPtr,
          componentTypeKey: componentTypeKey,
          vtablePtr: vtablePtr,
          activationCallbackTableIndex: activationCallbackTableIndex
        });
      }
    }
    // func80110 resolves component type keys through this runtime registry.
    var activationRegistryGlobalAddress = 4782044;
    var activationRegistryPtr = activationRegistryGlobalAddress + 4 <= view.byteLength
      ? view.getUint32(activationRegistryGlobalAddress, true)
      : null;
    // func80110 first consults these two globals for negative component keys
    // before falling back to the registry at 4782044.
    var activationResolverProviderAddress = 4782124;
    var activationResolverTableAddress = 4782128;
    var activationResolverProvider = activationResolverProviderAddress + 4 <= view.byteLength
      ? view.getUint32(activationResolverProviderAddress, true)
      : null;
    var activationResolverTableIndex = activationResolverTableAddress + 4 <= view.byteLength
      ? view.getUint32(activationResolverTableAddress, true)
      : null;
    return {
      managedGameObjectPtr: managedGameObjectPtr,
      nativeGameObjectPtr: nativePtr,
      componentEntriesPtr: entriesPtr,
      componentCount: componentCount,
      components: components,
      activationRegistryPtr: activationRegistryPtr,
      activationResolverProvider: activationResolverProvider,
      activationResolverTableIndex: activationResolverTableIndex,
      activationRegistryWindow: isPointerLike(view, activationRegistryPtr, 256)
        ? probe.dumpMemoryWindow(
            "UnityEngine.GameObject.SetActive.activationRegistry",
            activationRegistryPtr,
            Math.min(320, view.byteLength - activationRegistryPtr),
            {
              includeRawBytes: options.includeRawBytes === true,
              includePointers: false,
              previewBytes: 96,
              u32PreviewCount: 80,
              f32PreviewCount: 0
            }
          )
        : null,
      nativeWindow: probe.dumpMemoryWindow(
        "UnityEngine.GameObject.SetActive.nativeGameObject",
        nativePtr,
        Math.min(options.nativeWindowBytes || 256, view.byteLength - nativePtr),
        {
          includeRawBytes: options.includeRawBytes === true,
          includePointers: false,
          previewBytes: options.previewBytes || 96,
          u32PreviewCount: 64,
          f32PreviewCount: 16
        }
      )
    };
  }

  probe.installSlidingTraceHooks = function installSlidingTraceHooks(options) {
    var opts = options || {};
    var state = probe.slidingTrace || {
      randomRangeCalls: 0,
      frictionRangeCalls: 0,
      randomValueCalls: 0,
      randomSeedCalls: 0,
      initStateCalls: 0,
      fixedUpdateCalls: 0
    };
    probe.slidingTrace = state;

    var maxRandomEvents = opts.maxRandomEvents || 20000;
    var maxFixedUpdateEvents = opts.maxFixedUpdateEvents || 8000;
    var logOtherRandomRange = !!opts.logOtherRandomRange;
    var logRandomValue = !!opts.logRandomValue;
    var frictionMin = opts.frictionNoiseMin === undefined ? -0.0002 : Number(opts.frictionNoiseMin);
    var frictionMax = opts.frictionNoiseMax === undefined ? 0.0002 : Number(opts.frictionNoiseMax);

    function closeEnough(a, b, eps) {
      return Math.abs(Number(a) - Number(b)) <= (eps || 1e-7);
    }

    function isFrictionNoiseRange(minValue, maxValue) {
      return closeEnough(minValue, frictionMin, 1e-7) && closeEnough(maxValue, frictionMax, 1e-7);
    }

    function installSlidingTarget(index, name, signature, hookOptions) {
      var existing = probe.hooks.filter(function sameHook(hook) {
        return hook.index === index && hook.name === name;
      }).slice(-1)[0];
      if (existing && !opts.reinstall) return existing;
      if (existing && opts.reinstall) probe.uninstallTableHook(existing);
      return probe.installTableHook(index, name, Object.assign({
        signature: signature,
        traceCallEvent: false
      }, hookOptions || {}));
    }

    var installed = [];
    [
      installSlidingTarget(129032, "UnityEngine.Random.InitState", "vi", {
        beforeCall: function beforeRandomInitState(args, record) {
          state.initStateCalls += 1;
          pushEvent("sliding.random_init_state", {
            callIndex: record.calls,
            initStateCalls: state.initStateCalls,
            seed: sanitizeArg(args[0])
          });
        }
      }),
      installSlidingTarget(129033, "UnityEngine.Random.Range", "fff", {
        afterCall: function afterRandomRange(args, result, record) {
          state.randomRangeCalls += 1;
          var minValue = Number(args[0]);
          var maxValue = Number(args[1]);
          var value = Number(result);
          var isFriction = isFrictionNoiseRange(minValue, maxValue);
          if (isFriction) state.frictionRangeCalls += 1;
          if (state.randomRangeCalls > maxRandomEvents) return;
          if (!isFriction && !logOtherRandomRange) return;
          pushEvent(isFriction ? "sliding.random_range.friction" : "sliding.random_range.other", {
            callIndex: record.calls,
            randomRangeCalls: state.randomRangeCalls,
            frictionRangeCalls: state.frictionRangeCalls,
            min: minValue,
            max: maxValue,
            value: value,
            inferredNoSweepFriction: isFriction ? 0.001 + value : null,
            inferredSweepFriction: isFriction ? 0.0006 + value : null
          });
        }
      }),
      installSlidingTarget(129035, "UnityEngine.Random.get_value", "f", {
        afterCall: function afterRandomValue(args, result, record) {
          state.randomValueCalls += 1;
          if (!logRandomValue || state.randomValueCalls > maxRandomEvents) return;
          pushEvent("sliding.random_value", {
            callIndex: record.calls,
            randomValueCalls: state.randomValueCalls,
            value: Number(result)
          });
        }
      }),
      installSlidingTarget(129036, "UnityEngine.Random.get_seed", "i", {
        afterCall: function afterRandomSeed(args, result, record) {
          state.randomSeedCalls += 1;
          if (state.randomSeedCalls > maxRandomEvents) return;
          pushEvent("sliding.random_seed", {
            callIndex: record.calls,
            randomSeedCalls: state.randomSeedCalls,
            seed: sanitizeArg(result)
          });
        }
      }),
      installSlidingTarget(11105, "DCP_HumanVSAI.FixedUpdate", "vii", {
        beforeCall: function beforeDcpHumanVsAiFixedUpdate(args, record) {
          state.fixedUpdateCalls += 1;
          if (state.fixedUpdateCalls > maxFixedUpdateEvents) return;
          pushEvent("sliding.fixed_update.enter", {
            callIndex: record.calls,
            fixedUpdateCalls: state.fixedUpdateCalls,
            args: Array.prototype.slice.call(args, 0, 4).map(sanitizeArg)
          });
        },
        afterCall: function afterDcpHumanVsAiFixedUpdate(args, result, record) {
          if (state.fixedUpdateCalls > maxFixedUpdateEvents) return;
          pushEvent("sliding.fixed_update.exit", {
            callIndex: record.calls,
            fixedUpdateCalls: state.fixedUpdateCalls,
            result: sanitizeArg(result)
          });
        }
      })
    ].forEach(function keepInstalled(hook) {
      if (hook) installed.push(hook);
    });

    pushEvent("sliding.hooks_installed", {
      count: installed.length,
      maxRandomEvents: maxRandomEvents,
      maxFixedUpdateEvents: maxFixedUpdateEvents,
      logOtherRandomRange: logOtherRandomRange,
      logRandomValue: logRandomValue,
      frictionNoiseMin: frictionMin,
      frictionNoiseMax: frictionMax,
      targets: installed.map(function summarizeSlidingHook(hook) {
        return { index: hook.index, name: hook.name };
      })
    });
    return installed;
  };

  probe.installA0FixedTickResolverHook = function installA0FixedTickResolverHook(options) {
    // Read-only A0 instrumentation. It emits a script tick key and captures the
    // final f_ybva(Vector3 angularVelocity) call before the first stone PCM.
    var opts = options || {};
    var state = probe.a0FixedTickResolver || {
      nextTickSerial: 0,
      currentTick: null,
      velocityDispatchIndex: null,
      angularDispatchIndex: null,
      angularWriteSerial: 0,
      lastAngularWrite: null,
      lastAngularWrites: [],
      lastLinearWrite: null,
      frictionNoiseSerial: 0,
      lastFrictionNoise: null,
      lastFrictionNoises: [],
      staticWritebackRing: [],
      phaseOrderSerial: 0,
      phaseOrderRing: [],
      phaseOrderByAngularWrite: {},
      a2StaticTraceEnabled: opts.a2StaticTrace === true,
      a2StaticTraceArmed: false,
      a2StaticTraceRows: [],
      a2StaticTraceByTick: {},
      a8StaticWindowEnabled: opts.a8StaticWindow === true,
      a8StaticWindowStartTick: null,
      a9SnapshotWindowEnabled: opts.a9SnapshotWindow === true,
      a9SnapshotWindowStartTick: null,
      a9CapturedPreIntegrateTicks: {},
      a9UnresolvedTaskEmitted: false,
      a9SetterCoreByTick: {},
      a9CapturedSolverSetupTicks: {},
      a9UnresolvedNativeEmitted: false,
      // A10 is a read-only per-release pose capture.  It closes the one piece
      // of strict persistent-scene replay truth absent from RESETPOSITION:
      // the prior Rigidbody quaternion, particularly yaw.
      a10ReleaseOrientationEnabled: opts.a10ReleaseOrientation === true,
      a10CapturedReleaseSerial: 0,
      // Sampling-only opt-in.  RESETPOSITION itself only moves the existing
      // rigidbodies.  Capture their actual startup quaternions at the first
      // controlled reset, then restore exactly those values at later resets.
      // This avoids a costly scene reload and does not assume identity yaw.
      resetAllStoneRotationsEnabled: opts.resetAllStoneRotations === true,
      resetRotationBaselineByBody: {},
      // This is an explicitly opt-in runtime diagnostic mutation, not a
      // passive observation.  A fresh browser session contains one controlled
      // shot; applying the seed immediately before its first friction draw
      // makes that physical input reproducible without relying on UI/startup
      // Random consumption.
      rngSeedOnFirstFriction: Number.isInteger(opts.rngSeedOnFirstFriction)
        ? (Number(opts.rngSeedOnFirstFriction) | 0) : null,
      rngSeedApplied: false,
      rngInitHook: null,
      // Diagnostic-only deterministic replay channel.  Unlike InitState this
      // is scoped to the recovered DCP friction Range call and is therefore
      // immune to unrelated consumers of Unity's process-global RNG.
      rngFrictionManifest: Array.isArray(opts.rngFrictionManifest)
        ? opts.rngFrictionManifest.map(Number) : null,
      rngFrictionManifestSource: typeof opts.rngFrictionManifestSource === "string"
        ? opts.rngFrictionManifestSource : null,
      rngFrictionManifestIndex: 0,
      rngFrictionManifestApplied: false,
      rngFrictionManifestExhausted: false,
      c03FirstWritebackEnabled: opts.c03FirstWriteback === true,
      c03TargetNativeX: Number.isFinite(opts.c03TargetNativeX) ? Number(opts.c03TargetNativeX) : null,
      c03TargetNativeZ: Number.isFinite(opts.c03TargetNativeZ) ? Number(opts.c03TargetNativeZ) : null,
      c03TargetNativeTolerance: Math.max(0.001, Number(opts.c03TargetNativeTolerance) || 0.05),
      c03ActiveSpeedMin: Number.isFinite(opts.c03ActiveSpeedMin) ? Number(opts.c03ActiveSpeedMin) : null,
      c04DynamicWindowEnabled: opts.c04DynamicWindow === true,
      c04DynamicWindowLimit: Math.max(1, Math.min(Number(opts.c04DynamicWindowLimit) || 12, 2048)),
      c31CompactCoreTraceEnabled: opts.c31CompactCoreTrace === true,
      c31CompactCoreRawFrameLimit: Math.max(0, Math.min(Number(opts.c31CompactCoreRawFrameLimit) || 2048, 2048)),
      c04DynamicFrames: [],
      c04CurrentFrame: null,
      c54IntercallStaticEnabled: opts.c54IntercallStatic === true,
      c26TargetStaticEnabled: opts.c26TargetStatic === true,
      c26TargetStaticFrame: Math.max(0, Math.min(Number(opts.c26TargetStaticFrame) || 3, 23)),
      c05PcmWindowEnabled: opts.c05PcmWindow === true,
      c05PcmWindowLimit: Math.max(1, Math.min(Number(opts.c05PcmWindowLimit) || 6, 12)),
      c05PcmCalls: [],
      c25HistoryPcmEnabled: opts.c25HistoryPcm === true,
      c25HistoryPcmLimit: Math.max(1, Math.min(Number(opts.c25HistoryPcmLimit) || 32, 64)),
      c25HistoryPcmCalls: [],
      c03Armed: false,
      c03Flushed: false,
      c03Manager: null,
      c03PcmInput: null,
      c03DynamicSolve: null,
      firstStonePcmFlushed: false,
      firstStoneManagerTaskFlushed: false
    };
    probe.a0FixedTickResolver = state;
    // A page can reinstall the resolver after a launcher retry. Promote this
    // opt-in capture flag instead of silently retaining a previous false value.
    if (opts.c03FirstWriteback === true) state.c03FirstWritebackEnabled = true;
    if (Number.isFinite(opts.c03TargetNativeX) && Number.isFinite(opts.c03TargetNativeZ)) {
      state.c03TargetNativeX = Number(opts.c03TargetNativeX);
      state.c03TargetNativeZ = Number(opts.c03TargetNativeZ);
      state.c03TargetNativeTolerance = Math.max(0.001, Number(opts.c03TargetNativeTolerance) || 0.05);
    }
    if (Number.isFinite(opts.c03ActiveSpeedMin)) state.c03ActiveSpeedMin = Number(opts.c03ActiveSpeedMin);
    if (Number.isInteger(opts.rngSeedOnFirstFriction) && !state.rngSeedApplied) {
      state.rngSeedOnFirstFriction = Number(opts.rngSeedOnFirstFriction) | 0;
    }
    if (Array.isArray(opts.rngFrictionManifest) && !state.rngFrictionManifestApplied) {
      state.rngFrictionManifest = opts.rngFrictionManifest.map(Number);
      state.rngFrictionManifestSource = typeof opts.rngFrictionManifestSource === "string"
        ? opts.rngFrictionManifestSource : state.rngFrictionManifestSource;
      state.rngFrictionManifestIndex = 0;
      state.rngFrictionManifestExhausted = false;
    }
    if (opts.c04DynamicWindow === true) state.c04DynamicWindowEnabled = true;
    if (opts.c31CompactCoreTrace === true) state.c31CompactCoreTraceEnabled = true;
    if (Number.isFinite(Number(opts.c31CompactCoreRawFrameLimit))) {
      state.c31CompactCoreRawFrameLimit = Math.max(0, Math.min(Number(opts.c31CompactCoreRawFrameLimit), 2048));
    }

    function c31KeepsRawSolverFrame() {
      return !state.c31CompactCoreTraceEnabled || !state.c04CurrentFrame ||
        state.c04CurrentFrame.frameIndex < state.c31CompactCoreRawFrameLimit;
    }
    if (opts.c54IntercallStatic === true) state.c54IntercallStaticEnabled = true;
    if (opts.c26TargetStatic === true) state.c26TargetStaticEnabled = true;
    if (opts.c05PcmWindow === true) state.c05PcmWindowEnabled = true;
    if (opts.c25HistoryPcm === true) state.c25HistoryPcmEnabled = true;
    if (opts.a10ReleaseOrientation === true) state.a10ReleaseOrientationEnabled = true;
    var candidates = [
      { index: 11204, name: "FastDCP.FixedUpdate", movingCurlingOffset: 212 },
      { index: 10825, name: "AutoDCP.FixedUpdate", movingCurlingOffset: 240 },
      { index: 11105, name: "DCP_HumanVSAI.FixedUpdate", movingCurlingOffset: 260 },
      { index: 10980, name: "DCP.FixedUpdate", movingCurlingOffset: 232 }
    ];
    var velocityDispatchGlobal = 4659060;
    var angularDispatchGlobal = 4659068;
    // Static internal-call registration lookup from build.wasm.gz:
    // UnityEngine.Rigidbody::set_angularVelocity -> table 129354 -> func82503.
    // f_ybva/func32524 calls this entry indirectly, so hook this native endpoint
    // rather than f_ybva's direct Wasm call or its inaccessible Wasm global.
    var angularVelocitySetterTableIndex = 129354;
    // Adjacent registrations recovered from build.wasm.gz:
    // get_velocity=129351, set_velocity=129352,
    // get_angularVelocity=129353, set_angularVelocity=129354.
    var linearVelocityGetterTableIndex = 129351;
    var linearVelocitySetterTableIndex = 129352;
    var angularVelocityGetterTableIndex = 129353;
    // SetStonesByBody/ResetStones write Transform.position, not
    // Rigidbody.position.  The rotation reset must therefore use the same
    // Transform instance and execution boundary.
    var transformPositionSetterTableIndex = 129161;
    var transformRotationGetterTableIndex = 129164;
    var transformRotationSetterTableIndex = 129165;
    var randomRangeTableIndex = 129033;
    var randomInitStateTableIndex = 129032;
    var stonePcmIndex = 120118;
    var contactManagerTaskIndex = 120204;
    var dynamicSolveTableIndex = 120346;
    var dynamicSolveWritebackTableIndex = 120352;
    // Some two-stone islands are dispatched through the 4-wide kernel even
    // when only one lane is occupied.  C70's core state changed while the
    // single-pair hook saw no call, so retain the equivalent 4-wide boundary
    // as part of the same read-only C03/C04 evidence window.
    var dynamicSolve4TableIndex = 120349;
    var dynamicSolve4WritebackTableIndex = 120355;
    var staticSolveTableIndex = 120348;
    var staticWritebackTableIndex = 120354;
    // PhysX 4.1 task metadata recovered from the Unity wasm task graph.
    // preIntegrate copies PxsBodyCore v/w and body2World into PxSolverBodyData;
    // solverSetupSolve is the small-island path that runs solveVBlock and
    // integrateCore before it writes P/Q/v/w back to the core.
    var preIntegrateTaskIndex = 120590;
    var solverSetupSolveTaskIndex = 120569;

    function vector3At(view, ptr) {
      if (!isPointerLike(view, ptr, 12)) return null;
      return [readF32LE(view, ptr), readF32LE(view, ptr + 4), readF32LE(view, ptr + 8)];
    }

    // PhysX 4.1 wasm32 layout: Dy::SolverContext::solverBodyArray is at +16;
    // PxSolverBodyData is 112 bytes. PxSolverBody holds only solver deltas,
    // while this array holds the actual pre-solve v/w and body2World.
    function solverBodyDataAt(view, solverContextPtr, dataIndex) {
      if (!isPointerLike(view, solverContextPtr, 20) || !Number.isInteger(dataIndex)) return null;
      var arrayPtr = readU32LE(view, solverContextPtr + 16);
      var ptr = arrayPtr + dataIndex * 112;
      if (!isPointerLike(view, ptr, 112)) return null;
      return {
        ptr: ptr,
        dataIndex: dataIndex,
        linearVelocity: vector3At(view, ptr),
        invMass: readF32LE(view, ptr + 12),
        angularVelocity: vector3At(view, ptr + 16),
        body2World: decodeTransformCandidate(view, ptr + 80),
        lockFlags: readU16LE(view, ptr + 108)
      };
    }

    function staticSolverBodyDataSnapshots(view, solverContextPtr, dumps) {
      return (dumps || []).map(function (record) {
        var desc = record && record.desc;
        if (!desc) return null;
        return {
          bodyA: solverBodyDataAt(view, solverContextPtr, desc.bodyADataIndex),
          bodyB: solverBodyDataAt(view, solverContextPtr, desc.bodyBDataIndex)
        };
      }).filter(Boolean);
    }

    // C03 captures the first dynamic-dynamic solver frame. C04 optionally
    // extends this into a short post-contact window; both retain raw windows
    // from manager-validated core pointers rather than guessing from a
    // Rigidbody root pointer.
    // The manager layout has already been validated by the A0 actor/cache
    // audit; retain both raw windows and a guarded decoded view so offline
    // analysis never has to infer a body core from a Rigidbody root pointer.
    function c03CoreSnapshot(view, corePtr, label) {
      if (!isPointerLike(view, corePtr, 160)) return null;
      return {
        ptr: corePtr,
        decodedCandidate: decodeA9BodyCore(view, corePtr),
        window: probe.dumpMemoryWindow(label, corePtr, 160, {
          includeRawBytes: true,
          includePointers: false,
          previewBytes: 160,
          u32PreviewCount: 40,
          f32PreviewCount: 40,
          contactPreviewCount: 0
        })
      };
    }

    // C31 deliberately stores only the verified decoded core fields.  Unlike
    // C03/C04 forensic snapshots it carries no raw memory, constraint, cache,
    // or pointer scan data, so a long post-contact truth trace remains small.
    function c31CompactCoreSnapshot(view, corePtr) {
      if (!isPointerLike(view, corePtr, 160)) return null;
      return { ptr: corePtr, decodedCandidate: decodeA9BodyCore(view, corePtr) };
    }

    function armC03FirstWriteback(view, taskPtr) {
      if (!state.c03FirstWritebackEnabled || state.c03Armed || state.c03Flushed) return false;
      var task = decodePxsCMDiscreteUpdateTask(view, taskPtr, { cmTaskManagers: 128 });
      if (!task || !task.managers) return false;
      var managerRow = task.managers.find(function findDynamicPair(row) {
        return row.manager &&
          looksLikeDynamicStoneCore(view, row.manager.rigidCore0) &&
          looksLikeDynamicStoneCore(view, row.manager.rigidCore1);
      });
      if (!managerRow) return false;
      if (state.c03TargetNativeX !== null && state.c03TargetNativeZ !== null) {
        var targetMatched = [managerRow.manager.rigidCore0, managerRow.manager.rigidCore1].some(function(corePtr) {
          var core = decodeA9BodyCore(view, corePtr);
          return core &&
            Math.abs(core.p[0] - state.c03TargetNativeX) <= state.c03TargetNativeTolerance &&
            Math.abs(core.p[2] - state.c03TargetNativeZ) <= state.c03TargetNativeTolerance;
        });
        if (!targetMatched) return false;
      }
      if (state.c03ActiveSpeedMin !== null) {
        var activeMatched = [managerRow.manager.rigidCore0, managerRow.manager.rigidCore1].some(function(corePtr) {
          var core = decodeA9BodyCore(view, corePtr);
          if (!core || !Array.isArray(core.linearVelocity)) return false;
          return Math.hypot(Number(core.linearVelocity[0]) || 0, Number(core.linearVelocity[2]) || 0) >=
            state.c03ActiveSpeedMin;
        });
        if (!activeMatched) return false;
      }
      state.c03Armed = true;
      state.c03Manager = {
        taskPtr: sanitizeArg(taskPtr),
        taskIndex: managerRow.taskIndex,
        contactManager: managerRow.manager,
        coresBeforeSolve: [
          c03CoreSnapshot(view, managerRow.manager.rigidCore0, "C03.manager.rigidCore0.before"),
          c03CoreSnapshot(view, managerRow.manager.rigidCore1, "C03.manager.rigidCore1.before")
        ]
      };
      return true;
    }

    function captureC03DynamicSolve(view, args, edge) {
      if (!state.c03Armed || (state.c03Flushed && !state.c04DynamicWindowEnabled)) return null;
      var dump = dumpSolverConstraintDescs(view, "C03.dynamic." + edge, args[0], {
        solverDescRecords: Math.min(Number(args[1]) || 1, 4),
        solverBodyBytes: 64,
        solverConstraintBytes: 384,
        includeRawBytes: true,
        contactPreviewCount: 4
      });
      var snapshots = staticSolverBodyDataSnapshots(view, args[2], dump);
      return {
        solverContextPtr: sanitizeArg(args[2]),
        solverDescPtr: sanitizeArg(args[0]),
        blockConstraintCount: Number(args[1]) || 0,
        descs: dump,
        solverBodyData: snapshots,
        cores: state.c03Manager && state.c03Manager.contactManager ? [
          c03CoreSnapshot(view, state.c03Manager.contactManager.rigidCore0, "C03.rigidCore0." + edge),
          c03CoreSnapshot(view, state.c03Manager.contactManager.rigidCore1, "C03.rigidCore1." + edge)
        ] : null
      };
    }

    // C54 is intentionally read-only.  A dynamic pair batch is interleaved
    // with the active/target--ice BStatic blocks, so dynamic calls alone
    // cannot identify the writer that changes a PxSolverBody between two
    // dynamic regular iterations.
    function captureC54StaticSolve(view, args, edge) {
      var dump = dumpSolverConstraintDescs(view, "C54.static." + edge, args[0], {
        solverDescRecords: Math.min(Number(args[1]) || 1, 4),
        solverBodyBytes: 128,
        solverConstraintBytes: 640,
        includeRawBytes: true,
        contactPreviewCount: 4
      });
      return {
        solverContextPtr: sanitizeArg(args[2]),
        solverDescPtr: sanitizeArg(args[0]),
        blockConstraintCount: Number(args[1]) || 0,
        descs: dump,
        solverBodyData: staticSolverBodyDataSnapshots(view, args[2], dump)
      };
    }

    function c05PcmSnapshot(view, args, edge) {
      var cache = isPointerLike(view, args[5], 8) ? decodeCacheCandidate(view, args[5]) : null;
      var buffer = isPointerLike(view, args[6], 4112) ? decodeContactBufferCandidate(view, args[6], 8) : null;
      var out = {
        edge: edge,
        transform0: decodeTransformCandidate(view, args[2]),
        transform1: decodeTransformCandidate(view, args[3]),
        cache: cache,
        contactBuffer: buffer
      };
      if (cache && isPointerLike(view, cache.cachedDataPtr, 128)) {
        out.manifold = probe.dumpMemoryWindow("C05.pcm.manifold." + edge, cache.cachedDataPtr,
          Math.min(256, view.byteLength - cache.cachedDataPtr), {
            includeRawBytes: true,
            includePointers: false,
            previewBytes: 128,
            u32PreviewCount: 32,
            f32PreviewCount: 32,
            contactPreviewCount: 4
          });
      }
      return out;
    }

    function compactA2StaticSolverRow(view, descPtr, solverContextPtr) {
      if (!isPointerLike(view, descPtr, 32)) return null;
      var best = null;
      for (var i = 0; i < 4; i += 1) {
        var desc = decodeSolverConstraintDesc(view, descPtr + i * 32);
        if (!desc || !desc.bodyA || !desc.constraintLengthOver16) continue;
        var body = solverBodyDataAt(view, solverContextPtr, desc.bodyADataIndex);
        if (!body || !body.linearVelocity || !body.angularVelocity || !body.body2World) continue;
        var planarSpeedSq = body.linearVelocity[0] * body.linearVelocity[0] +
          body.linearVelocity[2] * body.linearVelocity[2];
        var candidate = {
          descIndex: i,
          solverBodyPtr: desc.bodyA,
          solverBodyDataIndex: desc.bodyADataIndex,
          constraintLengthOver16: desc.constraintLengthOver16,
          planarSpeedSq: planarSpeedSq,
          p: body.body2World.p,
          q: body.body2World.q,
          v: body.linearVelocity,
          w: body.angularVelocity
        };
        if (!best || candidate.planarSpeedSq > best.planarSpeedSq) best = candidate;
      }
      return best;
    }

    function appendA2StaticTrace(view, args) {
      if (!state.a2StaticTraceEnabled || !state.a2StaticTraceArmed) return;
      var tick = state.lastAngularWrite;
      if (!tick || !Number.isInteger(tick.tickSerial)) return;
      var compact = compactA2StaticSolverRow(view, args[0], args[2]);
      if (!compact || compact.planarSpeedSq < 1e-10) return;
      var row = Object.assign({
        tickSerial: tick.tickSerial,
        angularWriteSerial: tick.writeSerial,
        setterWy: tick.wy,
        scriptGetter: tick.scriptInputs || null,
        frictionNoise: state.lastFrictionNoise && state.lastFrictionNoise.tickSerial === tick.tickSerial
          ? state.lastFrictionNoise.value
          : null,
        linearSetter: state.lastLinearWrite && state.lastLinearWrite.tickSerial === tick.tickSerial
          ? state.lastLinearWrite.vector
          : null
      }, compact);
      var existing = state.a2StaticTraceByTick[row.tickSerial];
      if (existing) {
        if (row.planarSpeedSq <= existing.planarSpeedSq) return;
        var oldIndex = state.a2StaticTraceRows.indexOf(existing);
        if (oldIndex >= 0) state.a2StaticTraceRows[oldIndex] = row;
      } else {
        state.a2StaticTraceRows.push(row);
      }
      state.a2StaticTraceByTick[row.tickSerial] = row;
      if (state.a2StaticTraceRows.length > 2000) {
        state.a2StaticTraceRows.shift();
        state.a2StaticTraceByTick = {};
        state.a2StaticTraceRows.forEach(function indexTraceRow(item) {
          state.a2StaticTraceByTick[item.tickSerial] = item;
        });
      }
    }

    function isA8StaticWindowTick(tick) {
      if (!state.a8StaticWindowEnabled || !tick || !Number.isInteger(tick.tickSerial)) return false;
      if (!Number.isInteger(state.a8StaticWindowStartTick)) return false;
      return tick.tickSerial >= state.a8StaticWindowStartTick &&
        tick.tickSerial < state.a8StaticWindowStartTick + 8;
    }

    function isA9SnapshotWindowTick(tick) {
      if (!state.a9SnapshotWindowEnabled || !tick || !Number.isInteger(tick.tickSerial)) return false;
      if (!Number.isInteger(state.a9SnapshotWindowStartTick)) return false;
      return tick.tickSerial >= state.a9SnapshotWindowStartTick &&
        tick.tickSerial < state.a9SnapshotWindowStartTick + 8;
    }

    function managedCachedPtr(view, ptr) {
      if (!isPointerLike(view, ptr, 12)) return null;
      var nativePtr = readU32LE(view, ptr + 8);
      return isPointerLike(view, nativePtr, 4) ? nativePtr : null;
    }

    function existingHook(index, name) {
      return probe.hooks.filter(function sameHook(hook) {
        return hook.index === index && hook.name === name;
      }).slice(-1)[0];
    }

    function installSetterDispatch(kind, index) {
      if (!Number.isInteger(index) || index < 0) return null;
      var name = kind === "linear"
        ? "A0.Rigidbody.set_velocity.dispatch"
        : "A0.Rigidbody.set_angularVelocity.dispatch";
      var existing = existingHook(index, name);
      if (existing) return existing;
      return probe.installTableHook(index, name, {
        signature: "viii",
        traceCallEvent: false,
        beforeCall: function beforeA0VelocityWrite(args, record) {
          var tick = state.currentTick;
          if (!tick) return;
          var view = dataView();
          var write = {
            tickSerial: tick.tickSerial,
            controller: tick.controller,
            movingCurling: tick.movingCurling,
            bodyManagedPtr: sanitizeArg(args[0]),
            bodyNativePtr: view ? managedCachedPtr(view, args[0]) : null,
            vector: view ? vector3At(view, args[1]) : null
          };
          record.__a0VelocityWrite = write;
          pushEvent("a0.rigidbody_write.before", Object.assign({
            kind: kind,
            dispatchIndex: index
          }, write));
        },
        afterCall: function afterA0VelocityWrite(args, result, record) {
          var write = record.__a0VelocityWrite;
          if (!write) return;
          if (state.currentTick && state.currentTick.tickSerial === write.tickSerial) {
            state.currentTick.writeCount += 1;
          }
          pushEvent("a0.rigidbody_write.after", Object.assign({
            kind: kind,
            dispatchIndex: index
          }, write));
          record.__a0VelocityWrite = null;
        }
      });
    }

    function installAngularVelocitySetter(index) {
      function snapshotBytes(view, ptr, byteLength) {
        if (!isPointerLike(view, ptr, byteLength)) return null;
        var bytes = new Array(byteLength);
        for (var i = 0; i < byteLength; i += 1) bytes[i] = view.getUint8(ptr + i);
        return bytes;
      }

      function snapshotNativeBody(view, nativePtr, priorTargets) {
        var rootBytes = snapshotBytes(view, nativePtr, 1024);
        if (!rootBytes) return null;
        var targets = [];
        if (priorTargets) {
          targets = priorTargets.map(function (target) {
            return {
              ptr: target.ptr,
              rootOffsets: target.rootOffsets,
              bytes: snapshotBytes(view, target.ptr, 1024)
            };
          });
        } else {
          var targetByPtr = {};
          for (var offset = 0; offset < rootBytes.length; offset += 4) {
            var ptr = readU32LE(view, nativePtr + offset);
            if (ptr === nativePtr || !isPointerLike(view, ptr, 1024)) continue;
            var key = String(ptr);
            if (!targetByPtr[key] && targets.length < 64) {
              targetByPtr[key] = { ptr: ptr, rootOffsets: [], bytes: snapshotBytes(view, ptr, 1024) };
              targets.push(targetByPtr[key]);
            }
            if (targetByPtr[key]) targetByPtr[key].rootOffsets.push(offset);
          }
        }
        return { ptr: nativePtr, bytes: rootBytes, targets: targets };
      }

      function f32FromBytes(bytes, offset) {
        if (!bytes || offset < 0 || offset + 4 > bytes.length) return null;
        var buffer = new ArrayBuffer(4);
        var view = new DataView(buffer);
        for (var i = 0; i < 4; i += 1) view.setUint8(i, bytes[offset + i]);
        return view.getFloat32(0, true);
      }

      function changedRanges(beforeBytes, afterBytes) {
        if (!beforeBytes || !afterBytes || beforeBytes.length !== afterBytes.length) return null;
        var changed = [];
        var begin = -1;
        for (var i = 0; i < beforeBytes.length; i += 1) {
          if (beforeBytes[i] !== afterBytes[i]) {
            if (begin < 0) begin = i;
          } else if (begin >= 0) {
            changed.push([begin, i]);
            begin = -1;
          }
        }
        if (begin >= 0) changed.push([begin, beforeBytes.length]);
        return changed.slice(0, 32).map(function (range) {
          var wordOffset = range[0] & ~3;
          return {
            offset: range[0],
            byteLength: range[1] - range[0],
            before: beforeBytes.slice(range[0], range[1]),
            after: afterBytes.slice(range[0], range[1]),
            f32WordOffset: wordOffset,
            beforeF32: f32FromBytes(beforeBytes, wordOffset),
            afterF32: f32FromBytes(afterBytes, wordOffset)
          };
        });
      }

      function diffNativeBody(before, after) {
        if (!before || !after || before.ptr !== after.ptr) return null;
        var targetDeltas = [];
        for (var i = 0; i < before.targets.length; i += 1) {
          var beforeTarget = before.targets[i];
          var afterTarget = after.targets[i];
          var ranges = changedRanges(beforeTarget.bytes, afterTarget && afterTarget.bytes);
          if (ranges && ranges.length) {
            targetDeltas.push({
              ptr: beforeTarget.ptr,
              rootOffsets: beforeTarget.rootOffsets,
              changedRanges: ranges
            });
          }
        }
        return {
          rootRanges: changedRanges(before.bytes, after.bytes),
          targetDeltas: targetDeltas
        };
      }

      function setterMatchingSlots(delta, setterWy) {
        if (!delta) return [];
        var seen = {};
        var slots = [];
        delta.targetDeltas.forEach(function (target) {
          target.changedRanges.forEach(function (range) {
            if (typeof range.afterF32 !== "number" || Math.abs(range.afterF32 - setterWy) > 1e-9) return;
            var key = target.ptr + ":" + range.f32WordOffset;
            if (seen[key]) return;
            seen[key] = true;
            slots.push({ ptr: target.ptr, yOffset: range.f32WordOffset });
          });
        });
        return slots;
      }

      function readSetterBridgeSlots(view, slots) {
        if (!view || !slots) return [];
        return slots.map(function (slot) {
          return {
            ptr: slot.ptr,
            yOffset: slot.yOffset,
            xyz: [
              readF32LE(view, slot.ptr + slot.yOffset - 4),
              readF32LE(view, slot.ptr + slot.yOffset),
              readF32LE(view, slot.ptr + slot.yOffset + 4)
            ]
          };
        });
      }

      function finiteTransformCandidate(transform) {
        if (!transform || !transform.q || !transform.p) return false;
        var values = transform.q.concat(transform.p);
        if (values.some(function (value) { return !Number.isFinite(value); })) return false;
        var normSq = transform.q.reduce(function (sum, value) { return sum + value * value; }, 0);
        return normSq > 0.98 && normSq < 1.02 &&
          Math.abs(transform.p[0]) < 200 && Math.abs(transform.p[1]) < 100 && Math.abs(transform.p[2]) < 200;
      }

      // The bridge target contains the native setter state.  Capture only
      // plausible PxTransform-shaped windows so we can identify the exact
      // quaternion used for the velocity-space rotation without dumping it.
      function setterBridgeTransformCandidates(view, slots) {
        if (!view || !slots) return [];
        var seen = {};
        return slots.map(function (slot) {
          var candidates = [];
          for (var offset = 0; offset <= 1024 - 28; offset += 4) {
            var transform = decodeTransformCandidate(view, slot.ptr + offset);
            if (!finiteTransformCandidate(transform)) continue;
            var key = transform.q.join(",") + ":" + transform.p.join(",");
            if (seen[slot.ptr + ":" + key]) continue;
            seen[slot.ptr + ":" + key] = true;
            candidates.push({ offset: offset, transform: transform });
          }
          return { ptr: slot.ptr, yOffset: slot.yOffset, candidates: candidates.slice(0, 24) };
        });
      }

      var name = "A0.Rigidbody.set_angularVelocity.native." + index;
      var existing = existingHook(index, name);
      if (existing) return existing;
      return probe.installTableHook(index, name, {
        signature: "vii",
        traceCallEvent: false,
        beforeCall: function beforeAngularVelocitySetter(args) {
          var tick = state.currentTick;
          var view = dataView();
          var vector = view ? vector3At(view, args[1]) : null;
          if (!vector) return;
          state.angularWriteSerial += 1;
          state.lastAngularWrite = {
            writeSerial: state.angularWriteSerial,
            tickSerial: tick ? tick.tickSerial : null,
            controller: tick ? tick.controller : null,
            movingCurling: tick ? tick.movingCurling : null,
            bodyManagedPtr: sanitizeArg(args[0]),
            bodyNativePtr: view ? managedCachedPtr(view, args[0]) : null,
            scriptInputs: tick ? {
              linearVelocity: tick.lastLinearVelocityRead || null,
              angularVelocity: tick.lastAngularVelocityRead || null
            } : null,
            vector: vector,
            wy: vector[1],
            tableIndex: index
          };
          state.lastAngularWrites.push(state.lastAngularWrite);
          if (state.lastAngularWrites.length > 2) state.lastAngularWrites.shift();
          var release = probe.pendingReleaseProtocol;
          if (state.a10ReleaseOrientationEnabled && release &&
              release.serial > state.a10CapturedReleaseSerial && view) {
            // This runs before the first DCP angular setter of the commanded
            // release.  It is therefore the reset-preserved orientation, not
            // a pose inferred later from endpoint behavior.
            var releaseCore = findA9BodyCoreFromNative(view, state.lastAngularWrite.bodyNativePtr);
            var releaseBridgePose = findA10BridgePose(view, state.lastAngularWrite.bodyNativePtr);
            pushEvent("a10.release_reset_orientation", {
              release: release,
              tickSerial: tick ? tick.tickSerial : null,
              bodyManagedPtr: state.lastAngularWrite.bodyManagedPtr,
              bodyNativePtr: state.lastAngularWrite.bodyNativePtr,
              coreBeforeAngularSetter: releaseCore ? releaseCore.core : null,
              corePath: releaseCore ? releaseCore.path : null,
              bridgePoseBeforeAngularSetter: releaseBridgePose
            });
            state.a10CapturedReleaseSerial = release.serial;
          }
          if (state.a2StaticTraceEnabled && !state.a2StaticTraceArmed && tick) {
            state.a2StaticTraceArmed = true;
            state.a2StaticTraceRows = [];
            state.a2StaticTraceByTick = {};
          }
          if (state.a8StaticWindowEnabled && !Number.isInteger(state.a8StaticWindowStartTick) && tick) {
            state.a8StaticWindowStartTick = tick.tickSerial;
          }
          if (state.a9SnapshotWindowEnabled && !Number.isInteger(state.a9SnapshotWindowStartTick) && tick) {
            state.a9SnapshotWindowStartTick = tick.tickSerial;
          }
          if (isA9SnapshotWindowTick(tick) && view && tick) {
            // Do not infer a PxsBodyCore from pointer-shaped bytes. The previous
            // A9 scan was rejected: this captures only an observable setter delta.
            state.lastAngularWrite.a9NativeBefore = snapshotNativeBody(
              view, state.lastAngularWrite.bodyNativePtr
            );
            state.lastAngularWrite.bridgeTransformCandidatesBefore =
              setterBridgeTransformCandidates(view, state.a9SetterBridgeSlots);
            // installTableHook exposes one persistent hook record, not a
            // per-call record, so keep this synchronous call's snapshot here.
            state.a9PendingAngularWrite = state.lastAngularWrite;
          }
          if (tick) tick.angularWriteCount = (tick.angularWriteCount || 0) + 1;
        },
        afterCall: function afterAngularVelocitySetter(args, result, record) {
          var write = state.a9PendingAngularWrite;
          var tick = state.currentTick;
          if (!write || !isA9SnapshotWindowTick(tick)) return;
          var view = dataView();
          var after = view ? snapshotNativeBody(
            view, write.bodyNativePtr, write.a9NativeBefore && write.a9NativeBefore.targets
          ) : null;
          var delta = diffNativeBody(write.a9NativeBefore, after);
          var slots = setterMatchingSlots(delta, write.wy);
          if (slots.length) state.a9SetterBridgeSlots = slots;
          var bridgeAfterSetter = readSetterBridgeSlots(view, state.a9SetterBridgeSlots);
          state.a9LastBridgeAfterSetter = {
            tickSerial: write.tickSerial,
            slots: bridgeAfterSetter
          };
          pushEvent("a9.angular_setter_native_delta", {
            tickSerial: write.tickSerial,
            angularWriteSerial: write.writeSerial,
            setterWy: write.wy,
            bodyManagedPtr: write.bodyManagedPtr,
            bodyNativePtr: write.bodyNativePtr,
            sourceVectorBefore: write.vector,
            sourceVectorAfter: view ? vector3At(view, args[1]) : null,
            changedRanges: delta ? delta.rootRanges : null,
            targetDeltas: delta ? delta.targetDeltas : null,
            bridgeAfterSetter: bridgeAfterSetter,
            bridgeTransformCandidatesBefore: write.bridgeTransformCandidatesBefore
          });
          state.a9PendingAngularWrite = null;
        }
      });
    }

    function installLinearVelocitySetter(index) {
      var name = "A2.Rigidbody.set_velocity.native." + index;
      var existing = existingHook(index, name);
      if (existing) return existing;
      return probe.installTableHook(index, name, {
        signature: "vii",
        traceCallEvent: false,
        beforeCall: function beforeLinearVelocitySetter(args) {
          var tick = state.currentTick;
          var view = dataView();
          var vector = view ? vector3At(view, args[1]) : null;
          if (!vector) return;
          state.lastLinearWrite = {
            tickSerial: tick ? tick.tickSerial : null,
            bodyManagedPtr: sanitizeArg(args[0]),
            bodyNativePtr: view ? managedCachedPtr(view, args[0]) : null,
            vector: vector,
            tableIndex: index
          };
        }
      });
    }

    function allocatorForQuaternionScratch() {
      var candidates = findLikelyModules();
      for (var i = 0; i < candidates.length; i += 1) {
        var module = candidates[i].module;
        if (module && typeof module._malloc === "function" && typeof module._free === "function") {
          return { alloc: module._malloc, free: module._free, source: candidates[i].key + "._malloc" };
        }
      }
      // This WebGL build exposes malloc/free from the raw Wasm instance rather
      // than from Emscripten's public Module facade.  Keep the fallback tied to
      // the instance observed by the probe, so it cannot silently use memory
      // from an unrelated Wasm module on the page.
      for (var j = probe.instances.length - 1; j >= 0; j -= 1) {
        var instance = probe.instances[j] && probe.instances[j].instance;
        var exports = instance && instance.exports;
        if (exports && typeof exports.malloc === "function" && typeof exports.free === "function") {
          return { alloc: exports.malloc, free: exports.free, source: probe.instances[j].source + ".exports" };
        }
      }
      return null;
    }

    function withQuaternionScratch(callback) {
      var allocator = allocatorForQuaternionScratch();
      if (!allocator) throw new Error("no wasm allocator");
      var scratch = allocator.alloc(16);
      try {
        var view = dataView();
        if (!view || !inMemoryRange(view, scratch, 16)) throw new Error("invalid quaternion scratch");
        return callback(view, scratch);
      } finally {
        allocator.free(scratch);
      }
    }

    function readTransformRotation(getRotation, transformManagedPtr) {
      return withQuaternionScratch(function (view, scratch) {
        getRotation(transformManagedPtr, scratch);
        return [
          readF32LE(view, scratch), readF32LE(view, scratch + 4),
          readF32LE(view, scratch + 8), readF32LE(view, scratch + 12)
        ];
      });
    }

    function writeTransformRotation(setRotation, transformManagedPtr, quaternion) {
      return withQuaternionScratch(function (view, scratch) {
        for (var i = 0; i < 4; i += 1) view.setFloat32(scratch + i * 4, quaternion[i], true);
        setRotation(transformManagedPtr, scratch);
      });
    }

    function restoreResetRotation(args, reset, positionWrite) {
      if (!state.resetAllStoneRotationsEnabled || !reset || !positionWrite) return;
      if ((reset.rotationRestoreCount || 0) >= 16) return;
      var key = String(args[0]);
      var baseline = state.resetRotationBaselineByBody[key];
      var tableRecord = probe.tables[probe.tables.length - 1];
      var table = tableRecord && tableRecord.table;
      if (!table) {
        pushEvent("reset.rotation_restore_failed", {
          resetSerial: reset.serial,
          transformManagedPtr: sanitizeArg(args[0]),
          reason: "no wasm table"
        });
        return;
      }
      var getRotation = table.get(transformRotationGetterTableIndex);
      var setRotation = table.get(transformRotationSetterTableIndex);
      if (typeof getRotation !== "function" || typeof setRotation !== "function") {
        pushEvent("reset.rotation_restore_failed", {
          resetSerial: reset.serial,
          transformManagedPtr: sanitizeArg(args[0]),
          reason: "missing Transform rotation getter/setter"
        });
        return;
      }
      try {
        var startedAtMs = performance.now();
        if (!baseline) {
          if ((reset.rotationBaselineCount || 0) >= 16) return;
          baseline = readTransformRotation(getRotation, args[0]);
          state.resetRotationBaselineByBody[key] = baseline;
          reset.rotationBaselineCount = (reset.rotationBaselineCount || 0) + 1;
          pushEvent("reset.rotation_baseline_captured", {
            resetSerial: reset.serial,
            transformManagedPtr: sanitizeArg(args[0]),
            quaternionXyzw: baseline,
            durationMs: performance.now() - startedAtMs
          });
          return;
        }
        writeTransformRotation(setRotation, args[0], baseline);
        reset.rotationRestoreCount = (reset.rotationRestoreCount || 0) + 1;
        var after = readTransformRotation(getRotation, args[0]);
        pushEvent("reset.rotation_restored", {
          resetSerial: reset.serial,
          transformManagedPtr: sanitizeArg(args[0]),
          quaternionXyzw: baseline,
          quaternionAfterXyzw: after,
          durationMs: performance.now() - startedAtMs
        });
      } catch (err) {
        pushEvent("reset.rotation_restore_failed", {
          resetSerial: reset.serial,
          transformManagedPtr: sanitizeArg(args[0]),
          reason: err.message
        });
      }
    }

    function installTransformPositionSetter(index) {
      var name = "A10.Transform.set_position.native." + index;
      var existing = existingHook(index, name);
      if (existing) return existing;
      return probe.installTableHook(index, name, {
        signature: "vii",
        traceCallEvent: false,
        beforeCall: function beforeTransformPositionSetter(args, record) {
          if (!state.a10ReleaseOrientationEnabled && !state.resetAllStoneRotationsEnabled) return;
          var reset = probe.lastResetProtocol;
          if (!reset || !/^RESETPOSITION(?:\s|$)/.test(reset.text || "")) return;
          if (!Array.isArray(reset.positionWrites)) reset.positionWrites = [];
          // A reset writes at most the sixteen curling bodies.  Keeping a
          // tight bound ensures unrelated scene placement cannot turn this
          // evidence hook into an unbounded trace.
          if (reset.positionWrites.length >= 32) return;
          var view = dataView();
          reset.positionWrites.push({
            writeOrdinal: reset.positionWrites.length,
            transformManagedPtr: sanitizeArg(args[0]),
            sourceVector: view ? vector3At(view, args[1]) : null
          });
          record.__resetPositionWrite = {
            reset: reset,
            positionWrite: reset.positionWrites[reset.positionWrites.length - 1]
          };
        },
        afterCall: function afterTransformPositionSetter(args, result, record) {
          var resetWrite = record.__resetPositionWrite;
          record.__resetPositionWrite = null;
          if (!resetWrite) return;
          restoreResetRotation(args, resetWrite.reset, resetWrite.positionWrite);
        }
      });
    }

    function installVelocityGetter(kind, index) {
      var name = "A0.Rigidbody.get_" + kind + ".native." + index;
      var existing = existingHook(index, name);
      if (existing) return existing;
      return probe.installTableHook(index, name, {
        signature: "vii",
        traceCallEvent: false,
        afterCall: function afterVelocityGetter(args) {
          var tick = state.currentTick;
          if (!tick) return;
          var view = dataView();
          var vector = view ? vector3At(view, args[1]) : null;
          if (!vector) return;
          var read = {
            bodyManagedPtr: sanitizeArg(args[0]),
            bodyNativePtr: managedCachedPtr(view, args[0]),
            vector: vector,
            tableIndex: index
          };
          if (kind === "velocity") tick.lastLinearVelocityRead = read;
          else tick.lastAngularVelocityRead = read;
        }
      });
    }

    function installFrictionNoiseCapture() {
      function installRngInitHook() {
        if (state.rngInitHook) return state.rngInitHook;
        var name = "RNG.Random.InitState.seed_gate";
        var existing = existingHook(randomInitStateTableIndex, name);
        if (existing) {
          state.rngInitHook = existing;
          return existing;
        }
        state.rngInitHook = probe.installTableHook(randomInitStateTableIndex, name, {
          signature: "vi",
          traceCallEvent: false,
          beforeCall: function beforeRandomInitState(args) {
            pushEvent("rng.random_init_state", { seed: sanitizeArg(args[0]) });
          }
        });
        return state.rngInitHook;
      }

      if (state.rngSeedOnFirstFriction !== null) installRngInitHook();
      var name = "A0.UnityEngine.Random.Range.friction_ring";
      var existing = existingHook(randomRangeTableIndex, name);
      if (existing) return existing;
      return probe.installTableHook(randomRangeTableIndex, name, {
        signature: "fff",
        traceCallEvent: false,
        beforeCall: function beforeFrictionRandomRange(args) {
          if (Math.abs(Number(args[0]) + 0.0002) > 1e-7 ||
              Math.abs(Number(args[1]) - 0.0002) > 1e-7 ||
              state.rngSeedOnFirstFriction === null || state.rngSeedApplied) return;
          var initHook = installRngInitHook();
          if (!initHook || !initHook.tableRecord || !initHook.tableRecord.table) {
            pushEvent("rng.seed_apply_failed", { seed: state.rngSeedOnFirstFriction, reason: "init_state_hook_unavailable" });
            return;
          }
          try {
            // Invoke the current table entry rather than the saved original so
            // the applied seed is independently recorded in the event stream.
            initHook.tableRecord.table.get(randomInitStateTableIndex)(state.rngSeedOnFirstFriction);
            state.rngSeedApplied = true;
            pushEvent("rng.seed_applied", {
              seed: state.rngSeedOnFirstFriction,
              frictionNoiseSerialBefore: state.frictionNoiseSerial,
              tickSerial: state.currentTick && state.currentTick.tickSerial
            });
          } catch (err) {
            pushEvent("rng.seed_apply_failed", { seed: state.rngSeedOnFirstFriction, reason: err.message });
          }
        },
        overrideCall: function overrideFrictionRandomRange(args) {
          if (Math.abs(Number(args[0]) + 0.0002) > 1e-7 ||
              Math.abs(Number(args[1]) - 0.0002) > 1e-7 ||
              !state.rngFrictionManifest) return null;
          if (!state.rngFrictionManifestApplied) {
            state.rngFrictionManifestApplied = true;
            pushEvent("rng.friction_manifest_applied", {
              source: state.rngFrictionManifestSource,
              drawCount: state.rngFrictionManifest.length,
              tickSerial: state.currentTick && state.currentTick.tickSerial
            });
          }
          var index = state.rngFrictionManifestIndex;
          if (index >= state.rngFrictionManifest.length) {
            if (!state.rngFrictionManifestExhausted) {
              state.rngFrictionManifestExhausted = true;
              pushEvent("rng.friction_manifest_exhausted", {
                drawCount: state.rngFrictionManifest.length,
                attemptedIndex: index,
                tickSerial: state.currentTick && state.currentTick.tickSerial
              });
            }
            // Keep the game alive for forensic output, but the exhaustion
            // event invalidates this run as a strict replay fixture.
            return null;
          }
          var value = Number(state.rngFrictionManifest[index]);
          state.rngFrictionManifestIndex += 1;
          // A table-call override does not reliably reach ``afterCall`` in
          // every WebAssembly hook backend.  Emit the substituted draw here
          // as the canonical sliding event so the local P6 replay receives
          // exactly the same per-shot manifest values as Unity.
          pushEvent("sliding.random_range.friction", {
            callIndex: null,
            randomRangeCalls: null,
            frictionRangeCalls: state.rngFrictionManifestIndex,
            min: Number(args[0]),
            max: Number(args[1]),
            value: value,
            inferredNoSweepFriction: 0.001 + value,
            inferredSweepFriction: 0.0006 + value,
            manifestOverride: true
          });
          if (state.rngFrictionManifestIndex === state.rngFrictionManifest.length) {
            pushEvent("rng.friction_manifest_last_draw", {
              drawCount: state.rngFrictionManifest.length,
              tickSerial: state.currentTick && state.currentTick.tickSerial
            });
          }
          return { handled: true, result: value };
        },
        afterCall: function afterFrictionRandomRange(args, result) {
          if (Math.abs(Number(args[0]) + 0.0002) > 1e-7 ||
              Math.abs(Number(args[1]) - 0.0002) > 1e-7) return;
          var tick = state.currentTick;
          state.frictionNoiseSerial += 1;
          state.lastFrictionNoise = {
            noiseSerial: state.frictionNoiseSerial,
            tickSerial: tick ? tick.tickSerial : null,
            controller: tick ? tick.controller : null,
            value: Number(result)
          };
          state.lastFrictionNoises.push(state.lastFrictionNoise);
          if (state.lastFrictionNoises.length > 2) state.lastFrictionNoises.shift();
        }
      });
    }

    function installC54StaticSolve() {
      var name = "C54.solveContact_BStaticBlock.intercall";
      var existing = existingHook(staticSolveTableIndex, name);
      if (existing) return existing;
      return probe.installTableHook(staticSolveTableIndex, name, {
        signature: "viii",
        traceCallEvent: false,
        beforeCall: function beforeC54StaticSolve(args, record) {
          var view = dataView();
          if (!view || !state.c54IntercallStaticEnabled || !state.c04CurrentFrame || !c31KeepsRawSolverFrame() ||
              state.c04CurrentFrame.staticSolves.length >= 64) return;
          record.__c54StaticSolve = {
            sequence: state.c04CurrentFrame.solveSequence++,
            before: captureC54StaticSolve(view, args,
              "c04." + state.c04CurrentFrame.frameIndex + ".before")
          };
        },
        afterCall: function afterC54StaticSolve(args, result, record) {
          var row = record.__c54StaticSolve;
          var view = dataView();
          if (row && state.c04CurrentFrame && view) {
            row.after = captureC54StaticSolve(view, args,
              "c04." + state.c04CurrentFrame.frameIndex + ".after");
            state.c04CurrentFrame.staticSolves.push(row);
          }
          record.__c54StaticSolve = null;
        }
      });
    }

    function installStaticWritebackRing() {
      var name = "A0.solveContact_BStaticBlockWithWriteback.ring";
      var existing = existingHook(staticWritebackTableIndex, name);
      if (existing) return existing;
      return probe.installTableHook(staticWritebackTableIndex, name, {
        signature: "viii",
        traceCallEvent: false,
        beforeCall: function beforeStaticWriteback(args, record) {
          var view = dataView();
          if (!view) return;
          if (state.c54IntercallStaticEnabled && state.c04CurrentFrame && c31KeepsRawSolverFrame() &&
              state.c04CurrentFrame.staticWritebacks.length < 32) {
            record.__c54StaticWriteback = {
              sequence: state.c04CurrentFrame.solveSequence++,
              solverContextPtr: sanitizeArg(args[2]),
              before: captureC54StaticSolve(view, args,
                "c04." + state.c04CurrentFrame.frameIndex + ".writeback.before")
            };
            return;
          }
          if (state.c26TargetStaticEnabled && state.c04CurrentFrame &&
              state.c04CurrentFrame.frameIndex === state.c26TargetStaticFrame) {
            record.__c26Static = {
              solverContextPtr: sanitizeArg(args[2]),
              before: dumpSolverConstraintDescs(view, "C26.static.before", args[0], {
                // Static contact blocks are 37*16=592 bytes in the captured
                // 14000 frame.  The former 256-byte preview cannot reach all
                // five normal rows / four friction rows, so it cannot support
                // a Unity/local field closure.  This remains a bounded,
                // selected-frame capture (at most four descriptors).
                solverDescRecords: 4, solverBodyBytes: 128, solverConstraintBytes: 640,
                includeRawBytes: true, contactPreviewCount: 4
              })
            };
            record.__c26Static.bodyDataBefore = staticSolverBodyDataSnapshots(
              view, args[2], record.__c26Static.before);
            return;
          }
          var tick = state.lastAngularWrite;
          if (isA8StaticWindowTick(tick)) {
            record.__a8StaticWindow = {
              tickSerial: tick.tickSerial,
              angularWriteSerial: tick.writeSerial,
              setterWy: tick.wy,
              solverContextPtr: args[2],
              before: dumpSolverConstraintDescs(view, "A8.static.before", args[0], {
                solverDescRecords: 1,
                solverBodyBytes: 128,
                solverConstraintBytes: 256,
                includeRawBytes: false,
                contactPreviewCount: 4
              })
            };
            record.__a8StaticWindow.bridgeAfterSetter = state.a9LastBridgeAfterSetter &&
              state.a9LastBridgeAfterSetter.tickSerial === tick.tickSerial
              ? state.a9LastBridgeAfterSetter.slots : null;
            record.__a8StaticWindow.bridgeAtStaticEntry = (state.a9SetterBridgeSlots || []).map(function (slot) {
              return {
                ptr: slot.ptr,
                yOffset: slot.yOffset,
                xyz: [
                  readF32LE(view, slot.ptr + slot.yOffset - 4),
                  readF32LE(view, slot.ptr + slot.yOffset),
                  readF32LE(view, slot.ptr + slot.yOffset + 4)
                ]
              };
            });
            record.__a8StaticWindow.bodyDataBefore = staticSolverBodyDataSnapshots(
              view, args[2], record.__a8StaticWindow.before
            );
            return;
          }
          if (state.a2StaticTraceEnabled) {
            appendA2StaticTrace(view, args);
            return;
          }
          record.__a0StaticWriteback = {
            tickSerial: state.lastAngularWrite && state.lastAngularWrite.tickSerial,
            solverContextPtr: args[2],
            before: dumpSolverConstraintDescs(view, "A0.static.before", args[0], {
              solverDescRecords: 1,
              solverBodyBytes: 128,
              solverConstraintBytes: 128,
              includeRawBytes: false,
              contactPreviewCount: 0
            })
          };
          record.__a0StaticWriteback.bodyDataBefore = staticSolverBodyDataSnapshots(
            view, args[2], record.__a0StaticWriteback.before
          );
        },
        afterCall: function afterStaticWriteback(args, result, record) {
          var a8 = record.__a8StaticWindow;
          var c26 = record.__c26Static;
          var c54 = record.__c54StaticWriteback;
          var row = record.__a0StaticWriteback;
          var view = dataView();
          if (!view) return;
          if (c54) {
            c54.after = captureC54StaticSolve(view, args,
              "c04." + state.c04CurrentFrame.frameIndex + ".writeback.after");
            state.c04CurrentFrame.staticWritebacks.push(c54);
            record.__c54StaticWriteback = null;
            return;
          }
          if (c26) {
            c26.after = dumpSolverConstraintDescs(view, "C26.static.after", args[0], {
              solverDescRecords: 4, solverBodyBytes: 128, solverConstraintBytes: 640,
              includeRawBytes: true, contactPreviewCount: 4
            });
            c26.bodyDataAfter = staticSolverBodyDataSnapshots(view, c26.solverContextPtr, c26.after);
            state.c04CurrentFrame.c26StaticWritebacks.push(c26);
            record.__c26Static = null;
            return;
          }
          if (a8) {
            a8.after = dumpSolverConstraintDescs(view, "A8.static.after", args[0], {
              solverDescRecords: 1,
              solverBodyBytes: 128,
              solverConstraintBytes: 256,
              includeRawBytes: false,
              contactPreviewCount: 4
            });
            a8.bodyDataAfter = staticSolverBodyDataSnapshots(view, a8.solverContextPtr, a8.after);
            pushEvent("a8.static_contact_window", a8);
            record.__a8StaticWindow = null;
            return;
          }
          if (!row) return;
          row.after = dumpSolverConstraintDescs(view, "A0.static.after", args[0], {
            solverDescRecords: 1,
            solverBodyBytes: 128,
            solverConstraintBytes: 128,
            includeRawBytes: false,
            contactPreviewCount: 0
          });
          row.bodyDataAfter = staticSolverBodyDataSnapshots(view, row.solverContextPtr, row.after);
          state.staticWritebackRing.push(row);
          if (state.staticWritebackRing.length > 8) state.staticWritebackRing.shift();
          record.__a0StaticWriteback = null;
        }
      });
    }

    // PxsBodyCore is binary-stable in PhysX 4.1 wasm32.  Rather than assume the
    // Cm::Task base size, scan the small preIntegrate task header for its body-core
    // pointer array and select the moving core by planar velocity.
    function decodeA9BodyCore(view, corePtr) {
      if (!isPointerLike(view, corePtr, 160)) return null;
      var linearVelocity = vector3At(view, corePtr + 64);
      var angularVelocity = vector3At(view, corePtr + 80);
      var pose = decodeTransformCandidate(view, corePtr);
      var maxAngularVelocitySq = readF32LE(view, corePtr + 96);
      var angularDamping = readF32LE(view, corePtr + 108);
      var values = (linearVelocity || []).concat(angularVelocity || [], pose ? pose.p : [], pose ? pose.q : []);
      var quaternionNormSq = pose ? pose.q[0] * pose.q[0] + pose.q[1] * pose.q[1] +
        pose.q[2] * pose.q[2] + pose.q[3] * pose.q[3] : 0;
      if (!linearVelocity || !angularVelocity || !pose ||
          !Number.isFinite(maxAngularVelocitySq) || !Number.isFinite(angularDamping) ||
          !values.every(Number.isFinite) ||
          Math.abs(pose.p[0]) > 200 || pose.p[1] < 5 || pose.p[1] > 30 || Math.abs(pose.p[2]) > 200 ||
          Math.abs(linearVelocity[0]) > 20 || Math.abs(linearVelocity[1]) > 20 || Math.abs(linearVelocity[2]) > 20 ||
          Math.abs(angularVelocity[0]) > 10 || Math.abs(angularVelocity[1]) > 10 || Math.abs(angularVelocity[2]) > 10 ||
          quaternionNormSq < 0.95 || quaternionNormSq > 1.05 ||
          angularDamping < 0 || angularDamping > 1 ||
          maxAngularVelocitySq < 0.1 || maxAngularVelocitySq > 1e5) return null;
      return {
        ptr: corePtr,
        p: pose.p,
        q: pose.q,
        linearVelocity: linearVelocity,
        angularVelocity: angularVelocity,
        maxAngularVelocitySq: maxAngularVelocitySq,
        angularDamping: angularDamping,
        lockFlags: view.getUint8(corePtr + 158)
      };
    }

    function findA9MovingBodyCore(view, taskPtr) {
      if (!isPointerLike(view, taskPtr, 256)) return null;
      var best = null;
      for (var taskOffset = 0; taskOffset <= 252; taskOffset += 4) {
        var bodyArrayPtr = readU32LE(view, taskPtr + taskOffset);
        if (!isPointerLike(view, bodyArrayPtr, 4)) continue;
        for (var bodyIndex = 0; bodyIndex < 32; bodyIndex += 1) {
          var corePtr = readU32LE(view, bodyArrayPtr + bodyIndex * 4);
          var core = decodeA9BodyCore(view, corePtr);
          if (!core) continue;
          var planarSpeedSq = core.linearVelocity[0] * core.linearVelocity[0] +
            core.linearVelocity[2] * core.linearVelocity[2];
          if (planarSpeedSq < 0.01) continue;
          if (!best || planarSpeedSq > best.planarSpeedSq) {
            best = {
              taskFieldOffset: taskOffset,
              bodyArrayPtr: bodyArrayPtr,
              bodyIndex: bodyIndex,
              planarSpeedSq: planarSpeedSq,
              core: core
            };
          }
        }
      }
      return best;
    }

    function findA9BodyCoreFromNative(view, nativePtr) {
      if (!isPointerLike(view, nativePtr, 4)) return null;
      var queue = [{ ptr: nativePtr, depth: 0, path: [nativePtr] }];
      var seen = {};
      var best = null;
      while (queue.length) {
        var current = queue.shift();
        if (seen[current.ptr]) continue;
        seen[current.ptr] = true;
        var core = decodeA9BodyCore(view, current.ptr);
        if (core) {
          var speedSq = core.linearVelocity[0] * core.linearVelocity[0] +
            core.linearVelocity[2] * core.linearVelocity[2];
          if (!best || speedSq > best.planarSpeedSq) {
            best = { core: core, planarSpeedSq: speedSq, path: current.path.slice() };
          }
        }
        if (current.depth >= 2 || !isPointerLike(view, current.ptr, 256)) continue;
        for (var offset = 0; offset < 256; offset += 4) {
          var child = readU32LE(view, current.ptr + offset);
          if (isPointerLike(view, child, 160) && !seen[child]) {
            queue.push({ ptr: child, depth: current.depth + 1, path: current.path.concat([child]) });
          }
        }
      }
      return best;
    }

    function a10PlausibleSceneTransform(transform) {
      if (!transform || !transform.q || !transform.p) return false;
      var values = transform.q.concat(transform.p);
      if (!values.every(Number.isFinite)) return false;
      var normSq = transform.q.reduce(function (sum, value) { return sum + value * value; }, 0);
      return normSq > 0.98 && normSq < 1.02 &&
        Math.abs(transform.p[0]) < 200 && transform.p[1] > 5 && transform.p[1] < 30 &&
        Math.abs(transform.p[2]) < 200;
    }

    function findA10BridgePose(view, nativePtr) {
      // The verified Rigidbody root points to its Scb bridge at +52 and that
      // bridge holds the setter pose at +80.  Keep the scan bounded so this
      // remains a passive, low-volume fallback across build-layout variants.
      if (!isPointerLike(view, nativePtr, 256)) return null;
      var candidates = [];
      var rootOffsets = [52];
      for (var rootOffset = 0; rootOffset <= 252; rootOffset += 4) {
        if (rootOffset !== 52) rootOffsets.push(rootOffset);
      }
      for (var i = 0; i < rootOffsets.length; i += 1) {
        var childPtr = readU32LE(view, nativePtr + rootOffsets[i]);
        if (!isPointerLike(view, childPtr, 512)) continue;
        for (var childOffset = 0; childOffset <= 484; childOffset += 4) {
          var transform = decodeTransformCandidate(view, childPtr + childOffset);
          if (!a10PlausibleSceneTransform(transform)) continue;
          candidates.push({
            ptr: childPtr,
            rootOffset: rootOffsets[i],
            offset: childOffset,
            transform: transform,
            score: (rootOffsets[i] === 52 ? 1000 : 0) + (childOffset === 80 ? 100 : 0) -
              Math.abs(transform.p[1] - 14.4197845)
          });
        }
      }
      candidates.sort(function (left, right) { return right.score - left.score; });
      return candidates.length ? candidates[0] : null;
    }

    function installPhaseOrderTask(index, phaseName) {
      var name = "A1.3." + phaseName + ".phase_order";
      var existing = existingHook(index, name);
      if (existing) return existing;
      return probe.installTableHook(index, name, {
        signature: "vi",
        traceCallEvent: false,
        beforeCall: function beforeA13PhaseTask(args, record) {
          state.phaseOrderSerial += 1;
          record.__a13Phase = {
            phaseSerial: state.phaseOrderSerial,
            phase: phaseName,
            edge: "enter",
            tableIndex: index,
            taskPtr: sanitizeArg(args[0]),
            lastAngularWriteSerial: state.lastAngularWrite && state.lastAngularWrite.writeSerial,
            lastAngularWriteTick: state.lastAngularWrite && state.lastAngularWrite.tickSerial,
            lastAngularWriteWy: state.lastAngularWrite && state.lastAngularWrite.wy
          };
          state.phaseOrderRing.push(record.__a13Phase);
          if (state.phaseOrderRing.length > 8) state.phaseOrderRing.shift();
          appendPhaseForAngularWrite(record.__a13Phase);
          var tick = state.lastAngularWrite;
          if (phaseName === "PxsDynamics.solverSetupSolve" && state.c03Armed &&
              state.c03Manager && !state.c03Flushed) {
            var c03EntryView = dataView();
            if (c03EntryView) {
              state.c03Manager.coresAtSolverSetupEntry = [
                c03CoreSnapshot(c03EntryView, state.c03Manager.contactManager.rigidCore0,
                  "C03.rigidCore0.solverSetupEntry"),
                c03CoreSnapshot(c03EntryView, state.c03Manager.contactManager.rigidCore1,
                  "C03.rigidCore1.solverSetupEntry")
              ];
            }
          }
          if (phaseName === "PxsDynamics.solverSetupSolve" && state.c04DynamicWindowEnabled &&
              state.c03Armed && state.c03Manager &&
              state.c04DynamicFrames.length < state.c04DynamicWindowLimit) {
            var c04EntryView = dataView();
            state.c04CurrentFrame = {
              frameIndex: state.c04DynamicFrames.length,
              tickSerial: tick && tick.tickSerial,
              angularWriteSerial: tick && tick.writeSerial,
              phaseEntry: state.phaseOrderRing.slice(),
              entryCores: c04EntryView ? [
                state.c31CompactCoreTraceEnabled
                  ? c31CompactCoreSnapshot(c04EntryView, state.c03Manager.contactManager.rigidCore0)
                  : c03CoreSnapshot(c04EntryView, state.c03Manager.contactManager.rigidCore0,
                    "C04.rigidCore0.solverSetupEntry." + state.c04DynamicFrames.length),
                state.c31CompactCoreTraceEnabled
                  ? c31CompactCoreSnapshot(c04EntryView, state.c03Manager.contactManager.rigidCore1)
                  : c03CoreSnapshot(c04EntryView, state.c03Manager.contactManager.rigidCore1,
                    "C04.rigidCore1.solverSetupEntry." + state.c04DynamicFrames.length)
              ] : null,
              solveSequence: 0,
              dynamicSolves: [],
              dynamicWritebacks: [],
              staticSolves: [],
              staticWritebacks: [],
              c26StaticWritebacks: []
            };
          }
          if (phaseName === "PxsDynamics.preIntegrate" && isA9SnapshotWindowTick(tick) &&
              !state.a9CapturedPreIntegrateTicks[tick.tickSerial]) {
            var view = dataView();
            var before = view ? findA9MovingBodyCore(view, args[0]) : null;
            state.a9CapturedPreIntegrateTicks[tick.tickSerial] = true;
            if (before) {
              record.__a9PreIntegrateCore = {
                tickSerial: tick.tickSerial,
                angularWriteSerial: tick.writeSerial,
                setterWy: tick.wy,
                taskPtr: sanitizeArg(args[0]),
                taskFieldOffset: before.taskFieldOffset,
                bodyArrayPtr: before.bodyArrayPtr,
                bodyIndex: before.bodyIndex,
                planarSpeedSq: before.planarSpeedSq,
                coreBefore: before.core
              };
            } else if (!state.a9UnresolvedTaskEmitted && view) {
              state.a9UnresolvedTaskEmitted = true;
              pushEvent("a9.preintegrate_task_unresolved", {
                tickSerial: tick.tickSerial,
                angularWriteSerial: tick.writeSerial,
                setterWy: tick.wy,
                taskPtr: sanitizeArg(args[0]),
                taskWindow: probe.dumpMemoryWindow("A9.preIntegrate.task", args[0], 256, {
                  includeRawBytes: true,
                  pointerScanBytes: 256,
                  pointerTargetBytes: 32
                })
              });
            }
          }
          if (phaseName === "PxsDynamics.solverSetupSolve" && isA9SnapshotWindowTick(tick) &&
              !state.a9CapturedSolverSetupTicks[tick.tickSerial]) {
            state.a9CapturedSolverSetupTicks[tick.tickSerial] = true;
            var setterCore = state.a9SetterCoreByTick[tick.tickSerial];
            var solverSetupView = dataView();
            var setupCore = setterCore && solverSetupView ?
              decodeA9BodyCore(solverSetupView, setterCore.core.ptr) : null;
            if (setterCore && setupCore) {
              pushEvent("a9.native_core_to_solver_setup", {
                tickSerial: tick.tickSerial,
                angularWriteSerial: tick.writeSerial,
                setterWy: tick.wy,
                bodyNativePtr: tick.bodyNativePtr,
                corePath: setterCore.path,
                planarSpeedSq: setterCore.planarSpeedSq,
                coreAfterSetter: setterCore.core,
                coreBeforeSolverSetup: setupCore
              });
            }
          }
        },
        afterCall: function afterA13PhaseTask(args, result, record) {
          if (!record.__a13Phase) return;
          state.phaseOrderSerial += 1;
          var phaseEdge = {
            phaseSerial: state.phaseOrderSerial,
            phase: phaseName,
            edge: "exit",
            tableIndex: index,
            taskPtr: sanitizeArg(args[0]),
            lastAngularWriteSerial: state.lastAngularWrite && state.lastAngularWrite.writeSerial,
            lastAngularWriteTick: state.lastAngularWrite && state.lastAngularWrite.tickSerial,
            lastAngularWriteWy: state.lastAngularWrite && state.lastAngularWrite.wy
          };
          state.phaseOrderRing.push(phaseEdge);
          if (state.phaseOrderRing.length > 8) state.phaseOrderRing.shift();
          appendPhaseForAngularWrite(phaseEdge);
          if (phaseName === "PxsDynamics.solverSetupSolve" && state.c03Armed &&
              state.c03DynamicSolve && state.c03Manager && !state.c03Flushed) {
            var c03ExitView = dataView();
            if (c03ExitView) {
              state.c03Manager.coresAfterSolverSetup = [
                c03CoreSnapshot(c03ExitView, state.c03Manager.contactManager.rigidCore0,
                  "C03.rigidCore0.afterSolverSetup"),
                c03CoreSnapshot(c03ExitView, state.c03Manager.contactManager.rigidCore1,
                  "C03.rigidCore1.afterSolverSetup")
              ];
            }
            state.c03Flushed = true;
            pushEvent("c03.first_dynamic_writeback", {
              tickSerial: state.c03DynamicSolve.tickSerial,
              angularWriteSerial: state.c03DynamicSolve.angularWriteSerial,
              manager: state.c03Manager,
              pcmInput: state.c03PcmInput,
              dynamicSolve: state.c03DynamicSolve,
              phaseOrder: state.phaseOrderRing.slice()
            });
          }
          if (phaseName === "PxsDynamics.solverSetupSolve" && state.c04CurrentFrame) {
            var c04Frame = state.c04CurrentFrame;
            var c04ExitView = dataView();
            c04Frame.exitCores = c04ExitView ? [
              state.c31CompactCoreTraceEnabled
                ? c31CompactCoreSnapshot(c04ExitView, state.c03Manager.contactManager.rigidCore0)
                : c03CoreSnapshot(c04ExitView, state.c03Manager.contactManager.rigidCore0,
                  "C04.rigidCore0.solverSetupExit." + c04Frame.frameIndex),
              state.c31CompactCoreTraceEnabled
                ? c31CompactCoreSnapshot(c04ExitView, state.c03Manager.contactManager.rigidCore1)
                : c03CoreSnapshot(c04ExitView, state.c03Manager.contactManager.rigidCore1,
                  "C04.rigidCore1.solverSetupExit." + c04Frame.frameIndex)
            ] : null;
            c04Frame.phaseExit = state.phaseOrderRing.slice();
            state.c04DynamicFrames.push(c04Frame);
            if (state.c26TargetStaticEnabled && c04Frame.frameIndex === state.c26TargetStaticFrame) {
              pushEvent("c26.target_static_frame", {
                frameIndex: c04Frame.frameIndex,
                tickSerial: c04Frame.tickSerial,
                targetCoreEntry: c04Frame.entryCores && c04Frame.entryCores[1],
                targetCoreExit: c04Frame.exitCores && c04Frame.exitCores[1],
                staticWritebacks: c04Frame.c26StaticWritebacks
              });
            }
            state.c04CurrentFrame = null;
            pushEvent("c04.dynamic_solver_frame", c04Frame);
          }
          var a9 = record.__a9PreIntegrateCore;
          if (a9) {
            var view = dataView();
            a9.coreAfter = view ? decodeA9BodyCore(view, a9.coreBefore.ptr) : null;
            pushEvent("a9.preintegrate_core_window", a9);
            record.__a9PreIntegrateCore = null;
          }
          record.__a13Phase = null;
        }
      });
    }

    function appendPhaseForAngularWrite(phaseEdge) {
      var writeSerial = phaseEdge && phaseEdge.lastAngularWriteSerial;
      if (!Number.isInteger(writeSerial)) return;
      var bucket = state.phaseOrderByAngularWrite[writeSerial];
      if (!bucket) {
        bucket = [];
        state.phaseOrderByAngularWrite[writeSerial] = bucket;
      }
      bucket.push(phaseEdge);
      // A single fixed step may fan out to several solver tasks. Preserve the
      // first ordering evidence without turning this narrow probe into a task log.
      if (bucket.length > 16) bucket.shift();
      var keys = Object.keys(state.phaseOrderByAngularWrite)
        .map(function parseWriteKey(value) { return Number(value); })
        .filter(Number.isFinite)
        .sort(function ascending(a, b) { return a - b; });
      while (keys.length > 4) {
        delete state.phaseOrderByAngularWrite[keys.shift()];
      }
    }

    function installC03DynamicSolve(tableIndex, variant) {
      var name = "C03." + variant + ".first_dynamic_pair";
      var existing = existingHook(tableIndex, name);
      if (existing) return existing;
      return probe.installTableHook(tableIndex, name, {
        signature: "viii",
        traceCallEvent: false,
        beforeCall: function beforeC03DynamicSolve(args, record) {
          var view = dataView();
          if (!view) return;
          if (state.c03Armed && !state.c03Flushed && !state.c03DynamicSolve) {
            record.__c03DynamicSolve = {
              tickSerial: state.lastAngularWrite && state.lastAngularWrite.tickSerial,
              angularWriteSerial: state.lastAngularWrite && state.lastAngularWrite.writeSerial,
              phaseOrderAtEntry: state.phaseOrderRing.slice(),
              before: captureC03DynamicSolve(view, args, "before")
            };
          }
          if (state.c04CurrentFrame && c31KeepsRawSolverFrame() && state.c04CurrentFrame.dynamicSolves.length < 8) {
            record.__c04DynamicSolve = {
              sequence: state.c04CurrentFrame.solveSequence++,
              before: captureC03DynamicSolve(view, args,
                "c04." + state.c04CurrentFrame.frameIndex + ".before")
            };
          }
        },
        afterCall: function afterC03DynamicSolve(args, result, record) {
          var row = record.__c03DynamicSolve;
          var view = dataView();
          if (row && !state.c03Flushed && !state.c03DynamicSolve && view) {
            row.after = captureC03DynamicSolve(view, args, "after");
            row.phaseOrderAtExit = state.phaseOrderRing.slice();
            state.c03DynamicSolve = row;
          }
          var c04Row = record.__c04DynamicSolve;
          if (c04Row && state.c04CurrentFrame && view) {
            c04Row.after = captureC03DynamicSolve(view, args,
              "c04." + state.c04CurrentFrame.frameIndex + ".after");
            state.c04CurrentFrame.dynamicSolves.push(c04Row);
          }
          record.__c03DynamicSolve = null;
          record.__c04DynamicSolve = null;
        }
      });
    }

    function installC11DynamicWriteback(tableIndex, variant) {
      var name = "C11." + variant + ".dynamic_tail";
      var existing = existingHook(tableIndex, name);
      if (existing) return existing;
      return probe.installTableHook(tableIndex, name, {
        signature: "viii",
        traceCallEvent: false,
        beforeCall: function beforeC11DynamicWriteback(args, record) {
          var view = dataView();
          if (!view || !state.c04CurrentFrame || !c31KeepsRawSolverFrame() ||
              state.c04CurrentFrame.dynamicWritebacks.length >= 1) return;
          record.__c11DynamicWriteback = {
            sequence: state.c04CurrentFrame.solveSequence++,
            before: captureC03DynamicSolve(view, args,
              "c11." + state.c04CurrentFrame.frameIndex + ".writeback.before")
          };
        },
        afterCall: function afterC11DynamicWriteback(args, result, record) {
          var row = record.__c11DynamicWriteback;
          var view = dataView();
          if (row && state.c04CurrentFrame && view) {
            row.after = captureC03DynamicSolve(view, args,
              "c11." + state.c04CurrentFrame.frameIndex + ".writeback.after");
            state.c04CurrentFrame.dynamicWritebacks.push(row);
          }
          record.__c11DynamicWriteback = null;
        }
      });
    }

    function installFirstStoneManagerTaskFlush() {
      var name = "A0.first_stone_manager_task.angular_write_flush";
      var existing = existingHook(contactManagerTaskIndex, name);
      if (existing) return existing;
      return probe.installTableHook(contactManagerTaskIndex, name, {
        signature: "vi",
        traceCallEvent: false,
        beforeCall: function beforeFirstStoneManagerTask(args) {
          var view = dataView();
          if (!view || !isPointerLike(view, args[0], 52)) return;
          var hasDynamicPair = hasDynamicDynamicManager(view, args[0]);
          if (!hasDynamicPair) return;
          armC03FirstWriteback(view, args[0]);
          if (!state.firstStoneManagerTaskFlushed) {
            state.firstStoneManagerTaskFlushed = true;
            pushEvent("a0.angular_write.before_first_stone_task", {
              contactManagerTaskIndex: contactManagerTaskIndex,
              lastAngularWrite: state.lastAngularWrite,
              lastTwoAngularWrites: state.lastAngularWrites.slice(),
              lastTwoFrictionNoises: state.lastFrictionNoises.slice(),
              precedingStaticWritebacks: state.staticWritebackRing.slice(),
              nativeSetterCallCount: state.angularWriteSerial
            });
          }
        }
      });
    }

    function installFirstStonePcmFlush() {
      var name = "A0.first_stone_pcm.angular_write_flush";
      var existing = existingHook(stonePcmIndex, name);
      if (existing) return existing;
      return probe.installTableHook(stonePcmIndex, name, {
        signature: "iiiiiiiii",
        traceCallEvent: false,
        beforeCall: function beforeFirstStonePcm(args, record) {
          var view = dataView();
          if (state.c03Armed && !state.c03PcmInput && view) {
            state.c03PcmInput = {
              transform0: decodeTransformCandidate(view, args[2]),
              transform1: decodeTransformCandidate(view, args[3])
            };
          }
          if (!state.firstStonePcmFlushed) {
            state.firstStonePcmFlushed = true;
            pushEvent("a0.angular_write.last_pre_pcm", {
              pcmTableIndex: stonePcmIndex,
              lastAngularWrite: state.lastAngularWrite,
              lastTwoAngularWrites: state.lastAngularWrites.slice(),
              lastTwoFrictionNoises: state.lastFrictionNoises.slice(),
              phaseOrder: state.phaseOrderRing.slice(),
              phaseOrderByLastTwoAngularWrites: state.lastAngularWrites.map(function (write) {
                return {
                  writeSerial: write.writeSerial,
                  tickSerial: write.tickSerial,
                  edges: (state.phaseOrderByAngularWrite[write.writeSerial] || []).slice()
                };
              }),
              a2StaticTrace: state.a2StaticTraceEnabled ? state.a2StaticTraceRows.slice() : null,
              transform0: view ? decodeTransformCandidate(view, args[2]) : null,
              transform1: view ? decodeTransformCandidate(view, args[3]) : null,
              resolver: {
                actualController: state.lastAngularWrite && state.lastAngularWrite.controller,
                angularWriteCount: state.angularWriteSerial
              }
            });
          }
          if (state.c05PcmWindowEnabled && state.c03Armed && view &&
              state.c05PcmCalls.length < state.c05PcmWindowLimit) {
            record.__c05Pcm = {
              sequence: state.c05PcmCalls.length,
              before: c05PcmSnapshot(view, args, "before")
            };
          }
          if (state.c25HistoryPcmEnabled && view &&
              state.c25HistoryPcmCalls.length < state.c25HistoryPcmLimit) {
            record.__c25HistoryPcm = {
              sequence: state.c25HistoryPcmCalls.length,
              before: c05PcmSnapshot(view, args, "before")
            };
          }
        },
        afterCall: function afterFirstStonePcm(args, result, record) {
          var row = record.__c05Pcm;
          if (row) {
            var view = dataView();
            if (view) row.after = c05PcmSnapshot(view, args, "after");
            state.c05PcmCalls.push(row);
            pushEvent("c05.persistent_pcm_call", row);
            record.__c05Pcm = null;
          }
          var history = record.__c25HistoryPcm;
          if (!history) return;
          var historyView = dataView();
          if (historyView) history.after = c05PcmSnapshot(historyView, args, "after");
          state.c25HistoryPcmCalls.push(history);
          if (history.after && history.after.contactBuffer && history.after.contactBuffer.count > 0) {
            pushEvent("c25.history_positive_stone_pcm", history);
          }
          record.__c25HistoryPcm = null;
        }
      });
    }

    function resolveSetterDispatches() {
      var view = dataView();
      if (!view) return;
      var linear = readU32LE(view, velocityDispatchGlobal);
      var angular = readU32LE(view, angularDispatchGlobal);
      if (Number.isInteger(linear) && linear > 0 && state.velocityDispatchIndex !== linear) {
        state.velocityDispatchIndex = linear;
        installSetterDispatch("linear", linear);
      }
      if (Number.isInteger(angular) && angular > 0 && state.angularDispatchIndex !== angular) {
        state.angularDispatchIndex = angular;
        installSetterDispatch("angular", angular);
      }
    }

    var installed = candidates.map(function installCandidate(candidate) {
      var existing = existingHook(candidate.index, candidate.name);
      if (existing && !opts.reinstall) return existing;
      if (existing) probe.uninstallTableHook(existing);
      return probe.installTableHook(candidate.index, candidate.name, {
        signature: "vii",
        traceCallEvent: false,
        beforeCall: function beforeA0Tick(args, record) {
          var view = dataView();
          var controllerPtr = args[0];
          var movingCurling = view && inMemoryRange(view, controllerPtr + candidate.movingCurlingOffset, 4)
            ? readU32LE(view, controllerPtr + candidate.movingCurlingOffset)
            : null;
          state.currentTick = {
            tickSerial: state.nextTickSerial + 1,
            controller: { index: candidate.index, name: candidate.name, managedPtr: sanitizeArg(controllerPtr) },
            movingCurling: sanitizeArg(movingCurling),
            writeCount: 0,
            angularWriteCount: 0,
            lastLinearVelocityRead: null,
            lastAngularVelocityRead: null
          };
          state.nextTickSerial += 1;
          record.__a0Tick = state.currentTick;
        },
        afterCall: function afterA0Tick(args, result, record) {
          var tick = record.__a0Tick;
          if (state.currentTick === tick) state.currentTick = null;
          record.__a0Tick = null;
        }
      });
    }).filter(Boolean);

    var angularVelocityHook = installAngularVelocitySetter(angularVelocitySetterTableIndex);
    if (angularVelocityHook) installed.push(angularVelocityHook);
    var linearVelocitySetterHook = installLinearVelocitySetter(linearVelocitySetterTableIndex);
    if (linearVelocitySetterHook) installed.push(linearVelocitySetterHook);
    var linearVelocityGetterHook = installVelocityGetter("velocity", linearVelocityGetterTableIndex);
    if (linearVelocityGetterHook) installed.push(linearVelocityGetterHook);
    var angularVelocityGetterHook = installVelocityGetter("angularVelocity", angularVelocityGetterTableIndex);
    if (angularVelocityGetterHook) installed.push(angularVelocityGetterHook);
    if (state.a10ReleaseOrientationEnabled || state.resetAllStoneRotationsEnabled) {
      var positionSetterHook = installTransformPositionSetter(transformPositionSetterTableIndex);
      if (positionSetterHook) installed.push(positionSetterHook);
    }
    var frictionNoiseHook = installFrictionNoiseCapture();
    if (frictionNoiseHook) installed.push(frictionNoiseHook);
    var c54StaticSolveHook = installC54StaticSolve();
    if (c54StaticSolveHook) installed.push(c54StaticSolveHook);
    var staticWritebackHook = installStaticWritebackRing();
    if (staticWritebackHook) installed.push(staticWritebackHook);
    [
      [dynamicSolveTableIndex, "solveContactBlock"],
      [dynamicSolve4TableIndex, "solveContact4Block"]
    ].forEach(function installC03DynamicVariant(item) {
      var hook = installC03DynamicSolve(item[0], item[1]);
      if (hook) installed.push(hook);
    });
    [
      [dynamicSolveWritebackTableIndex, "solveContactBlockWithWriteback"],
      [dynamicSolve4WritebackTableIndex, "solveContact4BlockWithWriteback"]
    ].forEach(function installC11DynamicVariant(item) {
      var hook = installC11DynamicWriteback(item[0], item[1]);
      if (hook) installed.push(hook);
    });
    var preIntegrateHook = installPhaseOrderTask(preIntegrateTaskIndex, "PxsDynamics.preIntegrate");
    if (preIntegrateHook) installed.push(preIntegrateHook);
    var solverSetupSolveHook = installPhaseOrderTask(solverSetupSolveTaskIndex, "PxsDynamics.solverSetupSolve");
    if (solverSetupSolveHook) installed.push(solverSetupSolveHook);
    var managerTaskHook = installFirstStoneManagerTaskFlush();
    if (managerTaskHook) installed.push(managerTaskHook);
    var stonePcmHook = installFirstStonePcmFlush();
    if (stonePcmHook) installed.push(stonePcmHook);

    pushEvent("a0.fixed_tick_resolver.installed", {
      candidates: candidates,
      velocityDispatchGlobal: velocityDispatchGlobal,
      angularDispatchGlobal: angularDispatchGlobal,
      angularVelocitySetterTableIndex: angularVelocitySetterTableIndex,
      linearVelocitySetterTableIndex: linearVelocitySetterTableIndex,
      preIntegrateTaskIndex: preIntegrateTaskIndex,
      solverSetupSolveTaskIndex: solverSetupSolveTaskIndex,
      a2StaticTraceEnabled: state.a2StaticTraceEnabled,
      c03FirstWritebackEnabled: state.c03FirstWritebackEnabled,
      c04DynamicWindowEnabled: state.c04DynamicWindowEnabled,
      c04DynamicWindowLimit: state.c04DynamicWindowLimit,
      c54IntercallStaticEnabled: state.c54IntercallStaticEnabled,
      c31CompactCoreTraceEnabled: state.c31CompactCoreTraceEnabled,
      c05PcmWindowEnabled: state.c05PcmWindowEnabled,
      c05PcmWindowLimit: state.c05PcmWindowLimit,
      contactManagerTaskIndex: contactManagerTaskIndex,
      dynamicSolveTableIndex: dynamicSolveTableIndex,
      dynamicSolveWritebackTableIndex: dynamicSolveWritebackTableIndex,
      staticSolveTableIndex: staticSolveTableIndex,
      staticWritebackTableIndex: staticWritebackTableIndex,
      stonePcmIndex: stonePcmIndex,
      installed: installed.map(function summarizeHook(hook) {
        return { index: hook.index, name: hook.name };
      })
    });
    return installed;
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

  function decodeTransformCandidate(view, ptr) {
    if (!inMemoryRange(view, ptr, 28)) return null;
    return {
      layout: "PxTransform",
      q: [
        readF32LE(view, ptr),
        readF32LE(view, ptr + 4),
        readF32LE(view, ptr + 8),
        readF32LE(view, ptr + 12)
      ].map(cleanFloatValue),
      p: [
        readF32LE(view, ptr + 16),
        readF32LE(view, ptr + 20),
        readF32LE(view, ptr + 24)
      ].map(cleanFloatValue)
    };
  }

  function decodeNarrowPhaseParamsCandidate(view, ptr) {
    if (!inMemoryRange(view, ptr, 12)) return null;
    return {
      layout: "Gu::NarrowPhaseParams",
      contactDistance: cleanFloatValue(readF32LE(view, ptr)),
      meshContactMargin: cleanFloatValue(readF32LE(view, ptr + 4)),
      toleranceLength: cleanFloatValue(readF32LE(view, ptr + 8))
    };
  }

  function decodeConvexGeometryCandidate(view, ptr) {
    if (!inMemoryRange(view, ptr, 48)) return null;
    var geometryType = readU32LE(view, ptr);
    var geometryTypeNames = {
      0: "eSPHERE",
      1: "ePLANE",
      2: "eCAPSULE",
      3: "eBOX",
      4: "eCONVEXMESH",
      5: "eTRIANGLEMESH",
      6: "eHEIGHTFIELD"
    };
    var result = {
      layout: "Gu::GeometryUnion candidate",
      geometryType: geometryType,
      geometryTypeName: geometryTypeNames[geometryType] || "unknown",
      scale: [
        readF32LE(view, ptr + 4),
        readF32LE(view, ptr + 8),
        readF32LE(view, ptr + 12)
      ].map(cleanFloatValue),
      scaleRotation: [
        readF32LE(view, ptr + 16),
        readF32LE(view, ptr + 20),
        readF32LE(view, ptr + 24),
        readF32LE(view, ptr + 28)
      ].map(cleanFloatValue),
      meshPtr: readU32LE(view, ptr + 32),
      meshFlags: view.getUint8(ptr + 36)
    };
    if (geometryType === 4) {
      result.layout = "Gu::GeometryUnion / PxConvexMeshGeometryLL candidate";
      result.convexMeshPtr = result.meshPtr;
      result.hullDataPtr = readU32LE(view, ptr + 40);
      result.gpuCompatible = !!view.getUint8(ptr + 44);
    } else if (geometryType === 5) {
      result.layout = "Gu::GeometryUnion / PxTriangleMeshGeometry candidate";
      // PxTriangleMeshGeometry stores meshFlags at +32 and the mesh pointer at +36.
      // PxConvexMeshGeometry has a different tail layout, so do not reuse its offsets.
      result.meshFlags = view.getUint8(ptr + 32);
      result.meshPtr = readU32LE(view, ptr + 36);
      result.triangleMeshPtr = result.meshPtr;
    }
    return result;
  }

  function dumpTriangleMeshHeaderCandidate(view, label, triangleMeshPtr, options) {
    if (!isPointerLike(view, triangleMeshPtr, 32)) return null;
    var opts = options || {};
    var bytes = Math.min(opts.triangleMeshHeaderBytes || 1024, view.byteLength - triangleMeshPtr);
    var countPairs = [];
    for (var offset = 0; offset + 8 <= bytes; offset += 4) {
      var vertices = readU32LE(view, triangleMeshPtr + offset);
      var triangles = readU32LE(view, triangleMeshPtr + offset + 4);
      if (vertices > 2 && vertices <= 4096 && triangles > 0 && triangles <= 8192) {
        countPairs.push({ offset: offset, nbVertices: vertices, nbTriangles: triangles });
      }
    }
    var result = {
      layout: "Gu::TriangleMesh raw-header candidate",
      triangleMeshPtr: triangleMeshPtr,
      headerBytes: bytes,
      countPairs: countPairs,
      headerWindow: probe.dumpMemoryWindow(label + ".TriangleMesh", triangleMeshPtr, bytes, {
        includeRawBytes: opts.includeRawBytes !== false,
        // The header contains ordinary integer fields that often look like wasm
        // pointers.  Do not recursively scan it; the verified fields below are
        // the only arrays needed for an exact Unity plane topology comparison.
        includePointers: false,
        previewBytes: opts.previewBytes || 128,
        u32PreviewCount: Math.min(64, Math.floor(bytes / 4)),
        f32PreviewCount: Math.min(64, Math.floor(bytes / 4)),
        contactPreviewCount: 0
      })
    };

    // Gu::TriangleMesh on this 32-bit build has mNbVertices/mNbTriangles at
    // +16/+20 and mVertices/mTriangles at +24/+28.  The prior capture proves
    // that layout for Unity's rink plane (121 vertices, 200 triangles).  Read
    // the exact buffers directly instead of inferring them from a pointer scan.
    var nbVertices = readU32LE(view, triangleMeshPtr + 16);
    var nbTriangles = readU32LE(view, triangleMeshPtr + 20);
    var verticesPtr = readU32LE(view, triangleMeshPtr + 24);
    var trianglesPtr = readU32LE(view, triangleMeshPtr + 28);
    var meshFlags = view.getUint8(triangleMeshPtr + 64);
    var indexWidth = (meshFlags & 2) ? 2 : 4;
    var vertexBytes = nbVertices * 12;
    var triangleBytes = nbTriangles * 3 * indexWidth;
    var countsValid = nbVertices > 2 && nbVertices <= 4096 && nbTriangles > 0 && nbTriangles <= 8192;
    if (countsValid && inMemoryRange(view, verticesPtr, vertexBytes) && inMemoryRange(view, trianglesPtr, triangleBytes)) {
      result.verifiedLayout = {
        nbVertices: nbVertices,
        nbTriangles: nbTriangles,
        verticesPtr: verticesPtr,
        trianglesPtr: trianglesPtr,
        meshFlags: meshFlags,
        indexWidth: indexWidth,
        vertexBytes: vertexBytes,
        triangleBytes: triangleBytes
      };
      result.vertexBuffer = probe.dumpMemoryWindow(label + ".TriangleMesh.vertices", verticesPtr, vertexBytes, {
        includeRawBytes: true,
        includePointers: false,
        previewBytes: Math.min(opts.previewBytes || 128, vertexBytes),
        u32PreviewCount: Math.min(24, Math.floor(vertexBytes / 4)),
        f32PreviewCount: Math.min(24, Math.floor(vertexBytes / 4)),
        contactPreviewCount: 0
      });
      result.triangleBuffer = probe.dumpMemoryWindow(label + ".TriangleMesh.triangles", trianglesPtr, triangleBytes, {
        includeRawBytes: true,
        includePointers: false,
        previewBytes: Math.min(opts.previewBytes || 128, triangleBytes),
        u32PreviewCount: Math.min(24, Math.floor(triangleBytes / 4)),
        f32PreviewCount: Math.min(24, Math.floor(triangleBytes / 4)),
        contactPreviewCount: 0
      });
    }

    // Unity WebGL's Gu::TriangleMesh header has the face-remap pointer at +72.
    // Gu::BV4TriangleMesh embeds its BV4Tree at +124; the verified runtime
    // header puts mNbNodes at +144 and mNodes at +148. These are the remaining
    // cooked fields needed to import the rink object instead of re-cooking it.
    var faceRemapPtr = readU32LE(view, triangleMeshPtr + 72);
    var bvh4NodeCount = readU32LE(view, triangleMeshPtr + 144);
    var bvh4NodesPtr = readU32LE(view, triangleMeshPtr + 148);
    var bvh4InitData = readU32LE(view, triangleMeshPtr + 152);
    var faceRemapBytes = countsValid ? nbTriangles * 4 : 0;
    var bvh4NodeBytes = bvh4NodeCount * 16;
    if (countsValid && inMemoryRange(view, faceRemapPtr, faceRemapBytes)) {
      result.faceRemapBuffer = probe.dumpMemoryWindow(label + ".TriangleMesh.faceRemap", faceRemapPtr, faceRemapBytes, {
        includeRawBytes: true,
        includePointers: false,
        previewBytes: Math.min(opts.previewBytes || 128, faceRemapBytes),
        u32PreviewCount: Math.min(24, nbTriangles),
        f32PreviewCount: 0,
        contactPreviewCount: 0
      });
    }
    if (bvh4NodeCount > 0 && bvh4NodeCount <= 4096 &&
        inMemoryRange(view, bvh4NodesPtr, bvh4NodeBytes)) {
      result.bvh4 = {
        layout: "Gu::BV4TriangleMesh / BV4Tree verified runtime offsets",
        nbNodes: bvh4NodeCount,
        nodesPtr: bvh4NodesPtr,
        initData: bvh4InitData,
        nodeSize: 16,
        nodeBytes: bvh4NodeBytes,
        treeHeader: probe.dumpMemoryWindow(label + ".TriangleMesh.BV4Tree", triangleMeshPtr + 124, 64, {
          includeRawBytes: true,
          includePointers: false,
          previewBytes: 64,
          u32PreviewCount: 16,
          f32PreviewCount: 16,
          contactPreviewCount: 0
        }),
        nodeBuffer: probe.dumpMemoryWindow(label + ".TriangleMesh.BV4Tree.nodes", bvh4NodesPtr, bvh4NodeBytes, {
          includeRawBytes: true,
          includePointers: false,
          previewBytes: Math.min(opts.previewBytes || 128, bvh4NodeBytes),
          u32PreviewCount: Math.min(24, Math.floor(bvh4NodeBytes / 4)),
          f32PreviewCount: Math.min(24, Math.floor(bvh4NodeBytes / 4)),
          contactPreviewCount: 0
        })
      };
    }
    return result;
  }

  function decodeConvexHullDataCandidate(view, ptr) {
    if (!inMemoryRange(view, ptr, 64)) return null;
    var nbEdges = readU16LE(view, ptr + 36);
    var nbHullVertices = view.getUint8(ptr + 38);
    var nbPolygons = view.getUint8(ptr + 39);
    var polygonsPtr = readU32LE(view, ptr + 40);
    var bigConvexRawDataPtr = readU32LE(view, ptr + 44);
    var validCounts = (
      nbEdges > 0 && nbEdges < 4096 &&
      nbHullVertices > 0 && nbHullVertices <= 255 &&
      nbPolygons > 0 && nbPolygons <= 255
    );
    return {
      layout: "Gu::ConvexHullData32",
      aabbCenter: [
        readF32LE(view, ptr),
        readF32LE(view, ptr + 4),
        readF32LE(view, ptr + 8)
      ].map(cleanFloatValue),
      aabbExtents: [
        readF32LE(view, ptr + 12),
        readF32LE(view, ptr + 16),
        readF32LE(view, ptr + 20)
      ].map(cleanFloatValue),
      centerOfMass: [
        readF32LE(view, ptr + 24),
        readF32LE(view, ptr + 28),
        readF32LE(view, ptr + 32)
      ].map(cleanFloatValue),
      nbEdges: nbEdges,
      nbHullVertices: nbHullVertices,
      nbPolygons: nbPolygons,
      polygonsPtr: polygonsPtr,
      bigConvexRawDataPtr: bigConvexRawDataPtr,
      internal: [
        readF32LE(view, ptr + 48),
        readF32LE(view, ptr + 52),
        readF32LE(view, ptr + 56),
        readF32LE(view, ptr + 60)
      ].map(cleanFloatValue),
      countsLookValid: validCounts
    };
  }

  function decodeHullPolygonCounts(view, polygonsPtr, nbPolygons) {
    var counts = [];
    var vertexRefCount = 0;
    if (!inMemoryRange(view, polygonsPtr, nbPolygons * 20)) {
      return { counts: counts, vertexRefCount: null };
    }
    for (var i = 0; i < nbPolygons; i += 1) {
      var nbVerts = view.getUint8(polygonsPtr + i * 20 + 18);
      counts.push(nbVerts);
      vertexRefCount += nbVerts;
    }
    return { counts: counts, vertexRefCount: vertexRefCount };
  }

  function decodeBigConvexRawDataCandidate(view, ptr) {
    if (!inMemoryRange(view, ptr, 24)) return null;
    var subdiv = readU16LE(view, ptr);
    var nbSamples = readU16LE(view, ptr + 2);
    var samplesPtr = readU32LE(view, ptr + 4);
    var nbVerts = readU32LE(view, ptr + 8);
    var nbAdjVerts = readU32LE(view, ptr + 12);
    var valenciesPtr = readU32LE(view, ptr + 16);
    var adjacentVertsPtr = readU32LE(view, ptr + 20);
    var validCounts = (
      subdiv > 0 && subdiv <= 128 &&
      nbSamples > 0 && nbSamples <= 8192 &&
      nbVerts > 0 && nbVerts <= 255 &&
      nbAdjVerts > 0 && nbAdjVerts <= 4096
    );
    return {
      layout: "Gu::BigConvexRawData32",
      subdiv: subdiv,
      nbSamples: nbSamples,
      samplesPtr: samplesPtr,
      nbVerts: nbVerts,
      nbAdjVerts: nbAdjVerts,
      valenciesPtr: valenciesPtr,
      adjacentVertsPtr: adjacentVertsPtr,
      samplesBytes: nbSamples * 2,
      valenciesBytes: nbVerts * 4,
      adjacentVertsBytes: nbAdjVerts,
      countsLookValid: validCounts
    };
  }

  function dumpBigConvexRawDataArrays(view, label, bigConvex, options) {
    var opts = options || {};
    if (!bigConvex || !bigConvex.countsLookValid) return null;
    var out = {
      layout: "Gu::BigConvexRawData pointed arrays",
      samplesExpectedBytes: bigConvex.samplesBytes,
      valenciesExpectedBytes: bigConvex.valenciesBytes,
      adjacentVertsExpectedBytes: bigConvex.adjacentVertsBytes
    };
    var dumpOpts = {
      includeRawBytes: opts.includeRawBytes !== false,
      includePointers: false,
      previewBytes: opts.previewBytes || 256,
      u32PreviewCount: opts.u32PreviewCount || 64,
      f32PreviewCount: opts.f32PreviewCount || 64,
      contactPreviewCount: opts.contactPreviewCount || 8
    };
    if (isPointerLike(view, bigConvex.samplesPtr, Math.min(bigConvex.samplesBytes, 16))) {
      out.samplesWindow = probe.dumpMemoryWindow(
        label + ".bigConvexSamples",
        bigConvex.samplesPtr,
        Math.min(bigConvex.samplesBytes, view.byteLength - bigConvex.samplesPtr),
        dumpOpts
      );
    }
    if (isPointerLike(view, bigConvex.valenciesPtr, Math.min(bigConvex.valenciesBytes, 16))) {
      out.valenciesWindow = probe.dumpMemoryWindow(
        label + ".bigConvexValencies",
        bigConvex.valenciesPtr,
        Math.min(bigConvex.valenciesBytes, view.byteLength - bigConvex.valenciesPtr),
        dumpOpts
      );
    }
    if (isPointerLike(view, bigConvex.adjacentVertsPtr, Math.min(bigConvex.adjacentVertsBytes, 16))) {
      out.adjacentVertsWindow = probe.dumpMemoryWindow(
        label + ".bigConvexAdjacentVerts",
        bigConvex.adjacentVertsPtr,
        Math.min(bigConvex.adjacentVertsBytes, view.byteLength - bigConvex.adjacentVertsPtr),
        dumpOpts
      );
    }
    return out;
  }

  function dumpConvexHullRuntimeBuffers(view, label, hullData, options) {
    var opts = options || {};
    if (!hullData || !hullData.countsLookValid) return null;
    if (!isPointerLike(view, hullData.polygonsPtr, 20)) return null;

    var polygonBytes = hullData.nbPolygons * 20;
    var hullVertexBytes = hullData.nbHullVertices * 12;
    var facesByEdgesBytes = hullData.nbEdges * 2;
    var facesByVerticesBytes = hullData.nbHullVertices * 3;
    var polygonCounts = decodeHullPolygonCounts(view, hullData.polygonsPtr, hullData.nbPolygons);
    var vertexDataBytes = polygonCounts.vertexRefCount;
    var runtimeBytes = (
      polygonBytes +
      hullVertexBytes +
      facesByEdgesBytes +
      facesByVerticesBytes +
      (vertexDataBytes || 0)
    );
    runtimeBytes = Math.min(
      runtimeBytes,
      opts.hullRuntimeBytes || runtimeBytes,
      view.byteLength - hullData.polygonsPtr
    );

    var out = {
      layout: "Gu::ConvexHullData32 runtime extra buffer",
      polygonVertexCounts: polygonCounts.counts,
      vertexRefCount: polygonCounts.vertexRefCount,
      byteLayout: {
        polygons: { offset: 0, bytes: polygonBytes },
        hullVertices: { offset: polygonBytes, bytes: hullVertexBytes },
        facesByEdges8: { offset: polygonBytes + hullVertexBytes, bytes: facesByEdgesBytes },
        facesByVertices8: {
          offset: polygonBytes + hullVertexBytes + facesByEdgesBytes,
          bytes: facesByVerticesBytes
        },
        vertexData8: {
          offset: polygonBytes + hullVertexBytes + facesByEdgesBytes + facesByVerticesBytes,
          bytes: vertexDataBytes
        }
      },
      runtimeBufferWindow: probe.dumpMemoryWindow(
        label + ".hullRuntimeBuffer",
        hullData.polygonsPtr,
        runtimeBytes,
        {
          includeRawBytes: opts.includeRawBytes !== false,
          includePointers: false,
          previewBytes: opts.previewBytes || 256,
          u32PreviewCount: opts.u32PreviewCount || 64,
          f32PreviewCount: opts.f32PreviewCount || 64,
          contactPreviewCount: opts.contactPreviewCount || 8
        }
      )
    };

    if (isPointerLike(view, hullData.bigConvexRawDataPtr, 24)) {
      var bigConvex = decodeBigConvexRawDataCandidate(view, hullData.bigConvexRawDataPtr);
      out.bigConvexRawData = bigConvex;
      out.bigConvexRawDataWindow = probe.dumpMemoryWindow(
        label + ".bigConvexRawData",
        hullData.bigConvexRawDataPtr,
        Math.min(opts.bigConvexBytes || 512, view.byteLength - hullData.bigConvexRawDataPtr),
        {
          includeRawBytes: opts.includeRawBytes !== false,
          includePointers: false,
          previewBytes: opts.previewBytes || 256,
          u32PreviewCount: opts.u32PreviewCount || 64,
          f32PreviewCount: opts.f32PreviewCount || 64,
          contactPreviewCount: opts.contactPreviewCount || 8
        }
      );
      out.bigConvexRawDataArrays = dumpBigConvexRawDataArrays(
        view,
        label,
        bigConvex,
        opts
      );
    }
    return out;
  }

  function decodeCacheCandidate(view, ptr) {
    if (!inMemoryRange(view, ptr, 8)) return null;
    var cachedData = readU32LE(view, ptr);
    var cachedSize = readU16LE(view, ptr + 4);
    var pairData = view.getUint8(ptr + 6);
    var manifoldFlags = view.getUint8(ptr + 7);
    var out = {
      layout: "Gu::Cache / PxCache",
      cachedDataPtr: cachedData,
      cachedSize: cachedSize,
      pairData: pairData,
      manifoldFlags: manifoldFlags,
      isManifold: !!(manifoldFlags & 1),
      isMultiManifold: !!(manifoldFlags & 2)
    };
    if (isPointerLike(view, cachedData, 80)) {
      out.persistentManifoldCandidate = {
        layout: "Gu::PersistentContactManifold candidate",
        // For single convex-convex PCM, the base object begins with
        // PsTransformV + QuatV + QuatV, then these byte fields.
        numContacts: view.getUint8(cachedData + 64),
        capacity: view.getUint8(cachedData + 65),
        numWarmStartPoints: view.getUint8(cachedData + 66),
        aIndices: [
          view.getUint8(cachedData + 67),
          view.getUint8(cachedData + 68),
          view.getUint8(cachedData + 69),
          view.getUint8(cachedData + 70)
        ],
        bIndices: [
          view.getUint8(cachedData + 71),
          view.getUint8(cachedData + 72),
          view.getUint8(cachedData + 73),
          view.getUint8(cachedData + 74)
        ],
        contactPointsPtr: isPointerLike(view, readU32LE(view, cachedData + 76), 16)
          ? readU32LE(view, cachedData + 76)
          : null
      };
    }
    return out;
  }

  // wasm32 layout verified against PxsContactManager / PxcNpWorkUnit and the
  // runtime ShapeInteraction -> manager dump. Keep this narrow: it is used to
  // establish task ordering, not to mutate or reconstruct any PhysX state.
  function decodePxsContactManagerCandidate(view, ptr) {
    if (!isPointerLike(view, ptr, 72)) return null;
    return {
      layout: "PxsContactManager + PxcNpWorkUnit wasm32",
      ptr: ptr,
      rigidCore0: readU32LE(view, ptr + 16),
      rigidCore1: readU32LE(view, ptr + 20),
      shapeCore0: readU32LE(view, ptr + 24),
      shapeCore1: readU32LE(view, ptr + 28),
      frictionData: readU32LE(view, ptr + 36),
      flags: readU16LE(view, ptr + 40),
      frictionPatchCount: view.getUint8(ptr + 42),
      statusFlags: view.getUint8(ptr + 43),
      index: readU32LE(view, ptr + 48),
      transformCache0: readU32LE(view, ptr + 56),
      transformCache1: readU32LE(view, ptr + 60),
      edgeIndex: readU32LE(view, ptr + 64),
      npIndex: readU32LE(view, ptr + 68)
    };
  }

  function decodePxsCMDiscreteUpdateTask(view, ptr, options) {
    // PxsCMUpdateTask is a Cm::Task prefix followed by these wasm32 fields:
    // +28 cmArray, +32 outputs, +36 caches, +40 count, +44 dt, +48 context.
    // func70739 independently reads the same offsets (a[7]..a[12]).
    if (!isPointerLike(view, ptr, 52)) return null;
    var opts = options || {};
    var cmArrayPtr = readU32LE(view, ptr + 28);
    var outputsPtr = readU32LE(view, ptr + 32);
    var cachesPtr = readU32LE(view, ptr + 36);
    var count = readU32LE(view, ptr + 40);
    var maxManagers = Math.min(count, opts.cmTaskManagers || 128);
    var managers = [];
    if (isPointerLike(view, cmArrayPtr, maxManagers * 4)) {
      for (var index = 0; index < maxManagers; index += 1) {
        var managerPtr = readU32LE(view, cmArrayPtr + index * 4);
        var row = {
          taskIndex: index,
          contactManagerPtr: managerPtr,
          manager: decodePxsContactManagerCandidate(view, managerPtr)
        };
        if (isPointerLike(view, outputsPtr + index * 16, 16)) {
          row.output = {
            nbContacts: view.getUint8(outputsPtr + index * 16),
            nbPatches: view.getUint8(outputsPtr + index * 16 + 1),
            statusFlag: readU16LE(view, outputsPtr + index * 16 + 2)
          };
        }
        if (isPointerLike(view, cachesPtr + index * 8, 8)) {
          row.cache = decodeCacheCandidate(view, cachesPtr + index * 8);
        }
        // Kept opt-in because these are only needed for the A0-min question:
        // does the actor core already hold the pose consumed by the first PCM?
        if (opts.includeRigidCoreWindows === true) {
          var rigidCoreBytes = opts.rigidCoreBytes || 160;
          if (isPointerLike(view, row.manager && row.manager.rigidCore0, 32)) {
            row.rigidCore0Window = probe.dumpMemoryWindow(
              "PxsCMDiscreteUpdateTask.rigidCore0",
              row.manager.rigidCore0,
              Math.min(rigidCoreBytes, view.byteLength - row.manager.rigidCore0),
              {
                includeRawBytes: true,
                includePointers: false,
                previewBytes: rigidCoreBytes,
                u32PreviewCount: Math.ceil(rigidCoreBytes / 4),
                f32PreviewCount: Math.ceil(rigidCoreBytes / 4),
                contactPreviewCount: 0
              }
            );
          }
          if (isPointerLike(view, row.manager && row.manager.rigidCore1, 32)) {
            row.rigidCore1Window = probe.dumpMemoryWindow(
              "PxsCMDiscreteUpdateTask.rigidCore1",
              row.manager.rigidCore1,
              Math.min(rigidCoreBytes, view.byteLength - row.manager.rigidCore1),
              {
                includeRawBytes: true,
                includePointers: false,
                previewBytes: rigidCoreBytes,
                u32PreviewCount: Math.ceil(rigidCoreBytes / 4),
                f32PreviewCount: Math.ceil(rigidCoreBytes / 4),
                contactPreviewCount: 0
              }
            );
          }
        }
        managers.push(row);
      }
    }
    return {
      layout: "PxsCMDiscreteUpdateTask wasm32",
      ptr: ptr,
      cmArrayPtr: cmArrayPtr,
      outputsPtr: outputsPtr,
      cachesPtr: cachesPtr,
      count: count,
      dt: readF32LE(view, ptr + 44),
      contextPtr: readU32LE(view, ptr + 48),
      managers: managers,
      truncated: count > maxManagers
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

  function isDynamicDynamicFinalizer(target, argsLike) {
    if (target.name !== "createFinalizeSolverContacts") return true;
    var view = dataView();
    var descPtr = argsLike && argsLike[0];
    if (!view || !isPointerLike(view, descPtr, 100)) return false;
    // PxSolverContactDesc wasm32 layout, independently decoded by the offline
    // solver extractor: bodyState0/1 at +92/+96, dynamic is enum value 1.
    return readU32LE(view, descPtr + 92) === 1 && readU32LE(view, descPtr + 96) === 1;
  }

  function looksLikeDynamicStoneCore(view, ptr) {
    // This A0-min probe is deliberately scoped to the controlled curling
    // sheet. PxsRigidCore begins with body2World (quat at +0, position at
    // +16); the static rink core remains at y=14.304784..., while a supported
    // stone body core is near y=14.4324. Pointer presence alone is not enough:
    // stone-rink managers also have two cores.
    if (!isPointerLike(view, ptr, 28)) return false;
    var y = readF32LE(view, ptr + 20);
    return Number.isFinite(y) && y > 14.35 && y < 14.55;
  }

  function hasDynamicDynamicManager(view, taskPtr) {
    var task = decodePxsCMDiscreteUpdateTask(view, taskPtr, { cmTaskManagers: 128 });
    if (!task || !task.managers) return false;
    return task.managers.some(function hasTwoDynamicStoneCores(row) {
      return !!(
        row.manager &&
        looksLikeDynamicStoneCore(view, row.manager.rigidCore0) &&
        looksLikeDynamicStoneCore(view, row.manager.rigidCore1)
      );
    });
  }

  function shouldDumpPhysXNativeTarget(target, options, argsLike) {
    var opts = options || {};
    if (opts.armOnlyNames && opts.armOnlyNames.indexOf(target.name) !== -1) return false;
    // C108 is deliberately narrower than global "always" capture.  The
    // target stone can be identified from the same two PxTransform arguments
    // that feed PxcPCMContactConvexMesh; retain its static support calls from
    // reset/activation through the later collision without logging every ice
    // contact in the session.  It is passive and does not alter the cache.
    if (
      target.name === "PxcPCMContactConvexMesh" &&
      Number.isFinite(opts.c108StaticTargetNativeX) &&
      Number.isFinite(opts.c108StaticTargetNativeZ)
    ) {
      var c108View = dataView();
      var c108Tolerance = Math.max(0.000001, Number(opts.c108StaticTargetNativeTolerance) || 0.002);
      var c108Transforms = [
        decodeTransformCandidate(c108View, argsLike && argsLike[2]),
        decodeTransformCandidate(c108View, argsLike && argsLike[3])
      ].filter(function definedTransform(value) { return value && value.p; });
      var c108Matched = c108Transforms.some(function matchesC108Target(transformValue) {
        return Math.abs(transformValue.p[0] - opts.c108StaticTargetNativeX) <= c108Tolerance &&
          Math.abs(transformValue.p[2] - opts.c108StaticTargetNativeZ) <= c108Tolerance;
      });
      if (!c108Matched) return false;
    }
    if (
      opts.dynamicDynamicOnlyNames &&
      opts.dynamicDynamicOnlyNames.indexOf(target.name) !== -1 &&
      !isDynamicDynamicFinalizer(target, argsLike)
    ) return false;
    if (
      opts.dynamicDynamicTaskOnlyNames &&
      opts.dynamicDynamicTaskOnlyNames.indexOf(target.name) !== -1
    ) {
      var view = dataView();
      if (!view || !isPointerLike(view, argsLike && argsLike[0], 52)) return false;
      if (!hasDynamicDynamicManager(view, argsLike[0])) return false;
    }
    if (opts.alwaysNames && opts.alwaysNames.indexOf(target.name) !== -1) return true;
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
      solverDescRecords: opts.solverDescRecords || 4,
      solverConstraintBytes: opts.solverConstraintBytes || 4096,
      includeRigidCoreWindows: opts.includeRigidCoreWindows === true,
      rigidCoreBytes: opts.rigidCoreBytes || 160,
      labelPrefix: target.name + ".arg"
    };
  }

  function decodeSolverConstraintDesc(view, ptr) {
    if (!inMemoryRange(view, ptr, 32)) return null;
    var links = readU32LE(view, ptr + 8);
    var packedLengths = readU32LE(view, ptr + 20);
    return {
      ptr: ptr,
      bodyA: readU32LE(view, ptr),
      bodyB: readU32LE(view, ptr + 4),
      linkIndexA: links & 0xffff,
      linkIndexB: (links >>> 16) & 0xffff,
      bodyADataIndex: readU32LE(view, ptr + 12),
      bodyBDataIndex: readU32LE(view, ptr + 16),
      writeBackLengthOver4: packedLengths & 0xffff,
      constraintLengthOver16: (packedLengths >>> 16) & 0xffff,
      constraint: readU32LE(view, ptr + 24),
      writeBack: readU32LE(view, ptr + 28)
    };
  }

  function dumpSolverConstraintDescs(view, label, descPtr, options) {
    var opts = options || {};
    var records = [];
    var maxRecords = opts.solverDescRecords || 4;
    if (!isPointerLike(view, descPtr, 32)) return records;

    for (var i = 0; i < maxRecords; i += 1) {
      var recPtr = descPtr + i * 32;
      if (!inMemoryRange(view, recPtr, 32)) break;
      var desc = decodeSolverConstraintDesc(view, recPtr);
      if (!desc) break;
      var looksEmpty = (
        desc.bodyA === 0 &&
        desc.bodyB === 0 &&
        desc.constraint === 0 &&
        desc.writeBack === 0 &&
        desc.constraintLengthOver16 === 0
      );
      if (i > 0 && looksEmpty) break;

      var record = { index: i, desc: desc };
      if (isPointerLike(view, desc.constraint, 4) && desc.constraintLengthOver16 > 0) {
        var constraintBytes = Math.min(
          desc.constraintLengthOver16 * 16 + 16,
          opts.solverConstraintBytes || 4096,
          view.byteLength - desc.constraint
        );
        record.constraintWindow = probe.dumpMemoryWindow(
          label + ".solverDesc[" + i + "].constraint",
          desc.constraint,
          constraintBytes,
          {
            includeRawBytes: opts.includeRawBytes !== false,
            includePointers: false,
            previewBytes: opts.previewBytes || 256,
            u32PreviewCount: opts.u32PreviewCount || 64,
            f32PreviewCount: opts.f32PreviewCount || 64,
            contactPreviewCount: opts.contactPreviewCount || 8
          }
        );
      }
      if (isPointerLike(view, desc.bodyA, 64)) {
        record.bodyAWindow = probe.dumpMemoryWindow(
          label + ".solverDesc[" + i + "].bodyA",
          desc.bodyA,
          Math.min(opts.solverBodyBytes || 256, view.byteLength - desc.bodyA),
          {
            includeRawBytes: opts.includeRawBytes !== false,
            includePointers: false,
            previewBytes: opts.previewBytes || 128,
            u32PreviewCount: 32,
            f32PreviewCount: 32,
            contactPreviewCount: opts.contactPreviewCount || 8
          }
        );
      }
      if (isPointerLike(view, desc.bodyB, 64)) {
        record.bodyBWindow = probe.dumpMemoryWindow(
          label + ".solverDesc[" + i + "].bodyB",
          desc.bodyB,
          Math.min(opts.solverBodyBytes || 256, view.byteLength - desc.bodyB),
          {
            includeRawBytes: opts.includeRawBytes !== false,
            includePointers: false,
            previewBytes: opts.previewBytes || 128,
            u32PreviewCount: 32,
            f32PreviewCount: 32,
            contactPreviewCount: opts.contactPreviewCount || 8
          }
        );
      }
      if (isPointerLike(view, desc.writeBack, 4) && desc.writeBackLengthOver4 > 0) {
        record.writeBackWindow = probe.dumpMemoryWindow(
          label + ".solverDesc[" + i + "].writeBack",
          desc.writeBack,
          Math.min(desc.writeBackLengthOver4 * 4, opts.solverConstraintBytes || 4096),
          {
            includeRawBytes: opts.includeRawBytes !== false,
            includePointers: false,
            previewBytes: opts.previewBytes || 128,
            u32PreviewCount: 16,
            f32PreviewCount: 16,
            contactPreviewCount: opts.contactPreviewCount || 8
          }
        );
      }
      records.push(record);
    }
    return records;
  }

  function physxNativeExtraDumps(target, argsLike, options) {
    var opts = options || {};
    var view = dataView();
    if (!view) return [];
    var args = Array.prototype.slice.call(argsLike, 0, 16);
    var extras = [];

    if (
      target.name === "PxsContext.contactManagerDiscreteUpdate" &&
      isPointerLike(view, args[0], 52)
    ) {
      extras.push({
        label: target.name + ".task",
        task: decodePxsCMDiscreteUpdateTask(view, args[0], opts),
        window: probe.dumpMemoryWindow(
          target.name + ".task",
          args[0],
          Math.min(128, view.byteLength - args[0]),
          {
            includeRawBytes: opts.includeRawBytes !== false,
            includePointers: false,
            previewBytes: 128,
            u32PreviewCount: 32,
            f32PreviewCount: 32,
            contactPreviewCount: opts.contactPreviewCount || 8
          }
        )
      });
    }

    if (
      (target.name === "PxcPCMContactConvexConvex" ||
        target.name === "PxcPCMContactConvexMesh") &&
      isPointerLike(view, args[0], 4)
    ) {
      var pcm = {
        label: target.name + ".pcmInputs",
        shape0Ptr: args[0],
        shape1Ptr: args[1],
        transform0Ptr: args[2],
        transform1Ptr: args[3],
        paramsPtr: args[4],
        cachePtr: args[5],
        contactBufferPtr: args[6],
        renderOutputPtr: args[7]
      };
      pcm.transform0 = decodeTransformCandidate(view, args[2]);
      pcm.transform1 = decodeTransformCandidate(view, args[3]);

      if (isPointerLike(view, args[0], 48)) {
        pcm.shape0 = {
          decoded: decodeConvexGeometryCandidate(view, args[0]),
          window: probe.dumpMemoryWindow(
            target.name + ".shape0.GeometryUnion",
            args[0],
            Math.min(opts.geometryBytes || 96, view.byteLength - args[0]),
            {
              includeRawBytes: opts.includeRawBytes !== false,
              includePointers: false,
              previewBytes: opts.previewBytes || 128,
              u32PreviewCount: 24,
              f32PreviewCount: 24,
              contactPreviewCount: opts.contactPreviewCount || 8
            }
          )
        };
        if (pcm.shape0.decoded && pcm.shape0.decoded.geometryType === 4 && isPointerLike(view, pcm.shape0.decoded.hullDataPtr, 16)) {
          var shape0HullData = decodeConvexHullDataCandidate(view, pcm.shape0.decoded.hullDataPtr);
          pcm.shape0.hullData = shape0HullData;
          pcm.shape0.hullDataWindow = probe.dumpMemoryWindow(
            target.name + ".shape0.hullData",
            pcm.shape0.decoded.hullDataPtr,
            Math.min(opts.hullDataBytes || 512, view.byteLength - pcm.shape0.decoded.hullDataPtr),
            {
              includeRawBytes: opts.includeRawBytes !== false,
              includePointers: false,
              previewBytes: opts.previewBytes || 128,
              u32PreviewCount: 32,
              f32PreviewCount: 32,
              contactPreviewCount: opts.contactPreviewCount || 8
            }
          );
          pcm.shape0.hullRuntime = dumpConvexHullRuntimeBuffers(
            view,
            target.name + ".shape0",
            shape0HullData,
            opts
          );
        } else if (pcm.shape0.decoded && pcm.shape0.decoded.geometryType === 5) {
          pcm.shape0.triangleMeshRuntime = dumpTriangleMeshHeaderCandidate(
            view,
            target.name + ".shape0",
            pcm.shape0.decoded.triangleMeshPtr,
            opts
          );
        }
      }
      if (isPointerLike(view, args[1], 48)) {
        pcm.shape1 = {
          decoded: decodeConvexGeometryCandidate(view, args[1]),
          window: probe.dumpMemoryWindow(
            target.name + ".shape1.GeometryUnion",
            args[1],
            Math.min(opts.geometryBytes || 96, view.byteLength - args[1]),
            {
              includeRawBytes: opts.includeRawBytes !== false,
              includePointers: false,
              previewBytes: opts.previewBytes || 128,
              u32PreviewCount: 24,
              f32PreviewCount: 24,
              contactPreviewCount: opts.contactPreviewCount || 8
            }
          )
        };
        if (pcm.shape1.decoded && pcm.shape1.decoded.geometryType === 4 && isPointerLike(view, pcm.shape1.decoded.hullDataPtr, 16)) {
          var shape1HullData = decodeConvexHullDataCandidate(view, pcm.shape1.decoded.hullDataPtr);
          pcm.shape1.hullData = shape1HullData;
          pcm.shape1.hullDataWindow = probe.dumpMemoryWindow(
            target.name + ".shape1.hullData",
            pcm.shape1.decoded.hullDataPtr,
            Math.min(opts.hullDataBytes || 512, view.byteLength - pcm.shape1.decoded.hullDataPtr),
            {
              includeRawBytes: opts.includeRawBytes !== false,
              includePointers: false,
              previewBytes: opts.previewBytes || 128,
              u32PreviewCount: 32,
              f32PreviewCount: 32,
              contactPreviewCount: opts.contactPreviewCount || 8
            }
          );
          pcm.shape1.hullRuntime = dumpConvexHullRuntimeBuffers(
            view,
            target.name + ".shape1",
            shape1HullData,
            opts
          );
        } else if (pcm.shape1.decoded && pcm.shape1.decoded.geometryType === 5) {
          pcm.shape1.triangleMeshRuntime = dumpTriangleMeshHeaderCandidate(
            view,
            target.name + ".shape1",
            pcm.shape1.decoded.triangleMeshPtr,
            opts
          );
        }
      }
      if (isPointerLike(view, args[2], 28)) {
        pcm.transform0 = {
          decoded: decodeTransformCandidate(view, args[2]),
          window: probe.dumpMemoryWindow(
            target.name + ".transform0",
            args[2],
            32,
            {
              includeRawBytes: opts.includeRawBytes !== false,
              includePointers: false,
              previewBytes: 64,
              u32PreviewCount: 8,
              f32PreviewCount: 8,
              contactPreviewCount: opts.contactPreviewCount || 8
            }
          )
        };
      }
      if (isPointerLike(view, args[3], 28)) {
        pcm.transform1 = {
          decoded: decodeTransformCandidate(view, args[3]),
          window: probe.dumpMemoryWindow(
            target.name + ".transform1",
            args[3],
            32,
            {
              includeRawBytes: opts.includeRawBytes !== false,
              includePointers: false,
              previewBytes: 64,
              u32PreviewCount: 8,
              f32PreviewCount: 8,
              contactPreviewCount: opts.contactPreviewCount || 8
            }
          )
        };
      }
      if (isPointerLike(view, args[4], 12)) {
        pcm.narrowPhaseParams = {
          decoded: decodeNarrowPhaseParamsCandidate(view, args[4]),
          window: probe.dumpMemoryWindow(
            target.name + ".narrowPhaseParams",
            args[4],
            16,
            {
              includeRawBytes: opts.includeRawBytes !== false,
              includePointers: false,
              previewBytes: 64,
              u32PreviewCount: 4,
              f32PreviewCount: 4,
              contactPreviewCount: opts.contactPreviewCount || 8
            }
          )
        };
      }
      if (isPointerLike(view, args[5], 8)) {
        pcm.cache = {
          decoded: decodeCacheCandidate(view, args[5]),
          window: probe.dumpMemoryWindow(
            target.name + ".cache",
            args[5],
            Math.min(opts.cacheBytes || 64, view.byteLength - args[5]),
            {
              includeRawBytes: opts.includeRawBytes !== false,
              includePointers: false,
              previewBytes: 64,
              u32PreviewCount: 8,
              f32PreviewCount: 8,
              contactPreviewCount: opts.contactPreviewCount || 8
            }
          )
        };
        if (pcm.cache.decoded && isPointerLike(view, pcm.cache.decoded.cachedDataPtr, 16)) {
          pcm.cache.manifoldWindow = probe.dumpMemoryWindow(
            target.name + ".cache.cachedData",
            pcm.cache.decoded.cachedDataPtr,
            Math.min(
              pcm.cache.decoded.cachedSize || opts.manifoldBytes || 2048,
              opts.manifoldBytes || 2048,
              view.byteLength - pcm.cache.decoded.cachedDataPtr
            ),
            {
              includeRawBytes: opts.includeRawBytes !== false,
              includePointers: false,
              previewBytes: opts.previewBytes || 128,
              u32PreviewCount: 48,
              f32PreviewCount: 48,
              contactPreviewCount: opts.contactPreviewCount || 8
            }
          );
        }
      }
      if (isPointerLike(view, args[6], 4112)) {
        pcm.contactBuffer = {
          decoded: decodeContactBufferCandidate(view, args[6], opts.contactPreviewCount || 8),
          window: probe.dumpMemoryWindow(
            target.name + ".contactBuffer",
            args[6],
            4112,
            {
              includeRawBytes: opts.includeRawBytes !== false,
              includePointers: false,
              previewBytes: opts.previewBytes || 256,
              u32PreviewCount: opts.u32PreviewCount || 64,
              f32PreviewCount: opts.f32PreviewCount || 64,
              contactPreviewCount: opts.contactPreviewCount || 8
            }
          )
        };
      }
      extras.push(pcm);
    }

    if (target.name === "createFinalizeSolverContacts" && isPointerLike(view, args[0], 164)) {
      var contactDescPtr = args[0];
      var descPtr = readU32LE(view, contactDescPtr + 16);
      var data0Ptr = readU32LE(view, contactDescPtr + 28);
      var data1Ptr = readU32LE(view, contactDescPtr + 32);
      var shapeInteractionPtr = readU32LE(view, contactDescPtr + 112);
      var contactsPtr = readU32LE(view, contactDescPtr + 116);
      var frictionPtr = readU32LE(view, contactDescPtr + 136);
      var contactForcesPtr = readU32LE(view, contactDescPtr + 144);

      extras.push({
        label: target.name + ".contactDesc",
        ptr: contactDescPtr,
        descPtr: descPtr,
        data0Ptr: data0Ptr,
        data1Ptr: data1Ptr,
        shapeInteractionPtr: shapeInteractionPtr,
        contactsPtr: contactsPtr,
        numContacts: readU32LE(view, contactDescPtr + 120),
        frictionPtr: frictionPtr,
        frictionCount: readU32LE(view, contactDescPtr + 140) & 0xff,
        contactForcesPtr: contactForcesPtr,
        startFrictionPatchIndex: readU32LE(view, contactDescPtr + 148),
        numFrictionPatches: readU32LE(view, contactDescPtr + 152),
        startContactPatchIndex: readU32LE(view, contactDescPtr + 156),
        numContactPatches: readU16LE(view, contactDescPtr + 160),
        axisConstraintCount: readU16LE(view, contactDescPtr + 162),
        solverConstraintDescs: dumpSolverConstraintDescs(
          view,
          target.name + ".contactDesc",
          descPtr,
          opts
        )
      });

      if (isPointerLike(view, shapeInteractionPtr, 32)) {
        extras[extras.length - 1].shapeInteractionWindow = probe.dumpMemoryWindow(
          target.name + ".contactDesc.shapeInteraction",
          shapeInteractionPtr,
          Math.min(opts.shapeInteractionBytes || 1024, view.byteLength - shapeInteractionPtr),
          {
            includeRawBytes: opts.includeRawBytes !== false,
            includePointers: true,
            includeNestedRawBytes: opts.includeNestedRawBytes === true,
            pointerScanBytes: opts.pointerScanBytes || 512,
            maxNestedPointers: opts.maxNestedPointers || 24,
            nestedBytes: opts.nestedBytes || 512,
            previewBytes: opts.previewBytes || 256,
            u32PreviewCount: opts.u32PreviewCount || 64,
            f32PreviewCount: opts.f32PreviewCount || 64,
            contactPreviewCount: opts.contactPreviewCount || 8
          }
        );
      }
      if (isPointerLike(view, frictionPtr, 16)) {
        extras[extras.length - 1].frictionWindow = probe.dumpMemoryWindow(
          target.name + ".contactDesc.frictionPtr",
          frictionPtr,
          Math.min(opts.nestedBytes || 2048, view.byteLength - frictionPtr),
          {
            includeRawBytes: opts.includeRawBytes !== false,
            includePointers: false,
            previewBytes: opts.previewBytes || 256,
            u32PreviewCount: opts.u32PreviewCount || 64,
            f32PreviewCount: opts.f32PreviewCount || 64,
            contactPreviewCount: opts.contactPreviewCount || 8
          }
        );
      }
      if (isPointerLike(view, contactsPtr, 4112)) {
        extras[extras.length - 1].contactBufferWindow = probe.dumpMemoryWindow(
          target.name + ".contactDesc.contacts",
          contactsPtr,
          4112,
          {
            includeRawBytes: opts.includeRawBytes !== false,
            includePointers: false,
            previewBytes: opts.previewBytes || 256,
            u32PreviewCount: opts.u32PreviewCount || 64,
            f32PreviewCount: opts.f32PreviewCount || 64,
            contactPreviewCount: opts.contactPreviewCount || 8
          }
        );
      }
      if (isPointerLike(view, data0Ptr, 112)) {
        extras[extras.length - 1].data0Window = probe.dumpMemoryWindow(
          target.name + ".contactDesc.data0",
          data0Ptr,
          112,
          {
            includeRawBytes: opts.includeRawBytes !== false,
            includePointers: false,
            previewBytes: opts.previewBytes || 256,
            u32PreviewCount: 32,
            f32PreviewCount: 32,
            contactPreviewCount: opts.contactPreviewCount || 8
          }
        );
      }
      if (isPointerLike(view, data1Ptr, 112)) {
        extras[extras.length - 1].data1Window = probe.dumpMemoryWindow(
          target.name + ".contactDesc.data1",
          data1Ptr,
          112,
          {
            includeRawBytes: opts.includeRawBytes !== false,
            includePointers: false,
            previewBytes: opts.previewBytes || 256,
            u32PreviewCount: 32,
            f32PreviewCount: 32,
            contactPreviewCount: opts.contactPreviewCount || 8
          }
        );
      }
    }

    if (isSolverConsumeHookName(target.name) && isPointerLike(view, args[0], 32)) {
      extras.push({
        label: target.name + ".solverConstraintDesc",
        ptr: args[0],
        arg1: args[1],
        arg2: args[2],
        solverConstraintDescs: dumpSolverConstraintDescs(
          view,
          target.name,
          args[0],
          opts
        )
      });
    }

    return extras;
  }

  function isSolverConsumeHookName(name) {
    return (
      name === "solveContactBlock" ||
      name === "solveContact_BStaticBlock" ||
      name === "solveContact4Block" ||
      name === "solveContact4StaticBlock" ||
      name === "solveContactBlockWithWriteback" ||
      name === "solveContact_BStaticBlockWithWriteback" ||
      name === "solveContact4BlockWithWriteback" ||
      name === "solveContact4StaticBlockWithWriteback" ||
      name === "solveContactConcludeBlock" ||
      name === "solveContact_BStaticConcludeBlock" ||
      name === "solveContact4ConcludeBlock" ||
      name === "solveContact4StaticConcludeBlock"
    );
  }

  function physxNativePayload(phase, target, argsLike, result, record, dumpState, options) {
    var dumpOptions = physxNativeDumpOptions(target, options);
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
      pointerWindows: probe.dumpPointerArgs(argsLike, dumpOptions),
      extraDumps: physxNativeExtraDumps(target, argsLike, dumpOptions)
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
        if (!shouldDumpPhysXNativeTarget(target, opts, args)) {
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
