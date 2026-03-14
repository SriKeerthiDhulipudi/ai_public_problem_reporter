// AI Public Problem Reporter - Main Script

/**
 * Theme Management Functions
 */

function initializeTheme() {
  // Check localStorage for saved theme preference
  const savedTheme = localStorage.getItem("theme") || "light";

  // Apply saved theme to document root
  if (savedTheme === "dark") {
    document.documentElement.classList.add("dark-theme");
  } else {
    document.documentElement.classList.remove("dark-theme");
  }
}

function toggleTheme() {
  // Toggle dark-theme class on document root
  document.documentElement.classList.toggle("dark-theme");

  // Save preference to localStorage
  const isDarkTheme = document.documentElement.classList.contains("dark-theme");
  localStorage.setItem("theme", isDarkTheme ? "dark" : "light");
}

// Initialize theme on page load
document.addEventListener("DOMContentLoaded", function () {
  initializeTheme();

  // Attach theme toggle to button
  const themeToggle = document.querySelector(".theme-toggle");
  if (themeToggle) {
    themeToggle.addEventListener("click", toggleTheme);
  }
});

/**
 * API Helper Functions
 */

async function apiCall(endpoint, method = "GET", data = null) {
  const options = {
    method,
    headers: {
      "Content-Type": "application/json",
    },
  };

  if (data) {
    options.body = JSON.stringify(data);
  }

  try {
    const response = await fetch(endpoint, options);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    return await response.json();
  } catch (error) {
    console.error("API Error:", error);
    throw error;
  }
}

/**
 * Report Management Functions
 */

async function submitReport(formData) {
  return apiCall("/api/submit-report", "POST", formData);
}

async function getReports() {
  return apiCall("/api/reports");
}

async function getReport(referenceId) {
  return apiCall(`/api/reports/${referenceId}`);
}

async function updateReportStatus(referenceId, status) {
  return apiCall(`/api/reports/${referenceId}/status`, "PUT", { status });
}

async function getStatistics() {
  return apiCall("/api/statistics");
}

/**
 * Comment Functions
 */

async function getComments(referenceId) {
  return apiCall(`/api/reports/${referenceId}/comments`);
}

async function addComment(referenceId, comment) {
  return apiCall(`/api/reports/${referenceId}/comments`, "POST", { comment });
}

/**
 * Utility Functions
 */

function formatDate(dateString) {
  return new Date(dateString).toLocaleDateString("en-US", {
    year: "numeric",
    month: "long",
    day: "numeric",
  });
}

function formatDateTime(dateString) {
  return new Date(dateString).toLocaleString("en-US", {
    year: "numeric",
    month: "short",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });
}

function getSeverityEmoji(severity) {
  switch (severity.toLowerCase()) {
    case "high":
      return "🔴";
    case "medium":
      return "🟡";
    case "low":
      return "🟢";
    default:
      return "⚪";
  }
}

function getStatusEmoji(status) {
  switch (status.toLowerCase()) {
    case "submitted":
      return "📋";
    case "under review":
      return "👀";
    case "in progress":
      return "⚙️";
    case "resolved":
      return "✅";
    case "closed":
      return "🔒";
    default:
      return "❓";
  }
}

/**
 * Form Validation
 */

function validateReportForm(data) {
  const errors = [];

  if (!data.problem_type || data.problem_type.trim() === "") {
    errors.push("Problem type is required");
  }

  if (!data.location || data.location.trim() === "") {
    errors.push("Location is required");
  }

  if (!data.description || data.description.trim() === "") {
    errors.push("Description is required");
  }

  if (!data.date_noticed || data.date_noticed.trim() === "") {
    errors.push("Date noticed is required");
  }

  if (!["Low", "Medium", "High"].includes(data.severity)) {
    errors.push("Valid severity level is required");
  }

  if (data.email && !isValidEmail(data.email)) {
    errors.push("Valid email address is required");
  }

  return errors;
}

function isValidEmail(email) {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
}

/**
 * Search and Filter Functions
 */

function searchReports(query) {
  if (!query || query.trim() === "") {
    return getReports();
  }

  return apiCall(`/api/search?q=${encodeURIComponent(query)}`);
}

function filterByDepartment(reports, department) {
  if (!department || department === "all") {
    return reports;
  }
  return reports.filter((r) => r.department === department);
}

function filterBySeverity(reports, severity) {
  if (!severity || severity === "all") {
    return reports;
  }
  return reports.filter((r) => r.severity === severity);
}

function filterByStatus(reports, status) {
  if (!status || status === "all") {
    return reports;
  }
  return reports.filter((r) => r.status === status);
}

/**
 * UI Helper Functions
 */

