## Create commit message txt:

IMPORTANT The new version of the game is done it with a script. But if it's not work than you can do it with your hand. 

```bash
git log --all --pretty=format:"%h;; %al;; %s" > commitlog.txt  
```
This command will create a txt from the commit messages 

## Run the game in Windows PowerShell

IMPORTANT after that you clone the project please go to the src folder in the PowerShell

Maybe you should install argparse with pip

```bash
pip install configargparse
```

Clone subject repository.

```bash
git clone --mirror <LINK TO THE REPOSITORY> <NAME OF THE REPOSITORY>
```



```bash
python what_do_you_mean.py --config-file "my_config.ini"
```

