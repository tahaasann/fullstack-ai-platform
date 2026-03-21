import json
from services.lesson_loader import load_quiz_content


def evaluate_quiz(quiz_content_path: str, answers: dict) -> dict:
    """Evaluate submitted quiz answers against correct answers."""
    quiz_data = load_quiz_content(quiz_content_path)
    questions = quiz_data.get("questions", [])

    results = []
    correct_count = 0
    total_points = 0
    earned_points = 0

    for q in questions:
        qid = q["id"]
        q_type = q["type"]
        points = q.get("points", 10)
        total_points += points
        user_answer = answers.get(qid)
        is_correct = False

        if q_type == "multiple_choice":
            correct = q["correct"]
            is_correct = user_answer == correct

        elif q_type == "true_false":
            correct = q["correct"]
            is_correct = user_answer == correct

        elif q_type == "code_completion":
            correct_answers = q.get("correct_answers", [])
            if isinstance(user_answer, str):
                is_correct = user_answer.strip().lower() in [a.lower() for a in correct_answers]

        elif q_type == "explain_code":
            # Soft grading: check keyword presence
            keywords = q.get("correct_keywords", [])
            if isinstance(user_answer, str) and keywords:
                user_lower = user_answer.lower()
                matched = sum(1 for kw in keywords if kw.lower() in user_lower)
                is_correct = matched >= len(keywords) * 0.6
            # Always show sample answer regardless
            pass

        elif q_type == "order_steps":
            correct_order = q.get("correct_order", [])
            if isinstance(user_answer, list):
                is_correct = user_answer == correct_order

        if is_correct:
            correct_count += 1
            earned_points += points

        results.append({
            "question_id": qid,
            "question": q.get("question", ""),
            "type": q_type,
            "user_answer": user_answer,
            "is_correct": is_correct,
            "explanation": q.get("explanation", ""),
            "sample_answer": q.get("sample_answer", ""),
            "correct_answer": q.get("correct", q.get("correct_answers", q.get("correct_order", ""))),
            "points": points,
            "earned": points if is_correct else 0
        })

    score = (earned_points / total_points * 100) if total_points > 0 else 0
    passing_score = quiz_data.get("passing_score", 70)

    return {
        "score": round(score, 1),
        "passed": score >= passing_score,
        "correct_count": correct_count,
        "total_count": len(questions),
        "results": results
    }
