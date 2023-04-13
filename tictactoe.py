#!/usr/bin/python3
import os, sys, time, random, socket

board = {'tl': ' ', 'tm': ' ', 'tr': ' ', 'ml': ' ', 'mm': ' ', 'mr': ' ', 'bl': ' ', 'bm': ' ', 'br': ' '}

def board_printing(board):
	print(f'{board["tl"]}|{board["tm"]}|{board["tr"]}')
	print(f'-+-+-')
	print(f'{board["ml"]}|{board["mm"]}|{board["mr"]}')
	print(f'-+-+-')
	print(f'{board["bl"]}|{board["bm"]}|{board["br"]}')

def check_for_free_spot(board):
	print('Available: ', end = '')
	avlist = []
	for key in board.keys():
		if board[key] == ' ':
			print(key, end = ' ', sep = ',')
			avlist.append(key)
	return avlist

def clear_screen():
	if os.name in ['nt', 'NT', 'Nt']:
		os.system('cls')
	else:
		os.system('clear')

def check_win(board, turn):
	conditions = (# Horizontal
				  board["tl"] == f'{turn}' and board["tm"] == f'{turn}' and board["tr"] == f'{turn}', 			# t ROW
				  board["ml"] == f'{turn}' and board["mm"] == f'{turn}' and board["mr"] == f'{turn}', 			# m ROW
				  board["bl"] == f'{turn}' and board["bm"] == f'{turn}' and board["br"] == f'{turn}', 			# bTOM ROW
				  # Vertical
				  board["tl"] == f'{turn}' and board["ml"] == f'{turn}' and board["bl"] == f'{turn}', 			# Left Column
				  board["tm"] == f'{turn}' and board["mm"] == f'{turn}' and board["bm"] == f'{turn}', 			# m COLUMN
				  board["tr"] == f'{turn}' and board["mr"] == f'{turn}' and board["br"] == f'{turn}', 			# Right Column
				  # Diagonal
				  board["tl"] == f'{turn}' and board["mm"] == f'{turn}' and board["br"] == f'{turn}', 			# t Left to btom Right Diagonal
				  board["tr"] == f'{turn}' and board["mm"] == f'{turn}' and board["bl"] == f'{turn}'  			# t Right To btom Left Diagonal
	)
	for condition in conditions:
		if condition:
			return turn
		else:
			continue
	return None
	pass

def pvp():
	turn = 'O'
	for i in range(len(list(board.keys()))):
		clear_screen()
		board_printing(board)
		print()
		avlist = check_for_free_spot(board)
		print()
		while True:
			keyinput = input(f"Input Location for {turn}: ")
			if keyinput in avlist:
				board[keyinput] = turn
				break
		win = check_win(board, turn)
		if win != None:
			print(f"And The Winner is Player {turn}")
			board_printing(board)
			time.sleep(5)
			sys.exit(0)
		if turn == 'O':
			turn = 'X'
		else:
			turn = 'O'

def pvc():
	turn = 'O'
	for i in range(0, len(list(board.keys()))):
		clear_screen()
		board_printing(board)
		print()
		avlist = check_for_free_spot(board)
		print()
		if turn == 'O':
			while True:
				keyinput = input(f"Input Location for {turn}: ")
				if keyinput in avlist:
					break
				else:
					print("Can't Input it there")
			board[keyinput] = turn
		else:
			botturn(avlist, board)
		win = check_win(board, turn)
		if win != None:
			if turn == 'X':
				print("CPU IS THE WINNER")
			else:
				print("PLAYER IS THE WINNER")
			board_printing(board)
			time.sleep(5)
			sys.exit(0)
		if turn == 'O':
			turn = 'X'
		else:
			turn = 'O'
	print("It's a Draw")
	board_printing(board)
	time.sleep(5)
	sys.exit(0)

def botturn(avlist, board):
	loopbreakcheck = False
	for available in avlist:
		temp = board[available]
		board[available] = 'X'
		if check_win(board, 'X') != None:
			loopbreakcheck = True
			break
		else:
			board[available] = temp
	if not loopbreakcheck:
		for available in avlist:
			temp = board[available]
			board[available] = "O"
			if not check_win(board, 'O') == None:
				loopbreakcheck = True
				board[available] = 'X'
				break
			board[available] = temp
	if not loopbreakcheck:
		board[list(board.keys())[random.randint(0,len(avlist))]] = 'X'

