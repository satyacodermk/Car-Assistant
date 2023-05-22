
from email.mime import image
from tkinter import Button, Label, PhotoImage, Tk, font, mainloop, messagebox

player='X'
stop_game=False
mov_count=0
#21ebff
def on_enter(e):
    restart_btn.config(bg='blue',fg='red')

def on_leave(e):
    restart_btn.config(bg='green',fg='black')

def display_winner(plyr):
    if plyr=='draw':
        winner=messagebox.showinfo('Status',"It's Tie...")
    else:
        winner=messagebox.showinfo('Status',plyr+' Wins...')
        print(winner)
        
    player_turn.configure(text="CLICK Restart button to Play Again",font=('Arial',15),fg='#12ff21',bg='sky blue')

    

def clicked(r,c):
    global player
    global mov_count    
    mov_count+=1     #to count no of moves done by the player

    if player=='X' and board[r][c]==0 and stop_game==False:
        but[r][c].configure(text='X',font=('Arial',20),bg='red')
        board[r][c]='X'
        player='O'
        
        
    
    if player=='O' and board[r][c]==0 and stop_game==False:
        but[r][c].configure(text='O',font=('Arial',20),bg='white')
        board[r][c]='O'
        player='X'
    movs.configure(text=f'Moves Count : {mov_count}',font=('Arial',15),fg='red',bg='blue')
    player_turn.configure(text=f"It's Player: {player} Turn",font=('Arial',15),fg='#12ff21',bg='sky blue')

    check_winner()

def check_winner():
    global stop_game
    for i in range(3):
        if board[i][0]==board[i][1]==board[i][2]!=0:
            stop_game=True
            print(board[i][0])
            display_winner(board[i][0])
            break
        elif board[0][0]==board[1][1]==board[2][2]!=0:
            stop_game=True
            print(board[0][0])
            display_winner(board[0][0])
            break
        elif board[0][i]==board[1][i]==board[2][i]!=0:
            stop_game=True
            print(board[0][i])
            display_winner(board[0][i])
            break
        elif board[0][2]==board[i][1]==board[2][0]!=0:
            stop_game=True
            print(board[0][2])
            display_winner(board[0][2])
            break
        elif board[0][0] and board[0][1] and board[0][2] and board[1][0] and board[1][1] and board[1][2] and board[2][0] and board[2][1] and board[2][2]!=0:
            stop_game=True
            print(board[0][0])
            display_winner('draw')
            break

def restart_game():
    global player
    global stop_game
    global mov_count
    player='X'
    stop_game=False
    mov_count=0
    movs.configure(text=f'Moves Count : {mov_count}',font=('Arial',15),fg='red',bg='blue')
    player_turn.configure(text="Start the game",font=('Arial',15),fg='#12ff21',bg='sky blue')

    for i in range(3):
        for j in range(3):
            board[i][j]=0
            but[i][j].configure(text='',bg='white')


# def beginPage():
#     new_window=Tk()
#     new_window.title("let's tic-tac-toe")
#     new_window.resizable(False,False)
#     bgimg=PhotoImage(file="debug2.png")
#     new_window.geometry("900x900")
#     new_window.config(image=bgimg)
#     label1=Label(new_window,text="Welcome to the World of Game",font=('new times roman',30))
#     label1.place(x=50,y=150)

#     but=Button(new_window,text="Click me to get Started",bg='green',fg='white',font=('Arial',20),command=new_window.destroy)
#     but.place(x=60,y=210)
#     #print(but)
#     new_window.mainloop()
   


if __name__=='__main__':

    # beginPage()
    root=Tk()
    root.title('Tic Tac Toe')
    root.resizable(False,False)
    
    but=[[0 for i in range(3)] for i in range(3)]
    print(but)
    
    board=[[0 for i in range(3)] for i in range(3)]

    for i in range(3):
        for j in range(3):
            but[i][j]=Button(width=9,height=4,font=('Arial',20),command=lambda r=i,c=j:clicked(r,c))
            but[i][j].grid(row=i+1,column=j)

    player_turn=Label(root,text="Start the game",font=('Arial',15),fg='#12ff21',bg='sky blue')
    player_turn.grid(row=0,column=0,columnspan=3,padx=5,pady=5)

    restart_btn=Button(root,text='Restart',font=('Arial',15),fg='black',bg='green',command=restart_game)
    restart_btn.grid(row=4,column=0,columnspan=2,padx=5,pady=5)

    #applying the hover effect using event in tkinter use bind function to bind elements
    restart_btn.bind('<Enter>',on_enter)
    restart_btn.bind('<Leave>',on_leave)
    movs=Label(root,text='Moves Count : 0',font=('Arial',15),fg='red',bg='blue')
    movs.grid(row=4,column=2)

    mainloop()
    