function showNotification(message, type = "success", duration = 5000) {
  const notification = document.createElement("div");
  notification.className = `notification notification-${type}`;
  notification.textContent = message;

  document.body.appendChild(notification);

  setTimeout(() => {
    notification.style.opacity = "0";
    setTimeout(() => notification.remove(), 300);
  }, duration);
}

function showLoading(element) {
  if (element) {
    element.innerHTML = '<div class="loader">Loading...</div>';
  }
}

function hideLoading(element) {
  if (element) {
    element.innerHTML = "";
  }
}

/**
 * Export Functions
 */

async function exportReportsAsCSV() {
  try {
    const response = await fetch("/api/export/csv");
    const blob = await response.blob();

    const url = window.URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = `reports_${new Date().toISOString().split("T")[0]}.csv`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    window.URL.revokeObjectURL(url);

    showNotification("Reports exported successfully", "success");
  } catch (error) {
    console.error("Export error:", error);
    showNotification("Failed to export reports", "error");
  }
}

function exportReportsAsJSON(reports) {
  const dataStr = JSON.stringify(reports, null, 2);
  const dataBlob = new Blob([dataStr], { type: "application/json" });

  const url = window.URL.createObjectURL(dataBlob);
  const link = document.createElement("a");
  link.href = url;
  link.download = `reports_${new Date().toISOString().split("T")[0]}.json`;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  window.URL.revokeObjectURL(url);

  showNotification("Reports exported successfully", "success");
}

function printReport(reportId) {
  const printWindow = window.open("", "", "width=800,height=600");

  const element = document.querySelector(`[data-report-id="${reportId}"]`);
  if (element) {
    printWindow.document.write(element.innerHTML);
    printWindow.document.close();
    printWindow.print();
  }
}

/**
 * Chart/Visualization Functions
 */

function createStatisticsChart(stats) {
  // This would integrate with a charting library like Chart.js
  // For now, we'll just display text-based statistics

  const chart = {
    totalReports: stats.total_reports,
    bySeverity: stats.by_severity,
    byStatus: stats.by_status,
    byDepartment: stats.by_department,
  };

  return chart;
}

/**
 * Local Storage Functions
 */

function saveDraft(draft) {
  localStorage.setItem("reportDraft", JSON.stringify(draft));
}

function getDraft() {
  const draft = localStorage.getItem("reportDraft");
  return draft ? JSON.parse(draft) : null;
}

function clearDraft() {
  localStorage.removeItem("reportDraft");
}

function loadDraftIntoForm() {
  const draft = getDraft();
  if (!draft) return;

  Object.keys(draft).forEach((key) => {
    const element = document.querySelector(`[name="${key}"]`);
    if (element) {
      if (element.type === "radio") {
        document.querySelector(
          `[name="${key}"][value="${draft[key]}"]`,
        ).checked = true;
      } else {
        element.value = draft[key];
      }
    }
  });
}

/**
 * Event Listeners Setup
 */

document.addEventListener("DOMContentLoaded", function () {
  // Auto-save form drafts
  const form = document.getElementById("reportForm");
  if (form) {
    form.addEventListener("input", function () {
      const formData = new FormData(form);
      const draft = Object.fromEntries(formData);
      saveDraft(draft);
    });
  }

  // Load saved draft on form load
  loadDraftIntoForm();
});

/**
 * Accessibility Functions
 */

function announceToScreenReader(message) {
  const announcement = document.createElement("div");
  announcement.setAttribute("role", "status");
  announcement.setAttribute("aria-live", "polite");
  announcement.style.position = "absolute";
  announcement.style.left = "-10000px";
  announcement.textContent = message;

  document.body.appendChild(announcement);

  setTimeout(() => {
    announcement.remove();
  }, 1000);
}

/**
 * Performance Optimization
 */

// Debounce function for search
function debounce(func, wait) {
  let timeout;
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout);
      func(...args);
    };
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
  };
}

// Throttle function for scroll events
function throttle(func, wait) {
  let timeout;
  return function executedFunction(...args) {
    if (!timeout) {
      func(...args);
      timeout = setTimeout(() => {
        timeout = null;
      }, wait);
    }
  };
}

/**
 * Error Handling
 */

function handleError(error, userFriendlyMessage) {
  console.error("Error:", error);
  showNotification(
    userFriendlyMessage || "An error occurred. Please try again.",
    "error",
  );
}

/**
 * Analytics (Optional)
 */

function trackEvent(eventName, eventData) {
  // This would integrate with analytics service
  console.log("Event tracked:", eventName, eventData);
}

/**
 * Initialization
 */

window.addEventListener("load", function () {
  // Initialize tooltips, popovers, etc.
  console.log("Application loaded successfully");
});
