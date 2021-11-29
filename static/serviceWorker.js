//se crean variables para registrar la cache del server
const cacheName = "FASHION-STORE-CACHE"
//arreglo de archivos que se van a cachear
const filesToCache = [
    '/static/app.js',
    '/static/styleOffline.css',
    '/static/offline.html'
];

//cuando el evento instalar se ejecuta para instalar el service worker,
// este cachea todo lo que esta en la constante antes establecida.
self.addEventListener('install', (e)=>{
    console.log('[ServiceWorker] install');
    e.waitUntil(
        caches.open(cacheName)
        .then((cache)=>{
            console.log('[ServiceWorker] caheando la app...');
            return cache.addAll(filesToCache)
            .then(()=>self.skipWaiting())
        })
        .catch((err)=>console.log('No se pudo cachear', err))
    )
});
//este metodo esta a la escucha y cuando sea llamado
//va activar el service worker, este va actualizar la cache cada que algun
//archivo cambie, generalmente se llama despues del evento install
self.addEventListener('activate', (e)=>{
    console.log('[ServiceWorker] activate');
    const cacheWhitelist = [cacheName];

    e.waitUntil(
        caches.keys()
        .then((cacheNames)=>{
            cacheNames.map((cacheName)=>{
                if(cacheWhitelist.indexOf(cacheName)===-1){
                    return caches.delete(cacheName);
                }
            })
        })
        .then(()=>self.clients.claim())
    )
});
//el evento fetch se ejecuta cuando se hace una peticion a la pagina, 
//este metodo va a verificar si la peticion es de un archivo que se va a cachear
//si es asi va a devolver el archivo de la cache, si no va a devolver la peticion
// al server
self.addEventListener('fetch', (e)=>{
    console.log('[ServiceWorker] fetch');
    e.respondWith(
        caches.match(e.request)
        .then((res)=>{
            if(res){
                console.log('[ServiceWorker] devolviendo cache');
                return res;
            }
            console.log('[ServiceWorker] devolviendo server');
            return fetch(e.request);
        })
    );
});

