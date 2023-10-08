# What Do You Mean? Game
This game help to the players to understand how important is a good (for example) commit message. 

## Game turn 
The script:
1. Choose a random commit message
2. Choose the players (random) 
3. Generate a HTML page

The Game Master: 
4. Open the HTML page
5. Tell to the author and coworkers to write down the answers for the summary questions. 

Author and Coworkers:
6. Write down the answers
7. Give the paper to the neighbouring player. 
8. Read the paper out loud

The Game Master: 
9. Ask from the spectators the similarity question. 

The Spectators:
10. Raised their hands if they agree with the question.

The Game Master: 
11. Count the raised hands and write the number of the raised hands to the console and press enter.
12. After decide to continue the game or not. If yes just press enter and the turn is starting again from the beginning if not type `exit` and press enter.

## How to start the game? 
1. Please install the moduls what needed. (The script have requirements.txt)
2. check the config file what you would like to use. 
IMPORTANT: the program not validate the arguments and inputs. So please be careful when you set them.

If you use `PyCharmIDE`:
2. Set the `Paramters:` in `Edit configurations...` to this: 
```bash
--config-file <YOUR CONFIG FILE PATH> 
```
3. Press to the `Run` button

If you run the script in `Windows PowerShell` 
2. you can use this command with the right parameter:
```bash
python what_do_you_mean.py --config-file <YOUR CONFIG FILE PATH>
```

3. After that follow the commands in the console.

## Clone subject repository.

```bash
git clone --mirror <REPOSITORY PATH> <FOLDER PATH>
```

## Argparse parameters
You can find the argparse arguments description If you use in parameter the `-h`.
So run the script with -h parameter
```bash
python what_do_you_mean.py -h 
```

## In case if the script cannot reach/get the commit messages
Please open the repository what you would like to use and in the terminal use this command:
```bash
git log --all --pretty=format:"%h;; %al;; %s" > commitlog.txt  
```
This command create a commitlog.txt what you can use for the game. 


## Empty lines in the end of players.csv affect? 
I test it and it shouldn't. Ghost players not appears in the lists. But if it is possible avoid that situation. 

## If not enough `author` in the players.csv then the script will choose from every available commit? 
Yes, the script should work like that. You can change the `author-percent` parameter in the commit file. If you would like to use only the commits who are in the `players.csv`. 
Note: If the script use every commit than the author still can be in the `players.csv`.

## Is author always a player? 
No, if the author is not in the `player.csv` then won't be in the gamers. But if the `author` in the `players.csv` then always be an active player.

## Players only can be whose id in the players.csv?
Yes. 



