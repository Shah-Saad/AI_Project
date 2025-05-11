import tkinter as tk
from tkinter import messagebox
import random

class ModifiedChessGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Modified Chess - Bishop with Queen Movement")
        self.root.configure(bg="#2c3e50")
        
        # Constants
        self.BOARD_SIZE = 8
        self.SQUARE_SIZE = 70
        self.BOARD_COLORS = ["#f0d9b5", "#b58863"]  # Light and dark square colors
        self.CANVAS_WIDTH = self.BOARD_SIZE * self.SQUARE_SIZE
        self.CANVAS_HEIGHT = self.BOARD_SIZE * self.SQUARE_SIZE
        
        # Game state variables
        self.board = self.create_initial_board()
        self.current_player = "white"
        self.selected_piece = None
        self.selected_square = None
        self.game_over = False
        self.check_status = {"white": False, "black": False}
        self.move_history = []
        
        # Piece values for AI evaluation (modified to reflect bishop's enhanced role)
        self.piece_values = {
            "P": 1, "N": 3, "B": 9, "R": 5, "Q": 9, "K": 100,
            "p": -1, "n": -3, "b": -9, "r": -5, "q": -9, "k": -100
        }
        
        # Create widgets
        self.create_widgets()
        
        # Load images
        self.piece_images = {}
        self.load_piece_images()
        
        # Draw the initial board
        self.draw_board()
        self.draw_pieces()
        
    def create_widgets(self):
        # Main frame
        main_frame = tk.Frame(self.root, bg="#2c3e50")
        main_frame.pack(padx=20, pady=20)
        
        # Left panel - Board
        self.board_canvas = tk.Canvas(
            main_frame, 
            width=self.CANVAS_WIDTH, 
            height=self.CANVAS_HEIGHT, 
            bg="#2c3e50", 
            highlightthickness=0
        )
        self.board_canvas.grid(row=0, column=0, padx=10, pady=10)
        
        # Bind mouse clicks to canvas
        self.board_canvas.bind("<Button-1>", self.handle_click)
        
        # Right panel - Info and controls
        right_panel = tk.Frame(main_frame, bg="#2c3e50")
        right_panel.grid(row=0, column=1, sticky="ns", padx=10, pady=10)
        
        # Current player display
        self.player_frame = tk.Frame(right_panel, bg="#34495e", bd=2, relief=tk.RAISED)
        self.player_frame.pack(fill=tk.X, pady=10)
        
        self.player_label = tk.Label(
            self.player_frame, 
            text="Current Player: White", 
            font=("Arial", 12, "bold"), 
            bg="#34495e", 
            fg="white",
            padx=10, 
            pady=10
        )
        self.player_label.pack()
        
        # Check status display
        self.check_frame = tk.Frame(right_panel, bg="#34495e", bd=2, relief=tk.RAISED)
        self.check_frame.pack(fill=tk.X, pady=10)
        
        self.check_label = tk.Label(
            self.check_frame, 
            text="", 
            font=("Arial", 12), 
            bg="#34495e", 
            fg="white",
            padx=10, 
            pady=10
        )
        self.check_label.pack()
        
        # Control buttons
        buttons_frame = tk.Frame(right_panel, bg="#2c3e50")
        buttons_frame.pack(fill=tk.X, pady=10)
        
        self.new_game_btn = tk.Button(
            buttons_frame, 
            text="New Game", 
            font=("Arial", 12), 
            bg="#16a085", 
            fg="white",
            padx=20, 
            pady=10, 
            command=self.new_game
        )
        self.new_game_btn.pack(fill=tk.X, pady=5)
        
        self.quit_btn = tk.Button(
            buttons_frame, 
            text="Quit", 
            font=("Arial", 12), 
            bg="#c0392b", 
            fg="white",
            padx=20, 
            pady=10, 
            command=self.root.quit
        )
        self.quit_btn.pack(fill=tk.X, pady=5)
        
        # Move history
        history_frame = tk.Frame(right_panel, bg="#34495e", bd=2, relief=tk.RAISED)
        history_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        history_label = tk.Label(
            history_frame, 
            text="Move History", 
            font=("Arial", 12, "bold"), 
            bg="#34495e", 
            fg="white",
            padx=10, 
            pady=5
        )
        history_label.pack()
        
        self.history_listbox = tk.Listbox(
            history_frame, 
            font=("Arial", 10), 
            bg="#ECF0F1", 
            height=10,
            selectbackground="#3498db"
        )
        self.history_listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Rules reminder
        rules_frame = tk.Frame(right_panel, bg="#34495e", bd=2, relief=tk.RAISED)
        rules_frame.pack(fill=tk.X, pady=10)
        
        rules_label = tk.Label(
            rules_frame, 
            text="Modified Rules: Bishops move like Queens\n(diagonally and in straight lines)",
            font=("Arial", 10, "italic"), 
            bg="#34495e", 
            fg="#F39C12",
            padx=10, 
            pady=5,
            justify=tk.LEFT
        )
        rules_label.pack()
    
    def load_piece_images(self):
        # Use Unicode chess symbols since we can't load actual image files in this context
        unicode_symbols = {
            'P': '♙', 'N': '♘', 'B': '♗', 'R': '♖', 'Q': '♕', 'K': '♔',
            'p': '♟', 'n': '♞', 'b': '♝', 'r': '♜', 'q': '♛', 'k': '♚'
        }
        
        # Create text-based "images" using the Unicode symbols
        for piece, symbol in unicode_symbols.items():
            self.piece_images[piece] = symbol
        
    def create_initial_board(self):
        # Create an 8x8 board with pieces in the starting position
        board = [['' for _ in range(self.BOARD_SIZE)] for _ in range(self.BOARD_SIZE)]
        
        # Set up pawns
        for col in range(self.BOARD_SIZE):
            board[1][col] = 'p'  # Black pawns
            board[6][col] = 'P'  # White pawns
        
        # Set up back ranks
        back_rank = ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r']
        for col in range(self.BOARD_SIZE):
            board[0][col] = back_rank[col]  # Black pieces
            board[7][col] = back_rank[col].upper()  # White pieces
            
        return board
    
    def draw_board(self):
        # Clear the canvas
        self.board_canvas.delete("square")
        
        # Draw the squares
        for row in range(self.BOARD_SIZE):
            for col in range(self.BOARD_SIZE):
                x1 = col * self.SQUARE_SIZE
                y1 = row * self.SQUARE_SIZE
                x2 = x1 + self.SQUARE_SIZE
                y2 = y1 + self.SQUARE_SIZE
                
                # Determine square color (alternating pattern)
                color_idx = (row + col) % 2
                fill_color = self.BOARD_COLORS[color_idx]
                
                # Draw the square
                self.board_canvas.create_rectangle(
                    x1, y1, x2, y2, 
                    fill=fill_color, 
                    outline="", 
                    tags=("square", f"square_{row}_{col}")
                )
                
                # Add coordinate labels
                if row == 7:  # Bottom edge
                    self.board_canvas.create_text(
                        x1 + 10, y2 - 10, 
                        text=chr(97 + col),  # 'a' through 'h'
                        fill="#333333" if color_idx == 0 else "#FFFFFF",
                        font=("Arial", 8),
                        tags="square"
                    )
                if col == 0:  # Left edge
                    self.board_canvas.create_text(
                        x1 + 10, y1 + 10, 
                        text=str(8 - row),  # '8' through '1'
                        fill="#333333" if color_idx == 0 else "#FFFFFF",
                        font=("Arial", 8),
                        tags="square"
                    )
        
        # If a square is selected, highlight it
        if self.selected_square:
            row, col = self.selected_square
            x1 = col * self.SQUARE_SIZE
            y1 = row * self.SQUARE_SIZE
            x2 = x1 + self.SQUARE_SIZE
            y2 = y1 + self.SQUARE_SIZE
            
            # Draw highlight
            self.board_canvas.create_rectangle(
                x1, y1, x2, y2, 
                outline="#3498db", 
                width=3, 
                tags="square"
            )
            
            # Highlight legal moves
            if self.selected_piece:
                legal_moves = self.get_legal_moves(row, col)
                for move_row, move_col in legal_moves:
                    x1 = move_col * self.SQUARE_SIZE
                    y1 = move_row * self.SQUARE_SIZE
                    x2 = x1 + self.SQUARE_SIZE
                    y2 = y1 + self.SQUARE_SIZE
                    
                    # Draw a dot for legal moves
                    self.board_canvas.create_oval(
                        x1 + self.SQUARE_SIZE/2 - 5,
                        y1 + self.SQUARE_SIZE/2 - 5,
                        x1 + self.SQUARE_SIZE/2 + 5,
                        y1 + self.SQUARE_SIZE/2 + 5,
                        fill="#3498db",
                        outline="",
                        tags="square"
                    )
    
    def draw_pieces(self):
        # Clear existing pieces
        self.board_canvas.delete("piece")
        
        # Draw pieces based on the current board state
        for row in range(self.BOARD_SIZE):
            for col in range(self.BOARD_SIZE):
                piece = self.board[row][col]
                if piece:
                    x = col * self.SQUARE_SIZE + self.SQUARE_SIZE // 2
                    y = row * self.SQUARE_SIZE + self.SQUARE_SIZE // 2
                    
                    # Draw the piece (text-based for this implementation)
                    color = "white" if piece.isupper() else "black"
                    symbol = self.piece_images[piece]
                    
                    self.board_canvas.create_text(
                        x, y,
                        text=symbol,
                        fill=color,
                        font=("Arial", 36),
                        tags="piece"
                    )
    
    def handle_click(self, event):
        if self.game_over or (self.current_player == "black" and not self.selected_piece):
            return  # Ignore clicks if the game is over or it's AI's turn
        
        # Convert click coordinates to board position
        col = event.x // self.SQUARE_SIZE
        row = event.y // self.SQUARE_SIZE
        
        # Check if the click is within the board
        if 0 <= row < self.BOARD_SIZE and 0 <= col < self.BOARD_SIZE:
            if self.selected_piece:
                # A piece is already selected, try to move it
                legal_moves = self.get_legal_moves(self.selected_square[0], self.selected_square[1])
                if (row, col) in legal_moves:
                    # Valid move
                    self.make_move(self.selected_square[0], self.selected_square[1], row, col)
                    self.selected_piece = None
                    self.selected_square = None
                    
                    # Check for game-ending conditions
                    if self.is_checkmate("black"):
                        self.game_over = True
                        messagebox.showinfo("Game Over", "Checkmate! White wins!")
                    elif self.is_stalemate("black"):
                        self.game_over = True
                        messagebox.showinfo("Game Over", "Stalemate! The game is a draw.")
                    else:
                        # AI's turn
                        self.current_player = "black"
                        self.update_status_displays()
                        self.root.after(500, self.ai_move)  # Slight delay before AI moves
                elif self.board[row][col] and (self.board[row][col].isupper() if self.current_player == "white" else self.board[row][col].islower()):
                    # Clicked on a friendly piece, select it instead
                    self.selected_piece = self.board[row][col]
                    self.selected_square = (row, col)
                else:
                    # Invalid move, deselect
                    self.selected_piece = None
                    self.selected_square = None
            else:
                # No piece is selected yet
                piece = self.board[row][col]
                if piece and (piece.isupper() if self.current_player == "white" else piece.islower()):
                    # Selected a piece of the current player
                    self.selected_piece = piece
                    self.selected_square = (row, col)
            
            # Redraw the board to show selection and legal moves
            self.draw_board()
            self.draw_pieces()
    
    def make_move(self, from_row, from_col, to_row, to_col):
        # Record the move
        piece = self.board[from_row][from_col]
        captured = self.board[to_row][to_col]
        move_str = f"{self.get_algebraic_notation(piece, from_row, from_col, to_row, to_col, captured)}"
        self.move_history.append(move_str)
        self.history_listbox.insert(tk.END, f"{len(self.move_history)}. {move_str}")
        self.history_listbox.see(tk.END)  # Scroll to show the latest move
        
        # Update the board
        self.board[to_row][to_col] = self.board[from_row][from_col]
        self.board[from_row][from_col] = ''
        
        # Check for check status
        opponent = "black" if self.current_player == "white" else "white"
        self.check_status[opponent] = self.is_in_check(opponent)
        
        # Update the UI
        self.update_status_displays()
    
    def get_algebraic_notation(self, piece, from_row, from_col, to_row, to_col, captured):
        # Convert the move to algebraic notation
        piece_symbols = {'P': '', 'N': 'N', 'B': 'B', 'R': 'R', 'Q': 'Q', 'K': 'K',
                        'p': '', 'n': 'N', 'b': 'B', 'r': 'R', 'q': 'Q', 'k': 'K'}
        piece_sym = piece_symbols[piece]
        capture_sym = 'x' if captured else ''
        
        # Convert board coordinates to algebraic notation
        from_alg = chr(97 + from_col) + str(8 - from_row)
        to_alg = chr(97 + to_col) + str(8 - to_row)
        
        # For pawns, include the file when capturing
        if piece.upper() == 'P' and captured:
            return f"{chr(97 + from_col)}{capture_sym}{to_alg}"
        
        return f"{piece_sym}{capture_sym}{to_alg}"
    
    def get_legal_moves(self, row, col):
        piece = self.board[row][col]
        if not piece:
            return []
        
        # Determine if we're looking at a white or black piece
        is_white = piece.isupper()
        
        # Get possible moves based on piece type
        moves = []
        piece_type = piece.upper()
        
        if piece_type == 'P':  # Pawn
            moves = self.get_pawn_moves(row, col, is_white)
        elif piece_type == 'N':  # Knight
            moves = self.get_knight_moves(row, col, is_white)
        elif piece_type == 'B':  # Modified Bishop (moves like a Queen)
            moves = self.get_bishop_as_queen_moves(row, col, is_white)
        elif piece_type == 'R':  # Rook
            moves = self.get_rook_moves(row, col, is_white)
        elif piece_type == 'Q':  # Queen
            moves = self.get_queen_moves(row, col, is_white)
        elif piece_type == 'K':  # King
            moves = self.get_king_moves(row, col, is_white)
        
        # Filter out moves that would leave the king in check
        legal_moves = []
        for move_row, move_col in moves:
            # Make a temporary move
            temp_board = [row[:] for row in self.board]  # Deep copy
            temp_board[move_row][move_col] = temp_board[row][col]
            temp_board[row][col] = ''
            
            # Check if the king is in check after this move
            temp_game = ModifiedChessGame.__new__(ModifiedChessGame)  # Create instance without __init__
            temp_game.board = temp_board
            temp_game.BOARD_SIZE = self.BOARD_SIZE
            
            player = "white" if is_white else "black"
            if not temp_game.is_in_check(player):
                legal_moves.append((move_row, move_col))
        
        return legal_moves
    
    def get_pawn_moves(self, row, col, is_white):
        moves = []
        
        # Determine direction based on color
        direction = -1 if is_white else 1
        starting_row = 6 if is_white else 1
        
        # Forward move
        new_row = row + direction
        if 0 <= new_row < self.BOARD_SIZE and not self.board[new_row][col]:
            moves.append((new_row, col))
            
            # Double move from starting position
            if row == starting_row and not self.board[new_row + direction][col]:
                moves.append((new_row + direction, col))
        
        # Capture moves
        for c in [col - 1, col + 1]:
            if 0 <= new_row < self.BOARD_SIZE and 0 <= c < self.BOARD_SIZE:
                target = self.board[new_row][c]
                if target and (target.islower() if is_white else target.isupper()):
                    moves.append((new_row, c))
        
        return moves
    
    def get_knight_moves(self, row, col, is_white):
        moves = []
        
        # All possible knight moves
        knight_moves = [
            (-2, -1), (-2, 1), (-1, -2), (-1, 2),
            (1, -2), (1, 2), (2, -1), (2, 1)
        ]
        
        for dr, dc in knight_moves:
            new_row, new_col = row + dr, col + dc
            
            # Check if the move is within the board
            if 0 <= new_row < self.BOARD_SIZE and 0 <= new_col < self.BOARD_SIZE:
                target = self.board[new_row][new_col]
                
                # Empty square or enemy piece
                if not target or (target.islower() if is_white else target.isupper()):
                    moves.append((new_row, new_col))
        
        return moves
    
    def get_bishop_as_queen_moves(self, row, col, is_white):
        # Bishop now moves like a queen (diagonally + horizontally/vertically)
        # This is the key modification for the project
        return self.get_queen_moves(row, col, is_white)
    
    def get_rook_moves(self, row, col, is_white):
        moves = []
        
        # Horizontal and vertical directions
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        
        for dr, dc in directions:
            for steps in range(1, self.BOARD_SIZE):
                new_row, new_col = row + dr * steps, col + dc * steps
                
                # Check if the move is within the board
                if not (0 <= new_row < self.BOARD_SIZE and 0 <= new_col < self.BOARD_SIZE):
                    break
                
                target = self.board[new_row][new_col]
                
                if not target:  # Empty square
                    moves.append((new_row, new_col))
                elif (target.islower() if is_white else target.isupper()):  # Enemy piece
                    moves.append((new_row, new_col))
                    break
                else:  # Friendly piece
                    break
        
        return moves
    
    def get_queen_moves(self, row, col, is_white):
        moves = []
        
        # Horizontal, vertical, and diagonal directions
        directions = [
            (0, 1), (1, 0), (0, -1), (-1, 0),  # Horizontal and vertical
            (1, 1), (1, -1), (-1, 1), (-1, -1)  # Diagonal
        ]
        
        for dr, dc in directions:
            for steps in range(1, self.BOARD_SIZE):
                new_row, new_col = row + dr * steps, col + dc * steps
                
                # Check if the move is within the board
                if not (0 <= new_row < self.BOARD_SIZE and 0 <= new_col < self.BOARD_SIZE):
                    break
                
                target = self.board[new_row][new_col]
                
                if not target:  # Empty square
                    moves.append((new_row, new_col))
                elif (target.islower() if is_white else target.isupper()):  # Enemy piece
                    moves.append((new_row, new_col))
                    break
                else:  # Friendly piece
                    break
        
        return moves
    
    def get_king_moves(self, row, col, is_white):
        moves = []
        
        # All directions (horizontal, vertical, diagonal)
        directions = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]
        
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            
            # Check if the move is within the board
            if 0 <= new_row < self.BOARD_SIZE and 0 <= new_col < self.BOARD_SIZE:
                target = self.board[new_row][new_col]
                
                # Empty square or enemy piece
                if not target or (target.islower() if is_white else target.isupper()):
                    moves.append((new_row, new_col))
        
        return moves
    
    def find_king(self, player):
        # Find the position of the king for the given player
        king = 'K' if player == "white" else 'k'
        
        for row in range(self.BOARD_SIZE):
            for col in range(self.BOARD_SIZE):
                if self.board[row][col] == king:
                    return row, col
        
        return None  # Should never happen in a valid chess game
    
    def is_in_check(self, player):
        # Find the king's position
        king_pos = self.find_king(player)
        if not king_pos:
            return False
        
        king_row, king_col = king_pos
        
        # Check if any opponent's piece can capture the king
        opponent = "black" if player == "white" else "white"
        
        for row in range(self.BOARD_SIZE):
            for col in range(self.BOARD_SIZE):
                piece = self.board[row][col]
                
                # Check if it's an opponent's piece
                if piece and ((piece.islower() and opponent == "black") or (piece.isupper() and opponent == "white")):
                    # Get all possible moves for this piece
                    # We need a temporary game state to avoid infinite recursion
                    temp_game = ModifiedChessGame.__new__(ModifiedChessGame)  # Create instance without __init__
                    temp_game.board = self.board
                    temp_game.BOARD_SIZE = self.BOARD_SIZE
                    
                    if piece.upper() == 'P':
                        moves = temp_game.get_pawn_moves(row, col, piece.isupper())
                    elif piece.upper() == 'N':
                        moves = temp_game.get_knight_moves(row, col, piece.isupper())
                    elif piece.upper() == 'B':
                        moves = temp_game.get_bishop_as_queen_moves(row, col, piece.isupper())
                    elif piece.upper() == 'R':
                        moves = temp_game.get_rook_moves(row, col, piece.isupper())
                    elif piece.upper() == 'Q':
                        moves = temp_game.get_queen_moves(row, col, piece.isupper())
                    elif piece.upper() == 'K':
                        moves = temp_game.get_king_moves(row, col, piece.isupper())
                    else:
                        moves = []
                    
                    # Check if the king's position is in the list of possible moves
                    if (king_row, king_col) in moves:
                        return True
        
        return False
    
    def is_checkmate(self, player):
        # First, check if the player is in check
        if not self.is_in_check(player):
            return False
        
        # Check if there are any legal moves that can get out of check
        for row in range(self.BOARD_SIZE):
            for col in range(self.BOARD_SIZE):
                piece = self.board[row][col]
                
                # Check if it's a piece of the current player
                if piece and ((piece.isupper() and player == "white") or (piece.islower() and player == "black")):
                    legal_moves = self.get_legal_moves(row, col)
                    if legal_moves:
                        return False
        
        # No legal moves to get out of check
        return True
    
    def is_stalemate(self, player):
        # Check if the player is not in check
        if self.is_in_check(player):
            return False
        
        # Check if there are any legal moves
        for row in range(self.BOARD_SIZE):
            for col in range(self.BOARD_SIZE):
                piece = self.board[row][col]
                
                # Check if it's a piece of the current player
                if piece and ((piece.isupper() and player == "white") or (piece.islower() and player == "black")):
                    legal_moves = self.get_legal_moves(row, col)
                    if legal_moves:
                        return False
        
        # No legal moves, but not in check
        return True
    
    def update_status_displays(self):
        # Update current player label
        self.player_label.config(text=f"Current Player: {'White' if self.current_player == 'white' else 'Black'}")
        
        # Update check status label
        check_text = ""
        if self.check_status["white"]:
            check_text = "White is in check!"
        elif self.check_status["black"]:
            check_text = "Black is in check!"
        self.check_label.config(text=check_text)
    
 

    def ai_move(self):
        if self.game_over or self.current_player != "black":
            return

        all_moves = []
        for row in range(self.BOARD_SIZE):
            for col in range(self.BOARD_SIZE):
                piece = self.board[row][col]
                if piece and piece.islower():  # Black piece
                    legal_moves = self.get_legal_moves(row, col)
                    for to_row, to_col in legal_moves:
                        all_moves.append((row, col, to_row, to_col))

        if not all_moves:
            if self.is_in_check("black"):
                self.game_over = True
                messagebox.showinfo("Game Over", "Checkmate! White wins!")
            else:
                self.game_over = True
                messagebox.showinfo("Game Over", "Stalemate! The game is a draw.")
            return

        best_moves = []
        best_score = float('-inf')

        for from_row, from_col, to_row, to_col in all_moves:
            temp_board = [r[:] for r in self.board]
            captured_piece = temp_board[to_row][to_col]
            temp_board[to_row][to_col] = temp_board[from_row][from_col]
            temp_board[from_row][from_col] = ''

            score = self.evaluate_position(temp_board)

            if captured_piece:
                score += abs(self.piece_values.get(captured_piece, 0))

            if score > best_score:
                best_score = score
                best_moves = [(from_row, from_col, to_row, to_col)]
            elif score == best_score:
                best_moves.append((from_row, from_col, to_row, to_col))

        move = random.choice(best_moves)
        self.make_move(move[0], move[1], move[2], move[3])
        self.current_player = "white"
        self.selected_piece = None
        self.selected_square = None
        self.draw_board()
        self.draw_pieces()
        self.update_status_displays()

    def evaluate_position(self, board_state):
        score = 0
        for row in board_state:
            for piece in row:
                if piece in self.piece_values:
                    score += self.piece_values[piece]
        return score

    def new_game(self):
        self.board = self.create_initial_board()
        self.current_player = "white"
        self.selected_piece = None
        self.selected_square = None
        self.game_over = False
        self.check_status = {"white": False, "black": False}
        self.move_history = []
        self.history_listbox.delete(0, tk.END)
        self.draw_board()
        self.draw_pieces()
        self.update_status_displays()

# --- Launch the application ---
if __name__ == "__main__":
    root = tk.Tk()
    app = ModifiedChessGame(root)
    root.mainloop()
