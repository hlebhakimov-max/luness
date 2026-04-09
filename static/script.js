/**
 * Система: ДЖАРВИС 
 * Модуль: Масштабное вещание v7.0
 */

const searchInput = document.getElementById('search-input');
const searchBtn = document.getElementById('search-btn');
const resultsContainer = document.getElementById('results');
const pageTitle = document.getElementById('page-title');
const menuSearch = document.getElementById('menu-search');
const menuFavorites = document.getElementById('menu-favorites');
const searchSection = document.getElementById('search-section');

let favorites = JSON.parse(localStorage.getItem('jarvis_favs')) || [];
let globalVolume = localStorage.getItem('jarvis_volume') || 1; // Глобальная громкость

async function searchMusic() {
    const query = searchInput.value.trim();
    if (!query) return;

    pageTitle.innerText = "Результаты поиска (50)";
    resultsContainer.innerHTML = '<p style="color: #1DB954;">Джарвис обрабатывает массив данных...</p>';

    try {
        const response = await fetch('/search?query=' + encodeURIComponent(query));
        const songs = await response.json();
        renderTracks(songs);
    } catch (error) {
        resultsContainer.innerHTML = '<p>Ошибка связи.</p>';
    }
}

function renderTracks(songs) {
    resultsContainer.innerHTML = '';
    songs.forEach((song, index) => {
        const isFav = favorites.some(f => f.id === song.id);
        const card = document.createElement('div');
        card.className = 'track-card';
        card.innerHTML = `
            <button class="fav-btn" onclick='toggleFavorite(${JSON.stringify(song)})'>
                ${isFav ? '❤️' : '🤍'}
            </button>
            <img src="${song.cover}">
            <div class="track-info">
                <h3 title="${song.title}">${song.title}</h3>
                <p>${song.artist}</p>
            </div>
            <audio id="audio-${index}" controls onplay="syncOthers(${index})" onended="playNext(${index})">
                <source src="${song.url}" type="audio/mpeg">
            </audio>
        `;
        resultsContainer.appendChild(card);
        
        // Применяем глобальную громкость к новому плееру
        const audio = document.getElementById(`audio-${index}`);
        audio.volume = globalVolume;

        // Следим за изменением громкости на любом плеере
        audio.onvolumechange = () => {
            globalVolume = audio.volume;
            localStorage.setItem('jarvis_volume', globalVolume);
            syncVolumeAll(globalVolume);
        };
    });
}

// Синхронизация громкости на всех плеерах
function syncVolumeAll(vol) {
    const allAudios = document.querySelectorAll('audio');
    allAudios.forEach(a => a.volume = vol);
}

// Остановка других треков при запуске нового
window.syncOthers = function(currentIndex) {
    const allAudios = document.querySelectorAll('audio');
    allAudios.forEach((a, i) => {
        if (i !== currentIndex) a.pause();
    });
};

// Автоматическое включение следующей песни
window.playNext = function(currentIndex) {
    const nextAudio = document.getElementById(`audio-${currentIndex + 1}`);
    if (nextAudio) {
        nextAudio.play();
        nextAudio.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
};

window.toggleFavorite = function(song) {
    const index = favorites.findIndex(f => f.id === song.id);
    if (index > -1) favorites.splice(index, 1);
    else favorites.push(song);
    localStorage.setItem('jarvis_favs', JSON.stringify(favorites));
    if (pageTitle.innerText === "Избранное") renderTracks(favorites);
    else event.target.innerText = index > -1 ? '🤍' : '❤️';
};

menuSearch.onclick = () => {
    menuSearch.classList.add('active');
    menuFavorites.classList.remove('active');
    searchSection.style.display = 'flex';
    pageTitle.innerText = "Главная";
};

menuFavorites.onclick = () => {
    menuFavorites.classList.add('active');
    menuSearch.classList.remove('active');
    searchSection.style.display = 'none';
    pageTitle.innerText = "Избранное";
    renderTracks(favorites);
};

searchBtn.onclick = searchMusic;
searchInput.onkeypress = (e) => { if (e.key === 'Enter') searchMusic(); };
