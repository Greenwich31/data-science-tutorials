import streamlit as st
import chess
import chess.svg
import chess.pgn
from io import StringIO

st.set_page_config(page_title="Jeu d'échecs (Streamlit)", layout="wide")

# Initialisation
if 'board' not in st.session_state:
    st.session_state.board = chess.Board()
    st.session_state.move_history = []


def reset_game():
    st.session_state.board = chess.Board()
    st.session_state.move_history = []


st.title("Jouer aux échecs — Streamlit")

# Sidebar controls
with st.sidebar:
    st.header("Contrôles")
    if st.button("Nouvelle partie"):
        reset_game()
    orientation_str = st.selectbox("Orientation du plateau", options=["white", "black"], index=0)
    orientation = True if orientation_str == "white" else False
    size = st.slider("Taille du plateau (px)", min_value=200, max_value=900, value=480)
    st.markdown("---")
    st.write("**FEN actuelle**")
    st.code(st.session_state.board.fen())
    st.markdown("---")
    if st.button("Annuler le dernier coup"):
        if len(st.session_state.board.move_stack) > 0:
            st.session_state.board.pop()
            if st.session_state.move_history:
                st.session_state.move_history.pop()
        else:
            st.info("Aucun coup à annuler.")


# Affichage du plateau (SVG) via components.html
board = st.session_state.board
last_move = board.move_stack[-1] if board.move_stack else None
svg = chess.svg.board(board=board, size=size, lastmove=last_move, orientation=orientation)

st.components.v1.html(svg, height=size + 20)

# Zone de jeu: saisie du coup
st.subheader("Jouer un coup")
col1, col2 = st.columns([3, 1])
with col1:
    move_input = st.text_input("Entrez un coup (par ex. e2e4 ou Nf3)")
with col2:
    if st.button("Jouer"):
        s = move_input.strip()
        if not s:
            st.warning("Entrez un coup au format SAN (Nf3) ou UCI (e2e4).")
        else:
            moved = False
            # Essaie SAN
            try:
                move = board.parse_san(s)
                board.push(move)
                moved = True
            except Exception:
                try:
                    move = chess.Move.from_uci(s)
                    if move in board.legal_moves:
                        board.push(move)
                        moved = True
                    else:
                        st.error("Coup illégal.")
                except Exception:
                    st.error("Format de coup invalide. Essayez SAN (e.g. Nf3) ou UCI (e2e4).")

            if moved:
                # Sauvegarde historique en SAN lisible
                san = board.peek()  # dernier coup (objet Move)
                # Pour afficher SAN, il faut reconstruire PGN/partie
                # On transforme l'historique actuel en notation SAN simple:
                temp_board = chess.Board()
                sans = []
                for mv in board.move_stack:
                    sans.append(temp_board.san(mv))
                    temp_board.push(mv)
                st.session_state.move_history = sans

# Affichage de l'historique
st.subheader("Historique des coups")
if st.session_state.move_history:
    cols = st.columns(2)
    half = (len(st.session_state.move_history) + 1) // 2
    with cols[0]:
        for i, mv in enumerate(st.session_state.move_history[:half], start=1):
            st.write(f"{i}. {mv}")
    with cols[1]:
        for i, mv in enumerate(st.session_state.move_history[half:], start=half+1):
            st.write(f"{i}. {mv}")
else:
    st.write("Aucun coup joué pour le moment.")

# Export PGN / FEN
st.subheader("Exporter la partie")
col1, col2 = st.columns(2)
with col1:
    if st.button("Télécharger PGN"):
        game = chess.pgn.Game()
        node = game
        temp_board = chess.Board()
        for mv in board.move_stack:
            node = node.add_variation(mv)
        # Remplir headers minimaux
        game.headers["Result"] = board.result(claim_draw=True) if board.is_game_over() else "*"
        pgn_io = StringIO()
        exporter = chess.pgn.FileExporter(pgn_io)
        game.accept(exporter)
        pgn_data = pgn_io.getvalue()
        st.download_button("Télécharger PGN", data=pgn_data, file_name="partie.pgn", mime="text/plain")
with col2:
    st.download_button("Télécharger FEN", data=board.fen(), file_name="position.fen", mime="text/plain")

st.markdown("---")
st.caption("Application simple : input textuel des coups (SAN ou UCI). Si vous voulez un plateau cliquable ou une IA pour jouer contre, dites-le et je l'ajouterai !")
