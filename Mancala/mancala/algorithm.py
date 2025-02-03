from copy import deepcopy
from typing import Dict

from board import Board2players

def search_with_min_max(player_id: int, board: Board2players) -> Dict[str, int]:
    dp = {}
    original_player_id = player_id
    search_with_min_max.max_signature = [0] #関数内の静的変数

    def _evaluate(player_id: int, board: Board2players) -> Dict[str, int]:
        value = dp.get((board, player_id)) #"|".join([str(i) for i in board.data]) + f"_{player_id}")
        if value is not None:
            return value

        candidates = board.get_players_movable_grids(player_id=player_id)
        eval_tables = {}
        result = None
        for action in candidates.keys():
            tmp_board = deepcopy(board)
            act_again = tmp_board.move(action)
            if tmp_board.does_player_win(player_id=player_id):
                if player_id == original_player_id:
                    result = {"action": action, "value": 1}
                else:
                    result = {"action": action, "value": -1}
                break

            new_player_id = player_id if act_again else (player_id + 1) % board.NUMBER_OF_PLAYERS

            eval_tables[action] = _evaluate(player_id=new_player_id, board=tmp_board)["value"]

        if result is None:
            if player_id == original_player_id:
                best_action = max(eval_tables, key=eval_tables.get)
            else:
                best_action = min(eval_tables, key=eval_tables.get)

            result = {"action": best_action, "value": eval_tables[best_action]}

        #dp["|".join([str(i) for i in board.data]) + f"_{player_id}"] = result
        board_signature = board.signature()
        if board_signature < [13] :
            dp[(board, player_id)] = result
        if board_signature > search_with_min_max.max_signature :
            search_with_min_max.max_signature = board_signature
            print('max signature = ', search_with_min_max.max_signature)
        return result

    return _evaluate(player_id=player_id, board=board)


if __name__ == "__main__":
    board = Board2players(grids_per_player=3, init_pieces_per_grid=3, grids_between_players=3)
    print(search_with_min_max(player_id=0, board=board))
