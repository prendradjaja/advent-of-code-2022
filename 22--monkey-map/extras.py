def show(board, player):
    rmin = min(r for (r, c) in board)
    rmax = max(r for (r, c) in board)
    cmin = min(c for (r, c) in board)
    cmax = max(c for (r, c) in board)
    for r in range(rmin, rmax+1):
        for c in range(cmin, cmax+1):
            ch = board.get((r, c), ' ')
            if player == (r, c):
                ch = 'X'
            print(ch, end='')
        print()
