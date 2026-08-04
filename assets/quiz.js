/**
 * quiz.js — Interactive quiz widget for lessons
 * 
 * Usage in HTML:
 *   <div class="quiz" data-quiz-id="unique-id">
 *     <p class="quiz-question">Question text here?</p>
 *     <div class="quiz-options">
 *       <button class="quiz-option" data-correct="true">Correct answer</button>
 *       <button class="quiz-option">Wrong answer A</button>
 *       <button class="quiz-option">Wrong answer B</button>
 *       <button class="quiz-option">Wrong answer C</button>
 *     </div>
 *     <div class="quiz-feedback" hidden></div>
 *   </div>
 */

(function () {
  'use strict';

  const FEEDBACK = {
    correct: ['✅ 完全正确！', '✅ 答对了！', '✅ 没错！理解得很准确。'],
    incorrect: ['❌ 不太对，再想想？', '❌ 差一点，再试一次？', '❌ 这个不太准确，看看其他选项？'],
  };

  function randomPick(arr) {
    return arr[Math.floor(Math.random() * arr.length)];
  }

  function initQuiz(quizEl) {
    const options = quizEl.querySelectorAll('.quiz-option');
    const feedback = quizEl.querySelector('.quiz-feedback');
    let answered = false;

    options.forEach((btn) => {
      btn.addEventListener('click', () => {
        if (answered) return;

        const isCorrect = btn.dataset.correct === 'true';

        // Visual feedback
        options.forEach((b) => {
          b.disabled = true;
          b.classList.add('quiz-option--disabled');
          if (b.dataset.correct === 'true') {
            b.classList.add('quiz-option--correct');
          }
        });

        if (!isCorrect) {
          btn.classList.add('quiz-option--incorrect');
        }

        // Text feedback
        feedback.hidden = false;
        feedback.textContent = isCorrect
          ? randomPick(FEEDBACK.correct)
          : randomPick(FEEDBACK.incorrect);
        feedback.className = 'quiz-feedback ' + (isCorrect ? 'quiz-feedback--correct' : 'quiz-feedback--incorrect');

        // If incorrect, allow retry after a delay
        if (!isCorrect) {
          setTimeout(() => {
            options.forEach((b) => {
              if (!b.classList.contains('quiz-option--correct')) {
                b.disabled = false;
                b.classList.remove('quiz-option--disabled', 'quiz-option--incorrect');
              }
            });
            btn.disabled = true;
            btn.classList.add('quiz-option--disabled', 'quiz-option--incorrect');
            feedback.hidden = true;
          }, 1500);
        } else {
          answered = true;
        }
      });
    });
  }

  // Initialize all quizzes on page load
  document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.quiz').forEach(initQuiz);
  });
})();
