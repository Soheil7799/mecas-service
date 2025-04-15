// Configuration for API endpoints
const BASE_URL = "http://localhost:8000"; // Update with your actual backend URL

// Application state
const appState = {
  uploadedFilename: null,
  videoProcessed: false,
  filterConfig: {
    // Audio Filters
    gainApply: false,
    gainCompressorThreshold: -1.0,
    limiterThreshold: 0.0,

    voiceEnhanceApply: false,
    preemphasisAlpha: 3.0,
    highPassOrder: 2.0,

    denoiseDelayApply: false,
    noisePower: -15,
    delay: 100,
    delayGain: 50,

    phoneLikeApply: false,
    phoneSideGain: 0.0,
    phoneFilterOrder: 1.0,

    carLikeApply: false,
    carSideGain: 3.0,
    carFilterOrder: 1.0,

    // Video Filters
    grayScaleApply: false,
    invertApply: false,
    frameInterpolateApply: false,
    frameTargetFps: 60,
    upscaleApply: false,
    upscaleWidth: 1280,
    upscaleHeight: 720,
  },
};

// DOM Elements
const fileUpload = document.getElementById("fileUpload");
const uploadStatus = document.getElementById("uploadStatus");
const filtersSection = document.getElementById("filtersSection");
const videoSection = document.getElementById("videoSection");
const deleteSection = document.getElementById("deleteSection");
const processedVideo = document.getElementById("processedVideo");
const applyFiltersBtn = document.getElementById("applyFiltersBtn");
const applyStatus = document.getElementById("applyStatus");
const deleteFileBtn = document.getElementById("deleteFileBtn");
const deleteStatus = document.getElementById("deleteStatus");

// Toggle Button Elements
const toggleButtons = {
  gainCompressor: document.getElementById("gainCompressorBtn"),
  voiceEnhance: document.getElementById("voiceEnhanceBtn"),
  denoiseDelay: document.getElementById("denoiseDelayBtn"),
  phoneLike: document.getElementById("phoneLikeBtn"),
  carLike: document.getElementById("carLikeBtn"),
  grayscale: document.getElementById("grayscaleBtn"),
  colorInvert: document.getElementById("colorInvertBtn"),
  frameInterpolate: document.getElementById("frameInterpolateBtn"),
  upscale: document.getElementById("upscaleBtn"),
};

// Filter Control Elements
const filterControls = {
  gainCompressor: document.getElementById("gainCompressorControls"),
  voiceEnhance: document.getElementById("voiceEnhanceControls"),
  denoiseDelay: document.getElementById("denoiseDelayControls"),
  phoneLike: document.getElementById("phoneLikeControls"),
  carLike: document.getElementById("carLikeControls"),
  frameInterpolate: document.getElementById("frameInterpolateControls"),
  upscale: document.getElementById("upscaleControls"),
};

// Input Elements
const inputElements = {
  // Audio Filters
  gainCompressorThreshold: document.getElementById("gainCompressorThreshold"),
  limiterThreshold: document.getElementById("limiterThreshold"),
  preemphasisAlpha: document.getElementById("preemphasisAlpha"),
  highPassOrder: document.getElementById("highPassOrder"),
  noisePower: document.getElementById("noisePower"),
  delay: document.getElementById("delay"),
  delayGain: document.getElementById("delayGain"),
  phoneSideGain: document.getElementById("phoneSideGain"),
  phoneFilterOrder: document.getElementById("phoneFilterOrder"),
  carSideGain: document.getElementById("carSideGain"),
  carFilterOrder: document.getElementById("carFilterOrder"),

  // Video Filters
  frameTargetFps: document.getElementById("frameTargetFps"),
  upscaleWidth: document.getElementById("upscaleWidth"),
  upscaleHeight: document.getElementById("upscaleHeight"),
};

// Helper Functions
function showStatusMessage(element, message, type) {
  element.textContent = message;
  element.className = `status-message ${type}`;
}

function clearStatusMessage(element) {
  element.textContent = "";
  element.className = "status-message";
}

function toggleFilterSection(show) {
  if (show) {
    filtersSection.classList.remove("hidden");
    deleteSection.classList.remove("hidden");
  } else {
    filtersSection.classList.add("hidden");
    deleteSection.classList.add("hidden");
  }
}

