import React, { useState } from 'react';
import { CheckCircle, XCircle, RotateCcw } from 'lucide-react';

export default function App() {
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [score, setScore] = useState(0);
  const [showScore, setShowScore] = useState(false);
  const [selectedAnswer, setSelectedAnswer] = useState(null);
  const [answeredQuestions, setAnsweredQuestions] = useState([]);

  const questions = [
    {
      question: "What is the capital of France?",
      options: ["London", "Berlin", "Paris", "Madrid"],
      correctAnswer: 2
    },
    {
      question: "Which planet is known as the Red Planet?",
      options: ["Venus", "Mars", "Jupiter", "Saturn"],
      correctAnswer: 1
    },
    {
      question: "What is the largest ocean on Earth?",
      options: ["Atlantic Ocean", "Indian Ocean", "Arctic Ocean", "Pacific Ocean"],
      correctAnswer: 3
    },
    {
      question: "Who painted the Mona Lisa?",
      options: ["Vincent van Gogh", "Leonardo da Vinci", "Pablo Picasso", "Michelangelo"],
      correctAnswer: 1
    },
    {
      question: "What is the smallest prime number?",
      options: ["0", "1", "2", "3"],
      correctAnswer: 2
    }
  ];

  const handleAnswerClick = (selectedIndex) => {
    setSelectedAnswer(selectedIndex);
    
    const isCorrect = selectedIndex === questions[currentQuestion].correctAnswer;
    
    setAnsweredQuestions([...answeredQuestions, {
      question: currentQuestion,
      selected: selectedIndex,
      correct: isCorrect
    }]);

    if (isCorrect) {
      setScore(score + 1);
    }

    setTimeout(() => {
      const nextQuestion = currentQuestion + 1;
      if (nextQuestion < questions.length) {
        setCurrentQuestion(nextQuestion);
        setSelectedAnswer(null);
      } else {
        setShowScore(true);
      }
    }, 1000);
  };

  const resetQuiz = () => {
    setCurrentQuestion(0);
    setScore(0);
    setShowScore(false);
    setSelectedAnswer(null);
    setAnsweredQuestions([]);
  };

  const getButtonStyle = (index) => {
    if (selectedAnswer === null) {
      return "bg-white hover:bg-blue-50 border-2 border-gray-300";
    }
    
    if (index === questions[currentQuestion].correctAnswer) {
      return "bg-green-100 border-2 border-green-500";
    }
    
    if (index === selectedAnswer && index !== questions[currentQuestion].correctAnswer) {
      return "bg-red-100 border-2 border-red-500";
    }
    
    return "bg-gray-100 border-2 border-gray-300";
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center p-4">
      <div className="bg-white rounded-2xl shadow-xl p-8 w-full max-w-2xl">
        {showScore ? (
          <div className="text-center">
            <h2 className="text-3xl font-bold text-gray-800 mb-4">Quiz Complete! 🎉</h2>
            <div className="bg-blue-50 rounded-xl p-6 mb-6">
              <p className="text-5xl font-bold text-blue-600 mb-2">{score}/{questions.length}</p>
              <p className="text-gray-600">Correct Answers</p>
            </div>
            <p className="text-lg text-gray-700 mb-6">
              {score === questions.length && "Perfect score! Outstanding! 🌟"}
              {score >= questions.length * 0.7 && score < questions.length && "Great job! Well done! 👏"}
              {score >= questions.length * 0.4 && score < questions.length * 0.7 && "Not bad! Keep practicing! 💪"}
              {score < questions.length * 0.4 && "Keep learning and try again! 📚"}
            </p>
            <button
              onClick={resetQuiz}
              className="bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 px-6 rounded-lg flex items-center gap-2 mx-auto transition-colors"
            >
              <RotateCcw size={20} />
              Try Again
            </button>
          </div>
        ) : (
          <div>
            <div className="mb-6">
              <div className="flex justify-between items-center mb-4">
                <span className="text-sm font-semibold text-blue-600 bg-blue-100 px-3 py-1 rounded-full">
                  Question {currentQuestion + 1}/{questions.length}
                </span>
                <span className="text-sm font-semibold text-gray-600">
                  Score: {score}/{questions.length}
                </span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div
                  className="bg-blue-600 h-2 rounded-full transition-all duration-300"
                  style={{ width: `${((currentQuestion + 1) / questions.length) * 100}%` }}
                />
              </div>
            </div>

            <h2 className="text-2xl font-bold text-gray-800 mb-6">
              {questions[currentQuestion].question}
            </h2>

            <div className="space-y-3">
              {questions[currentQuestion].options.map((option, index) => (
                <button
                  key={index}
                  onClick={() => handleAnswerClick(index)}
                  disabled={selectedAnswer !== null}
                  className={`w-full text-left p-4 rounded-lg font-medium transition-all ${getButtonStyle(index)} ${
                    selectedAnswer === null ? 'cursor-pointer' : 'cursor-not-allowed'
                  }`}
                >
                  <div className="flex items-center justify-between">
                    <span>{option}</span>
                    {selectedAnswer !== null && index === questions[currentQuestion].correctAnswer && (
                      <CheckCircle className="text-green-600" size={24} />
                    )}
                    {selectedAnswer === index && index !== questions[currentQuestion].correctAnswer && (
                      <XCircle className="text-red-600" size={24} />
                    )}
                  </div>
                </button>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}