import pygame
import config

def handle_dialog_response(game, response):
    pygame.event.clear()
    response = response.lower()
    print(f"Received response: {response}")  # Debug Print
    
    if game.current_question_index == 0 and not game.waiting_for_answer:
        if response == 'y':
            print("Starting Question Sequence.")  # Debug Print
            game.waiting_for_answer = True
            ask_next_question(game)
        elif response == 'n':
            game.show_dialog(f"Austin!! {game.name} is not ready!!! Come here to help!", auto_hide_seconds=4)
        pygame.event.clear()
        return

    if game.waiting_for_answer:
        if check_answer(game, response):
            game.correct_answers += 1
            game.show_dialog(
                f"Good job! You've answered {game.correct_answers} out of {game.total_questions} questions correctly.",
                auto_hide_seconds=7)
            game.current_attempt = 0
            game.current_question_index += 1
            game.waiting_for_answer = False
            pygame.time.set_timer(pygame.USEREVENT + 2, 3000)
        else:
            game.current_attempt += 1
            game.health_bar.update_health(-10)

            if game.current_attempt >= game.max_attempts:
                correct_answer = game.questions[game.current_question_index]["answer"]
                game.dialog_box.show(f"Oh no! The correct answer was: {correct_answer}", auto_hide_seconds=5)
                game.current_attempt = 0
                game.waiting_for_answer = False
                game.current_question_index += 1
                pygame.time.set_timer(pygame.USEREVENT + 2, 5000)  # Give more time to read the correct answer
            else:
                attempts_left = game.max_attempts - game.current_attempt
                game.dialog_box.show(f"Wrong! Attempts left: {attempts_left}. Please try again!",
                                     auto_hide_seconds=3)
                set_timer(game)
            pygame.event.clear()

def ask_next_question(game):
    pygame.event.clear()
    if game.current_question_index < game.total_questions:
        question = game.questions[game.current_question_index]["question"]
        game.dialog_box.show(f"No# {game.current_question_index + 1}: {question}")
        game.waiting_for_answer = True
    else:
        if game.correct_answers == game.total_questions:
            game.dialog_box.show(
                "Congratulations! You've answered all 5 questions correctly. You've passed Level One!",
                auto_hide_seconds=5)
        else:
            game.show_dialog(
                f"You've only answered {game.correct_answers} out of {game.total_questions} questions correctly. You need to answer all 5 questions correctly to pass. Try again!",
                auto_hide_seconds=6)
            game.restart_level()
        game.waiting_for_answer = False

def check_answer(game, response):
    correct_answer = game.questions[game.current_question_index]["answer"]
    print(f"Checking answer: '{response.strip().lower()}' against correct answer: '{correct_answer.strip().lower()}'")
    return response.strip().lower() == correct_answer.strip().lower()

def set_timer(game):
    pygame.time.set_timer(pygame.USEREVENT + 2, 3000)