function toggleVideoSection(show) {
  if (show) {
    videoSection.classList.remove("hidden");
  } else {
    videoSection.classList.add("hidden");
  }
}

function resetAppState() {
  appState.uploadedFilename = null;
  appState.videoProcessed = false;

  // Reset all filter states
  for (const key in appState.filterConfig) {
    if (key.includes("Apply")) {
      appState.filterConfig[key] = false;
    }
  }

  // Reset UI
  clearStatusMessage(uploadStatus);
  clearStatusMessage(applyStatus);
  clearStatusMessage(deleteStatus);
  toggleFilterSection(false);
  toggleVideoSection(false);

  // Reset all toggle buttons
  for (const key in toggleButtons) {
    if (toggleButtons[key]) {
      toggleButtons[key].setAttribute("data-active", "false");
      toggleButtons[key].textContent =
        `○ ${toggleButtons[key].textContent.replace("✓ ", "").replace("○ ", "")}`;
    }
  }

  // Hide all filter controls
  for (const key in filterControls) {
    if (filterControls[key]) {
      filterControls[key].classList.add("hidden");
    }
  }

  // Reset file input
  fileUpload.value = "";
}

// Toggle Button Function
function setupToggleButton(buttonId, configKey, controlsId) {
  const button = document.getElementById(buttonId);
  const controls = document.getElementById(controlsId);

  if (button && controls) {
    button.addEventListener("click", () => {
      const currentState = button.getAttribute("data-active") === "true";
      const newState = !currentState;

      // Update button state
      button.setAttribute("data-active", newState.toString());
      button.textContent = `${newState ? "✓ " : "○ "}${button.textContent.replace("✓ ", "").replace("○ ", "")}`;

      // Update app state
      appState.filterConfig[configKey] = newState;

      // Show/hide controls
      if (controls) {
        if (newState) {
          controls.classList.remove("hidden");
        } else {
          controls.classList.add("hidden");
        }
      }
    });
  }
}

// Setup simple toggle buttons without controls
function setupSimpleToggleButton(buttonId, configKey) {
  const button = document.getElementById(buttonId);

  if (button) {
    button.addEventListener("click", () => {
      const currentState = button.getAttribute("data-active") === "true";
      const newState = !currentState;

      // Update button state
      button.setAttribute("data-active", newState.toString());
      button.textContent = `${newState ? "✓ " : "○ "}${button.textContent.replace("✓ ", "").replace("○ ", "")}`;

      // Update app state
      appState.filterConfig[configKey] = newState;
    });
  }
}

// File Upload Handler
fileUpload.addEventListener("change", async (event) => {
  const file = event.target.files[0];

  if (!file) return;

  // Validate file type
  const validTypes = ["video/mp4", "video/avi", "video/quicktime"];
  if (!validTypes.includes(file.type)) {
    showStatusMessage(
      uploadStatus,
      "Invalid file type. Please upload MP4, AVI, or MOV files.",
      "error",
    );
    return;
  }

  // Validate file size (200MB limit)
  if (file.size > 200 * 1024 * 1024) {
    showStatusMessage(uploadStatus, "File size exceeds 200MB limit", "error");
    return;
  }

  // Create FormData for file upload
  const formData = new FormData();
  formData.append("video_file", file);

  try {
    showStatusMessage(uploadStatus, "Uploading file...", "info");

    const response = await fetch(`${BASE_URL}/uploadfile/`, {
      method: "POST",
      body: formData,
    });

    const data = await response.text();

    if (response.status === 201) {
      appState.uploadedFilename = file.name;
      showStatusMessage(uploadStatus, "File uploaded successfully!", "success");
      toggleFilterSection(true);
    } else {
      showStatusMessage(uploadStatus, `Upload failed: ${data}`, "error");
    }
  } catch (error) {
    showStatusMessage(uploadStatus, `Upload error: ${error.message}`, "error");
  }
});

