import curses 
import json
import random
import time
import sys

CTRL_R = 18
CTRL_A = 1    
CTRL_N = 14
SPACE = 32

class Display:
    def __init__(self):
        self.time = 0
        
        
    def run(self):
        curses.wrapper(self.printSentence)
    
    def generateSentences(self):
        with open("sentences.json",'r') as file:
            data = json.load(file) 
        return data['words']
    
    def setupColor(self,stdscr):    
        curses.start_color()
        curses.init_color(2,128,128,128) # grey
        curses.init_color(3,500,1000,750) # green mint
        curses.init_color(4,1000,500,500) # red mint
        curses.init_color(5,792,892,792) # silver
        curses.init_color(6,755,755,453) # yellow
        curses.init_color(7,800,800,800) #white
        curses.init_color(8,573,573,900) # purple
        curses.init_pair(1, 7, 2) # background
        curses.init_pair(2, 3, 2) # green pair
        curses.init_pair(3, 4, 2) # red pair
        curses.init_pair(4,6,2) # yellow
        curses.init_pair(5,5,2) # silver
        curses.init_pair(6,8,2) # purple
        stdscr.bkgd(' ', curses.color_pair(1)) # set bakcground color
        self.default_color = curses.color_pair(1) | curses.A_DIM # background and leter type
        self.green = curses.A_DIM | curses.color_pair(2) 
        self.red = curses.A_DIM | curses.color_pair(3)
        
    
    def printTimeAndHelp(self,stdscr):
        localInfo = time.strftime("%A, %m/%d/%Y")
        aboutMe = "My Instagram -> @goncalobranquinho2005"
        y,_ = stdscr.getmaxyx()
        x1 = self.x//2 - (len(localInfo)//2)
        stdscr.addstr(5,x1,localInfo,curses.color_pair(4))
        x1 = self.x//2 - (len(aboutMe)//2)
        stdscr.addstr(7,x1,aboutMe,curses.color_pair(4))

        
    def changeCursor(self):
        sys.stdout.write("\033[6 q")
        sys.stdout.flush()
        
    def resetCursor(self):
        sys.stdout.write("\033[0 q")
        sys.stdout.flush()
    
    def printSentence(self,stdscr):
        stdscr.clear()
        self.setupColor(stdscr)
        self.y, self.x = stdscr.getmaxyx()
        words = self.generateSentences()
        self.sentences = []
        self.countChars = 0
        self.totalWordsNum = 0
        self.changeCursor()
        for _ in range(5):
            randomWords = random.choices(words,k = random.randint(5,7))
            self.totalWordsNum += len(randomWords)
            randomWords = ' '.join(randomWords)
            self.countChars += len(randomWords)
            self.sentences.append(randomWords)
        self.printTimeAndHelp(stdscr)
        commands = "ctrl-r -> restart | ctrl-c -> quit"
        y,_ = stdscr.getmaxyx()
        x1 = self.x//2 - (len(commands)//2)
        stdscr.addstr(y-5,x1,commands,curses.color_pair(4))
        self.printText(stdscr,y-5,7)   
        self.game(stdscr)
    
    
    def updatePos(self):
        self.y1,self.x1 = self.y//2 - (len(self.sentences)//2), (self.x//2 - (len(self.sentences[0]) // 2))
        
    
    def printText(self,stdscr,upY,downY):
        self.updatePos()
        stdscr.clear()
        y1, x1 = (upY+downY) // 2-3, self.x1
        for i,sentence in enumerate(self.sentences):
            x1 = (self.x//2 - (len(self.sentences[i]) // 2))
            stdscr.addstr(y1,x1,sentence,curses.color_pair(1))
            y1 += 1

    def reset(self,stdscr):
        curses.curs_set(1)
        self.printTimeAndHelp(stdscr)
        commands = "ctrl-r -> restart | ctrl-c -> quit"
        y,_ = stdscr.getmaxyx()
        x1 = self.x//2 - (len(commands)//2)
        stdscr.addstr(y-5,x1,commands,curses.color_pair(4))
        self.misses = 0
        self.totalClicks = 0
        self.updatePos()
        self.wellTypedWords = [0 for _ in range(self.countChars+len(self.sentences)-1)]
        y1, x1 = self.y1, self.x1
        stdscr.move(y1,x1)
        stdscr.refresh()

    
    def game(self,stdscr):
        y,x = stdscr.getmaxyx()
        curses.textpad.rectangle(stdscr,3,6,y-3,x-6)
        self.reset(stdscr)
        y1, x1 = self.y1, self.x1
        row = 0
        col = 0
        aux = 0 
        restart = False
        maxSize = len(self.sentences)
        start = time.perf_counter()
        
        while (True):
            input = stdscr.getch()
            char = ord(self.sentences[col][row])
            if input == CTRL_R:
                restart = True
                break
            if (input == curses.KEY_BACKSPACE):
                if col != 0 and row == 0:
                    col -= 1
                    row = len(self.sentences[col])-1
                    y1 -= 1
                    x1 = self.x//2 + ((len(self.sentences[col])-1) // 2)
                    self.wellTypedWords[aux-1] = 0
                    self.totalClicks -= 1
                    aux -= 1
                elif row != 0: 
                    row -= 1
                    x1 -= 1
                    self.totalClicks -= 1
                stdscr.addstr(y1,x1,self.sentences[col][row],curses.color_pair(1))
                if char == SPACE:
                    self.wellTypedWords[aux] = 0
                else:
                     self.wellTypedWords[aux] = -1
                aux -= 1
                
            else:
                if char == input:
                    stdscr.addstr(self.sentences[col][row],self.green)
                    self.wellTypedWords[aux] = 1
                else: 
                    stdscr.addstr(self.sentences[col][row],self.red)
                    self.wellTypedWords[aux] = -1
                    self.misses += 1
                if row == len(self.sentences[col])-1:
                    col += 1
                    row = 0
                    if col == maxSize:
                        break
                    y1 += 1
                    x1 = (self.x//2 - (len(self.sentences[col]) // 2))
                    aux += 1
                    self.wellTypedWords[aux+1] = 0
                else:
                    x1 += 1
                    row += 1
                if char == SPACE:
                    self.wellTypedWords[aux] = 0
                aux += 1
            
            stdscr.move(y1,x1)
            stdscr.refresh()
            self.totalClicks += 1
            
        if restart:
            y,_ = stdscr.getmaxyx()
            self.printText(stdscr,y-5,7) 
            self.game(stdscr)
        
        finish = time.perf_counter()
        self.time = finish - start
        self.totalClicks += 1
        self.correctWords()
        self.afterGame(stdscr)
        
    def correctWords(self):
        fst = 0
        self.wordsNum = 0
        while (fst < len(self.wellTypedWords)):
            flag = True
            while (fst < len(self.wellTypedWords) and self.wellTypedWords[fst] != 0):
                if self.wellTypedWords[fst] == -1:
                    flag = False
                fst += 1
            if flag:
                self.wordsNum += 1
            fst += 1
    
    def nextAction(self,stdscr):
        while (True):
            input = stdscr.getch()
            if input == CTRL_A:
                y,_ = stdscr.getmaxyx()
                self.printText(stdscr,y-5,7)
                self.game(stdscr)
                break
            if input == CTRL_N:
                self.printSentence(stdscr)
                break
        
    
    def afterGame(self, stdscr):
        stdscr.clear()
        self.printTimeAndHelp(stdscr)
        y,x = stdscr.getmaxyx()
        curses.curs_set(0)
        curses.textpad.rectangle(stdscr,3,6,y-3,x-6)
        yCenter = self.y//2
        xCenter = self.x//2
        with open("sentences.json",'r') as file:
            data = json.load(file) 
            ranking = data['score']
            prevScore = ranking[0][0]
            prevWPM = ranking[0][1]
        
        accuracy = round((self.totalClicks-self.misses)*100/self.totalClicks,2)
        score = accuracy
        wpm = round((self.wordsNum / (self.time / 60)),2)
        performance = (score/100) + (wpm/150)
        text = "ctrl-a -> repeat | ctrl-n -> next"
        record = "!! NEW RECORD !!"
        resumeWords = f"You have typed correctly {self.wordsNum} words out of {self.totalWordsNum}"
        resumeSpeed = f"with a typing speed of {wpm} WPM"
        resumeAcc = f"and a typing accuracy of {accuracy}%"
        y1 = yCenter-4

        for placement in ranking:
            currScore = placement[0]
            currWPM = placement[1]
            currPerformance = (currScore/100) + (currWPM/150)  
            if performance > currPerformance:
                placement[0] = score
                placement[1] = wpm
                score, wpm, performance = currScore, currWPM, currPerformance
        
        if (ranking[0][0] != prevScore or ranking[0][1] != prevWPM):
            stdscr.addstr(y1,xCenter-8,record,curses.color_pair(3))
            y1 += 2
        
        stdscr.addstr(y1,xCenter - (len(resumeWords) // 2),resumeWords,curses.color_pair(5))
        stdscr.addstr(y1+1,xCenter - (len(resumeSpeed) // 2),resumeSpeed,curses.color_pair(5))
        stdscr.addstr(y1+2,xCenter - (len(resumeAcc) // 2),resumeAcc,curses.color_pair(5))             
        stdscr.addstr(y1+4,xCenter-11,"⌗ ╰┈➤      %",curses.color_pair(6))
        stdscr.addstr(y1+4,xCenter+4,"|",curses.color_pair(5))
        stdscr.addstr(y1+4,xCenter+5,"  WPM",curses.color_pair(6))
        stdscr.addstr(y1+5,xCenter-3,"--------------",curses.color_pair(5))
        y1 += 6
        i = 1

        for placement in ranking:
            p1, p2 = placement[0], placement[1]
            if placement[0] == 1.0:
                p1, p2 = "N/A", "N/A"
            fst = f"Top {i}:"
            snd = f"   {p1:<5} | {p2:>5}"
            stdscr.addstr(y1,xCenter-11,fst,curses.color_pair(6))
            stdscr.addstr(y1,(xCenter-11)+(len(fst)),snd,curses.color_pair(5))
            y1 += 1
            i += 1

        stdscr.addstr(y1+2,xCenter - (len(text) // 2), text, curses.color_pair(4))
        stdscr.refresh()
        with open("sentences.json","w") as file:
            json.dump(data,file)
        self.nextAction(stdscr)
        
def main():
    app = Display()
    try: 
        app.run()
    except KeyboardInterrupt:
        app.resetCursor()
        sys.exit(0) 

if __name__ == "__main__":
    main()
