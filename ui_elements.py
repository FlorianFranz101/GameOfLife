import pygame
import pygame_gui
import numpy as np
from rle_converter import read_board_from_string
class UIElements:
    def __init__(self, game, ctrl, gameloop):
        self.game = game
        self.ctrl = ctrl
        self.gameloop = gameloop
    def define_elements(self, manager):
        mid = self.get_middle_of_screen()
        slider_layout_rect = pygame.Rect(0, 0, 100, 25)
        slider_layout_rect.bottomright = (-20, -20)
        speed_text_layout_rect = pygame.Rect(0, 0, 100, 50)
        speed_text_layout_rect.bottomright = (-0, -0)
        play_pause_btn_layout_rect = pygame.Rect(0, 0, 100, 50)
        play_pause_btn_layout_rect.bottomright = (-20, -20)
        xcells_field_layout_rect = pygame.Rect(0, 0, 100, 50)
        xcells_field_layout_rect.bottomright = (-20, -20)
        ycells_field_layout_rect = pygame.Rect(0, 0, 100, 50)
        ycells_field_layout_rect.bottomright = (-20, -20)
        ycells_field_layout_rect = pygame.Rect(0, 0, 100, 50)
        ycells_field_layout_rect.bottomright = (-20, -20)
        reset_board_btn = pygame.Rect(0, 0, 150, 50)
        reset_board_btn.bottomright = (-20, -20)
        dialog_rect = pygame.Rect(400, 400, 400, 400)
        dialog_rect.bottomright = (-mid[0]+200, -mid[1]+200)
        import_info = pygame.Rect(50,50, 300, 70)
        import_input = pygame.Rect(50,50, 300, 70)
        import_input.topleft = (50, 100)
        import_btn= pygame.Rect(50,50, 300, 70)
        import_btn.topleft = (50, 200)
        open_import_dialog_btn = pygame.Rect(0, 0, 150, 50)
        open_import_dialog_btn.bottomright = (-20, -20)
        self.speed_field = pygame_gui.elements.UIHorizontalSlider(relative_rect=slider_layout_rect,
                                                            start_value=5,
                                                            value_range=(1,10),
                                                            click_increment=1,
                                                            manager=manager,
                                                            anchors={'left': 'right',
                                                                    'right': 'right',
                                                                    'top': 'bottom',
                                                                    'bottom': 'bottom'})
        self.speed_text = pygame_gui.elements.UILabel(relative_rect=speed_text_layout_rect,
                                                            text="Speed :"+str(round(self.speed_field.get_current_value(), 1)),
                                                            manager=manager,
                                                            anchors={'left': 'right',
                                                                    'right': 'right',
                                                                    'top': 'bottom',
                                                                    'bottom': 'bottom',
                                                                    "bottom_target":self.speed_field})
        self.play_pause_btn = pygame_gui.elements.UIButton(relative_rect=play_pause_btn_layout_rect,
                                                            text="Play",
                                                            manager=manager,
                                                            anchors={'left': 'right',
                                                                    'right': 'right',
                                                                    'top': 'bottom',
                                                                    'bottom': 'bottom',
                                                                    "right_target":self.speed_field})
        self.ycells_field = pygame_gui.elements.UITextEntryLine(relative_rect=xcells_field_layout_rect,
                                                            manager=manager,
                                                            anchors={'left': 'right',
                                                                    'right': 'right',
                                                                    'top': 'bottom',
                                                                    'bottom': 'bottom',
                                                                    "right_target":self.play_pause_btn})
        self.xcells_field = pygame_gui.elements.UITextEntryLine(relative_rect=xcells_field_layout_rect,
                                                            manager=manager,
                                                            anchors={'left': 'right',
                                                                    'right': 'right',
                                                                    'top': 'bottom',
                                                                    'bottom': 'bottom',
                                                                    "right_target":self.ycells_field})
        self.reset_board_btn = pygame_gui.elements.UIButton(relative_rect=reset_board_btn,
                                                                    text="Resize Grid",
                                                                    manager=manager,
                                                                    anchors={'left': 'right',
                                                                            'right': 'right',
                                                                            'top': 'bottom',
                                                                            'bottom': 'bottom',
                                                                            "right_target":self.xcells_field})
        self.dialog_panel = pygame_gui.elements.UIPanel(relative_rect=dialog_rect,
                                                            starting_layer_height=1,
                                                            manager=manager,
                                                            visible=False,
                                                            anchors={'left': 'right',
                                                                    'right': 'right',
                                                                    'top': 'bottom',
                                                                    'bottom': 'bottom'})    
        self.import_btn = pygame_gui.elements.UIButton(relative_rect=import_btn,
                                                                    text="Import",
                                                                    manager=manager,
                                                                    container=self.dialog_panel)                                                            
        self.import_textfield = pygame_gui.elements.UITextEntryLine(relative_rect=import_input,
                                                            manager=manager,
                                                            container= self.dialog_panel
                                                        )
        self.import_info = pygame_gui.elements.UILabel(relative_rect=import_info,
                                                            text="Please enter your Pattern name. This Pattern must be a file ending with .rle inside the patterns folder",
                                                            manager=manager,
                                                            container= self.dialog_panel
                                                            )
        self.open_import_dialog_btn = pygame_gui.elements.UIButton(relative_rect=open_import_dialog_btn,
                                                                    text="Import Pattern",
                                                                    manager=manager,
                                                                    anchors={'left': 'right',
                                                                            'right': 'right',
                                                                            'top': 'bottom',
                                                                            'bottom': 'bottom',
                                                                            "right_target":self.reset_board_btn})
        
        

    def handle_event(self, event):
        # Speed
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.play_pause_btn:
                if(self.play_pause_btn.text == "Play"):
                    self.play_pause_btn.set_text("Pause")
                else:
                    self.play_pause_btn.set_text("Play")
                self.ctrl.is_paused = not self.ctrl.is_paused
            if(event.ui_element == self.import_btn):
                print("file", self.import_textfield.get_text())
                with open("patterns/"+self.import_textfield.get_text()+".rle", 'r') as file:
                    importtext = file.read()
                print("importtext", importtext)
                cells = read_board_from_string(importtext)
                self.ctrl.cellsx = cells.shape[1]
                self.ctrl.cellsy = cells.shape[0]
                self.game.cells = cells
                self.dialog_panel.visible = False
            if(event.ui_element == self.open_import_dialog_btn):
                setto = not self.dialog_panel.visible
                self.dialog_panel.visible = setto
                self.import_btn.visible = setto
                self.import_textfield.visible = setto
                self.import_info.visible = setto

            if event.ui_element == self.reset_board_btn:
                xcells = self.xcells_field.get_text()
                ycells = self.ycells_field.get_text()
                if(xcells.isdigit() and ycells.isdigit()):
                    self.ctrl.cellsx = int(xcells)
                    self.ctrl.cellsy = int(ycells)
                    self.ctrl.cellschanged = True
        if event.type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
            if event.ui_element == self.speed_field:
                self.ctrl.set_speed(round(self.speed_field.get_current_value(), 1))
                self.speed_text.set_text("Speed: "+str(self.ctrl.speed))
    def get_middle_of_screen(self):
        return (int(self.gameloop.surface.get_size()[0]/2),int(self.gameloop.surface.get_size()[1]/2))