def main():
	print("""TIC TAC TOE
Choose your opponent
	1. CPU
	2. Another Player (Same Machine Multiplayer)
	3. Another Player (Local Multiplayer)
	""")
	choice = input(" > ")
	
	if int(choice) == 1:
		pvc()
	elif int(choice) == 2:
		pvp()
	elif int(choice) == 3:
		lan_menu()
	else:
		print("bet you can't Read, Exiting")
		sys.exit(0)

# Multiplayer
host = False
def lan_menu():
	print("""CHOOSE Host, or Client
	1. Host
	2. Client
	3. Go Back""")
	choice = input(" > ")
	
	if int(choice) == 1:
		host_game()
		global host
		host = True
		pvp_lan()
	elif int(choice) == 2:
		connect_to_game()
		pvp_lan()
	elif int(choice) == 3:
		main()
	else:
		print("Bet you Can't Read, Returning you to Main Menu")
		main()

PORT = 4367
hostname = socket.gethostname()
hostip = "0.0.0.0"

def host_game():
	serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	serv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	print(f"Connect to {hostip} with Port {PORT}")
	print(f"{type(hostip)}")
	serv.bind((hostip, PORT))
	serv.listen(2)
	conn, address = serv.accept()
	conn.send(bytes("CONNECTION Successful, good luck", "utf-8"))
	clientdata = str(conn.recv(4096)).removeprefix("b'")
	clientdata = clientdata.removesuffix("'")
	conn.close()
	print(f"{clientdata}")
	pass

clientinput = ''

def connect_to_game():
	client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	global clientinput
	clientinput = input("Input the Host IP To Connect (Port selected automatically): ")
	print(f"{hostip} and type: {type(hostip)}")
	client.connect((clientinput, PORT))
	serverdata = str(client.recv(4096)).removeprefix("b'")
	serverdata = serverdata.removesuffix("'")
	client.send(bytes('Good Luck To you too', "utf-8"))
	client.close()
	print(f'{serverdata}')
	pass

def pvp_lan():
	turn = 'O'
	for i in range(len(list(board.keys()))):
		clear_screen()
		board_printing(board)
		print()
		avlist = check_for_free_spot(board)
		print()
		if host:
			if turn == 'O':
				wait_for_client_turn(board, turn)
			else:
				host_turn(board, turn, avlist)
		else:
			if turn == 'O':
				client_turn(board, turn, avlist)
			else:
				wait_for_host_turn(board, turn)
		win = check_win(board, turn)
		if win != None:
			print(f"And The Winner is Player {turn}")
			board_printing(board)
			time.sleep(5)
			sys.exit(0)
		if turn == 'O':
			turn = 'X'
		else:
			turn = 'O'

# HOST SIDE
def wait_for_client_turn(board, turn):		# FOR HOST
	serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	serv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	serv.bind((hostip, PORT))
	print("Client Turn, please wait")
	serv.listen(2)
	conn, addr = serv.accept()
	clientturn = str(conn.recv(4096)).removeprefix("b'")
	clientturn = clientturn.removesuffix("'")
	conn.close()
	board[clientturn] = turn
	pass

def host_turn(board, turn, avlist):				# FOR HOST
	serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	serv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	serv.bind((hostip, PORT))
	serv.listen(2)
	conn, addr = serv.accept()
	while True:
		keyinput = input("ENTER PLACE: ")
		if keyinput in avlist:
			board[keyinput] = turn
			break
	conn.send(bytes(keyinput, "utf-8"))
	conn.close()
	pass


# CLIENT SIDE
def wait_for_host_turn(board, turn):		# FOR CLIENT
	client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	client.connect((clientinput, PORT))
	print("Host's Turn, Please Wait")
	servdata = str(client.recv(4096)).removeprefix("b'")
	servdata = servdata.removesuffix("'")
	client.close()
	board[servdata] = turn
	pass

def client_turn(board, turn, avlist):				# FOR CLIENT
	client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	client.connect((clientinput, PORT))
	while True:
		keyinput = input("ENTER PLACE: ")
		if keyinput in avlist:
			board[keyinput] = turn
			break
	client.send(bytes(keyinput, "utf-8"))
	client.close()
	
	pass

if __name__ == "__main__":
	main()
