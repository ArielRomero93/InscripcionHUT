function startClock() {
    const timeZones = {
        argentina: -3,     // Buenos Aires
        chile: -3,         // Santiago, Chile
        brasil: -3,        // Brasília
        colombia: -5,      // Bogotá
        elsalvador: -6,    // San Salvador
        mexico: -6,        // Ciudad de México
        usa: -5,           // Washington D.C. (Hora del Este)
        canada: -5         // Ottawa (Hora del Este)
    };

    function updateClocks() {
        const nowUTC = new Date().getTime() + (new Date().getTimezoneOffset() * 60000);

        for (const [country, offset] of Object.entries(timeZones)) {
            const localTime = new Date(nowUTC + (offset * 3600000));
            const hours = localTime.getHours().toString().padStart(2, '0');
            const minutes = localTime.getMinutes().toString().padStart(2, '0');
            document.getElementById(country).textContent = `${hours}:${minutes}`;
        }
    }

    // Llamar a updateClocks inmediatamente para mostrar la hora actual
    updateClocks();

    // Actualizar cada minuto (60000 ms)
    setInterval(updateClocks, 60000);
}

window.onload = startClock;
