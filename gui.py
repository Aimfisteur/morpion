# -*- coding: utf-8 -*-
"""
Created on Mon Apr 10 22:04:23 2023

@author: Richard
"""

import tkinter as tk
from tkinter import messagebox
import morpionGame	
import minimax


# Votre fonction alphabeta et autres fonctions connexes ici

class MorpionGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Morpion")
        self.board = [['' for _ in range(3)] for _ in range(3)]
        self.player = None
        self.bot = None
        self.current_turn = None
        self.game=morpionGame.morpion()

        self.buttons = [[None for _ in range(3)] for _ in range(3)]

        for i in range(3):
            for j in range(3):
                self.buttons[i][j] = tk.Button(self.window, text='', width=10, height=3, command=lambda i=i, j=j: self.on_button_click(i, j))
                self.buttons[i][j].grid(row=i, column=j)

        self.choose_symbol()

    def choose_symbol(self):
        choice_window = tk.Toplevel(self.window)
        choice_window.title("Choix du symbole")
        tk.Label(choice_window, text="Choisissez votre symbole:").grid(row=0, column=0, columnspan=2)
        tk.Button(choice_window, text="X", command=lambda: self.set_symbols('X')).grid(row=1, column=0)
        tk.Button(choice_window, text="O", command=lambda: self.set_symbols('O')).grid(row=1, column=1)

    def set_symbols(self, symbol):
        self.player = symbol
        self.bot = 'O' if symbol == 'X' else 'X'
        if self.bot=='X':
            self.bot_move()
            self.current_turn = 'O'
        else:
            self.current_turn = 'X'
        self.window.focus_set()

    def on_button_click(self, i, j):
        if not self.player:
            messagebox.showerror("Erreur", "Veuillez choisir un symbole avant de jouer.")
            self.choose_symbol()
            return

        if self.board[i][j] == '' and self.current_turn == self.player:
            self.board[i][j] = self.player
            self.buttons[i][j].config(text=self.player, state=tk.DISABLED)
            self.game=self.game.result((i,j), self.player)
            self.check_win()

            self.current_turn = self.bot
            
            self.bot_move()

    def bot_move(self):
        if not self.is_board_full():
            #move = minimax.minimax(self.game, self.bot)[1]
            move = minimax.alphabeta(self.game, self.bot)[1]
            
            print(move)# Utilisez votre fonction alphabeta ici
            i, j = move[0], move[1]
            self.board[i][j] = self.bot
            self.game=self.game.result(((i,j)), self.bot)
            self.buttons[i][j].config(text=self.bot, state=tk.DISABLED)
            self.check_win()

            self.current_turn = self.player

    def check_win(self):
        
        if self.game.terminalTest():
            util=self.game.utility()
            if util==1:
                messagebox.showinfo("Félicitations", "Le joueur X a gagné !")
                self.reset_board()
                self.game=morpionGame.morpion()
            if util==0:
                messagebox.showinfo("Égalité", "C'est une égalité !")
                self.reset_board()
                self.game=morpionGame.morpion()
            if util==-1:
                messagebox.showinfo("Félicitations", "Le joueur O a gagné !")
                self.reset_board()
                self.game=morpionGame.morpion()
        

    def reset_board(self):
        self.board = [['' for _ in range(3)] for _ in range(3)]
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(text='', state=tk.NORMAL)

    def is_board_full(self):
        for row in self.board:
            for cell in row:
                if cell == '':
                    return False
        return True
    
    def run(self):
        self.window.mainloop()
    
    
gui = MorpionGUI()
gui.run()
                