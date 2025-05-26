// EJEMPLO DE IMPLEMENTACIÓN
// Este código muestra cómo implementar la funcionalidad de texto a voz
// utilizando la Web Speech API en un navegador web moderno.

document.addEventListener('DOMContentLoaded', () => {
  // Referencias a elementos de la interfaz
  const textInput = document.getElementById('texto');
  const voiceSelect = document.getElementById('voz');
  const speedRange = document.getElementById('velocidad');
  const volumeRange = document.getElementById('volumen');
  const playButton = document.getElementById('btnReproducir');
  const statusElement = document.getElementById('estado');

  // Estado de la aplicación
  const appState = {
    synth: null,
    voices: [],
    speaking: false
  };

  // Inicializar la aplicación
  initializeSpeechSynth();
  
  // Inicializar sintetizador de voz
  function initializeSpeechSynth() {
    if ('speechSynthesis' in window) {
      appState.synth = window.speechSynthesis;
      loadVoices();
      
      // En algunos navegadores, las voces se cargan de forma asíncrona
      appState.synth.onvoiceschanged = loadVoices;
      
      statusElement.textContent = 'Síntesis de voz disponible';
      statusElement.classList.add('online');
    } else {
      statusElement.textContent = 'Síntesis de voz no soportada';
      statusElement.classList.add('offline');
      disableControls();
    }
  }
  
  // Cargar voces disponibles
  function loadVoices() {
    appState.voices = appState.synth.getVoices();
    
    if (appState.voices.length > 0) {
      // Agrupar voces por idioma
      const voicesByLanguage = {};
      
      appState.voices.forEach(voice => {
        // Obtener código de idioma (primeros 2 caracteres)
        const langCode = voice.lang.substring(0, 2);
        const langName = getLanguageName(langCode);
        
        if (!voicesByLanguage[langName]) {
          voicesByLanguage[langName] = [];
        }
        
        voicesByLanguage[langName].push(voice);
      });
      
      // Limpiar select existente
      voiceSelect.innerHTML = '';
      
      // Crear optgroups para cada idioma
      Object.keys(voicesByLanguage).sort().forEach(lang => {
        const optgroup = document.createElement('optgroup');
        optgroup.label = lang;
        
        voicesByLanguage[lang].forEach(voice => {
          const option = document.createElement('option');
          option.value = voice.name;
          option.textContent = voice.name;
          optgroup.appendChild(option);
        });
        
        voiceSelect.appendChild(optgroup);
      });
      
      // Seleccionar voz en español si está disponible
      const spanishVoice = appState.voices.find(v => v.lang.startsWith('es'));
      if (spanishVoice) {
        voiceSelect.value = spanishVoice.name;
      }
    } else {
      voiceSelect.innerHTML = '<option disabled>No hay voces disponibles</option>';
    }
  }
  
  // Obtener nombre completo del idioma a partir del código
  function getLanguageName(code) {
    const languages = {
      'es': 'Español',
      'en': 'Inglés',
      'fr': 'Francés',
      'de': 'Alemán',
      'it': 'Italiano',
      'pt': 'Portugués',
      'ru': 'Ruso',
      'ja': 'Japonés',
      'ko': 'Coreano',
      'zh': 'Chino',
      'ar': 'Árabe',
      'hi': 'Hindi'
    };
    
    return languages[code] || `Idioma (${code})`;
  }
  
  // Reproducir texto
  function playText() {
    const text = textInput.value.trim();
    
    if (!text) {
      alert('Por favor, ingresa un texto para reproducir');
      return;
    }
    
    // Si ya está hablando, detenerlo
    if (appState.speaking) {
      appState.synth.cancel();
      appState.speaking = false;
      playButton.innerHTML = '<i class="fas fa-play"></i> Reproducir';
      return;
    }
    
    // Crear un nuevo objeto de síntesis de voz
    const utterance = new SpeechSynthesisUtterance(text);
    
    // Establecer propiedades
    utterance.rate = parseFloat(speedRange.value) / 175; // Ajustar velocidad
    utterance.volume = parseFloat(volumeRange.value);
    
    // Establecer voz seleccionada
    const selectedVoice = appState.voices.find(v => v.name === voiceSelect.value);
    if (selectedVoice) {
      utterance.voice = selectedVoice;
    }
    
    // Establecer eventos
    utterance.onstart = () => {
      appState.speaking = true;
      playButton.innerHTML = '<i class="fas fa-stop"></i> Detener';
    };
    
    utterance.onend = () => {
      appState.speaking = false;
      playButton.innerHTML = '<i class="fas fa-play"></i> Reproducir';
    };
    
    utterance.onerror = (event) => {
      console.error('Error en la síntesis:', event);
      appState.speaking = false;
      playButton.innerHTML = '<i class="fas fa-play"></i> Reproducir';
    };
    
    // Reproducir
    appState.synth.speak(utterance);
  }
  
  // Deshabilitar controles cuando no hay soporte
  function disableControls() {
    textInput.disabled = true;
    voiceSelect.disabled = true;
    speedRange.disabled = true;
    volumeRange.disabled = true;
    playButton.disabled = true;
  }
  
  // Configurar eventos
  playButton.addEventListener('click', playText);
  
  // Actualizar valores en pantalla para los controles deslizantes
  speedRange.addEventListener('input', () => {
    document.getElementById('velocidadValor').textContent = speedRange.value;
  });
  
  volumeRange.addEventListener('input', () => {
    document.getElementById('volumenValor').textContent = volumeRange.value;
  });
});

