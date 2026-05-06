import React from 'react';
import styles from './LoadingSpinner.module.css';

/**
 * LoadingSpinner - Indicador de carga elegante
 *
 * No recibe props. Se renderiza mientras el backend procesa.
 *
 * Muestra:
 * - Spinner animado
 * - Mensajes de estado
 */
function LoadingSpinner() {
  const messages = [
    'Analizando reseñas...',
    'Extrayendo emociones con BERT...',
    'Calculando similitud...',
    'Encontrando joyas ocultas...',
    'Casi listo...'
  ];

  // Mensaje aleatorio
  const randomMessage = messages[Math.floor(Math.random() * messages.length)];

  return (
    <div className={styles.spinner}>
      <div className={styles.spinner__container}>
        <div className={styles.spinner__animation}>
          <div className={styles.spinner__circle} />
          <div className={styles.spinner__circle} />
          <div className={styles.spinner__circle} />
        </div>

        <div className={styles.spinner__text}>
          <p className={styles.spinner__message}>{randomMessage}</p>
          <p className={styles.spinner__hint}>
            Esto puede tomar 1-2 segundos...
          </p>
        </div>
      </div>
    </div>
  );
}

export default LoadingSpinner;
