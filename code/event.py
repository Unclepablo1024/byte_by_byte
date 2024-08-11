import pygame

def handle_events(self):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            self.running = False
        elif event.type == pygame.USEREVENT + 1:
            self.dialog_box.hide()
        elif event.type == pygame.USEREVENT + 2:
            pygame.time.set_timer(pygame.USEREVENT + 2, 0)
            if self.current_question_index < len(self.questions):
                self.ask_next_question()
            else:
                self.show_dialog("Congratulations! You've completed all questions for Level One.",
                                 auto_hide_seconds=5)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                response = self.dialog_box.get_input()
                if response:
                    print(f"Dialog response received: {response}")
                    self.handle_dialog_response(response)
                    pygame.event.clear()  # Clear the event queue after processing the response
            elif event.key == pygame.K_BACKSPACE:
                self.dialog_box.backspace()
            elif self.boss_trigger and event.key == pygame.K_x:
                print("Attempting to change level...")  # Debug print
                self.next_level()
                self.boss_deaths += 1
                self.boss_trigger = False
                print(f"New level: {self.current_level}, Boss deaths: {self.boss_deaths}")  # Debug print
            else:
                self.dialog_box.add_char(event.unicode)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                self.character.attack()

    if not self.dialog_box.active:
        self.handle_continuous_input()
        