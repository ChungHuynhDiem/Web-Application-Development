setTimeout(function () {
  const alert = document.getElementById("autoAlert");
  if (alert) {
    const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
    bsAlert.close();
  }
}, 3000);