// Apply Filters Handler
applyFiltersBtn.addEventListener("click", async () => {
  if (!appState.uploadedFilename) {
    showStatusMessage(applyStatus, "No file uploaded", "error");
    return;
  }

  try {
    showStatusMessage(applyStatus, "Applying filters...", "info");

    // Update filter configuration from input values
    appState.filterConfig.gainCompressorThreshold = parseFloat(
      inputElements.gainCompressorThreshold.value,
    );
    appState.filterConfig.limiterThreshold = parseFloat(
      inputElements.limiterThreshold.value,
    );
    appState.filterConfig.preemphasisAlpha = parseFloat(
      inputElements.preemphasisAlpha.value,
    );
    appState.filterConfig.highPassOrder = parseFloat(
      inputElements.highPassOrder.value,
    );
    appState.filterConfig.noisePower = parseInt(inputElements.noisePower.value);
    appState.filterConfig.delay = parseInt(inputElements.delay.value);
    appState.filterConfig.delayGain = parseInt(inputElements.delayGain.value);
    appState.filterConfig.phoneSideGain = parseFloat(
      inputElements.phoneSideGain.value,
    );
    appState.filterConfig.phoneFilterOrder = parseFloat(
      inputElements.phoneFilterOrder.value,
    );
    appState.filterConfig.carSideGain = parseFloat(
      inputElements.carSideGain.value,
    );
    appState.filterConfig.carFilterOrder = parseFloat(
      inputElements.carFilterOrder.value,
    );
    appState.filterConfig.frameTargetFps = parseInt(
      inputElements.frameTargetFps.value,
    );
    appState.filterConfig.upscaleWidth = parseInt(
      inputElements.upscaleWidth.value,
    );
    appState.filterConfig.upscaleHeight = parseInt(
      inputElements.upscaleHeight.value,
    );

    // Prepare filter payload
    const payload = {
      fileName: appState.uploadedFilename,
      fileFormat: 1, // VIDEO
      fileExtension: appState.uploadedFilename.slice(
        appState.uploadedFilename.lastIndexOf("."),
      ),
      filePath: "./files/input",

      // Audio Filters
      gainComp: {
        enabled: appState.filterConfig.gainApply,
        compressorThreshold: appState.filterConfig.gainCompressorThreshold,
        limitThreshold: appState.filterConfig.limiterThreshold,
      },
      voiceEnh: {
        enabled: appState.filterConfig.voiceEnhanceApply,
        alpha: appState.filterConfig.preemphasisAlpha,
        highPass: appState.filterConfig.highPassOrder,
      },
      denDel: {
        enabled: appState.filterConfig.denoiseDelayApply,
        noisePower: appState.filterConfig.noisePower,
        delay: appState.filterConfig.delay,
        delayGain: appState.filterConfig.delayGain,
      },
      phoneLike: {
        enabled: appState.filterConfig.phoneLikeApply,
        sideGain: parseInt(appState.filterConfig.phoneSideGain),
        order: appState.filterConfig.phoneFilterOrder,
      },
      carLike: {
        enabled: appState.filterConfig.carLikeApply,
        sideGain: parseInt(appState.filterConfig.carSideGain),
        order: appState.filterConfig.carFilterOrder,
      },

      // Video Filters
      grayScale: {
        enabled: appState.filterConfig.grayScaleApply,
      },
      colorInvert: {
        enabled: appState.filterConfig.invertApply,
      },
      frameTarget: {
        enabled: appState.filterConfig.frameInterpolateApply,
        targetFPS: appState.filterConfig.frameTargetFps,
      },
      upscalingTarget: {
        enabled: appState.filterConfig.upscaleApply,
        width: appState.filterConfig.upscaleWidth,
        height: appState.filterConfig.upscaleHeight,
      },
    };

    const response = await fetch(`${BASE_URL}/application`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    });

    const data = await response.text();

    if (response.status === 200) {
      showStatusMessage(
        applyStatus,
        "Filters applied successfully!",
        "success",
      );
      appState.videoProcessed = true;

      // Stream the processed video
      streamProcessedVideo();
    } else {
      showStatusMessage(
        applyStatus,
        `Filter application failed: ${data}`,
        "error",
      );
    }
  } catch (error) {
    showStatusMessage(
      applyStatus,
      `Error applying filters: ${error.message}`,
      "error",
    );
  }
});

