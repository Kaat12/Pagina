//este metodo checa si hay un service worker registrado en el servidor
// y si lo encuentra lo activa
if('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('/serviceWorker.js').then(registration => {
      console.log('SW registrado!: ', registration);
    }).catch(registrationError => {
      console.log('SW fallo al registrar: ', registrationError);
    });
  });
}