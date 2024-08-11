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
                else:
                    self.dialog_box.add_char(event.unicode)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    self.character.attack()


                # Handles dialog prompt at the end of a level to move to the next one
                elif self.boss_trigger and event.key == pygame.K_x:
                    self.next_level()
                    self.boss_deaths += 1
                    self.boss_trigger = False

        if not self.dialog_box.active:
            self.handle_continuous_input()