// Stream Processed Video
async function streamProcessedVideo() {
  try {
    showStatusMessage(applyStatus, "Streaming processed video...", "info");

    const response = await fetch(`${BASE_URL}/stream/`);

    if (response.status === 200) {
      // Convert response to blob and create a URL
      const videoBlob = await response.blob();
      const videoUrl = URL.createObjectURL(videoBlob);

      // Set the video source and display it
      processedVideo.src = videoUrl;
      toggleVideoSection(true);
      showStatusMessage(
        applyStatus,
        "Video processed successfully!",
        "success",
      );
    } else {
      showStatusMessage(
        applyStatus,
        "Failed to stream processed video",
        "error",
      );
    }
  } catch (error) {
    showStatusMessage(
      applyStatus,
      `Streaming error: ${error.message}`,
      "error",
    );
  }
}

// Delete File Handler
deleteFileBtn.addEventListener("click", async () => {
  if (!appState.uploadedFilename) {
    showStatusMessage(deleteStatus, "No file to delete", "error");
    return;
  }

  try {
    const response = await fetch(`${BASE_URL}/`, {
      method: "DELETE",
    });

    const data = await response.text();

    if (response.status === 200) {
      showStatusMessage(deleteStatus, "File deleted successfully!", "success");

      // Reset app state and UI
      setTimeout(() => {
        resetAppState();
      }, 2000);
    } else {
      showStatusMessage(
        deleteStatus,
        `Failed to delete file: ${data}`,
        "error",
      );
    }
  } catch (error) {
    showStatusMessage(deleteStatus, `Delete failed: ${error.message}`, "error");
  }
});

// Setup drag and drop functionality
const dropArea = document.querySelector(".file-drop-area");

["dragenter", "dragover", "dragleave", "drop"].forEach((eventName) => {
  dropArea.addEventListener(eventName, preventDefaults, false);
});

function preventDefaults(e) {
  e.preventDefault();
  e.stopPropagation();
}

["dragenter", "dragover"].forEach((eventName) => {
  dropArea.addEventListener(eventName, highlight, false);
});

["dragleave", "drop"].forEach((eventName) => {
  dropArea.addEventListener(eventName, unhighlight, false);
});

function highlight() {
  dropArea.style.borderColor = "#2980b9";
  dropArea.style.backgroundColor = "rgba(52, 152, 219, 0.05)";
}

function unhighlight() {
  dropArea.style.borderColor = "#3498db";
  dropArea.style.backgroundColor = "";
}

dropArea.addEventListener("drop", handleDrop, false);

function handleDrop(e) {
  const dt = e.dataTransfer;
  const files = dt.files;

  if (files.length > 0) {
    fileUpload.files = files;
    // Trigger the change event manually
    const event = new Event("change");
    fileUpload.dispatchEvent(event);
  }
}

// Initialize all toggle buttons
function initializeToggleButtons() {
  // Audio filters with controls
  setupToggleButton("gainCompressorBtn", "gainApply", "gainCompressorControls");
  setupToggleButton(
    "voiceEnhanceBtn",
    "voiceEnhanceApply",
    "voiceEnhanceControls",
  );
  setupToggleButton(
    "denoiseDelayBtn",
    "denoiseDelayApply",
    "denoiseDelayControls",
  );
  setupToggleButton("phoneLikeBtn", "phoneLikeApply", "phoneLikeControls");
  setupToggleButton("carLikeBtn", "carLikeApply", "carLikeControls");

  // Video filters with controls
  setupToggleButton(
    "frameInterpolateBtn",
    "frameInterpolateApply",
    "frameInterpolateControls",
  );
  setupToggleButton("upscaleBtn", "upscaleApply", "upscaleControls");

  // Simple toggle buttons without controls
  setupSimpleToggleButton("grayscaleBtn", "grayScaleApply");
  setupSimpleToggleButton("colorInvertBtn", "invertApply");
}

// Initialize the application
function init() {
  // Initialize toggle buttons
  initializeToggleButtons();

  // Hide filters and video sections initially
  toggleFilterSection(false);
  toggleVideoSection(false);
}

// Start the application
init();
